#include <Servo.h>

#define POS_ON 104
#define POS_OFF 52
#define SRVO 9

Servo camera;


void setup()
{
    camera.attach(SRVO);
    setCameraState("off");
    Serial.begin(9600);
}

int setCameraState(String command) {
    if (command == "on") {
      camera.write(POS_ON);
    }
    if (command == "off") {
      camera.write(POS_OFF);
    }
    return 1;
}

void loop() {
   String command = Serial.readStringUntil('\n');
   setCameraState(command);
}