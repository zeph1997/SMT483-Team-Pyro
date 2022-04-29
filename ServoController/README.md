# Servo Controller Codebase
Below are the files that contain the code to control the pan tilt platform.

## ServoKit.py
The file `ServoKit.py` is referenced from https://github.com/ArduCAM/PCA9685/tree/master/example/Jetson

This allows us to control the pan tilt platform through the I2C interface.

## database.py
This file contains the code that is used to communicate with the Firebase real-time database. There is supposed to be a `secrets.py` file that contains the private key, however due to the public nature of this repository, we have removed it.

## servo_move.py
This file will be the file that is run when the scanning function of the pan tilt platform is activated. To run this on the Raspberry Pi, type the following:
```
python3 servo_move.py
```

The code will do the following:
* Initialise the cameras to start scanning from the left
* Check the database every 1 second if any of the cameras detect a fire 
* Move the cameras 30 degrees to the right every 5 seconds 
* If there is no fire detected after a full scan, update the database to mute the fire alarm as it is most likely a false alarm
