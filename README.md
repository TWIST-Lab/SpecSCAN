This repository contains all the codes that have been used for the various experiments of this project. The yolov3 and yolov5 folders have been cloned from the ultralytics repository. The yaml file (spectrogram.yaml) containing our experiment's metadata has been added to these folders. The model could be executed after loading the dataset and making necessary changes in the yaml file. The files frequency_split.py and time_split.py are used to chop the images along the different axes and modify the annotations as required.

Sample folder structure for the dataset and command for running the code:
.
|__train_data
   |__images
   |  |__train
   |  |  |__1.jpg
   |  |  |__2.jpg
   |  |  |__3.jpg
   |  |      .
   |  |      .
   |  |      .
   |  |__test
   |  |  |__1.jpg
   |  |  |__2.jpg
   |  |  |__3.jpg
   |  |      .
   |  |      .
   |  |      .
   |  |__val 
   |  |  |__1.jpg
   |  |  |__2.jpg
   |  |  |__3.jpg
   |  |      .
   |  |      .
   |  |      .
   |__labels
   |  |__train
   |  |  |__1.txt
   |  |  |__2.txt
   |  |  |__3.txt
   |  |      .
   |  |      .
   |  |      .
   |  |__test
   |  |  |__1.txt
   |  |  |__2.txt
   |  |  |__3.txt
   |  |      .
   |  |      .
   |  |      .
   |  |__val 
   |  |  |__1.txt
   |  |  |__2.txt
   |  |  |__3.txt
   |  |      .
   |  |      .
   |  |      .


To train the model:
python3 train.py --img 640 --batch 16 --epochs 200 --optimizer "Adam" --data spectrogram.yaml --weights yolov5s.pt --cache
