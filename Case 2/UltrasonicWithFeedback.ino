// Christian Amundsen
// Sande Hus og Hytter

#include <Math.h>
#include <LiquidCrystal.h>

const int led1Pin = 12;
const int led2Pin = 2;
const int led3Pin = 3;
const int potPin = A3;
const int trigPin = 10;  
const int echoPin = 11; 

LiquidCrystal lcd(8, 9, 4, 5, 6, 7);
float potVal = 0;
float duration, distance;  
int refDistance;
unsigned long pulseWidth;
int dist, refDist;


void setup() {

  Serial.begin(9600);

  pinMode(led1Pin,OUTPUT);
  pinMode(led2Pin,OUTPUT);
  pinMode(led3Pin,OUTPUT);

  pinMode(10, OUTPUT);   // Set pin 2 as trigger pin
  digitalWrite(10, LOW); // Set trigger LOW for continuous read
  pinMode(11, INPUT);    // Set pin 3 as monitor pin

  lcd.begin(16, 2);      // start the library
}


void loop() {

  potVal = analogRead(potPin);
  refDistance = (potVal * 100 / 1023);

  pulseWidth = pulseIn(11, HIGH); // Count how long the pulse is high in microseconds

  if(pulseWidth != 0) {
    distance = pulseWidth / 10;   // 10usec = 1 cm of distance
  }

  if (distance < refDistance) { 
    digitalWrite(led1Pin, HIGH); 
    digitalWrite(led2Pin, LOW); 
    digitalWrite(led3Pin, LOW); 
  }
  if (distance == refDistance) {  
    digitalWrite(led1Pin, LOW); 
    digitalWrite(led2Pin, HIGH); 
    digitalWrite(led3Pin, LOW); 
  }
  if (distance > refDistance) { 
    digitalWrite(led1Pin, LOW); 
    digitalWrite(led2Pin, LOW); 
    digitalWrite(led3Pin, HIGH); 
  }

  dist = round(distance);
  refDist = round(refDistance);

  lcd.setCursor(0,0);
  lcd.print("Goal: "); 
  lcd.setCursor(10,0);
  lcd.print(refDist);  
  if (refDist != 100) { lcd.setCursor(12,0); lcd.print(" "); }
  if (refDist < 10)   { lcd.setCursor(11,0); lcd.print(" "); }
  
  lcd.setCursor(0,1);
  lcd.print("Distance: "); 
  lcd.setCursor(10,1);
  lcd.print(dist); 
  if (dist < 100) { lcd.setCursor(12,1); lcd.print(" "); }
  if (dist < 10)   { lcd.setCursor(11,1); lcd.print(" "); }
  
  delay(1000);
}


