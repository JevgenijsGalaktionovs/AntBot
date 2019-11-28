#include <Arduino.h>

#include <ArduinoJson.h>
#include <millisDelay.h>

#include "json_router.h"
#include "dynamixel_driver.h"
#include "kalman_filter.h"
#include "fsr_sensor.h"

#define FREQUENCY_HZ(hz) (1000 / hz)
#define BAUDRATE          1000000

const int num_of_FSR = 6;

float FSR_Q[num_of_FSR] = {0.4,0.4,0.4};
float FSR_R[num_of_FSR] = {10,10,10};

KalmanFilterClass<num_of_FSR>KalmanFSR(1.0, 0, 1.0, 1.0, FSR_Q, FSR_R);

millisDelay serial_loop_timer, sensor_loop_timer;
const byte DIR_PIN = 2;

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
    sensor_loop_timer.start(FREQUENCY_HZ(20));
    KalmanFSR.initialiseFilter(FSR.FSR_pressure);
}

void loop(){
    if (serial_loop_timer.isFinished()) {
        serial_loop_timer.repeat();

        check_serial_port();

        if (sensor_loop_timer.isFinished()) {
            sensor_loop_timer.repeat();

            FSR.updateFSR();
            KalmanFSR.updatePrediction(FSR.FSR_pressure);
        } 

    }
}
