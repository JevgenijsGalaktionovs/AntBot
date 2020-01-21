#include "IMU_sensor.h"
#include <Wire.h>

float elapsedTime, currentTime, previousTime;


void IMUClass::begin(){
  Wire.begin();                      // Initialize comunication
  Wire.beginTransmission(ADDR_IMU);  // Start communication with IMU6050 // IMU=0x68
  Wire.write(ADDR_6B);               // Talk to the register 6B
  Wire.write(0);                     // Make reset - place a 0 into the 6B register
  Wire.endTransmission(true);        //end the transmission
  /*
  // Configure Accelerometer Sensitivity - Full Scale Range (default +/- 2g)
  Wire.beginTransmission(MPU);
  Wire.write(0x1C);                  //Talk to the ACCEL_CONFIG register (1C hex)
  Wire.write(0x10);                  //Set the register bits as 00010000 (+/- 8g full scale range)
  Wire.endTransmission(true);
  // Configure Gyro Sensitivity - Full Scale Range (default +/- 250deg/s)
  Wire.beginTransmission(MPU);
  Wire.write(0x1B);                   // Talk to the GYRO_CONFIG register (1B hex)
  Wire.write(0x10);                   // Set the register bits as 00010000 (1000deg/s full scale)
  Wire.endTransmission(true);
  delay(20);
  */
  delay(20);
  calculate_IMU_error();
}

void IMUClass::requestSensor(const int ADDR_ID, const int ADDR_REGISTER){
  Wire.beginTransmission(ADDR_ID);
  Wire.write(ADDR_REGISTER); // Start with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(ADDR_ID, 6, true); // Read 6 registers total, each axis value is stored in 2 registers
}

void IMUClass::update_IMU(){
  // === Read acceleromter data === //
  Wire.beginTransmission(ADDR_IMU);
  Wire.write(0x3B); // starting with register 0x3B (ACCEL_XOUT_H) [MPU-6000 and MPU-6050 Register Map and Descriptions Revision 4.2, p.40]
  Wire.endTransmission(false); // the parameter indicates that the Arduino will send a restart. As a result, the connection is kept active.
  Wire.requestFrom(ADDR_IMU, 7*2, true); // request a total of 7*2=14 registers

  ax = Wire.read()<<8 | Wire.read(); // reading registers: 0x3B (ACCEL_XOUT_H) and 0x3C (ACCEL_XOUT_L)
  ay = Wire.read()<<8 | Wire.read(); // reading registers: 0x3D (ACCEL_YOUT_H) and 0x3E (ACCEL_YOUT_L)
  az = Wire.read()<<8 | Wire.read(); // reading registers: 0x3F (ACCEL_ZOUT_H) and 0x40 (ACCEL_ZOUT_L)
  temp = Wire.read()<<8 | Wire.read(); // reading registers: 0x41 (TEMP_OUT_H) and 0x42 (TEMP_OUT_L)
  gx = Wire.read()<<8 | Wire.read(); // reading registers: 0x43 (GYRO_XOUT_H) and 0x44 (GYRO_XOUT_L)
  gy = Wire.read()<<8 | Wire.read(); // reading registers: 0x45 (GYRO_YOUT_H) and 0x46 (GYRO_YOUT_L)
  gz = Wire.read()<<8 | Wire.read(); // reading registers: 0x47 (GYRO_ZOUT_H) and 0x48 (GYRO_ZOUT_L)
  roll_pitch_yaw[0] = gx;
  roll_pitch_yaw[1] = gy;
  roll_pitch_yaw[2] = gz;
  // Serial.print(gx); Serial.print(", ");
  // Serial.print(gy); Serial.print(", ");
  // Serial.print(gz); Serial.println(", ");
  // Serial.print(ax); Serial.print(", ");
  // Serial.print(ay); Serial.print(", ");
  // Serial.print(az); Serial.println(", ");
  
  // WORK IS NOT DONE HERE
}

void IMUClass::calculate_IMU_error() {
  // We can call this funtion in the setup section to calculate the accelerometer and gyro data error. From here we will get the error values used in the above equations printed on the Serial Monitor.
  // Note that we should place the IMU flat in order to get the proper values, so that we then can the correct values
  // Read accelerometer values 200 times
  int c = 0; 
  while (c < 200) {
    requestSensor(ADDR_IMU, ADDR_ACCEL_XOUT_H);
    ax = (Wire.read() << 8 | Wire.read());
    ay = (Wire.read() << 8 | Wire.read());
    az = (Wire.read() << 8 | Wire.read());
    // Sum all readings
    AccErrorX = AccErrorX + ((atan((ay) / sqrt(pow((ax), 2) + pow((az), 2))) * 180 / PI));
    AccErrorY = AccErrorY + ((atan(-1 * (ax) / sqrt(pow((ay), 2) + pow((az), 2))) * 180 / PI));
    c++;
  }
  //Divide the sum by 200 to get the error value
  AccErrorX = AccErrorX / 200;
  AccErrorY = AccErrorY / 200;
  c = 0;

  // Read gyro values 200 times
  while (c < 200) {
    requestSensor(ADDR_IMU, ADDR_GYRO_FIRST_REG);
    gx = Wire.read() << 8 | Wire.read();
    gy = Wire.read() << 8 | Wire.read();
    gz = Wire.read() << 8 | Wire.read();
    // Sum all readings
    GyroErrorX = GyroErrorX + (gx);
    GyroErrorY = GyroErrorY + (gy);
    GyroErrorZ = GyroErrorZ + (gz);
    c++;
  }
  //Divide the sum by 200 to get the error value
  GyroErrorX = GyroErrorX / 200;
  GyroErrorY = GyroErrorY / 200;
  GyroErrorZ = GyroErrorZ / 200;
}

float * IMUClass::getRollPitchYaw(){
  return IMUClass::roll_pitch_yaw;
}

IMUClass IMU;