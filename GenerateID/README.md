# GenerateID
This script will generate/read the cameraID automatically without having the user to perform any tasks on the Raspberry Pi.
The steps are as follows:
1. The script will first try to read a text file on the Desktop to see if it exists
2. If it does not exist, then it will go to the database and find the total number of existing cameras, then add 1 and add itself to the database and save the cameraID to the Desktop in a text file
3. If the file exists, then all the camera function will reference this file to get the cameraID
