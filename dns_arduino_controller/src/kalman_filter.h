#ifndef kalman_filter_h
#define kalman_filter_h
#include <Arduino.h>

const byte IR_PIN_LEFT  = A2,
           IR_PIN_FRONT = A1,
           IR_PIN_RIGHT = A0;

class KalmanFilterClass {

public:
    float * getPrediction();
    float * getRaw();
    void initialiseFilter();
    void updatePrediction();
    
private:
    void read_ir();
    float phi  = 1;             // Dynamic model
    float G    = 0;             // Process weighted noise
    float u    = 1;             // System Input
    float H    = 1;             // Describes how state are mapped into outputs
    float Q[3] = {0.4,0.4,0.4}; // Process noise. Trust in the model. bigger value -> trust model less
    float R[3] = {10,10,10};    // Sensor covariance. How much you trust sensor. biger value -> trust sensor less
    float IR_distance[3];       // Raw IR data
    float x_prior[3];           // First prior state estimate
    float p_prior[3];           // Initial error covariance
    float K[3];                 // Initial Kalman gain
    float x_post[3];            // First posterior state estimate  (NEW VALUES)
    float p_post[3];            // First estimate error covariance
    float z_hat[3];             // Prediction of the measurement
};

extern KalmanFilterClass Kalman;

#endif

