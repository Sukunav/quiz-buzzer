#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <Wire.h>
#include <SoftwareSerial.h>
#include <WiFiUDP.h>
#define ESP_RX 4 //D2
#define ESP_TX 5 //D1
SoftwareSerial esp(ESP_RX,ESP_TX);
WiFiUDP udp;

char wifi_name[] = "Computer_lab1";
char password[] = "Ssv@1010";
char host[255];
const uint16_t port = 8080;
const uint16_t tempport = 12345;   


String pressstat;
String team;
String time1;
String reset_entry;
int Sno = 1;

WiFiClient client;
void setup() {
  Serial.begin(9600);

  WiFi.begin(wifi_name, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println(".");
  }
  esp.begin(9600);
  udp.begin(tempport);
  Serial.println("Connected to WiFi. IP: " + WiFi.localIP().toString());
  int packetSize = 0;
  while (packetSize<=0) {
    packetSize=udp.parsePacket();
  }
  int len = udp.read(host, 255);
  if (len > 0) host[len] = '\0';
  Serial.printf("Broadcast received: %s\n", host);
  while (!client.connected()) {
    client.connect(host,8080);
  }
  client.println("ready to communicate!");
  client.stop();
}


void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    if (esp.available()>0) {
      while (!client.connected()) {
        client.connect(host,port);
      }
      pressstat=esp.readStringUntil('\n');
      team=esp.readStringUntil('\n');
      time1=esp.readStringUntil('\n');
      client.println(String("SEND TO SERVER,")  + String(Sno) + "," + String(team) + "," + String(pressstat) + "," + String(time1));
      client.stop();
      while (!client.connected()) {
        client.connect(host,port);
      }
      client.println("CHECK FOR RESET:"+String(Sno));
      while (!client.available()) {}
      reset_entry = client.readStringUntil('\n');
      if (reset_entry == "reset") {
        esp.println(reset_entry);
        client.stop();
        Sno++;
        return;
      }
    }
    //loop that checks whether other buttons has been pressed
    if (Serial.available()<= 0) {
      while (!client.connected()) {
        client.connect(host,port);
      }
      client.println("CHECK FOR RESET EXTRA:"+String(Sno));
      while (!client.available()) {}
      reset_entry = client.readStringUntil('\n');
      if (reset_entry == "reset") {
        esp.println(reset_entry);
        client.stop();
        Sno++;
        return;
      }
    }
  }

  else {
    Serial.println("WiFi Disconnected");
    return;
  }
}



