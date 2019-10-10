#include <Arduino.h>

#include <ArduinoJson.h>
#include <millisDelay.h>

#include "json_router.h"
#include "dynamixel_driver.h"
#include "kalman_filter.h"
#include "fsr_sensor.h"
#include "IR_sensor.h"

#define FREQUENCY_HZ(hz) (1000 / hz)
#define BAUDRATE          1000000

const int num_of_IR = 3;
const int num_of_FSR = 6;

float IR_Q[num_of_IR] = {0.4,0.4,0.4};
float IR_R[num_of_IR] = {10,10,10};

float FSR_Q[num_of_FSR] = {0.4,0.4,0.4};
float FSR_R[num_of_FSR] = {10,10,10};

KalmanFilterClass<num_of_IR>KalmanIR(1.0, 0, 1.0, 1.0, IR_Q, IR_R);
KalmanFilterClass<num_of_FSR>KalmanFSR(1.0, 0, 1.0, 1.0, FSR_Q, FSR_R);


millisDelay serial_loop_timer, ir_loop_timer;
const byte DIR_PIN = 2;

// void demo_tactile(){
//     float *tactile_filtered;
//     unsigned int *tactile_raw;
//     tactile_raw = KalmanFSR.getRaw();
//     tactile_filtered = KalmanFSR.getPrediction();

//     unsigned int  FSR_raw_dist[6];
//     unsigned int  FSR_fil_dist[6];
//     for (int i=0;i<3;i++){
//         FSR_raw_dist[i] = tactile_raw[i];
//         FSR_fil_dist[i] = tactile_filtered[i];
//     }
//     Serial.print(FSR_raw_dist[0]);
//     Serial.print(",");
//     Serial.println(FSR_fil_dist[0]);
// }

// void demo_IR(){
//     float  *filtered_ir;
//     unsigned int *raw_ir;
//     raw_ir = KalmanIR.getRaw();
//     filtered_ir = KalmanIR.getPrediction();

//     unsigned int  IR_raw_dist[3];
//     unsigned int  IR_fil_dist[3];
//     for (int i=0;i<3;i++){
//         IR_raw_dist[i] = raw_ir[i];
//         IR_fil_dist[i] = filtered_ir[i];
//     }
//     Serial.print(IR_raw_dist[0]);
//     Serial.print(",");
//     Serial.println(IR_fil_dist[0]);
//     }

void start_serial_ports(void){ 
    Serial.begin(BAUDRATE);   // RPI       serial connection
    Serial2.begin(BAUDRATE);  // Dynamixel serial connection
    while (!Serial){;}
    Serial.flush();
    Serial2.flush();
    Dynamixel.begin(Serial2);
    Dynamixel.setDirectionPin(DIR_PIN);
}

void check_serial_port(void){ 
    // Check port. If data found, read it until "new line" symbol. Pass it to JSON parser.
    String inData;
    if(Serial.available() > 0){
        inData = Serial.readStringUntil('\n');
        json_parse_data(inData);
        inData="";
    }
}

void setup(){
    start_serial_ports();
    serial_loop_timer.start(FREQUENCY_HZ(1000)); // Initialiaze timer object
    ir_loop_timer.start(FREQUENCY_HZ(20));
    KalmanIR.initialiseFilter(IR.IR_distance);
    KalmanFSR.initialiseFilter(FSR.FSR_pressure);
}

void loop(){
    if (serial_loop_timer.isFinished()) {
        serial_loop_timer.repeat();

        check_serial_port();

        if (ir_loop_timer.isFinished()) {
            ir_loop_timer.repeat();

            FSR.updateFSR();
            IR.update_IR();
            KalmanIR.updatePrediction(IR.IR_distance);
            KalmanFSR.updatePrediction(FSR.FSR_pressure);
        } 

    }
}
