#include "tactile.h"

float * TactileClass::read_pressure(){
    return TactileClass::tactile;
}


void TactileClass::read_value(){
    float meassurement = analogRead(TACTILE_1);  
    tactile[0] = meassurement;
}
TactileClass Tactile;