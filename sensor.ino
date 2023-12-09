int trig = 7;
int echo = 8;
long unsigned time_us;
float distance_cm;

void setup() {
  // put your setup code here, to run once:
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);
  Serial.begin(9600); // corrected baud rate
}

float measure() {
  // put your main code here, to run repeatedly:
  digitalWrite(trig, LOW);
  delayMicroseconds(2); // Increased delay for stability
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);

  time_us = pulseIn(echo, HIGH);
  distance_cm = 0.017 * time_us;
  return distance_cm;
}

void loop() {
  float sum = 0;
  float dis = 0;

  for (int i = 1; i <= 100; i++) {
    dis = measure();
    sum = sum + dis;
  }

  float averageDistance = sum / 100.0; // Corrected to use floating-point division
  Serial.println("Averaged: " + String(floor(averageDistance/50)));
}
