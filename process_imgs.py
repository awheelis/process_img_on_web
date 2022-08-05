import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

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