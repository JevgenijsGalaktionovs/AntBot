#include <ArduinoJson.h>
#include "dynamixel_driver.h"
#include "json_router.h"
#include "kalman_filter.h"
#include "fsr_sensor.h"
#include "IR_sensor.h"


extern KalmanFilterClass<3>KalmanIR;
extern KalmanFilterClass<6>KalmanFSR;

// Serialization 
DataContainer CreatePackage1(float (&IR)[3]){ 
  DataContainer data;
  memcpy(data.IR_distance, IR, sizeof IR);
  return data;
}
DataContainer CreatePackage2(int (&pos)[18]){ 
  DataContainer data;
  memcpy(data.servo_pos, pos, sizeof pos);
  return data;
}
DataContainer CreatePackage3(int (&pwm)[18]){ 
  DataContainer data;
  memcpy(data.servo_pwm, pwm, sizeof pwm);
  return data;
}
DataContainer CreatePackage4(unsigned int (&tactile)[6]){ 
  DataContainer data;
  memcpy(data.FSR_pressure,tactile, sizeof tactile);
  return data;
}

JsonObject& SerializeData1(DataContainer &data_package){
  const size_t capacity_tx = JSON_OBJECT_SIZE(1) + JSON_ARRAY_SIZE(3); // USE https://arduinojson.org/v5/assistant/ to calculate this!!!
  StaticJsonBuffer<capacity_tx> buffer_tx;
  JsonObject& msg_tx = buffer_tx.createObject();
  JSONcheck(msg_tx);
  JsonArray& IR_dist = msg_tx.createNestedArray("IR_dist");

  for (int i=0; i < 3; i++){
    IR_dist.add(data_package.IR_distance[i]);
    }
  return msg_tx;
}
JsonObject& SerializeData2(DataContainer &data_package){
  const size_t capacity_tx = JSON_OBJECT_SIZE(1) + JSON_ARRAY_SIZE(18); // USE https://arduinojson.org/v5/assistant/ to calculate this!!!
  StaticJsonBuffer<capacity_tx> buffer_tx;
  JsonObject& msg_tx = buffer_tx.createObject();
  JSONcheck(msg_tx);
  JsonArray& sr_pos  = msg_tx.createNestedArray("sr_pos");

  for (int i=0; i < 18; i++){
    sr_pos.add(data_package.servo_pos[i]);
  }
  return msg_tx;
}
JsonObject& SerializeData3(DataContainer &data_package){
  const size_t capacity_tx = JSON_OBJECT_SIZE(1) + JSON_ARRAY_SIZE(18); // USE https://arduinojson.org/v5/assistant/ to calculate this!!!
  StaticJsonBuffer<capacity_tx> buffer_tx;
  JsonObject& msg_tx = buffer_tx.createObject();
  JSONcheck(msg_tx);
  JsonArray& sr_pwm  = msg_tx.createNestedArray("sr_pwm");

  for (int i=0; i < 18; i++){
    sr_pwm.add(data_package.servo_pwm[i]);
  }
  return msg_tx;
}
JsonObject& SerializeData4(DataContainer &data_package){
  const size_t capacity_tx = JSON_OBJECT_SIZE(1) + JSON_ARRAY_SIZE(6); // USE https://arduinojson.org/v5/assistant/ to calculate this!!!
  StaticJsonBuffer<capacity_tx> buffer_tx;
  JsonObject& msg_tx = buffer_tx.createObject();
  JSONcheck(msg_tx);
  JsonArray& FSR_pres = msg_tx.createNestedArray("FSR_pres");
  for (int i=0; i < 6; i++){
    FSR_pres.add(data_package.FSR_pressure[i]);
  }
  return msg_tx;
}


void JSONcheck(JsonObject& json_object){
  if(!json_object.success()){
    Serial.println("createObject() failed");
  }
}

// Setters
void json_setTorque(JsonObject& json_object){
  bool hasTorque = json_object.containsKey("torque");
  if(hasTorque){ 
    bool torque = json_object["torque"];
    if(torque){
      Dynamixel.setTorqueOn();
      }
    else{
      Dynamixel.setTorqueOff();   
      }
  }
  }

