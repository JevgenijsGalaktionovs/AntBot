#ifndef IR_sensor_h
#define IR_sensor_h
#include <Arduino.h>

const byte PIN_LEFT  = A2,
           PIN_FRONT = A1,
           PIN_RIGHT = A0;

class IRClass {

public:
    unsigned int IR_distance[3]; // Raw IR data
    void update_IR();
    unsigned int * getIR();
private:

};

extern IRClass IR;

#endif
