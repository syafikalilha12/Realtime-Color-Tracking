#include<Servo.h>
Servo X ;
char x;
long int v;
void setup() {
X.attach(4);
 Serial.begin(9600);
   X.write(90);
}

void loop() {
if(Serial.available()>2){
  x =Serial.read();
  v =Serial.parseInt();
 if(x =='a'){
    X.write(v);  
  }
  delay(10);
  }
}
