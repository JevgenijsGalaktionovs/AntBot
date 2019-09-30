#ifndef tactile_h
#define tactile_h
#include <Arduino.h>

const byte TACTILE_1  = A3;

class TactileClass {

public:
    float * read_pressure();
    void read_value();
private:
    float tactile[1];   

};

extern TactileClass Tactile;

#endif
