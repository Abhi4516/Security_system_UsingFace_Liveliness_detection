#include<Servo.h>
Servo door;
unsigned char cmd;
void setup() 
{
  Serial.begin(9600);
  door.attach(3);

}

void loop() 
{
  if(Serial.available()>0)
  {
    cmd = Serial.read();
    if(cmd == 'O')
    {
      door.write(180);
      delay(5000);
      door.write(0);
    }
  }

}
