from ast import Break
from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)



def generate_frame():
  camera = cv2.VideoCapture(0)

  while (camera.isOpened()):
    success, frame = camera.read()
    if not success:
      print("Can't receive frame(stream end?). Exisiting ...")
      break
  
    frame = cv2.imencode('.JPEG',frame, [cv2.IMWRITE_JPEG_QUALITY,20])[1].tobytes()
    #frame = memoryview(b'\x00'*32)

    yield(b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + frame + b'\r\n')
  
  

@app.route('/')
def index():
  return render_template('index.html')
  
@app.route('/video')
def video():
  return Response(generate_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__=="__main__":
  app.run(debug=True)
