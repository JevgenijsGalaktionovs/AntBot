#ifndef tactile_h
#define tactile_h
#include <Arduino.h>

const byte TACTILE_1  = A3;

class TactileClass {

public:
    float * read_preassure();

};

extern TactileClass Tactile;

#endif
