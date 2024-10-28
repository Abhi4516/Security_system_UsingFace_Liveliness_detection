FROM python:3.8-slim


RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    libxrender1 \
    libxext6 \
    libx11-6 \
    libxtst6 \
    python3-opencv \
    xvfb \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


ENV DISPLAY=:99


COPY . /app
WORKDIR /app


RUN pip install --default-timeout=100 --no-cache-dir -r Requirements.txt


COPY shape_predictor_68_face_landmarks.dat /app/shape_predictor_68_face_landmarks.dat
COPY haarcascade_frontalface_default.xml /app/haarcascade_frontalface_default.xml

COPY banklocker.db /app/locker.db
RUN chmod -R 777 /app/locker.db


EXPOSE 5000


CMD ["sh", "-c", "Xvfb :99 -screen 0 1024x768x16 & python mySite.py"]
