from tkinter import image_names
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import bottleneck as bn
import cv2

import logging

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
    # read in video
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    img_array = []
    count = 0
    while success and count < 1000:
        success, image = vidcap.read()
        if success:
            # print(success)
            img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            img_array.append(img_gray)
            count += 1
            # print(len(img_array))
    # use bottleneck (bn) for cal   culations
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, datefmt='%H:%M:%S')

    logging.info("converting list to array")
    img_array = np.array(img_array).astype(np.float64)

    logging.info("normalizing image")
    img_array = linear_normalization(img_array)

    logging.info("clipping video based on thresh")
    img_array = clip_img(img_array, H_PERCENT, L_PERCENT)

    logging.info("Getting MEAN frame")
    mean_vid = bn.nanmean(img_array, axis = 0)

    logging.info("Getting STD frame")
    std_vid = bn.nanstd(img_array, axis = 0)

    logging.info("Clip mean and std")
    mean_vid = clip_img(mean_vid, H_PERCENT, L_PERCENT)
    std_vid = clip_img(std_vid, H_PERCENT, L_PERCENT)

    logging.info("subtracting mean and dividing std")
    img_array -= mean_vid
    img_array /= std_vid
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