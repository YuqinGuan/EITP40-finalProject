/*
  Active Learning Labs
  Harvard University 
  tinyMLx - OV7675 Camera Test

*/

#include <TinyMLShield.h>
//#include <Arduino_OV767X.h>
#include <time.h>

bool commandRecv = false; // flag used for indicating receipt of commands from serial port
bool liveFlag = false; // flag as true to live stream raw camera bytes, set as false to take single images on command
bool captureFlag = false;

// Image buffer;
// QCIF: 176x144 x 2 bytes per pixel (RGB565)
byte image[320 * 240 * 2];//QVGA
int bytesPerFrame;

void setup() {
  Serial.begin(9600);
  while (!Serial);

  initializeShield();
  
  // Initialize the OV7675 camera
  if (!Camera.begin(QVGA, RGB565, 1, OV7675)) {
    Serial.println("Failed to initialize camera");
    while (1);
  }
  bytesPerFrame = Camera.width() * Camera.height() * Camera.bytesPerPixel();
}

void loop() {
  int i = 0;
  String command;
  bool clicked = readShieldButton();
  if (clicked) {
    captureFlag=true;
  }

  // Read incoming commands from serial monitor
  while (Serial.available()) {
    char c = Serial.read();
    if ((c != '\n') && (c != '\r')) {
      command.concat(c);
    } 
    else if (c == '\r') {
      commandRecv = true;
      command.toLowerCase();
    }
  }

  if (captureFlag) {
    captureFlag = false;
    Camera.readFrame(image);
    
    for (int i = 0; i < bytesPerFrame - 1; i += 2) {
      Serial.print("0x");
      Serial.print(image[i+1], HEX);
      Serial.print(image[i], HEX);
      if (i != bytesPerFrame - 2) {
        Serial.print(", ");
      }
    }
    Serial.println();
  } 
}