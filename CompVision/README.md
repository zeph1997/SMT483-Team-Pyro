# Computer Vision Model
We are using YOLOv5s. This is due to the lack of a TPU for the raspberry pi. Hence, the small model will ensure the best performance and give real-time analysis for fire.

We used V4 for our solution. To view the code, please open the V4 folder.

## Important file - detect.py
The file that contains the fire and smoke detection logic that the team had written is in the `detect.py` file that is found in the V4 folder. Notably, lines 169 to 173, and lines 190 to 201. This code will 

## database.py
This file contains the code that is used to communicate with the Firebase real-time database. There is supposed to be a `secrets.py` file that contains the private key, however due to the public nature of this repository, we have removed it.

## Script to Run Computer Vision Model V4
Run the following script in the 
```
python3 detect.py --weights runs/train/exp/weights/best_fire_smoke.pt --img 320 --source 0
```

## Version History
### V1
Version 1 detects Fire and Smoke (any colour)

### V2
Version 2 strips away Smoke detection and focuses on Fire. More indoor fire data is also fed to the model to enhance indoor fire detection.

### V3
Version 3 augment images in dataset by flipping the images horizontally and vertically to add more images to train the model, as well as adding null indoor images to train the model to reduce the number of false positives.

### V4
Version 4 builds on top of V3 and adds Black Smoke detection to the model.


