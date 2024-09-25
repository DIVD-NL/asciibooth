#!/usr/bin/env python

from flask import Flask, Response, redirect, send_from_directory, request
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
import io
import time
import libcamera
import shutil
from datetime import datetime
import re

app = Flask(__name__, static_url_path='/', static_folder='static')

@app.route("/")
def root():
    return send_from_directory(app.static_folder, 'index.html')

# setup camera and resolution
picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size": (1024,1024)})
video_config["transform"] = libcamera.Transform(hflip=1, vflip=0)
still_config = picam2.create_still_configuration(main={"size": (1024,1024)})
picam2.configure(video_config)
picam2.start()

def gather_img():
    while True:
        time.sleep(.2)
        data = io.BytesIO()
        picam2.capture_file(data, format='jpeg')
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + data.getbuffer() + b'\r\n')

email_re = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
def is_email(text: str) -> bool :
    return email_re.match(text) is not None

@app.route("/mjpeg")
def mjpeg():
    return Response(gather_img(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/capture")
def capture():
    data = io.BytesIO()
    picam2.switch_mode_and_capture_file(still_config, "static/capture.jpg", format='jpeg')
    picam2.switch_mode(video_config)
    return redirect("/print.html", code=302)

@app.route("/print", methods=['GET', 'POST'])
def printit():
    now = datetime.now()
    formatted_date = now.strftime('%Y%m%d%H%M%S')
    shutil.copy("static/capture.jpg", f"process/{formatted_date}.jpg")
    email = request.form.get('email')
    if is_email(email) :
        with open(f"process/{formatted_date}.email", "w") as fh:
            print(email, file=fh)
    return redirect("/")



app.run(host='0.0.0.0', threaded=True, debug=False)



