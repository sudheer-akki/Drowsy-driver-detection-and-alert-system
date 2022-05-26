from flask import Flask, render_template
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)

@app.route('/')
def index():
  retunr render_template
