import serial 
import time 
import logging

"""
DISCLAIMER: This file cannot be run on Arduino IDE.
"""

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Arduino Port
arduino = serial.Serial(port='COM4', baudrate=9600, timeout=.1)

def encodeState(trashPresent: bool, isRecyclable: bool) -> int:
    if not trashPresent:
        return 0
    return 1 + (2 if isRecyclable else 1) # Read ARDUINO.md for schema



# Arbitrarily assign values for testing
trashPresent = False
isRecyclable = False

state: int = encodeState(trashPresent, isRecyclable)

match state:
    case 0:
        logging.info("No trash detected")
    case 1:
        logging.info("Trash detected")
    case 2:
        logging.info("Trash is not recyclable")
    case 3:
        logging.info("Trash is recyclable")

arduino.write(bytes(state, 'utf-8'))
