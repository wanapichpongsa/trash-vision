import serial
from serial.tools import list_ports
import logging
import time

"""
DISCLAIMER: This file cannot be run on Arduino IDE.
"""

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Go to Tools -> Port -> (your port) to see your port
ports = list_ports.comports()
for port in ports:
    logging.info(f"Found port: {port.device} - {port.description}")
macPort = '/dev/cu.Bluetooth-Incoming-Port'
windowsPort = 'COM4'

try:
    startTime = time.time()
    arduino = serial.Serial(port=macPort, baudrate=9600, timeout=.1)
    logging.info(f"Opened port: {arduino.name}")

    def encodeState(trashPresent: bool, isRecyclable: bool) -> int:
        if not trashPresent and not isRecyclable:
            return 0
        elif not trashPresent and isRecyclable: # I don't know how this would be possible but just thought of it
            raise ValueError("Contradictory state: Trash not present but is recyclable")
        return (2 if isRecyclable else 1) # Read ARDUINO.md for schema

    # Arbitrarily assign values for testing
    trashPresent = False
    isRecyclable = False

    state: int = encodeState(trashPresent, isRecyclable)

    match state:
        case 0:
            logging.info("No trash detected")
        case 1:
            logging.info("Trash is not recyclable")
        case 2:
            logging.info("Trash is recyclable")

    # Once we exceed single byte communication, we use state.to_bytes(length=int, byteorder='little') Arduino is little-endian (AVR)
    logging.info(f"Writing: {state} as bytes: {bytes([state])}")
    arduino.write(bytes([state]))

    readState = arduino.read()
    readStateInt: int = int.from_bytes(readState, byteorder='little')
    logging.info(f"Wrote: {state} -> Read: {readStateInt}")
    if state != readStateInt:
        raise ValueError("Written state doesn't match read state")
    
except serial.SerialException as e:
    logging.error(f"Port error: {e}")
    raise e
finally:
    logging.info("Closing port")
    arduino.close()
    logging.info(f"Time Elapsed: {time.time() - startTime:.2f}s")