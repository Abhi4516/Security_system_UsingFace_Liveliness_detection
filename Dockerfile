FROM python:3.8-slim

# Install dependencies required for your application
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

# Set environment variable for display
ENV DISPLAY=:99

# Create application directory and copy files
COPY . /app
WORKDIR /app

# Install Python dependencies
RUN pip install --default-timeout=100 --no-cache-dir -r Requirements.txt

# Copy additional files
COPY shape_predictor_68_face_landmarks.dat /app/shape_predictor_68_face_landmarks.dat
COPY haarcascade_frontalface_default.xml /app/haarcascade_frontalface_default.xml

COPY banklocker.db /app/banklocker.db
RUN chmod -R 777 /app/banklocker.db

# Expose port 5000 for Flask
EXPOSE 5000

# Start Xvfb and then run the Flask app
CMD ["sh", "-c", "Xvfb :99 -screen 0 1024x768x16 & python mySite.py"]
