from flask import Flask, render_template, request, session, redirect, jsonify
from flask_socketio import SocketIO, send, emit
from functools import wraps
import my_secrets
import threading
import pyrebase
import os
import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

socketio = SocketIO(app)

firebase = pyrebase.initialize_app(my_secrets.get_firebase_config())
auth = firebase.auth()
db = firebase.database()

connection_counter = 0
connected = {}

SCDF_UID = "swArSSPIBJPERmh6pbs43GBe2vZ2"


def get_nearest_firedept(lat,lng):
    fire_depts = db.child("Fire Departments").get().val()
    nearest_fire_dept= ""
    minDist = 999999999999
    for i,j in fire_depts.items():
        if ((lat - float(j["long"])) ** 2) + ((lng - float(j["lat"])) ** 2) < minDist:
            minDist = ((lat - float(j["long"])) ** 2) + ((lng - float(j["lat"])) ** 2)
            nearest_fire_dept= i
    return nearest_fire_dept

def get_firedepts_branch():
    return db.child("Fire Departments").get().val()

def check_authenticated(uid):
    if uid in connected:
        return True
    return False    

def isMuteOver(timeString):
    timeList = timeString.split("_")
    if len(timeList) > 1:
        mutedTime = datetime.datetime(*[int(x) for x in timeList])
        timeDiff = datetime.datetime.now() - mutedTime
        if timeDiff.total_seconds()/3600 >= 1:
            return True
        return False
    return False

def location_exists(loc):
    if str(loc) in db.child("Locations").get().val():
        return True
    return False

def user_exists(uid):
    if str(uid) in db.child("Users").get().val():
        return True
    return False

def get_location_name(loc):
    if location_exists(loc):
        return db.child("Locations").child(loc).child("LocationName").get().val()
    return False

def user_owns_location(uid,loc):
    location_str=   db.child("Users").child(session["uid"]).child("UserLocations").get().val()
    if location_str == "all":
        return True
           
    if location_exists(loc) and user_exists(uid):
        if loc in db.child("Users").child(uid).child("UserLocations").get().val().split(","):
            return True
    return False

def get_logs(loc_array):
    to_send = {}
    locations = db.child("Locations").get().val()
    for i in loc_array:
        if i in locations:
            if "Logs" in db.child("Locations").child(i).get().val():
                to_send[i] = db.child("Locations").child(i).child("Logs").get().val()
            else:
                to_send[i] = {"-":{"Location":i,"Fire":"No Record","Camera":"No Record"}}
    return to_send

