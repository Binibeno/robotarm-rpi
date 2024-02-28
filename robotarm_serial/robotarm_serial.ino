#include "Braccio_fork.h"
#include <Servo.h>

Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

// the original libary is superior to the v2 in every way EXCEPT,
//that without modifying the original libary there is no way to cancel a movment that is in progress
// OR change the movements destination while it is in the progress of moving

//Set these values from the min/max values below.


void setup() {
  // see libary at https://github.com/arduino-libraries/Braccio
  Serial.begin(9600);
  Serial.println("Initializing... Please Wait");  //Start of initialization, see note below regarding begin method.

  // the braccio libary enforces these limits for angles (for good reasons!)
  /*
   Step Delay: a milliseconds delay between the movement of each servo.  Allowed values from 10 to 30 msec.
              This is basically the speed of the arm's movement.
   M1=base degrees. Allowed values from 0 to 180 degrees
   M2=shoulder degrees. Allowed values from 15 to 165 degrees
   M3=elbow degrees. Allowed values from 0 to 180 degrees
   M4=wrist vertical degrees. Allowed values from 0 to 180 degrees
   M5=wrist rotation degrees. Allowed values from 0 to 180 degrees
   M6=gripper degrees. Allowed values from 10 to 73 degrees. 10: the toungue is open, 73: the gripper is closed.
  */
  // the wrist-rot servo doesn't really like to go to the edge, I would limit it at 20-160

  //! my phyisical config is also different, my gripper goes from 25 to 95


  //All the servo motors will be positioned in the "safety" position:
  //Base (M1):90 degrees
  //Shoulder (M2): 45 degrees
  //Elbow (M3): 180 degrees
  //Wrist vertical (M4): 180 degrees
  //Wrist rotation (M5): 90 degrees
  //gripper (M6): 10 degrees

  Braccio.begin();

  //NOTE: The begin method takes approximately 8 seconds to start, due to the time required
  //to initialize the power circuitry and fuses.

  Serial.println("Initialization Complete, Begin Control");  //All setup is done, the arm is ready to move.
  Serial.println("Available Commands: 'm' memo, 'u' update all joints at once. ");
  Serial.println("Format: m[0-5][0-180] to change the position.");
  Serial.println("Example: m2090 to get joint 2 to 90°.");
  Serial.println("PLEASE USE ADAFRUIT METRO M0. It is important because regular arduino's serial seems to freeze for no good reason.");
  // DO NOT REMOVE THIS LINE
  Serial.println("READY");
}

char *JointTypes[] = {
  "base",
  "shoulder",
  "elbow",
  "wrist",
  "wrist rotation",
  "gripper"
};


int JointAngles[6] = { 90, 90, 90, 90, 90 };

// default joint
int currentJoint = 0;

void loop() {
  // how it works:
  // dictate servo positions one-by-one using m (memo)
  // move all at once using u (update)

  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');  // Read the input string until newline character
    input.trim();                                 // Remove leading and trailing whitespaces

    if (input.startsWith("m")) {                        // Check if the string starts with 'm'
      if (input.length() >= 5) {                        // Ensure the string is long enough
        int currentJoint = input.charAt(1) - '0';       // Convert the character to integer
        int currentAngle = input.substring(2).toInt();  // Convert the substring to integer

        JointAngles[currentJoint] = currentAngle;

        // Print the extracted values
        Serial.print("CurrentJoint: ");
        Serial.println(currentJoint);
        Serial.print("CurrentAngle: ");
        Serial.println(currentAngle);
        Serial.println("OK");
      } else {
        Serial.println("Invalid memo input length");
      }
    }

    // update from jointarray
    else if (input.startsWith("u")) {
      Braccio.ServoMovement(25, JointAngles[0], JointAngles[1], JointAngles[2], JointAngles[3], JointAngles[4], JointAngles[5]);
      delay(10);
    } else if (input.startsWith("check")) {
      Serial.println("READY");
    }

    else {
      Serial.println("Invalid input format");
    }
  }
}
