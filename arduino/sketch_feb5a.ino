#include <Braccio.h>
#include <Servo.h> 

constexpr long BAUD_RATE = 9600;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(BAUD_RATE); 
  Serial.setTimeout(1);
  Braccio.begin(); 
}

void loop() {
  // put your main code here, to run repeatedly:
  bool isRecyclable; 
  int python_response = Serial.readString().toInt();
  if(python_response == 0){
    isRecyclable = false; 
  } else if (python_response == 1){
    isRecyclable = true; 
  }
  else {
    Serial.println("Have not received communication yet");
  }
  if(python_response == 0 || python_response == 1){
    pickUpTrash();
    depositTrash(isRecyclable)
  }
  delay(1000); 
}

/* Base (M1):90 degrees
Shoulder (M2): 45 degree
Elbow (M3): 180 degrees
Wrist vertical (M4): 180 degrees
Wrist rotation (M5): 90 degrees
Gripper (M6): 10 degrees
*/ 

void pickUpTrash(){
  Braccio.ServoMovement(20, 90, 45, 90, 180, 90, 10);
  delay(500);
  Braccio.ServoMovement(20, 90, 45, 90, 180, 90, 70);
}

void depositTrash(bool isRecyclable){
  if(isRecyclable){
    Braccio.ServoMovement(20, 45, 45, 120, 180, 90, 70);
    Braccio.ServoMovement(20, 45, 45, 90, 180, 90, 10);
  } else {
    Braccio.ServoMovement(20, 135, 45, 120, 180, 90, 70);
    Braccio.ServoMovement(20, 135, 45, 90, 180, 90, 10);
  }
}