import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, send_file
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
import process_imgs
import cv2


UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov'])

app = Flask(__name__, static_url_path="/static")
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
# limit upload size upto 8mb
# app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            if request.form["submit_button"] == "Invert":
                img = process_imgs.invert(img_path)
                return_image(img, filename)

            elif request.form["submit_button"] == "Flip":
                img = process_imgs.flip(img_path)
                return_image(img, filename)

            elif request.form["submit_button"] == "Background Suppress":
                video = process_imgs.suppress_background(img_path)
                return_video(video, filename)

            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('index.html')


def return_image(img_arr, filename):
    output_stream = open(app.config['DOWNLOAD_FOLDER'] + filename, 'wb')
    pil_img = Image.fromarray(img_arr)
    pil_img.save(output_stream)

def return_video(video_arr, file_path):
    """
    video_arr: np array of video frames
    file_path: file location 
    """
    w, h = int(video_arr.shape[1]), int(video_arr.shape[2])
    fps = 25
    out = cv2.VideoWriter(app.config['DOWNLOAD_FOLDER'] + file_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (h, w), 0)
    for frame in video_arr:
        out.write(frame)
    out.release()



    # file_loc = app.config['DOWNLOAD_FOLDER'] + file_path
    # w, h = video_arr.shape[1], video_arr.shape[2]
    # print(w, h)
    # out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (w, h), isColor = False)
    # for frame in video_arr:
    #     out.write(frame)

    # out.release() 
    # send_file(file_path, as_attachment = True)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(debug = True, host='localhost', port=port)
