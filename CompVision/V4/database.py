from firebase import Firebase
import secret
import datetime


firebase = Firebase(secret.get_firebase_config())
auth = firebase.auth()
db = firebase.database()

# get location code
def get_cam_count():
    return int(db.child("LocationCount").get().val())

def gen_cam_code():
    camCount = int(db.child("LocationCount").get().val()) + 1
    db.child("LocationCount").set(camCount)
    return camCount

def gen_new_camera_branch(camCode):
    toAdd = {camCode:{"CameraFire":0,"CameraSweep":0,"DispatchBy":0,"LocationDetails":0,"LocationName":"0","Mute":0,"ThermalFire":0,"lat":1.29,"long":103.8}}
    db.child("Locations").update(toAdd)

def get_cam_code():
    toGenerateId = False
    try:
        with open("/home/pi/Desktop/cam_id.txt","r") as f:
            camCode = f.readline()
            camCode = camCode.strip()
            if camCode == "0":
                toGenerateId = True
            else:
                return camCode
    except:
        toGenerateId = True

    if toGenerateId:
        camCode = f"L{gen_cam_code():0=3d}"
        with open("/home/pi/Desktop/cam_id.txt","w") as f:
            f.write(camCode)
        gen_new_camera_branch(camCode)
    print(camCode)
    return camCode

LOCATION = get_cam_code()

def camera_detect_fire():
    db.child("Locations").child(LOCATION).child("CameraFire").set(1)
    db.child("Locations").child(LOCATION).child("Logs").update({datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f"):{"Fire":"Fire Detected","Camera":"Visual Camera"}})
    return True

def camera_detect_no_fire():
    db.child("Locations").child(LOCATION).child("CameraFire").set(0)
    db.child("Locations").child(LOCATION).child("Logs").update({datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f"):{"Fire":"Fire No Longer Detected","Camera":"Visual Camera"}})
    return True