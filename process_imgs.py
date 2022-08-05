from tkinter import image_names
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import bottleneck as bn
import cv2

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
    while success:
        success, image = vidcap.read()
        if success:
            # print(success)
            img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            img_array.append(img_gray)
            # print(len(img_array))

    # use bottleneck (bn) for calculations
    print("converting to array")
    img_array = np.array(img_array).astype(np.uint8)
    print(img_array.shape)
    mean_vid = bn.nanmean(img_array, axis = 0).astype(np.uint8)
    print("got mean frame")
    # std_vid = bn.nanstd(img_array, axis = 0)
    # print("got std frame")
    # print(std_vid.shape)
    # std_vid = std_vid.astype(np.unit8)
    # print(std_vid.shape)
    # compute the std of stack
    # compute median of stack
    # do (video - med)/std
    # return video 
    img_array -= mean_vid
    return img_array

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