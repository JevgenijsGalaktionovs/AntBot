#ifndef dynamixel_driver_h
#define dynamixel_driver_h

#if (ARDUINO >= 100)
 #include <Arduino.h>    
#else
 #include <WProgram.h>
 #include <pins_arduino.h>
#endif

#define NONE                            0x00
#define READ                            0x01
#define ALL                             0x02

#define STATUS_PACKET_TIMEOUT           100
#define STATUS_FRAME_BUFFER             5

#define ARRAY_LENGTH(x)  (sizeof(x) / sizeof((x)[0]))

//######## Address Table for Dynamixel MX-series #########
#define ADDR_MX_ID                 7
#define ADDR_MX_BAUDRATE           8
#define ADDR_MX_OPERATION_MODE     11
#define ADDR_MX_SECONDARY_ID       12
#define ADDR_MX_PWM_LIMIT          36
#define ADDR_MX_CURRENT_LIMIT      38
#define ADDR_MX_VELOCITY_LIMIT     44
#define ADDR_MX_TORQUE_ENABLE      64
#define ADDR_MX_GOAL_PWM           100
#define ADDR_MX_ACCEL_PROFILE      108
#define ADDR_MX_VELOC_PROFILE      112
#define ADDR_MX_GOAL_POSITION      116
#define ADDR_MX_PRESENT_PWM        124
#define ADDR_MX_PRESENT_LOAD       126
#define ADDR_MX_PRESENT_VELOCITY   128
#define ADDR_MX_PRESENT_POSITION   132

#define SERVO_AMOUNT               18

#define LEN_4BYTE                  4
#define LEN_2BYTE                  2
#define LEN_1BYTE                  1

#define TORQUE_ENABLE              {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1}
#define TORQUE_DISABLE             {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}

#define PWM                        600
#define ACC_PR                     100
#define VEL_PR                     100


class DynamixelClass {
public:
  // Constructor
  DynamixelClass(): Direction_Pin(-1), Status_Return_Value(READ) { }

  // Connection
  void begin(long);
  void begin(HardwareSerial&, long);
  void begin(Stream&);
  void end(void);
  void setDirectionPin(unsigned char);

  // Synchronised Servo Setters
  // For All (18) servos
  void Reboot(void);
  void setAllAccelProfile(int (&accel_prof)[18]);
  void setAllVelocProfile(int (&veloc_prof)[18]);
  void setAllPWMLimit(int (&pwm_arr)[18]);
  void setTorqueOff();
  void setTorqueOn();
  void setAllPositions(int (&pos_arr)[18]);
  // For N servos.
  void setNPositions(int pos_arr[], size_t n);
  void setNVelocProfile(int vel_arr[], size_t n);
  void setNAccelProfile(int acc_arr[], size_t n);
  void setNPWMLimit(int pwm_arr[], size_t n); 

  // Single Servo Setters
  void setHoldingTorque(unsigned char ID, bool Set);
  void setGoalPosition(unsigned char ID, int pos);
  void setGoalVelocity(unsigned char ID, unsigned int vel);
  void setProfileAcceleration(unsigned char ID, unsigned int pac);
  void setProfileVelocity(unsigned char ID, unsigned int pvl);
  void setMode(unsigned char ID, unsigned int mode);
  void setCurrent(unsigned char ID, unsigned int cur, unsigned int cur1);

  // Single Servo Getters
  int   getPosition(unsigned char ID);
  float getPositionDegrees(unsigned char ID);
  float getCurrent(unsigned char ID);

  // Synchronised Servo Getters
  int *getAllPWM(void);
  int *getAllPosition(void);
  int *getAllVelocity(void);


  Stream *_serial;
    
    
private:
  unsigned int SingleWrite(unsigned char ID, unsigned short addr, unsigned char *arr, int n);
  void         SingleRead(unsigned char ID, unsigned short addr, int n);
  void         set18Parameters(int (&DATA)[18], byte DATA_LENGTH, unsigned int ADDR_MX);
  void         setNParameters(int *DATA, size_t n, byte DATA_LENGTH, unsigned int ADDR_MX);
  unsigned int SyncWrite(unsigned short addr, unsigned char*arr, int n, int dataN);

  void SendAndRead(unsigned short addr, int DATA_LEN);
  void SyncRead(unsigned short addr, int DATA_LENGTH);
  void getParameters(void);

  void transmitInstructionPacket(int transLen);
  void readReturnPacket(void);
  void readAll(void);

  unsigned short update_crc(unsigned char *data_blk_ptr, unsigned short data_blk_size);
  void           clearRXbuffer(void);

    // Packet Operations






  unsigned char   Instruction_Packet_Array[64];   // Array to hold instruction packet data
  unsigned int    ReturnPacket[300];              // Array to hold returned status packet data
  unsigned long   Time_Counter;                   // Timer for time out watchers
  char            Direction_Pin;                  // Pin to control TX/RX buffer chip
  unsigned char   Status_Return_Value;            // Status packet return states ( NON , READ , ALL )
  unsigned int    data[SERVO_AMOUNT*3];           // Data from ReturnPacket. Each servo: [ID,data_highbyte,data_lowbyte]
  int             returndata[SERVO_AMOUNT];       // Data return
};


extern DynamixelClass Dynamixel;

#endif
