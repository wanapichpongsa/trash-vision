import serial 
import time 
arduino = serial.Serial(port='COM4', baudrate=9600, timeout=.1) 

isRecyclable = False

if isRecyclable:
    arduino.write(bytes(0, 'utf-8')) 
else:
    arduino.write(bytes(1, 'utf-8')) 