def reset_mute_time(loc):
    db.child("Locations").child(loc).child("Mute").set(0)
    db.child("Locations").child(loc).child("Logs").update({datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f"):{"Fire":"Unmuted","Camera":"Manual"}})

def get_locations_branch():
    return db.child("Locations").get().val()

def get_marker_branch():
    return [db.child("Locations").get().val(),  db.child("Fire Departments").get().val()]
    
def get_location_specific_data(loc):
    if location_exists(loc):
        return db.child("Locations").child(loc).get().val()

def register_camera_with_user(camCode, locationName,uid):
    if str(camCode) in db.child("Locations").get().val():
        if "Owner" not in db.child("Locations").child(str(camCode)).get().val():
            toUpdate = {"LocationName":locationName,"Owner":uid}
            db.child("Locations").child(str(camCode)).update(toUpdate)
            return True
    return False

def check_and_unset_mute():
    try:
        for cam,details in get_locations_branch().items():
            if "Mute" in details and details["Mute"] != 0 and isMuteOver(details["Mute"]):
                reset_mute_time(cam)
        return True
    except:
        False

def get_user_locations(uid):
    check_and_unset_mute()
    location_str= db.child("Users").child(uid).child("UserLocations").get().val()
    return location_str.split(",")

def set_mute(loc,my_time):
    datetimestamp = my_time.strftime("%Y_%m_%d_%H_%M_%S")
    t = threading.Timer(3600,reset_mute_time,[loc])
    t.start()
    db.child("Locations").child(loc).child("Mute").set(datetimestamp)

def stream_handler(m):
        if isinstance(m['data'],int):
            _, loc, cam = m['path'].split("/")
            muteTimeStamp = db.child("Locations").child(loc).child("Mute").get().val()
            if cam == "Mute" and m['data'] == 0: # user manually unmute
                socketio.emit('unmuted_data',{"Location":loc,"data":get_location_specific_data(loc)},namespace='/')
            if muteTimeStamp == 0 or muteTimeStamp == "0":
                val = int(m['data'])
                socketio.emit('update',{'Location':loc,'Camera':cam,'Value':val},namespace='/')
            elif isMuteOver(muteTimeStamp):
                reset_mute_time(loc)
                socketio.emit('unmuted_data',{"Location":loc,"data":get_location_specific_data(loc)},namespace='/')
        else:
            socketio.emit('original_data',get_marker_branch(),namespace='/')

@socketio.on('camera_sweep_heard',namespace="/")
def camera_sweep_heard(data):
    db.child("Locations").child(data[0]).child("CameraSweep").set(0)
    my_now = datetime.datetime.now()
    set_mute(data[0],my_now)

@socketio.on('dispatched',namespace="/")
def dispatch(data):
    db.child("Locations").child(data[0]).update({"DispatchBy": data[1]})
    db.child("Locations").child(data[0]).child("Logs").update({datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f"):{"Fire":"Fire Team Dispatched","Camera":f"Dispatched Team: {data[1]}"}})
    db.child("Fire Departments").child(data[1]).update({"IsDispatched": data[0]})

@socketio.on('clear_dispatch',namespace="/")
def clear_dispatch(data):
    db.child("Locations").child(data[0]).update({"DispatchBy": 0})
    db.child("Locations").child(data[0]).child("Logs").update({datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f"):{"Fire":"Fire Team Called Back","Camera":f"Team Return: {data[1]}"}})
    db.child("Fire Departments").child(data[1]).update({"IsDispatched": 0})

@socketio.on("mute",namespace="/")
def mute_location(data):
    try:
        if user_owns_location(session["uid"],data[0]):
            my_now = datetime.datetime.now()
            set_mute(data[0],my_now)
            log_datetimestamp = my_now.strftime("%Y_%m_%d_%H_%M_%S_%f")
            db.child("Locations").child(data[0]).child("Logs").update({log_datetimestamp:{"Fire":"Muted","Camera":"Manual"}})
    except:
        return redirect("/login")

@socketio.on("unmute",namespace="/")
def unmute_location(data):
    try:
        if user_owns_location(session["uid"],data[0]):
            reset_mute_time(data[0])
    except:
        return redirect("/login")

@socketio.on("false_alarm_late",namespace="/")
def false_alarm_late(data):
    to_send = {"Location":data[0],"LocationName":get_location_name(data[0])}
    emit("notify_false_alarm_late",to_send,namespace='/')

@socketio.on('connected',namespace="/")
def handle_message():
    global connection_counter
    # Check if there is already an active connection
    # On 1st connection, start thread to stream from database
    if not connection_counter: 
        my_stream = db.child("Locations").stream(stream_handler)
        connection_counter += 1
    # 2nd connection onwards, emit initialisation data
    else: 
        emit('original_data', get_marker_branch())

@app.route("/") 
def root(): 
    try:
        if check_authenticated(session['uid']):
            campus_name= db.child("Users").child(session["uid"]).child("CampusName").get().val()
            return render_template("index.html",  campus_name= campus_name)
        return redirect("/login")
    except Exception as e:
        return redirect("/login")

@app.route("/camera-management", methods= ["GET", "POST"])
def profile_setting(): 
    try:
        if check_authenticated(session['uid']):
            if request.method == "POST":
                locationName = request.form["inputLocationName"]
                locationDetails = request.form["inputLocationDetails"]
                camID = request.form["inputCamID"]
                lat = request.form["inputLat"]
                long = request.form["inputLong"]

                if user_owns_location(session["uid"], camID):
                    toUpdateCamInfo = {"LocationName":locationName,"LocationDetails":locationDetails,"lat": lat, "long": long}
                    db.child("Locations").child(camID).update(toUpdateCamInfo)

            location_str=   db.child("Users").child(session["uid"]).child("UserLocations").get().val()
            if location_str == "all":
                location_arr = db.child("Locations").get().val().keys()
                isSCDF = True
            else:
                location_arr = location_str.split(",")
                isSCDF = False
            camera_info=[]
            campus_name= db.child("Users").child(session["uid"]).child("CampusName").get().val()

            for loc in location_arr:
                loc_branch= db.child("Locations").child(loc).get().val()
                camera_info.append([loc,loc_branch["LocationName"], loc_branch["LocationDetails"], loc_branch["lat"], loc_branch["long"]])

            return render_template("profile_setting.html", camera_info= camera_info, campus_name= campus_name, isSCDF=isSCDF)
        else:
            return redirect("/login")
    except:
        return redirect("/login")

@app.route("/user-guide") 
def user_guide():
    try:
        if check_authenticated(session['uid']):
            campus_name= db.child("Users").child(session["uid"]).child("CampusName").get().val()
            location_str=   db.child("Users").child(session["uid"]).child("UserLocations").get().val()
            if location_str == "all":
                return render_template("user_guide_scdf.html",  campus_name= campus_name)
            else:
                return render_template("user_guide_fm.html",  campus_name= campus_name)
    except:
        return redirect("/login")

@app.route("/camera-logs",methods=["GET"])
def camera_logs():
    try:
        if check_authenticated(session["uid"]):
            campus_name = db.child("Users").child(session["uid"]).child("CampusName").get().val()
            location_str =   db.child("Users").child(session["uid"]).child("UserLocations").get().val()
            if location_str == "all":
                location_arr = db.child("Locations").get().val().keys()
            else:
                location_arr = location_str.split(",")
            send_cam_logs = get_logs(location_arr)
            return render_template("camera-logs.html",cam_info=send_cam_logs,campus_name= campus_name )
        else:
            return redirect("/login")
    except:
        return redirect("/login")

@app.route("/isAdmin",methods=["GET"])
def check_is_admin():
    try:
        if session["uid"] == SCDF_UID:
            return jsonify(True)
        return jsonify(False)
    except:
        return redirect("/login")

@app.route("/getLocations",methods=["GET"])
def getLocations():
    try:
        return db.child("Users").child(session["uid"]).child("UserLocations").get().val()
    except:
        return redirect("/login")

@app.route("/register", methods=["GET","POST"])
def register(): 
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        confpassword = request.form["confpassword"]
        locationName = request.form["locationName"]
        locationDescription = request.form["locationDescription"]
        cameraIds = [x.strip() for x in request.form["cameraIds"].split(",")]
        
        if password != confpassword:
            return render_template("register.html",message="Passwords do not match")
        
        try:
            user = auth.create_user_with_email_and_password(email,password)
            # create the user branch in the database using the uid
            user_id = user["idToken"]
            uid = user["localId"]
            toAddUser = {uid : {"CampusName":locationName,"CampusDescription":locationDescription,"UserLocations":",".join(cameraIds)}}
            for i in cameraIds:
                if register_camera_with_user(i,locationName,uid):
                    continue
                else:
                    auth.delete_user_account(user_id)
                    auth.current_user = None
                    return render_template("register.html",message=f"Camera ID: {i} does not exist or is used.")
            else:
                db.child("Users").update(toAddUser)
                session['user'] = user_id
                session['uid'] = uid
                session["email"] = email
                connected[uid] = {'user':user_id,'email':email}
                auth.current_user = None
                return redirect("/")
            
        except:
            return render_template("register.html",message="This email has been taken")

    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            user_id = user['idToken']
            uid = user['localId']
            session['user'] = user_id
            session["uid"] = uid
            session["email"] = email
            connected[uid] = {'user':user_id,'email':email}
            auth.current_user = None
            return redirect("/")  
        except:
            return render_template("login.html", message="Wrong Credentials" )  
    
    return render_template("login.html")

@app.route("/logout",methods=["GET","POST"])
def logout():
    try:
        if check_authenticated(session['uid']):
            auth.current_user = None
            connected.pop(session['uid'])
            session.pop('user',None)
            session.pop('uid',None)
            session.pop('email',None)
        return redirect('/login')
    except:
        return redirect('/login')

if __name__ == '__main__':
    socketio.run(app)