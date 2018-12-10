#!/usr/bin/env python

from   dynamixel_library import *
from   timeit            import default_timer as timer
import math

def CalcVG1(femur,tibia,coxa_vel,femur_vel,tibia_vel):
    VG1 = ((-0.45676e0 * femur_vel - 0.45676e0 * tibia_vel) * coxa_vel * math.sin(femur + tibia) - 0.11485e1 * math.sin(femur) * coxa_vel * femur_vel)     \
          * math.cos(femur + tibia) + ((-0.11485e1 * femur_vel - 0.11485e1 * tibia_vel) * coxa_vel * math.cos(femur) + (-0.99487e0 * femur_vel - 0.99487e0 \
          * tibia_vel) * coxa_vel) * math.sin(femur + tibia) + ((-0.12977e-2 * femur_vel - 0.12977e-2 * tibia_vel) * coxa_vel * math.cos(tibia) ** 2       \
          + (0.16812e-3 * femur_vel + 0.16812e-3 * tibia_vel) * coxa_vel * math.sin(tibia) * math.cos(tibia) + (0.74273e-3 * femur_vel + 0.64886e-3        \
          * tibia_vel) * coxa_vel) * math.cos(femur) ** 2 + ((0.16812e-3 * femur_vel + 0.16812e-3 * tibia_vel) * coxa_vel * math.sin(femur)                \
          * math.cos(tibia) ** 2 + ((0.12977e-2 * femur_vel + 0.12977e-2 * tibia_vel) * coxa_vel * math.sin(tibia) * math.sin(femur) + 0.4091100000e-5     \
          * femur_vel * tibia_vel + 0.2045600000e-5 * femur_vel ** 2 + 0.2045600000e-5 * tibia_vel ** 2) * math.cos(tibia) + (-0.84058e-4 * tibia_vel      \
          - 0.28885e1 * femur_vel) * coxa_vel * math.sin(femur) + (0.1599900000e-5 * femur_vel * tibia_vel + 0.7999700000e-6 * femur_vel ** 2              \
          + 0.7999700000e-6 * tibia_vel ** 2) * math.sin(tibia) + 0.2972700000e-5 * femur_vel ** 2) * math.cos(femur) + (0.64886e-3 * tibia_vel            \
          + 0.64886e-3 * femur_vel) * coxa_vel * math.cos(tibia) ** 2 + ((0.1599900000e-5 * femur_vel * tibia_vel + 0.7999700000e-6 * femur_vel ** 2       \
          + 0.7999700000e-6 * tibia_vel ** 2) * math.sin(femur) + (-0.84058e-4 * femur_vel - 0.84058e-4 * tibia_vel) * coxa_vel * math.sin(tibia))         \
          * math.cos(tibia) + ((-0.4091100000e-5 * femur_vel * tibia_vel - 0.2045600000e-5 * femur_vel ** 2 - 0.2045600000e-5 * tibia_vel ** 2)            \
          * math.sin(tibia) - 0.25024e1 * coxa_vel * femur_vel - 0.8335900000e-6 * femur_vel ** 2) * math.sin(femur) + (-0.37137e-3 * femur_vel            \
          - 0.32443e-3 * tibia_vel) * coxa_vel
    return VG1
def CalcVG2(femur,tibia,coxa_vel,femur_vel,tibia_vel):
    VG2 = (0.5742493540e0 * tibia_vel ** 2 + 0.1148498708e1 * femur_vel * tibia_vel) * math.sin(femur) * math.cos(femur + tibia) + (-0.5742493540e0
          * tibia_vel ** 2 - 0.1148498708e1 * femur_vel * tibia_vel) * math.cos(femur) * math.sin(femur + tibia) + ((0.2045560000e1 / 10 ** 6 * femur_vel
          + 0.2045560000e1 / 10 ** 6 * tibia_vel - 0.2045560000e1 / 10 ** 6) * coxa_vel* math.cos(tibia) + (-0.7999700000e1 / 10 ** 7 + 0.7999700000e1
          / 10 ** 7 * femur_vel + 0.7999700000e1 / 10 ** 7 * tibia_vel) * coxa_vel* math.sin(tibia) + (0.2972740000e1 / 10 ** 6 * femur_vel - 0.2972740000e1
          / 10 ** 6) * coxa_vel) * math.cos(femur) + ((-0.7999700000e1 / 10 ** 7 + 0.7999700000e1 / 10 ** 7 * femur_vel + 0.7999700000e1 / 10 ** 7
          * tibia_vel) * coxa_vel* math.cos(tibia) + (0.2045560000e1 / 10 ** 6 - 0.2045560000e1 / 10 ** 6 * femur_vel - 0.2045560000e1 / 10 ** 6 * tibia_vel)
          * coxa_vel* math.sin(tibia) + (-0.8335900000e1 / 10 ** 7 * femur_vel + 0.8335900000e1 / 10 ** 7) * coxa_vel) * math.sin(femur)
    return VG2
