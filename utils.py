import face_recognition
import cv2
import time
import os
import imutils
from blinks import *  

process_this_frame = True

def faceRecognition():
    global process_this_frame
    global blink

    known_face_names = []
    known_face_encodings = []

    # Load known faces from the dataset directory
    for filename in os.listdir("dataset"):
        image = face_recognition.load_image_file("dataset/" + filename)
        encodings = face_recognition.face_encodings(image)
        
        # Add encoding only if a face is detected in the image
        if encodings:
            known_face_encodings.append(encodings[0])
            known_face_names.append(filename.split('.')[0])
        else:
            print(f"Warning: No face detected in file {filename}")

    # Load and process the test image
    frame = cv2.imread('static/images/test_image.jpg')
    small_frame = cv2.resize(frame, (0, 0), fx=1, fy=1)
    rgb_small_frame = small_frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    people = len(face_locations)  

    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
        face_names.append(name)

    process_this_frame = not process_this_frame
    return face_names, blink, people


def video_feed():
    global blink
    blink = 'Eye Blinking Not Detected !!!'
    print("[INFO] starting video stream...")
    vs = cv2.VideoCapture(0)
    time.sleep(2.0)

    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    while True:
        ret, frame = vs.read()
        frame = imutils.resize(frame, width=400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(20, 20))
        people = len(faces)  

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            face = frame[y:y + h, x:x + w]
            cv2.imwrite('static/images/test_image.jpg', face)

        faces, _, _ = detector.run(image=gray, upsample_num_times=0, adjust_threshold=0.0)
        for face in faces:
            landmarks = predictor(gray, face)
            left_eye_ratio = get_blink_ratio(left_eye_landmarks, landmarks)
            right_eye_ratio = get_blink_ratio(right_eye_landmarks, landmarks)
            blink_ratio = (left_eye_ratio + right_eye_ratio) / 2

            if blink_ratio > BLINK_RATIO_THRESHOLD:
                blink = 'Eye Blinking Detected..!!'
        
        if blink == 'Eye Blinking Detected..!!':
            cv2.putText(frame, blink, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        else:
            cv2.putText(frame, blink, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

        imgencode = cv2.imencode('.jpg', frame)[1]
        stringData = imgencode.tobytes()
        yield (b'--frame\r\n' b'Content-Type: text/plain\r\n\r\n' + stringData + b'\r\n')

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    print("[INFO] cleaning up...")
    vs.release()
    cv2.destroyAllWindows()


