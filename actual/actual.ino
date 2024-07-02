#include "actual.h"
char msgEnd = ';';
String instruccion;
bool newMsg = false;

int speed = 0;

void config_encoders()
{
  // Configuracion de MotorShield
  md.init();

  // Configuracion de encoders
  pinMode(encoder0PinA, INPUT);
  digitalWrite(encoder0PinA, HIGH);       // Incluir una resistencia de pullup en le entrada
  pinMode(encoder0PinB, INPUT);
  digitalWrite(encoder0PinB, HIGH);       // Incluir una resistencia de pullup en le entrada
  pinMode(encoder1PinA, INPUT);
  digitalWrite(encoder1PinA, HIGH);       // Incluir una resistencia de pullup en le entrada
  pinMode(encoder1PinB, INPUT);
  digitalWrite(encoder1PinB, HIGH);       // Incluir una resistencia de pullup en le entrada
  attachInterrupt(digitalPinToInterrupt(encoder0PinA), doEncoder0A, CHANGE);  // encoder 0 PIN A
  attachInterrupt(digitalPinToInterrupt(encoder0PinB), doEncoder0B, CHANGE);  // encoder 0 PIN B
  attachInterrupt(digitalPinToInterrupt(encoder1PinA), doEncoder1A, CHANGE);  // encoder 1 PIN A
  attachInterrupt(digitalPinToInterrupt(encoder1PinB), doEncoder1B, CHANGE);  // encoder 1 PIN B
}

void motor_v()
{
  //Seguridad: Establece voltaje máximo para motores
    if (voltage_m0 > 12.0){
      voltage_m0 = 12.0;
    }
    else if (voltage_m0 < -12.0){
      voltage_m0 = -12.0;
    }

    if (voltage_m1 > 12.0){
      voltage_m1 = 12.0;
    }
    else if (voltage_m1 < -12.0){
      voltage_m1 = -12.0;
    }

    // Motor Voltage
    md.setM1Speed(voltage_m0*400.0/12.0);
    md.setM2Speed(voltage_m1*400.0/12.0);
}

void act_encoder_pos()
{
  // Actualizando informacion de los encoders
  newposition0 = encoder0Pos;
  newposition1 = encoder1Pos;
}

void act_vel()
{
  //-----------------------------------
  // Calculando velocidad del motor en unidades de RPM
  float rpm = 31250;
  vel0 = (float)(newposition0 - oldposition0) * rpm / (newtime - time_ant); //RPM
  vel1 = (float)(newposition1 - oldposition1) * rpm / (newtime - time_ant); //RPM
  oldposition0 = newposition0;
  oldposition1 = newposition1;
}

//Se definen funciones PID para cada una de las ruedas
float controller_m0(float kp, float ki, float kd, float vel_deseada)
{
  float e_0 = 0;   // error
  // correcciones separadas
  float c_p = 0;
  float c_i = 0;
  float c_d = 0;
  float c_0 = 0;

  e_0 = vel_deseada - vel0;

  c_p = (kp + (kd / dt)) * e_0;
  c_i = (-kp + (ki * dt) - (2 * kd / dt)) * e_1_m0;
  c_d = (kd / dt) * e_2_m0;
  c_0 = c_1_m0 + c_p + c_i + c_d;

  c_1_m0 = c_0;
  e_2_m0 = e_1_m0;
  e_1_m0 = e_0;
    
  return c_0;
}

float controller_m1(float kp, float ki, float kd, float vel_deseada)
{
  float e_0 = 0;   // error
  // correcciones separadas
  float c_p = 0;
  float c_i = 0;
  float c_d = 0;
  float c_0 = 0;

  e_0 = vel_deseada + vel1;

  c_p = (kp + (kd / dt)) * e_0;
  c_i = (-kp + (ki * dt) - (2 * kd / dt)) * e_1_m1;
  c_d = (kd / dt) * e_2_m1;
  c_0 = c_1_m1 + c_p + c_i + c_d;

  c_1_m1 = c_0;
  e_2_m1 = e_1_m1;
  e_1_m1 = e_0;
    
  return -c_0;
}


String readBuff() {
  String buffArray;
  //int i = 0;

  while (Serial3.available() > 0) { //Entro a este while mientras exista algo en el puerto serial
    char buff = Serial3.read(); //Leo el byte entrante
    if (buff == msgEnd) {
      newMsg = true;
      break; //Si el byte entrante coincide con mi delimitador, me salgo del while
    } else {
      buffArray += buff; //Si no, agrego el byte a mi string para construir el mensaje
      //i += 1;
    }
    delay(10);
  }

  return buffArray;  //Retorno el mensaje
}


void setup()
{
  // Configuracion de Serial Port
  Serial.begin(38400);    
  Serial3.begin(38400);       // Inicializacion del puerto serial (Monitor Serial)
  Serial.println("start");

  config_encoders();
}


void loop() {
  if ((micros() - time_ant) >= Period)
  {
    newtime = micros();
    act_encoder_pos();
    act_vel();


    // Controlador PID valores
    float kp = 0.2;
    float ki = 0.017;
    float kd = 0.0001;

    
    
    

  
  if (Serial3.available() > 0) {
    instruccion = readBuff(); //Leer el mensaje entrante
    //Serial.print("mensaje: ");
    Serial.println(instruccion);
    if (instruccion[0] == 'A' && newMsg) {
      speed = (instruccion.substring(1)).toInt();
      
      voltage_m0 = controller_m0(kp, ki, kd, -speed);
      voltage_m1 = controller_m1(kp, ki, kd, -speed);
    }
    else if (instruccion[0] == 'O' && newMsg) {
      speed = (instruccion.substring(1)).toInt();
      voltage_m0 = controller_m0(kp, ki, kd, -speed/2);
      voltage_m1 = controller_m0(kp, ki, kd, speed/2);
    }
    else if(instruccion[0] == 'F' && newMsg) {
      voltage_m0 = 0;
      voltage_m1 = 0;
    }
  }


  
    //print4();
    //print3();


    motor_v();


    time_ant = newtime;
}
}

    

