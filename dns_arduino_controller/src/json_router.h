#ifndef json_router_h
#define json_router_h


struct DataContainer{
    int servo_pos[18];
    int servo_pwm[18];
    unsigned int FSR_pressure[6];
    float IR_distance[3];
    float IMU_data[3];
};

// Serialization & Parsing
DataContainer CreatePackage1(float (&IR)[3]);
DataContainer CreatePackage2(int (&pos)[18]);
DataContainer CreatePackage3(int (&pwm)[18]);
DataContainer CreatePackage4(unsigned int (&tactile)[6]);

JsonObject& SerializeData1(DataContainer &data_package); // Takes struct and converts to a JSON string
JsonObject& SerializeData2(DataContainer &data_package);
JsonObject& SerializeData3(DataContainer &data_package);
JsonObject& SerializeData4(DataContainer &data_package);

void JSONcheck    (JsonObject& json_object);
// Setters
void json_setTorque      (JsonObject& json_object);
void json_setReboot      (JsonObject& json_object);
void json_set1Position   (JsonObject& json_object);
void json_set18Aprof     (JsonObject& json_object);
void json_set18Vprof     (JsonObject& json_object);
void json_set18PWMLimit  (JsonObject& json_object);
void json_set18Position  (JsonObject& json_object);
void json_setNPosition   (JsonObject& json_object);
void json_setNVprof      (JsonObject& json_object);
void json_setNAprof      (JsonObject& json_object);
void json_setNPWMLimit   (JsonObject& json_object);


// Getters
void json_get18Position  (JsonObject& json_object);
void json_get18PWM       (JsonObject& json_object);
void json_getIR          (JsonObject& json_object);
void json_getIR_kalman   (JsonObject& json_object);
void json_getFSR         (JsonObject& json_object);
void json_checkRequests  (JsonObject& json_object);
void json_parse_data     (String inData);

void demo_IR();
void demo_tactile();
void demo_IR2();
#endif // json_router_h
