from firebase import Firebase
import secret
import datetime

LOCATION = "Location1"

firebase = Firebase(secret.get_firebase_config())
auth = firebase.auth()
db = firebase.database()

def camera_detect_fire():
    db.child("Locations").child(LOCATION).child("CameraFire").set(1)
    db.child("Locations").child(LOCATION).child("Logs").update({datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f"):{"loc":LOCATION,"fire":"yes","camera":"Thermal"}})
    return True

def camera_detect_no_fire():
    db.child("Locations").child(LOCATION).child("CameraFire").set(0)
    db.child("Locations").child(LOCATION).child("Logs").update({datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f"):{"loc":LOCATION,"fire":"yes","camera":"Thermal"}})
    return True