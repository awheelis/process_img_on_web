"""
George Alexander Wheelis (2022)

File with video processing algorithms for app.py (flask script)

FUNCTIONS: 
    invert() - inverts an image
    flip() - rotates an image by 90 degrees
    suppress_background() - executes background suppressions on a video
    blob_detection() - takes a background suppressed video and the original
        and does blob detection. This makes the background suppression script 
        cleaner looking and makes desired objects bigger. Mask is then applied 
        to the original video 
        [not implemented!]
    clip_image() - clips image with numpy functions. Gets rid of the top 
        X percentile and bottom Y percentile
    linear_normalization() - normalizes values in array to that between 0 and 1
    

"""


from tkinter import image_names
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import bottleneck as bn
import cv2
import logging
from datetime import datetime


# TODO: read pep8 coding standards and make this script cleaner

K = 3 # background suppression threshold
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

def estimate_time_to_complete():
    """
    takes in height, width, and frame count of video 
    returns predicted time to complete the function

    figure out: 
    - does video processing scale linearly based on size???
    """

def suppress_background(video_path):
    # TODO: add a time estimate for the program

    start_time = datetime.now()
    # read in video
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    img_array = []
    count = 0

    while success and count < 220:
        success, image = vidcap.read()
        if success:
            # print(success)
            img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            img_array.append(img_gray)
            count += 1

    vid_width = vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)  
    vid_height = vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    vid_frame_num = len(img_array)

    print("size of video:")
    print(f"w: {vid_width}, h: {vid_height}, n: {vid_frame_num}")
    video_size = vid_width * vid_height * vid_frame_num

    estimate_time_to_complete()

    # use bottleneck (bn) for cal   culations
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, datefmt='%H:%M:%S')

    logging.info("converting list to array")
    img_array = np.array(img_array)

    logging.info("clipping video based on thresh")
    img_array = clip_img(img_array, H_PERCENT, L_PERCENT)
    
    logging.info("Getting MEDIAN frame")
    mean_vid = bn.median(img_array, axis = 0)

    logging.info("Getting STD frame")
    std_vid = bn.nanstd(img_array, axis = 0)

    logging.info("subtracting mean and dividing std") 
    img_array -= mean_vid
    img_array /= std_vid

    # TODO: threshold it by k...
    logging.info(f"creating mask based off of K = {K}")
    img_array = (img_array > K).astype(np.uint8)

    # TODO: convert to values from 0-255
    img_array *= 255

    img_array = img_array.astype(np.uint8)
    logging.info("done w processing... \nsending to user...")

    elapsed_time = datetime.now() - start_time
    print(elapsed_time.total_seconds())
    print(video_size)

    return img_array


def blob_detection(video_path):
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
    img_array = np.array(img_array)



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
    logging.info("This doesn't do anything lol")
    None

if __name__ == "__main__":
    main()
