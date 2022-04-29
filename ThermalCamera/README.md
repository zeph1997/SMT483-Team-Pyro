# Thermal Camera Codebase
Below are the files used to control and read the data from the thermal camera.

## amg8833_i2c.py
The file `amg8833_i2c.py` is referenced from https://github.com/makerportal/AMG8833_IR_cam

This allows us to read the sensors of the thermal camera. We modified this file to set the threshold of 60 degrees celcius to detect a fire and return a boolean value isFire in the function `read_temp()` on line 121. 

## database.py
This file contains the code that is used to communicate with the Firebase real-time database. There is supposed to be a `secrets.py` file that contains the private key, however due to the public nature of this repository, we have removed it.

## thermal_cam.py
This file will be the file that is run when the thermal camera is activated. To run this on the Raspberry Pi, type the following:
```
python3 thermal_cam.py
```
We have set the number of frames to be 12 consecutive frames to determine a fire is present. 
