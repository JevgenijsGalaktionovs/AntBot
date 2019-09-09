#include <dynamixel_driver.h>

//############################ Public Methods ##################################
// Serial Connection
void DynamixelClass::begin(long baud){
  #if defined(__AVR_ATmega32U4__) || defined(__MK20DX128__) || defined(__AVR_ATmega2560__)
    Serial2.begin(baud);  // Set up Serial for Leonardo and Mega
    _serial = &Serial2;
  #else
    Serial.begin(baud);   // Set up Serial for all others (Uno, etc)
    _serial = &Serial;
  #endif 
}
void DynamixelClass::begin(HardwareSerial &HWserial, long baud){
  HWserial.begin(baud); // Set up Serial for a specified Serial object
  _serial = &HWserial;
}
void DynamixelClass::begin(Stream &serial){
  _serial = &serial;  // Set a reference to a specified Stream object (Hard or Soft Serial)
}
void DynamixelClass::end(){
  #if defined(__AVR_ATmega32U4__) || defined(__MK20DX128__) || defined(__AVR_ATmega2560__)
    Serial2.end();
  #else
    Serial.end();
  #endif
}
void DynamixelClass::setDirectionPin(unsigned char D_Pin){
  Direction_Pin = D_Pin;
  pinMode(Direction_Pin, OUTPUT);
}

// Single Setters
void DynamixelClass::setHoldingTorque(unsigned char ID, bool Set){
  unsigned char arr[1] = {Set};
  SingleWrite(ID, 0x40, arr, 1);
}
void DynamixelClass::setGoalPosition(unsigned char ID, int pos){
  pos %= 4096;
  unsigned char arr[] =
    {
     (pos & 0xFF),
     (pos & 0xFF00) >> 8,
     (pos & 0xFF0000) >> 16,
     (pos & 0xFF000000) >> 24
    };

  SingleWrite(ID, 0x74, arr, 4);
}
void DynamixelClass::setProfileAcceleration(unsigned char ID, unsigned int pac){
  pac %= 32767;
  unsigned char arr[] =
  {
    (pac & 0xFF),
    (pac & 0xFF00) >> 8,
    (pac & 0xFF0000) >> 16,
    (pac & 0xFF000000) >> 24
  };
  SingleWrite(ID, 0x6C, arr, 4);
}
void DynamixelClass::setProfileVelocity(unsigned char ID, unsigned int pvl){
  pvl %= 1023;
  unsigned char arr[] =
  {
    (pvl & 0xFF),
    (pvl & 0xFF00) >> 8,
    (pvl & 0xFF0000) >> 16,
    (pvl & 0xFF000000) >> 24
  };
  SingleWrite(ID, 0x70, arr, 4);
}
void DynamixelClass::setGoalVelocity(unsigned char ID, unsigned int vel){
  vel  %= 1023;
  unsigned char arr[] =
  {
    (vel & 0xFF),
    (vel & 0xFF00) >> 8,
    (vel & 0xFF0000) >> 16,
    (vel & 0xFF000000) >> 24
  };
  SingleWrite(ID, 0x68, arr, 4);
}
void DynamixelClass::setCurrent(unsigned char ID, unsigned int cur, unsigned int cur1){
  unsigned char arr[] =
  {
    cur,
    cur1,
    //(cur & 0xFF),
    //(cur & 0xFF00) >> 8,
  };
  SingleWrite(ID, 0x66, arr, 2);
}
void DynamixelClass::setMode(unsigned char ID, unsigned int mode){
  unsigned char arr[] =
  {
    (mode & 0xFF),
  };
  SingleWrite(ID, 0x0B, arr, 1);
}

