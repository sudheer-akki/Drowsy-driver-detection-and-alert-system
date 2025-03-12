FROM ubuntu:18.04

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "detect_drowsiness.py"]
