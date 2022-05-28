FROM ubuntu:18.04

COPY . /app

RUN pip install -r requirments.txt


CMD python3 detect_drowsiness.py
