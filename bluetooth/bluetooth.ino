#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SoftwareSerial.h>


LiquidCrystal_I2C lcd(0x27, 16, 2);

const int potPin = A0;

int potValue = 0; 
int p = 0;
float maxVoltage = 3.3; 
int maxpotValue = 677; 
float voltage; 

#define user1 15
#define user2 2

#define RX 11
#define TX 10

SoftwareSerial bluetooth(TX, RX);


float vypocet_napeti(){
    potValue = analogRead(potPin); 
    voltage = (maxVoltage/maxpotValue) * potValue; 
    String text = " V";
    String printedValue = String(potValue); 
    return voltage;
    
}
void setup() {
  Serial.begin(9600);
  delay(1000);
  lcd.init();           
  lcd.backlight();     ­
  lcd.setCursor(2, 0);  
  lcd.print("LET projekt"); 
  lcd.setCursor(0, 1);  
  lcd.print("Tep. frek a SpO2"); 
  delay(500);
  lcd.clear();
  pinMode(user1, INPUT);
  pinMode(user2, INPUT);
  bluetooth.begin(9600);

}

void obrazovka1(){
    float napeti = vypocet_napeti();
    Serial.println(napeti);
    lcd.setCursor(5, 0);
    lcd.backlight();
    lcd.print(napeti);
    bluetooth.println(napeti);
    delay(600);
    lcd.clear();
}

void obrazovka2()
{
  // TO DO
  lcd.print("User 2"); 
}

void loop()
{
  bool digit = HIGH; // TO DO digitalRead(user1);
  if (digit == HIGH){
    obrazovka1();}
  else{
    obrazovka2();
  }

}
