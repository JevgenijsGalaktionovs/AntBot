#!/usr/bin/env python

from   dynamixel_library import *
from   timeit            import default_timer as timer
import math

def CalcVG1(hexapod_ids,current_id,femur,tibia,coxa_vel,femur_vel,tibia_vel):

    if current_id in hexapod_ids.get('Left_Side'):

        tibia += 0.9296391541
        femur += 0.1867048514
        fe_plus_ti = femur + tibia - 0.3734097028
    else:
        tibia -= 0.9296391541
        femur -= 0.1867048514
        fe_plus_ti = femur + tibia + 0.3734097

    VG1 = (-0.1053414800e-3 * coxa_vel * femur_vel - 0.1053414800e-3 * coxa_vel * tibia_vel) * math.cos(fe_plus_ti) ** 2 + ((-0.4567637116e-3 * femur_vel ** 2 \
           + (-0.1559274903e-2 * coxa_vel - 0.9135274232e-3 * tibia_vel) * femur_vel - 0.1559274903e-2 * coxa_vel * tibia_vel - 0.4567637116e-3 * tibia_vel ** 2) * math.sin(fe_plus_ti) \
           + (-0.1148498708e-2 * femur_vel ** 2 + (-0.5742493540e-3 * tibia_vel - 0.2296997416e-2 * coxa_vel) * femur_vel) * math.sin(femur) + 0.1863410000e-5 * femur_vel ** 2 \
           + 0.1863410000e-5 * tibia_vel ** 2 + 0.3726820000e-5 * femur_vel * tibia_vel) * math.cos(fe_plus_ti) + ((-0.1148498708e-2 * femur_vel ** 2 \
           + (-0.2296997416e-2 * coxa_vel - 0.1722748062e-2 * tibia_vel) * femur_vel - 0.2296997416e-2 * coxa_vel * tibia_vel - 0.5742493540e-3 * tibia_vel ** 2) * math.cos(femur) \
           + 0.1162750000e-5 * femur_vel ** 2 + (-0.9948745700e-3 * coxa_vel + 0.2325500000e-5 * tibia_vel) * femur_vel + 0.1162750000e-5 * tibia_vel ** 2 \
           - 0.9948745700e-3 * coxa_vel * tibia_vel) * math.sin(fe_plus_ti) - 0.1965636000e-4 * math.cos(femur) ** 2 * coxa_vel * femur_vel \
           + ((-0.6758505736e-2 * coxa_vel * femur_vel - 0.3217835478e-2 * femur_vel ** 2) * math.sin(femur) + 0.3991010000e-5 * femur_vel ** 2) * math.cos(femur) \
           + (-0.2973700000e-6 * femur_vel ** 2 - 0.3385763796e-2 * coxa_vel * femur_vel) * math.sin(femur) + 0.6249892000e-4 * coxa_vel * femur_vel + 0.5267074000e-4 * coxa_vel * tibia_vel
    return VG1
def CalcVG2(hexapod_ids,current_id,femur,tibia,coxa_vel,femur_vel,tibia_vel):

    if current_id in hexapod_ids.get('Left_Side'):

        tibia += 0.9296391541
        femur += 0.1867048514
        fe_plus_ti = femur + tibia - 0.3734097028
    else:
        tibia -= 0.9296391541
        femur -= 0.1867048514
        fe_plus_ti = femur + tibia + 0.3734097


    VG2 = ((-0.4567637116e0 * femur_vel - 0.4567637116e0 * tibia_vel + 0.4567637116e0) * coxa_vel * math.sin(fe_plus_ti) + ((-0.1148498708e1 * femur_vel \
          + 0.1148498708e1) * coxa_vel + 0.1148498708e1 * femur_vel * tibia_vel + 0.5742493540e0 * tibia_vel ** 2) * math.sin(femur)) * math.cos(fe_plus_ti) \
          + ((-0.1148498708e1 * femur_vel - 0.1148498708e1 * tibia_vel + 0.1148498708e1) * coxa_vel - 0.1148498708e1 * femur_vel * tibia_vel \
          - 0.5742493540e0 * tibia_vel ** 2) * math.cos(femur) * math.sin(fe_plus_ti) + ((-0.2888145424e1 * femur_vel + 0.2888145424e1) * coxa_vel * math.sin(femur) \
          + (-0.1863410000e-5 + 0.1863410000e-5 * femur_vel + 0.1863410000e-5 * tibia_vel) * coxa_vel * math.cos(tibia) + (0.1162750000e-5 - 0.1162750000e-5 * femur_vel \
          - 0.1162750000e-5 * tibia_vel) * coxa_vel * math.sin(tibia) + (0.3991010000e-5 * femur_vel - 0.3991010000e-5) * coxa_vel) * math.cos(femur) \
          + ((0.1162750000e-5 - 0.1162750000e-5 * femur_vel - 0.1162750000e-5 * tibia_vel) * coxa_vel * math.cos(tibia) + (0.1863410000e-5 - 0.1863410000e-5 * femur_vel \
          - 0.1863410000e-5 * tibia_vel) * coxa_vel * math.sin(tibia) + (-0.2973700000e-6 * femur_vel + 0.2973700000e-6) * coxa_vel) * math.sin(femur)
    return VG2
