from tkinter import image_names
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import bottleneck as bn
import cv2
import logging

# TODO: make a pull request, code, and then a merge request
# TODO: add file and function headers 

K = 2.5 # background suppression threshold
H_PERCENT = 99 # upper clipping thresh
L_PERCENT = 1 # lower clipping thresh

def invert(img_path):
    img = np.array(Image.open(img_path))
    # subtract entire image by 255 and mult by -1
    img = img.astype(np.int8)
    img = img - 255
    img = img * -1
    img = img.astype(np.uint8)
    return img

def flip(img_path):
    img = np.array(Image.open(img_path))
    # subtract entire image by 255 and mult by -1
    img = np.rot90(img)
    img = img.astype(np.uint8)
    return img

def suppress_background(video_path):

    # TODO: add a time estimate

    # read in video
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    img_array = []
    count = 0
    while success and count < 100:
        success, image = vidcap.read()
        if success:
            # print(success)
            img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # img_gray = cv2.blur(img_gray, (5,5))
            img_array.append(img_gray)
            count += 1
            # print(len(img_array))
    # use bottleneck (bn) for cal   culations
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, datefmt='%H:%M:%S')

    logging.info("converting list to array")
    img_array = np.array(img_array).astype(np.float64)

    logging.info("clipping video based on thresh")
    img_array = clip_img(img_array, H_PERCENT, L_PERCENT)

    logging.info("normalizing image")
    img_array = linear_normalization(img_array)
    
    logging.info("Getting MEDIAN frame")
    mean_vid = bn.median(img_array, axis = 0)

    logging.info("Getting STD frame")
    std_vid = bn.nanstd(img_array, axis = 0)

    logging.info("subtracting mean and dividing std") 
    img_array -= mean_vid
    img_array /= std_vid

    # TODO: threshold it by k...
    img_array = (img_array > K).astype(np.uint8)

    # TODO: convert to values from 0-255
    img_array *= 255

    img_array = img_array.astype(np.uint8)
    logging.info("done w processing...sending to user...")

    return img_array

def clip_img(arr, h, l): 
    """
    takes in an array and clips by the h percentile and l percentile
    arr: array
        image array
    h: float
        higher thresh
    l: float
        lower thresh
    """
    clip_max = np.percentile(arr, h)
    clip_min = np.percentile(arr, l)

    arr = np.clip(arr, clip_min, clip_max)
    return arr

def linear_normalization(arr):
    """
    scales from 0-1 with x' = (x - xmin)/(xmax - xmin)
    arr: array
        image/video array
    """
    arr = (arr - np.min(arr))/(np.max(arr) - np.min(arr))
    return arr

def main():
    None

if __name__ == "__main__":
    main()
"""

    image = np.array(Image.open(path).convert('L'))
    image[:100, :100] = 0
    output_stream = open(app.config['DOWNLOAD_FOLDER'] + filename, 'wb')
    pil_img = Image.fromarray(image)
    pil_img.save(output_stream)
    
"""