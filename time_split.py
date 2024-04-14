import cv2
import os
import glob
import math

def split_image(image):
    basename = os.path.basename(image)
    filename = os.path.splitext(basename)[0]
    img = cv2.imread(image)

    height, width, _ = img.shape
    height_1ms = math.ceil(height/20)

    seconds = 15    #ms in output spectrogram
    split_image = img[0:seconds*height_1ms, 0:width]
    cv2.imwrite(f"train_data/time_split_images/{filename}.jpg", split_image)    #output directory


directory_path = f"train_data/input_images"    #input directory
image_files = glob.glob(os.path.join(directory_path, '*.jpg'))
for image in image_files:
    split_image(image)
