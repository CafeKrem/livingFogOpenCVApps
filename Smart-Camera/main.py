import cv2
import sys
from mail import sendEmail
from flask import Flask, render_template, Response
from flask_basicauth import BasicAuth
import time
import threading
from imutils.video.pivideostream import PiVideoStream
import imutils

# initialize the camera and grab a reference to the raw camera capture
camera = PiVideoStream().start()

# flip camera 
# camera.rotation = 180

# allow the camera to warmup
time.sleep(0.2)

email_update_interval = 600 # sends an email only once in this time interval

def gen_frames(): 
    

    face_cascade = cv2.CascadeClassifier('./Haarcascades/haarcascade_frontalface_default.xml')
    count_face = 0
    
    while True : 
        frame = camera.read() 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
        faces = face_cascade.detectMultiScale(gray,1.1,7)
        
        n = len(faces)
        if n > 0 : 
            print("Face detected") 
            count_face += 1 
       
        if count_face == 15 : 
            #sendEmail(frame)
            count_face = 0  
            print("Mail Send it")
        #Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)     
	 
        ret,buffer=cv2.imencode('.jpg',frame)
        frame=buffer.tobytes()

        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



# App Globals (do not edit)
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)
last_epoch = 0


@app.route('/')
@basic_auth.required
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