def CalcVG3(femur,tibia,coxa_vel,femur_vel,tibia_vel):
    VG3 = 0.5742493540e0 * math.sin(femur) * math.cos(femur + tibia) * femur_vel * tibia_vel - 0.5742493540e0 * math.cos(femur) * math.sin(femur + tibia) \
          * femur_vel * tibia_vel + ((0.2045560000e-5 * femur_vel + 0.2045560000e-5 * tibia_vel - 0.2045560000e-5) * coxa_vel* math.cos(tibia) + (-0.7999700000e-6 + 0.7999700000e-6
          * femur_vel + 0.7999700000e-6 * tibia_vel) * coxa_vel* math.sin(tibia) - 0.2972740000e-5 * coxa_vel) * math.cos(femur) + ((-0.7999700000e-6 + 0.7999700000e-6 * femur_vel
          + 0.7999700000e-6 * tibia_vel) * coxa_vel* math.cos(tibia) + (0.2045560000e-5 - 0.2045560000e-5 * femur_vel - 0.2045560000e-5 * tibia_vel) * coxa_vel* math.sin(tibia) \
          + 0.8335900000e-6 * coxa_vel) * math.sin(femur)
    return VG3

def CalcM11(femur,tibia):
    M11 = 0.22838e0 * math.cos(femur + tibia) ** 2 + (0.11485e1 * math.cos(femur) + 0.99487e0) * math.cos(femur + tibia) \
          + (-0.84058e-4 * math.cos(tibia) ** 2 - 0.64886e-3 * math.sin(tibia) * math.cos(tibia) + 0.14443e1) * math.cos(femur) ** 2 \
          + (-0.64886e-3 * math.sin(femur) * math.cos(tibia) ** 2 + 0.84058e-4 * math.sin(femur) * math.sin(tibia) * math.cos(tibia) \
          + 0.37137e-3   * math.sin(femur) + 0.25024e1) * math.cos(femur) + 0.42029e-4 * math.cos(tibia) ** 2 + 0.32443e-3 * math.sin(tibia) \
          * math.cos(tibia) + 0.10854e1
    return M11
def CalcM12(femur,tibia):
    M12 = (-0.7999700000e-6 * math.cos(tibia) + 0.2045600000e-5 * math.sin(tibia) + 0.8335900000e-6) * math.cos(femur) \
          + 0.2045600000e-5 * math.cos(tibia) * math.sin(femur) + (0.7999700000e-6 * math.sin(tibia) + 0.2972700000e-5) * math.sin(femur)
    return M12
def CalcM13(femur,tibia):
    M13 = (-0.7999700000e-6 * math.cos(tibia) + 0.2045560000e-5 * math.sin(tibia)) * math.cos(femur) + 0.2045560000e-5 * math.cos(tibia) \
          * math.sin(femur) + 0.7999700000e-6 * math.sin(tibia) * math.sin(femur)
    return M13

def CalcM21(femur,tibia):
    M21 = (-0.7999700000e-6 * math.cos(tibia) + 0.2045600000e-5 * math.sin(tibia) + 0.8335900000e-6) * math.cos(femur) \
          + 0.2045600000e-5 * math.cos(tibia) * math.sin(femur) + (0.7999700000e-6 * math.sin(tibia) + 0.2972700000e-5) * math.sin(femur)
    return M21 # Same as M12
