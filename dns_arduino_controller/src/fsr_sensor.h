#ifndef fsr_sensor_h
#define fsr_sensor_h
#include <Arduino.h>

#define TACTILE_LEG_1 A8
#define TACTILE_LEG_2 A9
#define TACTILE_LEG_3 A10
#define TACTILE_LEG_4 A11
#define TACTILE_LEG_5 A12
#define TACTILE_LEG_6 A13

const byte TACTILE_LIST[] = {TACTILE_LEG_1,TACTILE_LEG_2,TACTILE_LEG_3,TACTILE_LEG_4,TACTILE_LEG_5,TACTILE_LEG_6};

class FSRClass {

public:
    unsigned int  FSR_pressure[6];
    void updateFSR();
    unsigned int  * getFSR();

private:


};

extern FSRClass FSR;

#endif
