
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
            if camCode == "0":
                toGenerateId = True
            else:
                print(camCode)
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


