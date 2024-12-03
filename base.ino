#include <SoftwareSerial.h>
#define ARDUINO_RX 10
#define ARDUINO_TX 11 
SoftwareSerial arduino(ARDUINO_RX,ARDUINO_TX);

const int buttonPin = 3; // Pin for the button
const int ledPin = 13;   // Pin for the LED
const int buzzerPin = 8; // Pin for the buzzer
const int relayPower=5;


void setup() {
  pinMode(buttonPin, INPUT_PULLUP); // Use internal pull-up resistor
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT); // Set buzzer pin as output
  pinMode(relayPower,OUTPUT);
  digitalWrite(relayPower,HIGH);
  Serial.begin(9600);
  arduino.begin(9600);
}

String reset_entry;
void loop() {
  unsigned long initialtime=0;
  if (digitalRead(buttonPin) == LOW) {
    unsigned long finaltime=millis()-initialtime;
    float calctime=(finaltime/1000.0)+((finaltime%1000)/1000.0);
    String time1= String (calctime);
    String pressed="pressed";
    String team="prithvi";
    arduino.println(pressed);
    arduino.println(team);
    arduino.println(time1);
    digitalWrite(ledPin, HIGH); // Turn on LED
    digitalWrite(buzzerPin,HIGH);
    tone(buzzerPin, 500, 3000); // Play a tone at 1000 Hz for 500 ms
    delay(7000); // Keep LED on for 3 seconds
    digitalWrite(ledPin,LOW);
    digitalWrite(buzzerPin,LOW);
    noTone(buzzerPin);
    while (!arduino.available()) {}
    reset_entry=arduino.readStringUntil('\n');
    if (reset_entry=="reset") {
      Serial.println("reset received 10s over");
      return;
    }
  }

  if (arduino.available()>0) {
    reset_entry=arduino.readStringUntil('\n');
    if (reset_entry=="reset") {
      Serial.println("reset received button not pressed");
      return;
    }
  }
}
  