# TrashVision Arduino Documentation

## Testing and Development
Install Arduino IDE from https://www.arduino.cc/en/software
1. Open sketch_feb5a.ino in Arduino IDE
2. Select Tools → Board → "Arduino Uno"
3. Select Tools → Port → (your Arduino port)
4. Click Upload button (→) or Ctrl/Cmd + U

### Editing Arduino Files (.ino, .pde) on VsCode
Install Arduino by *moozzyk* extension on VSCode

## Logic

### Serialisation
We use Boolean logic for each static state of the robot. (e.g., False = Stay Still, True = Move)

This won't work if there's multiple states of course, so we have to develop a 'schema', which is basically a relational database that associates binary values with the state of the robot.

ASCII Style Example Schema:
**NOTE:** Pickup trash is implicit in state 1 and 2. Think about it (if AI model detects that trash is non-recyclable or recyclable, it means trash exists in video frame)
```
DEC | BIN | STATE
0   | 0000 | Stay Still
1   | 0001 | Deposit Non-Recyclable #(left bin)
2   | 0002 | Deposit Recyclable #(right bin)
```

### Robot Arm Movement

**NOTE:** All servos are like your joints, circularly rotating, CLOCKWISE by default.

**Mathematical Imagery:**

REMEMBER: Movement cannot exceed 0° or 180°, so HALF a circle.

1. For vertical movements, imagine half circle stood up at the right:
- 0° = down (6 o'clock position)
- 90° = horizontal (3 o'clock position)
- 180° = up (12 o'clock position)
2. For horizontal movements imagine half circle laid down at the bottom:
- 0° = far right
- 90° = center
- 180° = far left

Have a look at the movement schema below:
**DISCLAIMER:** We do not use JSON. This is written in natural language for your understanding.
```json
{
  "Speed": {
    "degrees": 20,
    "chronologicalUnit": "second"
  },
  "Base (M1)": {
    "degrees": 90,
    "movementType": "horizontal",
    "movementDirection": ["left", "right"]  // <- or ->
  },
  "Shoulder (M2)": {
    "degrees": 45,
    "movementType": "vertical",
    "movementDirection": ["up", "down"]
  },
  "Elbow (M3)": {
    "degrees": 180,
    "movementType": "vertical",
    "movementDirection": ["up", "down"]
  },
  "Wrist vertical (M4)": {
    "degrees": 180,
    "movementType": "vertical",
    "movementDirection": ["up", "down"]
  },
  "Wrist rotation (M5)": {
    "degrees": 90,
    "movementType": "rotation",
    "movementDirection": ["left", "right"]
  },
  "Gripper (M6)": {
    "degrees": 10,
    "movementType": "grip",
    "movementDirection": ["open", "close"]
  }
}
```

**Function Call Format**
```cpp
Braccio.ServoMovement(speed, base, shoulder, elbow, wristVertical, wristRotation, gripper)
```


