#include <Braccio.h>
#include <Servo.h>
#include <iostream>

/*
NOTICE: See ARDUINO.md 'Testing and Development' to run this file.
*/

constexpr long BAUD_RATE = 9600; //BAUD is serial communication speed (e.g., 9600bits/second)

// Servo is Braccio motors that rotate between 0 and 180 degrees
Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_ver;
Servo wrist_rot;
Servo gripper;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(BAUD_RATE); 
  Serial.setTimeout(1); // 1ms window of waiting for data before continuing
  Braccio.begin(); 
}

// see ARDUINO.md 'Logic' for reasoning behind degree arguments for Braccio.ServoMovement()
void pickUpTrash() {
  // TO JAMES: Shouldn't wrist_ver be 90° i.e., straight ahead?
  Braccio.ServoMovement(20, 90, 45, 90, 90, 90, 10);
  delay(500);
  // Same position but gripper closes (70°)
  Braccio.ServoMovement(20, 90, 45, 90, 90, 90, 70);
}

void depositTrash(int serialMessage){
  bool isRecyclable;
  if (serialMessage == 1) {
    isRecyclable = false;  // Non-recyclable -> left bin
  } else if (serialMessage == 2) {
    isRecyclable = true;   // Recyclable -> right bin
  }

  if (isRecyclable) {
    Braccio.ServoMovement(20, 45, 45, 120, 90, 90, 70);
    Braccio.ServoMovement(20, 45, 45, 90, 90, 90, 10);
  } else {
    Braccio.ServoMovement(20, 135, 45, 120, 180, 90, 70);
    Braccio.ServoMovement(20, 135, 45, 90, 180, 90, 10);
  }
}

// Upon upload (command U), the Arduino will run this loop indefinitely. No need for return 0 for C/C++ compiler.
void loop() {
  // put your main code here, to run repeatedly:
  readAISerial = Serial.read();
  if (readAISerial > 0) {
    pickUpTrash();
    depositTrash(readAISerial);
  } else if (readAISerial > 2) {
    std::cerr << "Invalid movement command received: " << readAISerial << "\n";
  }

  delay(5000); // 5 seconds for safety
}