def CalcM22(femur,tibia):
    M22 = 0.1148498708e1 * math.cos(femur + tibia) * math.cos(femur) + 0.1148498708e1 * math.sin(femur + tibia) * math.sin(femur) + 0.1673075444e1
    return M22
def CalcM23(femur,tibia):
    M23 = 0.5742493540e0 * math.cos(femur + tibia) * math.cos(femur) + 0.5742493540e0 * math.sin(femur + tibia) * math.sin(femur) + 0.2288066590e0
    return M23

def CalcM31(femur,tibia):
    M31 = (-0.7999700000e-6 * math.cos(tibia) + 0.2045560000e-5 * math.sin(tibia)) * math.cos(femur) + 0.2045560000e-5 * math.cos(tibia) \
          * math.sin(femur) + 0.7999700000e-6 * math.sin(tibia) * math.sin(femur)
    return M31
def CalcM32(femur,tibia):
    M32 = 0.5742493540e0 * math.cos(femur + tibia) * math.cos(femur) + 0.5742493540e0 * math.sin(femur + tibia) * math.sin(femur) + 0.2288066590e0
    return M32
def CalcM33():
    return 0.2288066590

def Motion():

    start = timer()
    sample_rate = 0.1
    ID_list = [1,2,3]


    #Rp_1 = [math.pi]*21
    #Rp_2 = [math.pi]*21
    #Rp_3 = [math.pi]*21



    #Rp_1 =[0, 0.002433, 0.009210, 0.01966, 0.03317, 0.04895, 0.06638, 0.08477, 0.1036, 0.1223, 0.1405, 0.1579, 0.1742, 0.1891, 0.2025, 0.2142, 0.2242, 0.2321, 0.2380, 0.2417, 0.2430]
    #Rp_1 =[(x+math.pi) for x in Rp_1]
    #Rp_2 =[0.6981, 0.7117, 0.7473, 0.7980, 0.8569, 0.9165, 0.9695, 1.009, 1.031, 1.029, 1.002, 0.9470, 0.8721, 0.7819, 0.6829, 0.5796, 0.4773, 0.3824, 0.3013, 0.2454, 0.2234]
    #Rp_2 =[(x+math.pi) for x in Rp_2]
    #Rp_3 =[-1.016, -1.023, -1.041, -1.065, -1.088,-1.105, -1.112, -1.106 ,-1.084, -1.047,-0.9921, -0.9201, -0.8347, -0.7376, -0.6325, -0.5219, -0.4102, -0.3037, -0.2108, -0.1454, -0.1195]
    #Rp_3 =[(x+math.pi) for x in Rp_3]

    #Rv_1 =[0, 0.04667, 0.08723, 0.1210, 0.1476, 0.1672, 0.1801, 0.1869, 0.1884, 0.1854, 0.1786, 0.1687, 0.1563, 0.1418, 0.1258, 0.1083, 0.08964, 0.06960, 0.04821, 0.02510, 0]
    #Rv_2 =[0, 0.2547, 0.4429, 0.5610, 0.6044, 0.5748, 0.4744, 0.3136, 0.1037, -0.1415, -0.4141, -0.6588, -0.8366, -0.9537, -1.021, -1.036, -0.9984, -0.8928, -0.7051, -0.4061, 0]
    #Rv_3 =[0,-0.1347, -0.2166, -0.2413, -0.2094, -0.1290, -0.009536, 0.1356, 0.2954, 0.4618, 0.6347, 0.7931, 0.9176, 1.015, 1.085, 1.119,1.104,1.013,0.8182,0.4778,0]


    #Ra_1 =[0 ,0.4503,0.3862,0.3163, 0.2446, 0.1749, 0.1099, 0.05135, 0.0004560, -0.04273, -0.07665, -0.1073, -0.1307, -0.1494, -0.1650, -0.1785, -0.1911, -0.2041, -0.2187, -0.2364, -0.2646]
    #Ra_2 =[0, 2.361,1.678, 0.9582, 0.2156, -0.5189, -1.199, -1.776, -2.2220, -2.546, -2.859, -2.237, -1.577, -1.018, -0.5099, -0.004997, 0.5582, 1.268, 2.188, 3.314, 4.575]
    #Ra_3 =[0, -1.206, -0.6512, -0.07053, 0.4750, 0.9395, 1.288, 1.512, 1.624, 1.680, 1.797, 1.468, 1.164, 0.8989, 0.6070, 0.2172, -0.3378, -1.173, -2.349, -3.828, -5.397]

    Ra_1 = [0]*21
    Ra_2 = [0]*21

    Ra_3 = [0]*21
    Rv_1 = [0]*21
    Rv_2 = [0]*21
    Rv_3 = [0]*21
    Rp_1 =[math.pi]*21
    Rp_2 =[0.6981+math.pi]*21
    Rp_3 =[-1.016+math.pi]*21

    Rp_all_servos = [Rp_1,Rp_2,Rp_3]
    Rv_all_servos = [Rv_1,Rv_2,Rv_3]
    Ra_all_servos = [Ra_1,Ra_2,Ra_3]

    #Kp_coxa  = 2
    #Kv_coxa  = 0
    # Kv_coxa  = 1
    # Kp_coxa  = 1
    #Kp_femur = 2
    #Kv_femur = 0
    # Kp_femur = 0.0027
    # Kv_femur = 0.1044
    # Kp_tibia = 0.0012
    # Kv_tibia = 0.0689
    #Kp_tibia = 2
    #Kv_tibia = 0

    Kp_coxa = 2
    Kp_femur = 10
    Kp_tibia = 10
    Kv_coxa = 1
    Kv_femur = 1
    Kv_tibia = 1

    coloumb_fr_mx28    = 0.0508
    coloumb_fr_mx106   = 0.3037
    coloumb_fr_mx64    = 0.1492

    pos_visc_fr_mx28  = 0.0096
    pos_visc_fr_mx106 = 0.0388
    pos_visc_fr_mx64  = 0.0198
    neg_visc_fr_mx28  = -0.0097
    neg_visc_fr_mx106 = -0.0392
    neg_visc_fr_mx64  = -0.0200

    pwm_list = [0]*18
    empty_pwm_list = [0]*18
    servo_pwm_list = [0]*18
    E_pos   = [0]*len(ID_list)
    E_vel   = [0]*len(ID_list)
    T       = [0]*len(ID_list)

    pwm_int = [0]*len(ID_list)
    servo_type = 1
    cycle_number   = 0
    EnableTorqueAllServos()
    while timer() - start < 2.00 :
        cycle_start = timer()
        all_pos        = ReadAllPositions()
        all_pos_rad    = [(x/4096.0)*2*math.pi for x in all_pos]
        all_vel        = ReadAllVelocity()
        all_vel_radsec = [((x*0.229*2*math.pi)/60) for x in all_vel]

        for i in range(len(ID_list)):

            if servo_type == 1: # MX-28, coxa = i, femur= i+1, tibia=i+2

                if all_vel_radsec[i] > 0:
                    Friction = pos_visc_fr_mx28 * all_vel_radsec[i] + coloumb_fr_mx28
                    #print Friction
                elif all_vel_radsec[i] == 0:
                    Friction = 0
                    #print Friction
                else:
                    Friction = neg_visc_fr_mx28 * all_vel_radsec[i] - coloumb_fr_mx28
                    #print Friction
                pwm_convert_coefficient = 354  # max pwm/stall torque mx28   885/2.5
                VG  = CalcVG1(all_pos_rad[i+1],all_pos_rad[i+2],all_vel_radsec[i],all_vel_radsec[i+1],all_vel_radsec[i+2])
                M_11 = CalcM11(all_pos_rad[i+1],all_pos_rad[i+2])
                M_12 = CalcM12(all_pos_rad[i+1],all_pos_rad[i+2])
                M_13 = CalcM13(all_pos_rad[i+1],all_pos_rad[i+2])
                E_pos[i]   = Rp_all_servos[i][cycle_number]   - all_pos_rad[ID_list[i]-1]
                E_pos[i+1] = Rp_all_servos[i+1][cycle_number] - all_pos_rad[ID_list[i+1]-1]
                E_pos[i+2] = Rp_all_servos[i+2][cycle_number] - all_pos_rad[ID_list[i+2]-1]
                E_vel[i]   = Rv_all_servos[i][cycle_number]   - all_vel_radsec[ID_list[i]-1]
                E_vel[i+1] = Rv_all_servos[i+1][cycle_number] - all_vel_radsec[ID_list[i+1]-1]
                E_vel[i+2] = Rv_all_servos[i+2][cycle_number] - all_vel_radsec[ID_list[i+2]-1]
                print "MX-28 E_pos: ", E_pos[i]
		#print "MX-28 VG: ", VG
		#print "MX-28 M_11: ", M_11
		#print "MX-28 M_12: ", M_12
		#print "MX-28 M_13: ", M_13
                #print "MX-28 E_vel[i]: ", E_vel[i]
		#print "MX-28 E_vel[i+1]: ", E_vel[i+1]
                #print "MX-28 E_vel[i+2]: ", E_vel[i+2]
                T[i]  = M_11 * (E_pos[i]   * Kp_coxa  + E_vel[i]   * -Kv_coxa  + Ra_all_servos[i][cycle_number])   \
                      + M_12 * (E_pos[i+1] * Kp_femur + E_vel[i+1] * -Kv_femur + Ra_all_servos[i+1][cycle_number]) \
                      + M_13 * (E_pos[i+2] * Kp_tibia + E_vel[i+2] * -Kv_tibia + Ra_all_servos[i+2][cycle_number]) \
                      + Friction + VG
                # print "M_11: ",M_11
                # print "M_12: ",M_12
                # print "M_13: ",M_13
                # print "MX28 Evel: ", E_vel[i]
                pwm_int[i] = int(pwm_convert_coefficient * T[i])
                servo_pwm_list[ID_list[i]-1] = pwm_int[i]

            elif servo_type == 2: # MX-106, coxa = i-1, femur= i, tibia=i+1

                if all_vel_radsec[i] > 0:
                    Friction = pos_visc_fr_mx106 * all_vel_radsec[i] + coloumb_fr_mx106
                elif all_vel_radsec[i] == 0:
                    Friction = pos_visc_fr_mx106 * all_vel_radsec[i] + coloumb_fr_mx106
                else:
                    Friction = neg_visc_fr_mx106 * all_vel_radsec[i] - coloumb_fr_mx106

                pwm_convert_coefficient = 105.3571  # max pwm/stall torque mx106   885/8.4
                VG  = CalcVG2(all_pos_rad[i],all_pos_rad[i+1],all_vel_radsec[i-1],all_vel_radsec[i],all_vel_radsec[i+1])
                M_21 = CalcM21(all_pos_rad[i],all_pos_rad[i+1])
                M_22 = CalcM22(all_pos_rad[i],all_pos_rad[i+1])
                M_23 = CalcM23(all_pos_rad[i],all_pos_rad[i+1])
                E_pos[i-1] = Rp_all_servos[i-1][cycle_number] - all_pos_rad[ID_list[i-1]-1]
                E_pos[i]   = Rp_all_servos[i][cycle_number]   - all_pos_rad[ID_list[i]-1]
                E_pos[i+1] = Rp_all_servos[i+1][cycle_number] - all_pos_rad[ID_list[i+1]-1]
                E_vel[i-1] = Rv_all_servos[i-1][cycle_number] - all_vel_radsec[ID_list[i-1]-1]
                E_vel[i]   = Rv_all_servos[i][cycle_number]   - all_vel_radsec[ID_list[i]-1]
                E_vel[i+1] = Rv_all_servos[i+1][cycle_number] - all_vel_radsec[ID_list[i+1]-1]
                print "MX-106 E_pos: ", E_pos[i]
                T[i]  = M_21 * (E_pos[i-1] * Kp_coxa  + 0 + 0) \
                      + M_22 * (E_pos[i]   * Kp_femur + 0 + 0) \
                      + M_23 * (E_pos[i+1] * Kp_tibia + 0 + 0) \
                      + VG  + Friction # Friction = 0.3037

                # T[i]  = M_22 * (E_pos[i]   * Kp_femur + E_vel[i]   * Kv_femur + Ra_all_servos[i][cycle_number]) + VG  + Friction
                # T[i] = 0

                print "VG: ", VG
                print "M_21: ", M_21
                print "M_22: ", M_22
                print "M_23: ", M_23
                print "MX106 T[i]: ", T[i]
                pwm_int[i] = int(pwm_convert_coefficient * T[i])
                servo_pwm_list[ID_list[i]-1] = pwm_int[i]

            elif servo_type == 3: # MX-64, coxa = i-2, femur= i-1, tibia=i

                if all_vel_radsec[i] > 0:
                    Friction = pos_visc_fr_mx64 * all_vel_radsec[i] + coloumb_fr_mx64
                elif all_vel_radsec[i] == 0:
                    Friction = pos_visc_fr_mx64 * all_vel_radsec[i] + coloumb_fr_mx64
                else:
                    Friction = neg_visc_fr_mx64 * all_vel_radsec[i] - coloumb_fr_mx64


                pwm_convert_coefficient = 147.5  # max pwm/stall torque mx64   885/6
                VG  = CalcVG3(all_pos_rad[i-1],all_pos_rad[i],all_vel_radsec[i-2],all_vel_radsec[i-1],all_vel_radsec[i])
                M_31 = Creturn 0.2288066590alcM31(all_pos_rad[i-1],all_pos_rad[i])
                M_32 = CalcM32(all_pos_rad[i-1],all_pos_rad[i])
                M_33 = CalcM33()
                E_pos[i-2] = Rp_all_servos[i-2][cycle_number] - all_pos_rad[ID_list[i-2]-1]
                E_pos[i-1] = Rp_all_servos[i-1][cycle_number] - all_pos_rad[ID_list[i-1]-1]
                E_pos[i]   = Rp_all_servos[i][cycle_number] - all_pos_rad[ID_list[i]-1]
                E_vel[i-2] = Rv_all_servos[i-2][cycle_number] - all_vel_radsec[ID_list[i-2]-1]
                E_vel[i-1] = Rv_all_servos[i-1][cycle_number] - all_vel_radsec[ID_list[i-1]-1]
                E_vel[i]   = Rv_all_servos[i][cycle_number] - all_vel_radsec[ID_list[i]-1]
                print "MX64 E_pos[i]: ", E_pos[i]
                T[i]  = M_31 * (E_pos[i-2] * Kp_coxa  + E_vel[i-2] * -Kv_coxa  + Ra_all_servos[i-2][cycle_number])  \
                      + M_32 * (E_pos[i-1] * Kp_femur + E_vel[i-1] * -Kv_femur + Ra_all_servos[i-1][cycle_number])  \
                      + M_33 * (E_pos[i]   * Kp_tibia + E_vel[i]   * -Kv_tibia + Ra_all_servos[i][cycle_number])    \
                      + VG + Friction
                # T[i]  = M_33 * (E_pos[i]   * Kp_tibia + E_vel[i]   * Kv_tibia + Ra_all_servos[i][cycle_number]) + VG + Friction
                # T[i] = 0
                # print "MX64 T[i]: ", T[i]
                pwm_int[i] = int(pwm_convert_coefficient * T[i])
                servo_pwm_list[ID_list[i]-1] = pwm_int[i]

            servo_type +=1
            if servo_type > 3:
                servo_type = 1

        cycle_number +=1
        print servo_pwm_list[0:3]
        #WriteAllPWM(servo_pwm_list)
        cycle_end = timer() - cycle_start
        delay = sample_rate - cycle_end
        print delay
        time.sleep(delay)
    end = timer() - start
    WriteAllPWM(empty_pwm_list)
    print "Execution Time: " , end # Uses via points. Need to update formulas from another file. Need to adjust servo ID list for 1 servo.


Motion()
empty = [0]*18
WriteAllPWM(empty)
