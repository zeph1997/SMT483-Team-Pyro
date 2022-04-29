# SMT483-Team-Pyro
Team Pyro's Codebase for SMT483
# <p align="center">SMT483 Team Pyro Codebase</p>

<p align="center">A repository of all the code written by Team Pyro for SMT483 in AY 21/22 T2</p>

## Contents
  * [Brief Introduction](#brief-introduction)
  * [Folder Directory](#folder-directory)
    * [Hardware](#hardware)
        * [Thermal Camera](#thermal-camera)
        * [Visual Camera](#visual-camera)
        * [Pan Tilt Platform](#pan-tilt-platform)
        * [Generate ID](#generate-id)
    * [Software](#software)
        * [Frontend and Backend](#frontend-and-backend)
        * [Database](#database)

## Brief Introduction
This repository contains the code for the hardware (Pyro) and the Software (Pyro View). Due to the public nature of this repository, the private keys have been removed. Hence, if you download this repository and try to run the server, it will not work as there is no connection to the database. 

However, the solution is deployed and you may try out the live demo at https://team-pyro-dashboard.herokuapp.com/

## Folder Directory
This is the folder directory for the different components of the project. As this project includes the hardware code, we have separated them into their respective folders. 

### Hardware
These code reside on the Raspbery Pi as part of the edge computing architecture.

#### Thermal Camera
You may view the code relating to the thermal camera here - [Go to Thermal Camera Folder](ThermalCamera/README.md)

#### Visual Camera
You may view the code relating to the visual camera as well as the computer vision model here - [Go to Visual Camera Folder](CompVision/README.md)

#### Pan Tilt Platform
You may view the code relating to the pan tilt platform here - [Go to Pan Tilt Platform Folder](ServoController/README.md)

#### Generate ID
You may view the code to Generate/Read the cameraID automatically on the Raspberry Pi here - [Go to Generate ID Folder](GenerateID)

### Software
The code here is formatted to fit the Flask Web Framework. They all reside in the FlaskDashboard folder. For the frontend, the web pages can be found in the `templates` folder. The javascript can be found in the web pages.

#### Frontend and Backend
You may view the code to Frontend and Backend code, formatted in the Flask Web Framework directory requirements here - [Go to Flask Dashboard Folder](FlaskDashboard/README.md)

#### Database
You may view the Firebase real-time database JSON object here - [Go to Database Folder](Firebase/README.md)