def CalcVG3(hexapod_ids,current_id,femur,tibia,coxa_vel,femur_vel,tibia_vel):

    if current_id in hexapod_ids.get('Left_Side'):

        tibia += 0.9296391541
        femur += 0.1867048514
        fe_plus_ti = femur + tibia - 0.3734097028
    else:
        tibia -= 0.9296391541
        femur -= 0.1867048514
        fe_plus_ti = femur + tibia + 0.3734097

    VG3 = ((-0.4567637116e-3 * tibia_vel - 0.4567637116e-3 * femur_vel + 0.4567637116e-3) * coxa_vel* math.sin(fe_plus_ti) \
          + ((-0.5742493540e-3 * femur_vel + 0.1148498708e-2) * coxa_vel+ 0.5742493540e-3 * femur_vel * tibia_vel) * math.sin(femur) \
          + (-0.1863410000e-5 + 0.1863410000e-5 * femur_vel + 0.1863410000e-5 * tibia_vel) * coxa_vel) * math.cos(fe_plus_ti) \
          + (((-0.5742493540e-3 * femur_vel + 0.1148498708e-2 - 0.5742493540e-3 * tibia_vel) * coxa_vel- 0.5742493540e-3 * femur_vel * tibia_vel) * math.cos(femur) \
          + (-0.1162750000e-5 + 0.1162750000e-5 * femur_vel + 0.1162750000e-5 * tibia_vel) * coxa_vel) * math.sin(fe_plus_ti) \
          + (0.3217835478e-2 * math.sin(femur) * coxa_vel- 0.3991010000e-5 * coxa_vel) * math.cos(femur) + 0.2973700000e-6 * math.sin(femur) * coxa_vel

    return VG3

def CalcM11(hexapod_ids,current_id,femur,tibia):

    if current_id in hexapod_ids.get('Left_Side'):

        tibia += 0.9296391541
        femur += 0.1867048514
        fe_plus_ti = femur + tibia - 0.3734097028
    else:
        tibia -= 0.9296391541
        femur -= 0.1867048514
        fe_plus_ti = femur + tibia + 0.3734097


    M11 =  0.7796374516e-3 * math.cos(fe_plus_ti) ** 2 + (-0.5267074000e-4 * math.sin(fe_plus_ti) + 0.2296997416e-2 * math.cos(femur) \
    + 0.9948745700e-3) * math.cos(fe_plus_ti) + 0.3379252868e-2 * math.cos(femur) ** 2 + (-0.9828180000e-5 * math.sin(femur) + 0.3385763796e-2) * math.cos(femur) + 0.2905660038e-2
    return M11
def CalcM12(hexapod_ids,current_id,femur,tibia):

    if current_id in hexapod_ids.get('Left_Side'):

        tibia += 0.9296391541
        femur += 0.1867048514
        fe_plus_ti = femur + tibia - 0.3734097028
    else:
        tibia -= 0.9296391541
        femur -= 0.1867048514
        fe_plus_ti = femur + tibia + 0.3734097

    M12 = 0.2283818558e-3 * math.cos(fe_plus_ti) ** 2 + (0.1148498708e-2 * math.cos(femur) - 0.1162750000e-5) * math.cos(fe_plus_ti) \
          + 0.1863410000e-5 * math.sin(fe_plus_ti) + 0.1608917739e-2 * math.cos(femur) ** 2 + 0.2973700000e-6 * math.cos(femur) + 0.3991010000e-5 * math.sin(femur)
    return M12
