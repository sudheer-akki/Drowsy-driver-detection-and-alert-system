# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 20:45:27 2020

@author: Akki
"""

import numpy as np
import imutils
import scipy
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import time
import dlib
import cv2
from playsound import playsound
from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)


import argparse



  
  

@app.route('/')
def index():
  return render_template('index.html')
  
@app.route('/video')
def video():
  return Response(generate_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')



def sound_alarm(path):
    #playsound.default.samplerate = fs
    #playsound.playsound(path, fs)
    playsound(path)
    
def eye_aspect_ratio(eye):
    A=dist.euclidean(eye[1],eye[5])
    B=dist.euclidean(eye[2],eye[4])
    
    C = dist.euclidean(eye[0],eye[3])
    
    ear = (A+B)/(2.0*C)
    
    return ear

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", default="shape_predictor.dat",
	help="path to facial landmark predictor")
ap.add_argument("-a", "--alarm", type=str, default="alarm.mp3",
	help="path alarm.mp3 file")
ap.add_argument("-w", "--webcam", type=int, default=0,
	help="index of webcam on system")
args = vars(ap.parse_args())


EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 48


ALARM_ON = False

"""initialize dlib's face detector (HOG-based) and then create
the facial landmark predictor"""

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])   

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]


def generate_frame():
  COUNTER = 0
  cap = cv2.VideoCapture(0)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
  time.sleep(1.0)

  while (cap.isOpened()):
    success, frame = cap.read()
    if not success:
      print("Can't receive frame(stream end?). Exisiting ...")
      break
    gray = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
    rects = detector(gray,0)
        
        
    for rect in rects:
      shape = predictor(gray,rect)
      shape = face_utils.shape_to_np(shape)
            
      leftEye = shape[lStart:lEnd]
      rightEye = shape[rStart:rEnd]
      leftEAR = eye_aspect_ratio(leftEye)
      rightEAR = eye_aspect_ratio(rightEye)
            
      ear = (leftEAR + rightEAR) / 2.0
            
      leftEyeHull = cv2.convexHull(leftEye)
      rightEyeHull = cv2.convexHull(rightEye)
            
      cv2.drawContours(frame,[leftEyeHull],-1 , (0,255,0),1)
      cv2.drawContours(frame , [rightEyeHull],-1 , (0,255,0),1)
            
      if ear < EYE_AR_THRESH:
        COUNTER += 1
                
        if COUNTER >= EYE_AR_CONSEC_FRAMES:
          if not ALARM_ON:
            ALARM_ON = True
            if args["alarm"] != "":
              t=Thread(target = sound_alarm, args =(args["alarm"],))
              t.daemon = True
              t.start()               
          cv2.putText(frame, "DROWSINESS ALERT!!!", (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
      else:
        COUNTER=0
        ALARM_ON = False
                
      cv2.putText(frame,"EAR: {:.2f}".format(ear),(300,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),2)

      frame = cv2.imencode('.JPEG',frame, [cv2.IMWRITE_JPEG_QUALITY,20])[1].tobytes()
      #frame = memoryview(b'\x00'*32)

      yield(b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + frame + b'\r\n')
# start the video stream thread
#print("[INFO] starting video stream thread...")

    
            
        # cv2.imshow("frame",frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break 

# cap.release()
# cv2.destroyAllWindows()

if __name__=="__main__":
  app.run(debug=True)
