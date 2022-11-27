FROM python:3.8-slim-buster
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN mkdir /app
ADD . /app
WORKDIR /app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["python3", "AI_CAR-thebatman.py"]