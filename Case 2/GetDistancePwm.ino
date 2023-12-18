
unsigned long pulseWidth;

void setup()
{
  Serial.begin(9600); // Start serial communications

  pinMode(10, OUTPUT); // Set pin 2 as trigger pin
  digitalWrite(10, LOW); // Set trigger LOW for continuous read

  pinMode(11, INPUT); // Set pin 3 as monitor pin
}

void loop()
{
  pulseWidth = pulseIn(11, HIGH); // Count how long the pulse is high in microseconds

  // If we get a reading that isn't zero, let's print it
  if(pulseWidth != 0)
  {
    pulseWidth = pulseWidth / 10; // 10usec = 1 cm of distance
    Serial.println(pulseWidth); // Print the distance
  }
  delay(200);
}
