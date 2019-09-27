#ifndef tactile_h
#define tactile_h
#include <Arduino.h>

const byte TACTILE_1  = A3;

class TactileClass {

public:
    float read_preassure();
    void read_value();
private:
    float tactile;   

};

extern TactileClass Tactile;

#endif
