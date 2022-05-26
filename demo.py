from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)

if not camera.isOpened():
  print("Cannot open Camera")
  exit()

def generate_frame():
  ret, frame = camera.read()
  if not ret:
    print("Can't receive frame(stream end?). Exisiting ...")
    break
  else:
    ret, frame = cv2.imencode('.jpg',frame)
    frame = buffer.tobytes()
  yield(b'--frame\r\n' + b'Content-Type:image/jpeg\r\n\r\n' + frame + b'\r\n')
  return frame
  

@app.route('/')
def index():
  retunr render_template('index.html')
  
@app.route('/video')
def video():
  return Response(generate_frame(),mimetype='mulitpart/x-mixed-replace; boundary=frame')



if __name__=="__main__":
  app.run(debug=True)