void json_setReboot(JsonObject& json_object){
  bool hasReboot = json_object.containsKey("reboot");
  if(hasReboot){ 
      Dynamixel.Reboot();
  }
  }

void json_set1Position(JsonObject& json_object){
  // Uses dynamixel single write function for 1 servo
  bool hasPosition = json_object.containsKey("pos_1");
  if(hasPosition){ 
      unsigned char ID  = json_object["pos_1"][0];
      int  pos = json_object["pos_1"][1];
      Dynamixel.setGoalPosition(ID, pos);
  }
  }


void json_set18Position(JsonObject& json_object){
  // Uses dynamixel Sync write function for 18 servos
  bool hasPosition = json_object.containsKey("pos_all");
  if(hasPosition){ 
      int pos_all[18];
      for (int i=0;i<18;i++){
        pos_all[i] = json_object["pos_all"][i];
      }
      Dynamixel.setAllPositions(pos_all);
  }
  }
void json_set18Aprof(JsonObject& json_object){
  bool has18Aprof = json_object.containsKey("aprof_all");
  if(has18Aprof){ 
    int aprof_all[18];
    for (int i = 0; i<18 ; i++){
      aprof_all[i] = json_object["aprof_all"][i];
    }
    Dynamixel.setAllAccelProfile(aprof_all);
  }
  }

void json_set18Vprof(JsonObject& json_object){
  bool has18Vprof = json_object.containsKey("vprof_all");
  if(has18Vprof){ 
    int vprof_all[18];
    for (int i = 0;i<18;i++){
      vprof_all[i] = json_object["vprof_all"][i];
    }   
    Dynamixel.setAllVelocProfile(vprof_all);
  }
  }

void json_set18PWMLimit(JsonObject& json_object){
  bool has18PWMLimit = json_object.containsKey("pwm_all");
  if(has18PWMLimit){ 
    int pwm_all[18];
    for (int i = 0;i<18;i++){
      pwm_all[i] = json_object["pwm_all"][i];
    }     
    Dynamixel.setAllPWMLimit(pwm_all);
  }
  }


void json_setNPosition(JsonObject& json_object){
  // Uses dynamixel sync write function for N servos
  bool hasNPosition = json_object.containsKey("pos_n");
  if(hasNPosition){
      size_t arr_size = json_object["pos_n"].size();
      int data_arr[arr_size];
      for (unsigned int i=0;i<arr_size;i++){
        data_arr[i] = json_object["pos_n"][i];
      }
      Dynamixel.setNPositions(data_arr, arr_size);
  }
  }
void json_setNPWMLimit(JsonObject& json_object){
  // Uses dynamixel sync write function for N servos
  bool hasNPWMLimit = json_object.containsKey("pwm_n");
  if(hasNPWMLimit){
      size_t arr_size = json_object["pwm_n"].size();
      int data_arr[arr_size];
      for (unsigned int i=0;i<arr_size;i++){
        data_arr[i] = json_object["pwm_n"][i];
      }
      Dynamixel.setNPWMLimit(data_arr, arr_size);
  }
  }
void json_setNVprof(JsonObject& json_object){
  // Uses dynamixel sync write function for N servos
  bool hasNVprof = json_object.containsKey("vprof_n");
  if(hasNVprof){
      size_t arr_size = json_object["vprof_n"].size();
      int data_arr[arr_size];
      for (unsigned int i=0;i<arr_size;i++){
        data_arr[i] = json_object["vprof_n"][i];
      }
      Dynamixel.setNVelocProfile(data_arr, arr_size);
  }
  }
void json_setNAprof(JsonObject& json_object){
  // Uses dynamixel sync write function for N servos
  bool hasNAprof = json_object.containsKey("aprof_n");
  if(hasNAprof){
      size_t arr_size = json_object["aprof_n"].size();
      int data_arr[arr_size];
      for (unsigned int i=0;i<arr_size;i++){
        data_arr[i] = json_object["aprof_n"][i];
      }
      Dynamixel.setNAccelProfile(data_arr, arr_size);
  }
  }



