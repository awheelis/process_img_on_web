from tkinter import image_names
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import bottleneck as bn
import cv2

H_PERCENT = .99 # upper clipping thresh
L_PERCENT = 0.01 # lower clipping thresh

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
    while success and count < 100:
        success, image = vidcap.read()
        if success:
            # print(success)
            img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            img_array.append(img_gray)
            count += 1
            # print(len(img_array))
    # use bottleneck (bn) for cal   culations
    print("converting to array")
    img_array = np.array(img_array).astype(np.uint8)
    print(img_array.shape)
    mean_vid = bn.nanmean(img_array, axis = 0)
    print("got mean frame")
    std_vid = bn.nanstd(img_array, axis = 0)
    print("got std frame")
    # do (video - med)/std

    print(np.max(std_vid), np.min(std_vid))
    print("std(std): ", np.std(std_vid))
    print("mean(std): ", np.mean(std_vid))
    print("std(mean): ", np.std(mean_vid))
    print("mean(mean): ", np.mean(mean_vid))

    # clip!
    mean_vid = clip_img(mean_vid, H_PERCENT, L_PERCENT)
    std_vid = clip_img(std_vid, H_PERCENT, L_PERCENT)
    print(np.max(std_vid), np.min(std_vid))
    print("std(std): ", np.std(std_vid))
    print("mean(std): ", np.mean(std_vid))
    print("std(mean): ", np.std(mean_vid))
    print("mean(mean): ", np.mean(mean_vid))
    img_array -= mean_vid.astype(np.uint8)

    print(img_array.shape)
    # normalize and clip
    # image_array -= np.max

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