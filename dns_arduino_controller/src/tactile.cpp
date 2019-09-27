#include "tactile.h"

float TactileClass::read_preassure(){
    return TactileClass::tactile;
}


void TactileClass::read_value(){
    float meassurement = analogRead(TACTILE_1);  
    tactile = meassurement;
}
TactileClass Tactile;