void json_get18Position(JsonObject& json_object){
  // uses sync read to get all positions
  bool hasReadPosition = json_object.containsKey("read_pos_all");
  if(hasReadPosition){ 
      struct DataContainer data_package;
      int *tmp_positions;
      int positions[18];
      tmp_positions = Dynamixel.getAllPosition();
      for(int x=0;x<18;x++){
      positions[x] = tmp_positions[x];
      }
      data_package = CreatePackage2(positions);
      JsonObject& msg_tx = SerializeData2(data_package);
      // Serial.println(positions[17]); 
      msg_tx.printTo(Serial);
      Serial.println();
  }
  }   

  void json_get18PWM(JsonObject& json_object){
  // uses sync read to get all positions
  bool hasReadPWM = json_object.containsKey("read_pwm_all");
  if(hasReadPWM){ 
      struct DataContainer data_package;
      int *tmp_pwm;
      int pwm[18];
      tmp_pwm = Dynamixel.getAllPWM();
      for(int x=0;x<18;x++){
      pwm[x] = tmp_pwm[x];
      }
      data_package = CreatePackage3(pwm);
      JsonObject& msg_tx = SerializeData3(data_package);
      msg_tx.printTo(Serial);
      Serial.println();
  }
  }   

void json_getIR_kalman(JsonObject& json_object){
  bool hasReadIR = json_object.containsKey("read_IR_filt");
  if(hasReadIR){ 
      struct DataContainer data_package;
      float  *filtered_ir;
      filtered_ir = KalmanIR.getPrediction();
      float  IR_fil_dist[3];
      for (int i=0;i<3;i++){
        IR_fil_dist[i] = filtered_ir[i];
      }
      data_package = CreatePackage1(IR_fil_dist);
      JsonObject& msg_tx = SerializeData1(data_package);
      msg_tx.printTo(Serial);
      Serial.println();
      }
  }

void json_getFSR(JsonObject& json_object){
  bool hasReadTactile = json_object.containsKey("read_FSR_filt");
  if(hasReadTactile){ 
      struct DataContainer data_package;
      unsigned int  *tactile_tmp;
      unsigned int tactile_value[6];
      tactile_tmp = FSR.getFSR();
      for (int i=0;i<6;i++){
      tactile_value[i] = tactile_tmp[i];
      }
      data_package = CreatePackage4(tactile_value);
      JsonObject& msg_tx = SerializeData4(data_package);
      msg_tx.printTo(Serial);
      Serial.println();
      }
}
// void json_getIR(JsonObject& json_object){
//   bool hasReadRawIR = json_object.containsKey("read_IR_raw");
//   if(hasReadRawIR){ 
//       struct DataContainer data_package;
//       unsigned int   *raw_ir;
//       raw_ir = IR.getIR();
//       float  IR_dist[3];
//       for (int i=0;i<3;i++){
//       IR_dist[i] = raw_ir[i];
//       }
//       data_package = CreatePackage1(IR_dist);
//       JsonObject& msg_tx = SerializeData1(data_package);
//       msg_tx.printTo(Serial);
//       Serial.println();
//       }
// }

void json_checkRequests(JsonObject& json_object){
  json_setReboot       (json_object);
  json_setTorque       (json_object);
  json_set1Position    (json_object);
  json_set18Aprof      (json_object);
  json_set18Vprof      (json_object);
  json_set18PWMLimit   (json_object);
  json_set18Position   (json_object);
  json_setNPosition    (json_object);
  json_setNAprof       (json_object);
  json_setNVprof       (json_object);
  json_setNPWMLimit    (json_object);
  json_get18Position   (json_object);
  json_get18PWM        (json_object);
  // json_getIR           (json_object);  
  json_getFSR          (json_object);
  json_getIR_kalman    (json_object);
  }

void json_parse_data(String inData){ 
    // DATA RECEIVING AND PARSING
        const size_t capacity_rx = 2*JSON_ARRAY_SIZE(18) + JSON_OBJECT_SIZE(6) + 230;
        StaticJsonBuffer<capacity_rx> buffer_rx; 
        JsonObject& msg_rx = buffer_rx.parseObject(inData);
        json_checkRequests(msg_rx);
        buffer_rx.clear();
  }
