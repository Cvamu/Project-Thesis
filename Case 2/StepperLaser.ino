#include <math.h>
#include <AccelStepper.h>

// Define the stepper motor and the pins that is connected to
AccelStepper stepper(1, 2, 5); // (Typeof driver: with 2 pins, STEP, DIR)


const int dist0 = 300; //distance from laser to the sawblade
const int h = 810; //height the laser is mounted on. Table height for prototypes
int x; // global def of varaiables
float alpha;
int a;
int adjust = 1;

void setup() {
  Serial.begin(9600);
  stepper.setMaxSpeed(2000); // Set maximum speed value for the stepper
  stepper.setAcceleration(2000); // Set acceleration value for the stepper
  stepper.setCurrentPosition(0); // Set the current position to 0 steps
 while (adjust!=0) {  //a adjustmen phase once the laser is turned on, to make sure the 0 value is indeed straight down
     Serial.println("Adjust: ");
  while (!Serial.available()) {
    // Wait for input
  }
  
  adjust = Serial.parseInt();
  Serial.print("Received adjust: ");
  Serial.println(adjust);

  // Clear the Serial buffer to avoid reading line endings as 0
  while (Serial.available() > 0) {
    char junk = Serial.read();
  }
stepper.moveTo(adjust);
stepper.runToPosition();
stepper.setCurrentPosition(0);
  } 
}

void loop() {
  Serial.println("input x: "); //takes in input from user
  while (!Serial.available()) {
    // Wait for input
  }
  
  x = Serial.parseInt();
  Serial.print("Received x: ");
  Serial.println(x);

  // Clear the Serial buffer to avoid reading line endings as 0
  while (Serial.available() > 0) {
    char junk = Serial.read();
  }

  if (x < dist0) {
    a = dist0 - x;
    alpha = atan2(a, h);
   stepper.moveTo(round((alpha) * (1600 / M_PI))); //set desired move
    
  } else if (x > dist0) {
    a = x - dist0;
    alpha = atan2(a, h);
    stepper.moveTo(round( -(alpha) * (1600 / M_PI))); //set desired move
  } else {
    alpha = 0;
    stepper.moveTo(0); //90 deg, same as initial pos
  }

  // Print calculated alpha and steps for debugging
  Serial.print("Calculated alpha: ");
  Serial.println(alpha * (180 / M_PI));
  Serial.print("Calculated stepps: ");
  Serial.println((alpha) * (1600 / M_PI));

  stepper.runToPosition(); // Moves the motor to target position w/ acceleration/ deceleration and it blocks until is in position
 
}
