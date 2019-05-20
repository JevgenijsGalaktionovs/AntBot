#!/usr/bin/env python


import rospy
import numpy as np
from std_msgs.msg import Int16


def kf_ini(ir_raw):
    # A function to initialize the Kalman filter

    # Variables for KF.
    phi = 1      # Dynamic model
    G   = 0      # Process weighted noise
    u   = 1      # System Input
    H   = 1      # Describes how state are mapped into outputs
    Q   = 0.07   # Process noise
    R   = 100    # Sensor covariance

    # Initial filtering, runs only once
    x_prior = phi * ir_raw + G * u              # First prior state estimate
    p_prior = 1                                 # Initial error covariance
    K       = p_prior / (p_prior + R)           # Initial Kalman gain
    x_post  = x_prior + K * (ir_raw - x_prior)  # First posterior state estimate
    p_post  = (1 - K) * p_prior                 # First estimate error covariance


def kf_run(self, phi, G, u, H, Q, R, ir_raw, x_prior, p_prior, K, x_post, p_post):
    # Continously updates the state estimate with every new measurement

    # Time Update (Prediction)
    # ========================
    # Project the state ahead
    self.x_prior = phi * self.x_post + G * u
    z_hat   = H * self.x_prior

    # Project the error covariance ahead
    self.p_prior = phi * self.p_post * phi + Q


    # Measurement Update (Correction)
    # ===============================
    # Compute the Kalman Gain
    self.K       = self.p_prior * H / (H * self.p_prior * H + R)

    # Update the estimate using sensor measurement
    self.x_post  = self.x_prior + self.K * (ir_raw - self.z_hat)

    # Update the error covariance
    self.p_post  = (1 - self.K * H) * self.p_prior

    # Return the updated state
    return self.x_post


def kf_pub():
    # A function to publish the updated state retrieved from the Kalman filter

    kf_upd_pub = rospy.Publisher('kf_updated', Int16, queue_size=1) # Topic for KF to be published to
    rospy.init_node('pub_kalman', anonymous=True)                   # Initiate the ROS publisher node for the KF
    rate = rospy.Rate(10)                                           # 10 hz
    while not rospy.is.shutdown():                                  # Loop as long as no ctrl+c is called in terminal

            kf_upd_input = kf_run(ir_raw)               # Update the state by running the KF
            if (kf_upd_input > 20):                     # If estimated state is within range
                if (kf_upd_input < 150):                # same
                    rospy.loginfo(kf_upd_input)         # Log the info
                    kf_upd_pub.publish(kf_upd_input)    # Publish the updated state to the topic
            rate.sleep()

if __name__ == '__main__':
    try:
        kf_ini()
        kf_pub()
    except rospy.ROSInterruptException:
        pass
