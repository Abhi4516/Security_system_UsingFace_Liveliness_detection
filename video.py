
from imutils.video import VideoStream
import imutils
import time
import cv2
import csv

def video_feed():

	print("[INFO] starting video stream...")
	vs = cv2.VideoCapture(0)

	time.sleep(2.0)

	while True:
	
		ret,frame = vs.read()
		frame = imutils.resize(frame, width=400)
		cv2.imwrite('static/images/test_image.jpg',frame)

		imgencode=cv2.imencode('.jpg',frame)[1]
		stringData=imgencode.tostring()
		
		yield (b'--frame\r\n'
			b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')

		key = cv2.waitKey(1) & 0xFF
	
		
		if key == ord("q"):
			break


	print("[INFO] cleaning up...")
	csv.close()
	cv2.destroyAllWindows()
	vs.stop()