def CalcM13(hexapod_ids,current_id,femur,tibia):

    if current_id in hexapod_ids.get('Left_Side'):

        tibia += 0.9296391541
        femur += 0.1867048514
        fe_plus_ti = femur + tibia - 0.3734097028
    else:
        tibia -= 0.9296391541
        femur -= 0.1867048514
        fe_plus_ti = femur + tibia + 0.3734097

    M13 = 0.2283818558e-3 * math.cos(fe_plus_ti) ** 2 + (0.5742493540e-3 * math.cos(femur) - 0.1162750000e-5) * math.cos(fe_plus_ti) + 0.1863410000e-5 * math.sin(fe_plus_ti)
    return M13
def CalcM21(hexapod_ids,current_id,femur,tibia):

    if current_id in hexapod_ids.get('Left_Side'):

        tibia += 0.9296391541
        femur += 0.1867048514
        fe_plus_ti = femur + tibia - 0.3734097028
    else:
        tibia -= 0.9296391541
        femur -= 0.1867048514
        fe_plus_ti = femur + tibia + 0.3734097

    M21 = 0.2283818558e-3 * math.cos(fe_plus_ti) ** 2 + (0.1148498708e-2 * math.cos(femur) - 0.1162750000e-5) * math.cos(fe_plus_ti) \
          + 0.1863410000e-5 * math.sin(fe_plus_ti) + 0.1608917739e-2 * math.cos(femur) ** 2 + 0.2973700000e-6 * math.cos(femur) + 0.3991010000e-5 * math.sin(femur)
    return M21
def CalcM22(hexapod_ids,current_id,femur,tibia):

    if current_id in hexapod_ids.get('Left_Side'):

        tibia += 0.9296391541
        femur += 0.1867048514
        fe_plus_ti = femur + tibia - 0.3734097028
    else:
        tibia -= 0.9296391541
        femur -= 0.1867048514
        fe_plus_ti = femur + tibia + 0.3734097

    M22 = 0.1148498708e1 * math.cos(fe_plus_ti) * math.cos(femur) \
          + 0.1148498708e1 * math.sin(fe_plus_ti) * math.sin(femur) + 0.1673076902e1

    return M22
def CalcM23(hexapod_ids,current_id,femur,tibia):

    if current_id in hexapod_ids.get('Left_Side'):

        tibia += 0.9296391541
        femur += 0.1867048514
        fe_plus_ti = femur + tibia - 0.3734097028
    else:
        tibia -= 0.9296391541
        femur -= 0.1867048514
        fe_plus_ti = femur + tibia + 0.3734097

    M23 = 0.5742493540e-3 * math.cos(fe_plus_ti) * math.cos(femur) + 0.5742493540e-3 * math.sin(fe_plus_ti) * math.sin(femur) + 0.6531850058e-3
    return M23
def CalcM31(hexapod_ids,current_id,femur,tibia):

    if current_id in hexapod_ids.get('Left_Side'):

        tibia += 0.9296391541
        femur += 0.1867048514
        fe_plus_ti = femur + tibia - 0.3734097028
    else:
        tibia -= 0.9296391541
        femur -= 0.1867048514
        fe_plus_ti = femur + tibia + 0.3734097

    M31 = 0.2283818558e-3 * math.cos(fe_plus_ti) ** 2 + (0.5742493540e-3 * math.cos(femur) \
          - 0.1162750000e-5) * math.cos(fe_plus_ti) + 0.1863410000e-5 * math.sin(fe_plus_ti)
    return M31
def CalcM32(hexapod_ids,current_id,femur,tibia):

    if current_id in hexapod_ids.get('Left_Side'):

        tibia += 0.9296391541
        femur += 0.1867048514
        fe_plus_ti = femur + tibia - 0.3734097028
    else:
        tibia -= 0.9296391541
        femur -= 0.1867048514
        fe_plus_ti = femur + tibia + 0.3734097

    M32 = 0.5742493540e-3 * math.cos(fe_plus_ti) * math.cos(femur) + 0.5742493540e-3 * math.sin(fe_plus_ti) * math.sin(femur) + 0.6531850058e-3
    return M32
