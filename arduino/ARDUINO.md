# TrashVision Arduino Documentation

## Testing and Development
Install Arduino IDE from https://www.arduino.cc/en/software
1. Open sketch_feb5a.ino in Arduino IDE
2. Select Tools → Board → "Arduino Uno"
3. Select Tools → Port → (your Arduino port)
4. Click Upload button (→) or Ctrl/Cmd + U

## Logic
We use Boolean logic for each static state of the robot. (e.g., False = Stay Still, True = Move)

This won't work if there's multiple states of course, so we have to develop a 'schema', which is basically a relational database that associates binary values with the state of the robot.

ASCII Style Example Schema:
```
DEC | BIN | STATE
0   | 0000 | Stay Still
1   | 0001 | Pick Up Trash
2   | 0010 | Deposit Non-Recyclable #(left bin)
3   | 0011 | Deposit Recyclable #(right bin)
```