// Single Getters
int   DynamixelClass::getPosition(unsigned char ID){
  clearRXbuffer();
  SingleRead(ID, 0x84, 4);                   //Read from adress 0x84 (Present Position), byte size 4
  getParameters();                      //Filters parameters from ReturnPacket

  int sum;
  sum = (data[2] << 8) | data[1];       //Converting two information bytes into a integer (position data)
  return sum;
}
float DynamixelClass::getPositionDegrees(unsigned char ID){
  //Converting from raw data to degrees (360/4095)
  float posd;
  posd = getPosition(ID) * 0.088;

  //Debug information
  Serial.print("Position of ID: ");
  Serial.print(ID);
  Serial.print(" in DEG: ");
  Serial.println(posd);

  return posd;
}
float DynamixelClass::getCurrent(unsigned char ID){
  clearRXbuffer();
  SingleRead(ID, 0x7E, 4);                   //Read from adress 0x7E (Present Load), byte size 4 (should be 2?)
  getParameters();                      //Filters parameters from ReturnPacket

  float sum;
  sum = (data[2] << 8) | data[1];       //Converting two information bytes into a float (load data)

  //Converting load to percentage


  //Debug information
  Serial.print("Load of ID: ");
  Serial.print(data[0]);
  Serial.print(" is ");
  Serial.println(sum);

  return sum;
}

// Sync Setters
void DynamixelClass::setAllPWMLimit(int (&PWM_arr)[18]){
  set18Parameters(PWM_arr, LEN_2BYTE, ADDR_MX_PWM_LIMIT);
}
void DynamixelClass::setAllPositions(int (&pos_arr)[18]){
  set18Parameters(pos_arr, LEN_4BYTE, ADDR_MX_GOAL_POSITION);
}
void DynamixelClass::setAllAccelProfile(int (&accel_prof)[18]){
  set18Parameters(accel_prof, LEN_4BYTE, ADDR_MX_ACCEL_PROFILE);
}
void DynamixelClass::setAllVelocProfile(int (&veloc_prof)[18]){
  set18Parameters(veloc_prof, LEN_4BYTE, ADDR_MX_VELOC_PROFILE);
}
void DynamixelClass::setTorqueOff(){
  int torq_dis[18] = TORQUE_DISABLE;
  set18Parameters(torq_dis, LEN_1BYTE, ADDR_MX_TORQUE_ENABLE);
}
void DynamixelClass::setTorqueOn(){
  int torq_en[18] = TORQUE_ENABLE;
  set18Parameters(torq_en, LEN_1BYTE, ADDR_MX_TORQUE_ENABLE);
}
void DynamixelClass::setNPositions(int pos_arr[], size_t n){
  setNParameters(pos_arr, n, LEN_4BYTE, ADDR_MX_GOAL_POSITION);
}
void DynamixelClass::setNVelocProfile(int vel_arr[], size_t n){
  setNParameters(vel_arr, n, LEN_4BYTE, ADDR_MX_VELOC_PROFILE);
}
void DynamixelClass::setNAccelProfile(int acc_arr[], size_t n){
  setNParameters(acc_arr, n, LEN_4BYTE, ADDR_MX_ACCEL_PROFILE);
}
void DynamixelClass::setNPWMLimit(int pwm_arr[], size_t n){
  setNParameters(pwm_arr, n, LEN_2BYTE, ADDR_MX_PWM_LIMIT);
}
// Sync Getters
int *DynamixelClass::getAllPWM(void){
  SendAndRead(ADDR_MX_GOAL_PWM, LEN_2BYTE);
  return returndata; //Return pointer to array of positions
}

int *DynamixelClass::getAllPosition(void){
  SendAndRead(ADDR_MX_PRESENT_POSITION, LEN_4BYTE);
  return returndata; //Return pointer to array of positions
}
int *DynamixelClass::getAllVelocity(void){
  SendAndRead(ADDR_MX_PRESENT_VELOCITY, LEN_4BYTE);
  return returndata; //Return pointer to array of positions
}
void DynamixelClass::Reboot(void) {
  int packet_len = 3;
  Instruction_Packet_Array[0] = 0xFE;
  Instruction_Packet_Array[1] = (packet_len & 0xFF); //length
  Instruction_Packet_Array[2] = (packet_len & 0xFF00) >> 8; //length
  Instruction_Packet_Array[3] = 0x08; //Instruction "Reboot"

  clearRXbuffer();
  transmitInstructionPacket(packet_len);
}