def CalcM33():
    return 0.6531850058e-3


# This is the last version with last(correct) Tau, M and VG formulas. But no 20 via points. 
def Motion2seconds(seconds,R_pos,Kp_coxa,Kp_femur,Kp_tibia): #

    start = timer()
    INTERVAL = 0.1
    hexapod_ids = {'Right_Side': [1,2,3,7,8,9,13,14,15], 'Left_Side': [4,5,6,10,11,12,16,17,18]}

    ID_list = [1,2,3,    4,5,6,    7,8,9,
               10,11,12, 13,14,15, 16,17,18]

    N_to_pwm_mx28  = 354
    # N_to_pwm_mx106 = 105.3571
    N_to_pwm_mx106 = 120
    N_to_pwm_mx64  = 147.5

    coloumb_fr_mx28    = 0.0508
    coloumb_fr_mx106   = 0.3037
    coloumb_fr_mx64    = 0.1492

    pos_visc_fr_mx28  = 0.0096
    pos_visc_fr_mx106 = 0.0388
    pos_visc_fr_mx64  = 0.0198
    neg_visc_fr_mx28  = -0.0097
    neg_visc_fr_mx106 = -0.0392
    neg_visc_fr_mx64  = -0.0200

    servo_pwm_list = [0]*18
    E_pos   = [0]*len(ID_list)
    T       = [0]*len(ID_list)
    pwm     = [0]*len(ID_list)
    pwm_int = [0]*len(ID_list)

    servo_type = 1          # function always starts with servo ID1, which is mx28(servo type 1).
    counter_sample = 0      # just for printing

    while timer() - start < seconds:
        start_time     = timer()
        all_pos        = ReadAllPositions()
        # all_pos_rad    = [(x/4096.0)*2*math.pi for x in all_pos]
        all_pos_rad    = [(((x/2047.5)-1)*math.pi) for x in all_pos]
        all_vel        = ReadAllVelocity()
        all_vel_radsec = [((x*0.229*2*math.pi)/60) for x in all_vel]



        for i in range(len(ID_list)):

            if servo_type == 1: # MX-28

                if all_vel_radsec[i] > 0:
                    Friction = pos_visc_fr_mx28 * all_vel_radsec[i] + coloumb_fr_mx28
                elif all_vel_radsec[i] == 0:
                    Friction = 0
                else:
                    Friction = neg_visc_fr_mx28 * all_vel_radsec[i] - coloumb_fr_mx28

                VG1      = CalcVG1(hexapod_ids,ID_list[i],all_pos_rad[i+1],all_pos_rad[i+2],all_vel_radsec[i],all_vel_radsec[i+1],all_vel_radsec[i+2])
                M_11     = CalcM11(hexapod_ids,ID_list[i],all_pos_rad[i+1],all_pos_rad[i+2])
                E_pos[i] = R_pos[ID_list[i]-1] - all_pos_rad[ID_list[i]-1]
                T[i]     = M_11 * (E_pos[i] * Kp_coxa) + Friction + VG1

                pwm_int[i] = int(N_to_pwm_mx28 * T[i])
                servo_pwm_list[ID_list[i]-1] = pwm_int[i]

            elif servo_type == 2: # MX-106
                if all_vel_radsec[i] > 0:
                    Friction = pos_visc_fr_mx106 * all_vel_radsec[i] + coloumb_fr_mx106
                elif all_vel_radsec[i] == 0:
                    if ID_list[i] == 2 or ID_list[i] == 8 or ID_list[i] == 14:
                        Friction = coloumb_fr_mx106
                    else:
                        Friction = -coloumb_fr_mx106
                else:
                    Friction = neg_visc_fr_mx106 * all_vel_radsec[i] - coloumb_fr_mx106

                VG2      = CalcVG2(hexapod_ids,ID_list[i],all_pos_rad[i],all_pos_rad[i+1],all_vel_radsec[i-1],all_vel_radsec[i],all_vel_radsec[i+1])
                M_22     = CalcM22(hexapod_ids,ID_list[i],all_pos_rad[i],all_pos_rad[i+1])
                E_pos[i] = R_pos[ID_list[i]-1] - all_pos_rad[ID_list[i]-1]
                T[i]     = M_22 * (E_pos[i] * Kp_femur) + Friction + VG2

                pwm_int[i] = int(N_to_pwm_mx106 * T[i])
                servo_pwm_list[ID_list[i]-1] = pwm_int[i]

            elif servo_type == 3: # MX-64
                if all_vel_radsec[i] > 0:
                    Friction = pos_visc_fr_mx64 * all_vel_radsec[i] + coloumb_fr_mx64
                elif all_vel_radsec[i] == 0:
                    if ID_list[i] == 3 or ID_list[i] == 9 or ID_list[i] == 15:
                        Friction = coloumb_fr_mx64
                    else:
                        Friction = -coloumb_fr_mx64
                else:
                    Friction = neg_visc_fr_mx64 * all_vel_radsec[i] - coloumb_fr_mx64

                VG3      = CalcVG3(hexapod_ids,ID_list[i],all_pos_rad[i-1],all_pos_rad[i],all_vel_radsec[i-2],all_vel_radsec[i-1],all_vel_radsec[i])
                M_33     = CalcM33()
                E_pos[i] = R_pos[ID_list[i]-1] - all_pos_rad[ID_list[i]-1]
                T[i]     = M_33 * (E_pos[i] * Kp_tibia) + Friction + VG3

                pwm_int[i] = int(N_to_pwm_mx64 * T[i])
                servo_pwm_list[ID_list[i]-1] = pwm_int[i]

            servo_type +=1
            if servo_type > 3:
                servo_type = 1

        counter_sample +=1
        print "PWM",counter_sample," Leg1:",servo_pwm_list[0:3],"Leg2:", servo_pwm_list[3:6],"Leg3:", servo_pwm_list[6:9],"Leg4:", servo_pwm_list[9:12],"Leg5:", servo_pwm_list[12:15],"Leg6:", servo_pwm_list[15:18]

        error_in_degrees = [((x*180)/math.pi) for x in E_pos]
        error_rounded = [round(x, 5) for x in error_in_degrees]
        print "ERR",counter_sample," Leg1:",error_rounded[0:3],"Leg2:", error_rounded[3:6],"Leg3:", error_rounded[6:9],"Leg4:", error_rounded[9:12],"Leg5:", error_rounded[12:15],"Leg6:", error_rounded[15:18]
        # print "ERR",counter_sample," Leg1:",error_rounded[0:3],"Leg4:", error_rounded[9:12],"Leg5:", error_rounded[12:15]
        print "Average Error in Degrees: " ,sum(([abs(x) for x in error_rounded]))/len(error_rounded)
        avg_err_leg1 = sum(([abs(x) for x in  error_rounded[0:3]]))/len(error_rounded[0:3])
        avg_err_leg2 = sum(([abs(x) for x in error_rounded[3:6]]))/len(error_rounded[3:6])
        avg_err_leg3 = sum(([abs(x) for x in error_rounded[6:9]]))/len(error_rounded[6:9])
        avg_err_leg4 = sum(([abs(x) for x in error_rounded[9:12]]))/len(error_rounded[9:12])
        avg_err_leg5 = sum(([abs(x) for x in error_rounded[12:15]]))/len(error_rounded[12:15])
        avg_err_leg6 = sum(([abs(x) for x in error_rounded[15:18]]))/len(error_rounded[15:18])
        print "Avg.Err. Leg1: ", round(avg_err_leg1,4),\
              "Avg.Err. Leg2: ", round(avg_err_leg2,4),\
              "Avg.Err. Leg3: ", round(avg_err_leg3,4),\
              "Avg.Err. Leg4: ", round(avg_err_leg4,4),\
              "Avg.Err. Leg5: ", round(avg_err_leg5,4),\
              "Avg.Err. Leg6: ", round(avg_err_leg6,4)
        print ""
        WriteAllPWM(servo_pwm_list)
        end_time   = timer() - start_time
        delay_secs = INTERVAL - end_time
        #print 'Cycle Time: ',delay_secs
        time.sleep(delay_secs)
