#include "IR_sensor.h"

unsigned int * IRClass::getIR(){
    return IRClass::IR_distance;
}

void IRClass::update_IR(){
    unsigned int volts_ir[3];
    /* Updates IR_distance array with freshly read values from 3 IR sensors */
    volts_ir[0] = analogRead(PIN_FRONT); // value from sensor * (5/1024)
    volts_ir[1] = analogRead(PIN_RIGHT); // value from sensor * (5/1024)
    volts_ir[2] = analogRead(PIN_LEFT);  // value from sensor * (5/1024)
    for (int i=0;i<3;i++){
        IR_distance[i] = 10650.08 * pow(volts_ir[i], - 0.935) - 10;
        if (IR_distance[i] > 150){
            IR_distance[i] = 150;
        }
    }
}

IRClass IR;
