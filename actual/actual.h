
// Importar librerias
#include "DualVNH5019MotorShield.h"
DualVNH5019MotorShield md;

#include "QTRSensors.h"
QTRSensors qtr;


// Definicion de PINs
#define encoder0PinA  19
#define encoder0PinB  18
#define encoder1PinA  20
#define encoder1PinB  21

// Variables tiempo
unsigned long time_ant = 0;
const int Period = 10000;   // 10 ms = 100Hz
const float dt = Period *0.000001f;   // Tiempo de muestreo
float voltage_m0 = 0.0;   // Voltaje que se aplica a motor 0
float voltage_m1 = 0.0;   // Voltaje que se aplica a motor 1

// Variables de los encoders y posicion
volatile long encoder0Pos = 0;
volatile long encoder1Pos = 0;
long newposition0;
long oldposition0 = 0;
long newposition1;
long oldposition1 = 0;
unsigned long newtime;
float vel0;   // Velocidad del motor 0 en RPM
float vel1;   // Velocidad del motor 1 en RPM


float vel_deseada_m0 = 0;
float vel_deseada_m1 = 0;


// variables controllador motores
// m0
float e_1_m0 = 0;
float e_2_m0 = 0;
float c_1_m0 = 0;

// m1
float e_1_m1 = 0;
float e_2_m1 = 0;
float c_1_m1 = 0;


//-----------------------------------
// CONFIGURANDO INTERRUPCIONES
void doEncoder0A()
{
  if (digitalRead(encoder0PinA) == digitalRead(encoder0PinB)) {
    encoder0Pos++;
  } else {
    encoder0Pos--;
  }
}

void doEncoder0B()
{
  if (digitalRead(encoder0PinA) == digitalRead(encoder0PinB)) {
    encoder0Pos--;
  } else {
    encoder0Pos++;
  }
}

void doEncoder1A()
{
  if (digitalRead(encoder1PinA) == digitalRead(encoder1PinB)) {
    encoder1Pos++;
  } else {
    encoder1Pos--;
  }
}

void doEncoder1B()
{
  if (digitalRead(encoder1PinA) == digitalRead(encoder1PinB)) {
    encoder1Pos--;
  } else {
    encoder1Pos++;
  }
}


// ----------------------------------------------
// modularización 

void print()
{
  // Reportar datos
    Serial.print("$,");
    Serial.print(newtime);
    Serial.print(",");
    Serial.print(newposition0);
    Serial.print(",");
    Serial.print(newposition1);
    Serial.print(",");
    Serial.print(vel0);
    Serial.print(",");
    Serial.print(vel1);
    Serial.print(",");
    Serial.print(voltage_m0);
    Serial.print(",");
    Serial.print(voltage_m1);
    Serial.println(",");
}

void print2()
{
  // Reportar datos
    Serial.print(" | ");
    Serial.print(newposition0);
    Serial.print(" | ");
    Serial.print(newposition1);
    Serial.print(" | ");
    Serial.print(vel0);
    Serial.print(" | ");
    Serial.print(vel1);
    Serial.print(" | ");
    Serial.print(voltage_m0);
    Serial.print(" | ");
    Serial.print(voltage_m1);
    Serial.println(" | ");
}

void print3()
{
  // Reportar datos
    Serial.print(" Pos_0: ");
    Serial.print(newposition0);
    Serial.print(" | Vel_0: ");
    Serial.print(vel0);
    Serial.print(" | voltage_0: ");
    Serial.print(voltage_m0);
    Serial.println(" | ");
}

void print4()
{
  // Reportar datos
    Serial.print(" Pos_1: ");
    Serial.print(-1 * newposition1);
    Serial.print(" | Vel_1: ");
    Serial.print(-1 * vel1);
    Serial.print(" | voltage_1: ");
    Serial.print(-1 * voltage_m1);
    Serial.print(" |           ");
}