//########################## Private Methods ###################################
void DynamixelClass::getParameters(void){
  int j = 0;
  for (unsigned int i = 0; i < ARRAY_LENGTH(ReturnPacket); i++)
  {
    //Filtering the parameters from the returnpacket, by searching for the instruction (0x00, 0x55, 0x00)
    if (ReturnPacket[i] == 0x55 && ReturnPacket[i - 1] == 0 && ReturnPacket[i + 1] == 0)
    {
      //Saving ID
      data[j] = ReturnPacket[i - 3];

      //Saving parameter bytes
      data[j + 1] = ReturnPacket[i + 2];
      data[j + 2] = ReturnPacket[i + 3];
      j += 3;
    }
  }
  int sum;
  for (int i = 0; i < SERVO_AMOUNT*3; i += 3) // 0,3,6, 9,12,15, 18,21,24, 27,30,33, 36,39,42, 45,48,51?
  {
    sum = (data[i + 2] << 8) | data[i + 1]; //Converting two information bytes into a integer (position data)

    returndata[data[i] - 1] = sum;        //Array for storing multiple positions
  }
}
unsigned int DynamixelClass::SingleWrite(unsigned char ID, unsigned short addr, unsigned char *arr, int n) {
  n += 5;
  Instruction_Packet_Array[0] = ID;
  Instruction_Packet_Array[1] = (n & 0xFF); //length
  Instruction_Packet_Array[2] = (n & 0xFF00) >> 8; //length
  Instruction_Packet_Array[3] = 0x03; //Instruction
  Instruction_Packet_Array[4] = (addr & 0xFF); //address
  Instruction_Packet_Array[5] = (addr & 0xFF00) >> 8; //address

  for (int i = 0; i < n - 5; i++) {
    Instruction_Packet_Array[i + 6] = arr[i];
  }

  clearRXbuffer();
  transmitInstructionPacket(n);
  return 0;
}
void DynamixelClass::SingleRead(unsigned char ID, unsigned short addr, int n) {

  n += 3;
  Instruction_Packet_Array[0] = ID;
  Instruction_Packet_Array[1] = (n & 0xFF); //length of packet
  Instruction_Packet_Array[2] = (n & 0xFF00) >> 8; //length of packet
  Instruction_Packet_Array[3] = 0x02; //Instruction
  Instruction_Packet_Array[4] = (addr & 0xFF); //address
  Instruction_Packet_Array[5] = (addr & 0xFF00) >> 8; //address
  Instruction_Packet_Array[6] = ((n - 3) & 0xFF); //data length
  Instruction_Packet_Array[7] = ((n - 3) & 0xFF00) >> 8; // data length

  clearRXbuffer();

  transmitInstructionPacket(n);
  readReturnPacket();
}
void DynamixelClass::setNParameters(int data[], size_t n, byte DATA_LENGTH, unsigned int ADDR_MX){ // WORKS

  const char one_pt_size   = DATA_LENGTH + 1; // Parameter size. Data length + 1 byte for servo ID value
  const char sr_num        = n / 2;
  const char total_pt_size = sr_num * one_pt_size;
  unsigned char *parameter = new unsigned char[total_pt_size]; // reserving a package: servo_amount * bytes_needed_per_1_servo.
  
  int sr_count = 0;

  for (int i = 0; i < sr_num; i++) // Creating parameters for each servo
  {
      parameter[sr_count * one_pt_size]       = data[i+sr_count];             // Parameter 1: servo ID
      parameter[sr_count * one_pt_size + 1]   = (data[i + sr_count + 1] & 0xFF);             // Parameter 2: BYTE 1
      if (DATA_LENGTH >= LEN_2BYTE){
        parameter[sr_count * one_pt_size + 2] = (data[i + sr_count + 1] & 0xFF00) >> 8;      // Parameter 3: BYTE 2 
      }
      if (DATA_LENGTH == LEN_4BYTE){
        parameter[sr_count * one_pt_size + 3] = (data[i + sr_count + 1] & 0xFF0000) >> 16;   // Parameter 4: BYTE 3
        parameter[sr_count * one_pt_size + 4] = (data[i + sr_count + 1] & 0xFF000000) >> 24; // Parameter 5: BYTE 4
      }     
      sr_count++;
  }
  SyncWrite(ADDR_MX, parameter, total_pt_size, DATA_LENGTH);
  delete[] parameter;
}
void DynamixelClass::set18Parameters(int (&DATA)[18], byte DATA_LENGTH, unsigned int ADDR_MX){ // WORKS

  const char one_pt_size   = DATA_LENGTH + 1; // Parameter size. Data length + 1 byte for servo ID value
  const char sr_num       = ARRAY_LENGTH(DATA); //IDs must be consecutive from 1 to 18 (uncluding "1" and "18") . FOR NOW...
  const char total_pt_size = sr_num * one_pt_size;
  unsigned char *parameter = new unsigned char[total_pt_size]; // reserving a package: servo_amount * bytes_needed_per_1_servo.
  int sr_count = 0;

  for (int i = 0; i < sr_num; i++) // Creating parameters for each servo
  {
      parameter[sr_count * one_pt_size]       = i + 1;                        // Parameter 1: servo ID
      parameter[sr_count * one_pt_size + 1]   = (DATA[i] & 0xFF);             // Parameter 2: BYTE 1
      if (DATA_LENGTH >= LEN_2BYTE){
        parameter[sr_count * one_pt_size + 2] = (DATA[i] & 0xFF00) >> 8;      // Parameter 3: BYTE 2 
      }
      if (DATA_LENGTH == LEN_4BYTE){
        parameter[sr_count * one_pt_size + 3] = (DATA[i] & 0xFF0000) >> 16;   // Parameter 4: BYTE 3
        parameter[sr_count * one_pt_size + 4] = (DATA[i] & 0xFF000000) >> 24; // Parameter 5: BYTE 4
      }     
      sr_count++;
  }
  SyncWrite(ADDR_MX, parameter, total_pt_size, DATA_LENGTH);
  delete[] parameter;
}
unsigned int DynamixelClass::SyncWrite(unsigned short addr, unsigned char *arr, int n, int dataN){
  n += 7;

  Instruction_Packet_Array[0] = 0xFE; //ID broadcast (253)
  Instruction_Packet_Array[1] = (n & 0xFF); //length
  Instruction_Packet_Array[2] = (n & 0xFF00) >> 8; //length
  Instruction_Packet_Array[3] = 0x83; //instruction
  Instruction_Packet_Array[4] = (addr & 0xFF); //address
  Instruction_Packet_Array[5] = (addr & 0xFF00) >> 8; //address
  Instruction_Packet_Array[6] = (dataN & 0xFF); //length
  Instruction_Packet_Array[7] = (dataN & 0xFF00) >> 8; //length

  for (int i = 0; i < n - 7; i++) {
    Instruction_Packet_Array[i + 8] = arr[i];
  }
  clearRXbuffer();
  transmitInstructionPacket(n);
  return 0;

}
void DynamixelClass::SyncRead(unsigned short ADDR, int DATA_LEN){

  clearRXbuffer();
  // TO TEST: IF its DATA_LEN or just "4" for instr_packet_array[4,5,6,7]???
  int packet_len = 4 + SERVO_AMOUNT + 3;                    // Packet Length = number of Parameters + 3
  Instruction_Packet_Array[0] = 0xFE;                       // ID broadcast (253)
  Instruction_Packet_Array[1] = (packet_len & 0xFF);        // Low-order  byte from the length of packet
  Instruction_Packet_Array[2] = (packet_len & 0xFF00) >> 8; // High-order byte from the length of packet
  Instruction_Packet_Array[3] = 0x82;                       // Instruction
  // Instruction Packet
  Instruction_Packet_Array[4] = (ADDR & 0xFF);              // Low-order  byte from the starting address
  Instruction_Packet_Array[5] = (ADDR & 0xFF00) >> 8;       // High-order byte from the starting address
  Instruction_Packet_Array[6] = (DATA_LEN & 0xFF);          // Low-order  byte from the data length(X)
  Instruction_Packet_Array[7] = (DATA_LEN & 0xFF00) >> 8;   // High-order byte from the data length(X)

  //Ask information from ID 1 to ID 18
  for (int x = 0; x < 18; x++){
    Instruction_Packet_Array[8+x] =  x+1; // ID
  }
  clearRXbuffer();
  transmitInstructionPacket(packet_len);
}
void DynamixelClass::SendAndRead(unsigned short addr, int DATA_LEN){
  SyncRead(addr, DATA_LEN);
  readReturnPacket();   // Read ReturnPacket
  getParameters();      // Filters parameters from ReturnPacket
}
void DynamixelClass::transmitInstructionPacket(int transLen) { // Transmit instruction packet to Dynamixel

  if (Direction_Pin > -1) {
    digitalWrite(Direction_Pin, HIGH); // Set TX Buffer pin to HIGH
  }

  unsigned char arrLen = transLen + 7;
  unsigned char pt[arrLen];

  pt[0] = 0xFF;
  pt[1] = 0xFF;
  pt[2] = 0xFD;
  pt[3] = 0x00;
  int i;
  for (i = 0; i <= transLen; i++) {
    pt[i + 4] = Instruction_Packet_Array[i];
  }

  unsigned short crc = update_crc(pt, arrLen - 2);

  unsigned char CRC_L = (crc & 0x00FF);
  unsigned char CRC_H = (crc >> 8) & 0x00FF;

  i += 4;

  pt[i++] = CRC_L;
  pt[i] = CRC_H;

  for (i = 0; i < arrLen; i++) {
    _serial->write(pt[i]);
  }
  noInterrupts();

  #if defined(__AVR_ATmega32U4__) || defined(__MK20DX128__) || defined(__AVR_ATmega2560__) // Leonardo and Mega use Serial2
    if ((UCSR1A & B01100000) != B01100000) {                                            // Wait for TX data to be sent
      _serial->flush();
    }

  #elif defined(__SAM3X8E__)

    //if(USART_GetFlagStatus(USART1, USART_FLAG_TC) != RESET)
    _serial->flush();
    //}

  #else
    if ((UCSR0A & B01100000) != B01100000) {                                            // Wait for TX data to be sent
      _serial->flush();
    }

  #endif

  if (Direction_Pin > -1) {
    digitalWrite(Direction_Pin, LOW);                                               //Set TX Buffer pin to LOW after data has been sent
  }

  interrupts();

  delay(10);

}
void DynamixelClass::readReturnPacket(void) {
  int i = 0;
  //Read information when available
  while (_serial->available() > 0) {
    int incomingbyte;
    // Serial.print(incomingbyte);
    // Serial.print(",");
    incomingbyte = _serial->read();        // Save incomingbyte
    delayMicroseconds(35);                 // BUGFIX. Without this delay, it can't read status packets of more than 11 servos at once.
    ReturnPacket[i] = incomingbyte;        // Save data in ReturnPacket array
    i++;
  }

}
void DynamixelClass::readAll(void) {
  //Print all incomming serial data, when available
  while (_serial->available() > 0) {
    int incomingbyte;
    incomingbyte = _serial->read();
    Serial.println(incomingbyte, HEX);    //Print incomingbyte, one by one - in HEX
  }
}
void DynamixelClass::clearRXbuffer(void) {

  while (_serial->read() != -1);  // Clear RX buffer;

}
unsigned short DynamixelClass::update_crc(unsigned char *data_blk_ptr, unsigned short data_blk_size){
  unsigned short crc_accum = 0;
  unsigned short i, j;
  unsigned short crc_table[256] = {
    0x0000, 0x8005, 0x800F, 0x000A, 0x801B, 0x001E, 0x0014, 0x8011,
    0x8033, 0x0036, 0x003C, 0x8039, 0x0028, 0x802D, 0x8027, 0x0022,
    0x8063, 0x0066, 0x006C, 0x8069, 0x0078, 0x807D, 0x8077, 0x0072,
    0x0050, 0x8055, 0x805F, 0x005A, 0x804B, 0x004E, 0x0044, 0x8041,
    0x80C3, 0x00C6, 0x00CC, 0x80C9, 0x00D8, 0x80DD, 0x80D7, 0x00D2,
    0x00F0, 0x80F5, 0x80FF, 0x00FA, 0x80EB, 0x00EE, 0x00E4, 0x80E1,
    0x00A0, 0x80A5, 0x80AF, 0x00AA, 0x80BB, 0x00BE, 0x00B4, 0x80B1,
    0x8093, 0x0096, 0x009C, 0x8099, 0x0088, 0x808D, 0x8087, 0x0082,
    0x8183, 0x0186, 0x018C, 0x8189, 0x0198, 0x819D, 0x8197, 0x0192,
    0x01B0, 0x81B5, 0x81BF, 0x01BA, 0x81AB, 0x01AE, 0x01A4, 0x81A1,
    0x01E0, 0x81E5, 0x81EF, 0x01EA, 0x81FB, 0x01FE, 0x01F4, 0x81F1,
    0x81D3, 0x01D6, 0x01DC, 0x81D9, 0x01C8, 0x81CD, 0x81C7, 0x01C2,
    0x0140, 0x8145, 0x814F, 0x014A, 0x815B, 0x015E, 0x0154, 0x8151,
    0x8173, 0x0176, 0x017C, 0x8179, 0x0168, 0x816D, 0x8167, 0x0162,
    0x8123, 0x0126, 0x012C, 0x8129, 0x0138, 0x813D, 0x8137, 0x0132,
    0x0110, 0x8115, 0x811F, 0x011A, 0x810B, 0x010E, 0x0104, 0x8101,
    0x8303, 0x0306, 0x030C, 0x8309, 0x0318, 0x831D, 0x8317, 0x0312,
    0x0330, 0x8335, 0x833F, 0x033A, 0x832B, 0x032E, 0x0324, 0x8321,
    0x0360, 0x8365, 0x836F, 0x036A, 0x837B, 0x037E, 0x0374, 0x8371,
    0x8353, 0x0356, 0x035C, 0x8359, 0x0348, 0x834D, 0x8347, 0x0342,
    0x03C0, 0x83C5, 0x83CF, 0x03CA, 0x83DB, 0x03DE, 0x03D4, 0x83D1,
    0x83F3, 0x03F6, 0x03FC, 0x83F9, 0x03E8, 0x83ED, 0x83E7, 0x03E2,
    0x83A3, 0x03A6, 0x03AC, 0x83A9, 0x03B8, 0x83BD, 0x83B7, 0x03B2,
    0x0390, 0x8395, 0x839F, 0x039A, 0x838B, 0x038E, 0x0384, 0x8381,
    0x0280, 0x8285, 0x828F, 0x028A, 0x829B, 0x029E, 0x0294, 0x8291,
    0x82B3, 0x02B6, 0x02BC, 0x82B9, 0x02A8, 0x82AD, 0x82A7, 0x02A2,
    0x82E3, 0x02E6, 0x02EC, 0x82E9, 0x02F8, 0x82FD, 0x82F7, 0x02F2,
    0x02D0, 0x82D5, 0x82DF, 0x02DA, 0x82CB, 0x02CE, 0x02C4, 0x82C1,
    0x8243, 0x0246, 0x024C, 0x8249, 0x0258, 0x825D, 0x8257, 0x0252,
    0x0270, 0x8275, 0x827F, 0x027A, 0x826B, 0x026E, 0x0264, 0x8261,
    0x0220, 0x8225, 0x822F, 0x022A, 0x823B, 0x023E, 0x0234, 0x8231,
    0x8213, 0x0216, 0x021C, 0x8219, 0x0208, 0x820D, 0x8207, 0x0202
  };

  for (j = 0; j < data_blk_size; j++)
  {
    i = ((unsigned short)(crc_accum >> 8) ^ data_blk_ptr[j]) & 0xFF;
    crc_accum = (crc_accum << 8) ^ crc_table[i];
  }

  return crc_accum;
}

DynamixelClass Dynamixel;
