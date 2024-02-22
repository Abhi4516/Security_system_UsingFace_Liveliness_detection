import serial

ser = serial.Serial('COM9',9600,timeout=0.1)
ser.setDTR(False)
ser.close()

def sendSerial(data):
    ser.open()
    ser.write(data)
    ser.close()
