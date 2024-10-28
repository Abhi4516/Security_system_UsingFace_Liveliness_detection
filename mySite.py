# import the necessary packages
from flask import Flask, render_template, redirect, url_for, request,session,Response
import os
import cv2
from utils import *
import pandas as pd
from playsound import playsound
import sqlite3
#from sms import *
#camerafrom arduino import *

username=''
password=''

app = Flask(__name__)

app.secret_key = '1234'
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/', methods=['GET', 'POST'])
def landing():
	return render_template('home.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
	return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	global username
	global password
	global full_name,age,gender,contact
	error = ""

	if request.method=='POST':
		username = request.form['username']
		password = request.form['password']
		full_name = request.form['full_name']
		age = request.form['age']
		gender = request.form['gender']
		contact = request.form['contact']
		
		return redirect(url_for('register1'))
		
	return render_template('register.html',error=error)

@app.route('/register1', methods=['GET', 'POST'])
def register1():
	global username
	global password
	global full_name,age,gender,contact
	
	if request.method=='POST':

		username = request.form['username']
		password = request.form['password']

		con = sqlite3.connect('locker.db')
		cursorObj = con.cursor()
		cursorObj.execute("CREATE TABLE IF NOT EXISTS Users (UserName text,Password text)")
		cursorObj.execute("INSERT INTO Users VALUES(?,?)",(username,password))
		con.commit()

		img = cv2.imread('static/images/test_image.jpg')
		cv2.imwrite('dataset/'+username+'.jpg', img)

		return redirect(url_for('register'))

	return render_template('register1.html',username=username,password= password,full_name=full_name,contact=contact,age=age,gender=gender)


@app.route('/login', methods=['GET', 'POST'])
def login():
	global username
	global password
	error = ""

	if request.method=='POST':
		username = request.form['username']
		password = request.form['password']

		con = sqlite3.connect('locker.db')
		cursorObj = con.cursor()
		cursorObj.execute(f"SELECT UserName from Users WHERE UserName='{username}' AND password = '{password}';")
	
		if(cursorObj.fetchone()):
			return redirect(url_for('login1'))
		else:
			error = "Invalid Credentials Please try again..!!!"
		
	return render_template('login.html',error=error)

@app.route('/login1', methods=['GET', 'POST'])
def login1():
	global username
	global password
	error = ''
	
	if request.method=='POST':
		username = request.form['username']
		password = request.form['password']
		face,blink,people = faceRecognition()
		print('Detected Face:',face,blink,people)
		if(blink == 'Eye Blinking Detected..!!'):
			if(people > 1):
				error = 'Multiple Faces Detected, Plz Try again..!!'
				#sendSMS('Multiple Faces Detected for Locker:'+username)
			elif(people == 0):
				error = 'Unknown Face Detected Plz Try again..!!'
				#sendSMS('Multiple Faces Detected for Locker:'+username)
			else:
				if(face[0] == username):
					return redirect(url_for('locker'))
				else:
					error = 'Unknown Face Detected Plz Try again..!!'
					#sendSMS('Multiple Faces Detected for Locker:'+username)
		else:
			error = 'No Live Face Found'
			#sendSMS('Live Face Not Found for Locker:'+username)			

	return render_template('login1.html',username=username,password= password,error=error)



@app.route('/locker')
def locker():
	#sendSerial(b'O')
	return render_template('locker.html')

@app.route('/video_stream')
def video_stream():

	return Response(video_feed(),mimetype='multipart/x-mixed-replace; boundary=frame')


# No caching at all for API endpoints.
@app.after_request
def add_header(response):
	# response.cache_control.no_store = True
	response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
	response.headers['Pragma'] = 'no-cache'
	response.headers['Expires'] = '-1'
	return response


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, threaded=True)