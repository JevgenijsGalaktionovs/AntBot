#include "kalman_filter.h"

//############################ Public Methods ##################################
float * KalmanFilterClass::getPrediction(){
    return KalmanFilterClass::x_post;
}

float * KalmanFilterClass::getRaw(){
    return KalmanFilterClass::IR_distance;
}

void KalmanFilterClass::initialiseFilter(){
    /* A function to initialize the Kalman filter */
    read_ir();
    for (int i = 0; i < 3; i++){
        x_prior[i] = phi * IR_distance[i] + G * u;              // First prior state estimate
        p_prior[i] = 1;                                                  // Initial error covariance
        K[i]       = p_prior[i] / (p_prior[i] + R[i]);                   // Initial Kalman gain
        x_post[i]  = x_prior[i] + K[i] * (IR_distance[i] - x_prior[i]);  // First posterior state estimate
        p_post[i]  = (1 - K[i]) * p_prior[i];                            // First estimate error covariance
    }
}
void KalmanFilterClass::updatePrediction(){
    /* Continously updates the state estimate with every new measurement */
    read_ir();
    for (int i = 0; i < 3; i++){
        // Time Update (Prediction)
        x_prior[i] = phi * x_post[i] + G * u;
        z_hat[i]   = H * x_prior[i];
        p_prior[i] = phi * p_post[i] * phi + Q[i];  // Project the error covariance ahead
        // Measurement Update (Correction)
        K[i]       = p_prior[i] * H / (H * p_prior[i] * H + R[i]);  // Compute the Kalman Gain
        x_post[i]  = x_prior[i] + K[i] * (IR_distance[i] - z_hat[i]);        // Update the estimate using sensor measurement
        p_post[i]  = (1 - K[i] * H) * p_prior[i];                         // Update the error covariance
    }
}
//############################ Private Methods ##################################
void KalmanFilterClass::read_ir(){
    /* Updates IR_distance array with freshly read values from 3 IR sensors */
    float volts_ir_front = analogRead(IR_PIN_FRONT); // value from sensor * (5/1024)
    float volts_ir_right = analogRead(IR_PIN_RIGHT); // value from sensor * (5/1024)
    float volts_ir_left  = analogRead(IR_PIN_LEFT);  // value from sensor * (5/1024)
    IR_distance[0] = 10650.08 * pow(volts_ir_front, - 0.935) - 10;
    if (IR_distance[0] > 150){
        IR_distance[0] = 150;
    }
    IR_distance[1] = 10650.08 * pow(volts_ir_right, - 0.935) - 10;
    if (IR_distance[1] > 150){
        IR_distance[1] = 150;
    }

    IR_distance[2] = 10650.08 * pow(volts_ir_left,  - 0.935) - 10;
    if (IR_distance[2] > 150){
        IR_distance[2] = 150;
    }
}

KalmanFilterClass Kalman;