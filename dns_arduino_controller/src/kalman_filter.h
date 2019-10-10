#ifndef kalman_filter_h
#define kalman_filter_h
#include <Arduino.h>

const byte IR_PIN_LEFT  = A6,
           IR_PIN_FRONT = A5,
           IR_PIN_RIGHT = A4;



template<int n>
class KalmanFilterClass {
    public:
        // Constructor
        KalmanFilterClass(float g_phi, float g_G, float g_u, float g_H, float g_Q[], float g_R[]) :
            phi(g_phi), G(g_G), u(g_u), H(g_H){
                for(int i=0;i<n;i++){
                    Q[i] = g_Q[i];  
                    R[i] = g_R[i];
                    }
            }

        float * getPrediction(){
            return x_post;
        }

        unsigned int * getRaw(){
            return sensor_val;
        }

        void initialiseFilter(unsigned int sensor_data[]){
        /* A function to initialize the Kalman filter */
            for (int i = 0; i < n; i++){
                sensor_val[i] = sensor_data[i];

                x_prior[i] = phi * sensor_val[i] + G * u;                        // First prior state estimate
                p_prior[i] = 1;                                                  // Initial error covariance
                K[i]       = p_prior[i] / (p_prior[i] + R[i]);                   // Initial Kalman gain
                x_post[i]  = x_prior[i] + K[i] * (sensor_val[i] - x_prior[i]);   // First posterior state estimate
                p_post[i]  = (1 - K[i]) * p_prior[i];                            // First estimate error covariance
            }
        }
        void updatePrediction(unsigned int sensor_data[]){
        /* Continously updates the state estimate with every new measurement */
            for (int i = 0; i < n; i++){
                sensor_val[i] = sensor_data[i];
                // Time Update (Prediction)
                x_prior[i] = phi * x_post[i] + G * u;
                z_hat[i]   = H * x_prior[i];
                p_prior[i] = phi * p_post[i] * phi + Q[i];                           // Project the error covariance ahead
                // Measurement Update (Correction)
                K[i]       = p_prior[i] * H / (H * p_prior[i] * H + R[i]);           // Compute the Kalman Gain
                x_post[i]  = x_prior[i] + K[i] * (sensor_val[i] - z_hat[i]);         // Update the estimate using sensor measurement
                p_post[i]  = (1 - K[i] * H) * p_prior[i];                            // Update the error covariance
            }
        }

        unsigned int sensor_val[n];

        //Kalman Filter parameters
        float phi;  // Dynamic model
        float G;    // Process weighted noise
        float u;    // System Input
        float H;    // Describes how state are mapped into outputs
        float Q[n]; // Process noise. Trust in the model. bigger value -> trust model less
        float R[n]; // Sensor covariance. How much you trust sensor. biger value -> trust sensor less

    private:
        //Kalman Filter variables
        float x_prior[n]; // First prior state estimate
        float p_prior[n]; // Initial error covariance
        float K[n];       // Initial Kalman gain
        float x_post[n];  // First posterior state estimate  (NEW VALUES)
        float p_post[n];  // First estimate error covariance
        float z_hat[n];   // Prediction of the measurement
};

#endif