#include "fsr_sensor.h"

unsigned int  * FSRClass::getFSR(){
    return FSRClass::FSR_pressure;
}

void FSRClass::updateFSR(){
    unsigned int  fsr_readings[6];
    for(int i=0;i<6;i++){
        fsr_readings[i] = analogRead(TACTILE_LIST[i]);
        FSR_pressure[i] = fsr_readings[i];
    }
}

FSRClass FSR;