import time
from ServoKit import *
import database

# on activate, start scanning
servoKit = ServoKit(2)
starting_angle = 0
move_step = 30
full_scan_no_fire = False
while True:
    # move the camera
    servoKit.setAngle(0,starting_angle)
    to_exit = False
    for i in range(4):
        if database.fire_detected():
            to_exit = True
            break
        time.sleep(1)
    if starting_angle >= 180:
        database.full_sweep()
        full_scan_no_fire = True
        starting_angle = 0
        servoKit.setAngle(0,starting_angle)
        break
    elif database.fire_detected() or to_exit:
        break
    starting_angle += move_step
if full_scan_no_fire:
    print("Full scan conducted, no fire found")
else:
    print("Fire Detected from at least one camera")

