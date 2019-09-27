#include <Arduino.h>

#include <ArduinoJson.h>
#include <millisDelay.h>

#include "json_router.h"
#include "dynamixel_driver.h"
#include "kalman_filter.h"
#include "tactile.h"

#define FREQUENCY_HZ(hz) (1000 / hz)
#define BAUDRATE          1000000

millisDelay serial_loop_timer, ir_loop_timer;
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
    ir_loop_timer.start(FREQUENCY_HZ(20));
    Kalman.initialiseFilter(); // Run Kalman for the first iteration
}

void loop(){
    if (serial_loop_timer.isFinished()) {
        serial_loop_timer.repeat();
        check_serial_port();

        if (ir_loop_timer.isFinished()) {
            ir_loop_timer.repeat();
            Kalman.updatePrediction(); // Update IR prediction
            //demo_IR();
        } // ir_loop_timer stops here.

    } // serial_loop_timer stops here.
}
