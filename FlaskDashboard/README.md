# Pyro View
The code here belongs to both the frontend and backend system. The code structure follows the Flask Web Framework. This is the folder that has been uploaded to Heroku and deployed successfully. You may view the live demo at https://team-pyro-dashboard.herokuapp.com/

You may use the following credentials to log in:
#### Facility Manager
Email: zephngns@gmail.com
Password: test123

#### SCDF
Email: pblyn11@gmail.com
Password: test123

The web routes and business logic are contained within the `app.py` file. 
To run the server, you can run the file `app.py`. There is supposed to be a `my_secrets.py` file that contains the private key, however due to the public nature of this repository, we have removed it. with the following code
```
python app.py
```

## Frontend
To access the frontend code, please go to the templates folder. The javascript code can be found in the web pages.
Here are the mapping for the pages:
* Dashboard - index.html
* Login - login.html
* Registration - register.html
* Camera Management - profile-setting.html
* Camera Logs - camera-logs.html
* User Guide for Facility Managers - user_guide_fm.html
* User Guide for SCDF - user_guide_scdf.html

## Backend Flask Server Dependencies
* Flask - pip install Flask
* Flask-SocketIO - pip install Flask-SocketIO (For websockets)
* Pyrebase4 - pip install pyrebase4 (Firebase API Wrapper)


