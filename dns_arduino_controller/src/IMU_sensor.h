#ifndef IMU_sensor_h
#define IMU_sensor_h
#include <Arduino.h>

#define ADDR_ACCEL_XOUT_H 59   // Accl data first register address 0x3B
#define ADDR_GYRO_FIRST_REG 67 // Gyro data first register address 0x43
 
const int ADDR_IMU = 104, // IMU6050 I2C address
          ADDR_6B  = 107;

class IMUClass {
public:
    float roll_pitch_yaw[3]; // Raw IR data
    float ax, ay, az;
    float gx, gy, gz;
    float temp;
    float accAngleX, accAngleY, gyroAngleX, gyroAngleY, gyroAngleZ;
    float roll, pitch, yaw;
    float AccErrorX, AccErrorY, GyroErrorX, GyroErrorY, GyroErrorZ;
    
    void begin();
    void update_IMU();
    float * getRollPitchYaw();

private:
    void requestSensor(const int ADDR_ID, const int ADDR_REGISTER);
    void calculate_IMU_error();
};

extern IMUClass IMU;

#endif