#!/usr/bin/env python2
import time
import os

from PIL import Image, ImageDraw

from locomotion     import *
from service_router import torque, readIR

step_full_dist_cm  = 8
step_start_dist_cm = 2
slipage_factor       = 1.018
step                 = 20
pixel_to_cm_ratio    = 5.9677


def get_map(map_name):
    ''' Parameter: string with map name, starting with slash symbol "/"
        Function:  converts image to black and white representation
        Return:    object of 'PixelAccess' type (a map)
        Note:      image must be in the same folder as this code file
    '''
    file_dir = os.path.dirname(__file__)
    im = Image.open(file_dir + map_name)
    im = im.convert("L")
    threshold = 230
    im = im.point(lambda p: p > threshold and 255)
    image = im.load()
    print "Image size is:", im.size[0], "x", im.size[1], "(width x height)"
    return image, im


map_name = "/hallway.jpg"
pixels, image = get_map(map_name)


def pathPlanning():
    ''' Function:  executes path planning algorith of AntBot robot in the hallway
        Note:      function STRONGLY requires an optimization. Alpha version.
        Note2:     can only be used by AntBot, only in a hallway map
    '''

    # Some testing goal points. Values are [width, heigth] pixel on the map image.
    # s1_goal_1 = [140,  11]
    # s1_goal_2 = [135,  33]
    # s2_goal_2 = [13, 13]
    # s2_goal_3 = [30, 13]
    # s3_goal_1 = [30, 60]
    # s3_goal_2 = [10, 70]

    # Map checkpoints
    point_F = [65,  22]   # Point F (62cm from Fridge Line)
    point_FH = [22,  39]  # Point FH (Horizontal fridge line defining Segment 3)
    point_A = [22,  22]   # Point A (Segment 2 center)
    point_B = [22,  77]   # Point B (Segment 3 center)

    point_O = point_F     # Point O (Origin, start point)
    point_G = point_B     # Point G (Goal)

    X_coordinateCM, Y_coordinateCM  = get_coordinates(tuple(point_G), point_O)
    robot_x              = -Y_coordinateCM  # distance to goal pos in cm robot x
    robot_y              = -X_coordinateCM  # distance to goal pos in cm robot y
    traveled_cm_dist     = [0, 0]  # In cm [x,y]
    traveled_pixel_dist  = []      # In pixels [x,y]
    segment3_bool        = False
    one_time_check       = False
    current_pixel_pos    = point_O
    starting_pixel_pos   = point_O

    torque(1)
    standUp()

    while 1:

        # Segment 1 : From point_O to Fridge Vertical line
        if current_pixel_pos[0] > point_F[0]:  # Robots "y"
            print "Segment 1"
            tripodGait_start(0, step, 15)
            traveled_cm_dist[0] += step_start_dist_cm * slipage_factor  # Distance til goal position Y
            robot_y -= step_start_dist_cm * slipage_factor
            print "Remaining cm on robot Y-axis (st): ", robot_y
            while current_pixel_pos[0] > point_F[0]:
                tripodGait_full(0, step, 15, 1)
                traveled_cm_dist[0] += step_full_dist_cm * slipage_factor
                robot_y -= step_full_dist_cm * slipage_factor
                print "Remaining cm on robot Y-axis (full): ", robot_y
                traveled_pixel_dist = [value / pixel_to_cm_ratio for value in traveled_cm_dist]
                current_pixel_pos = [x - y for x, y in zip(starting_pixel_pos, traveled_pixel_dist)]
                pixels[int(current_pixel_pos[0]), int(current_pixel_pos[1])] = 0
                print "We are here now: ", current_pixel_pos
                time.sleep(0.01)

                has_moved = distance_adjust2()
                if has_moved is True:
                    print "Positioned ok. Doing a start step."
                    break  # break inner loop to initiate Segment 1 loop with start step (stupid idea)

                if check_goal(robot_y, 5, "Y"):
                    degree_adjust(1)
                    if robot_x >= 0:
                        distance_adjust(3)
                        goal_step = 20
                        dist_pr_start = step_start_dist_cm
                        dist_pr_full  = step_full_dist_cm
                    else:
                        distance_adjust(4)
                        goal_step = -20
                        dist_pr_start = -step_start_dist_cm
                        dist_pr_full  = -step_full_dist_cm

                    tripodGait_start(goal_step, 0, 15)
                    traveled_cm_dist[1] += dist_pr_start * slipage_factor  # Distance til goal position Y
                    robot_x -= dist_pr_start * slipage_factor
                    print "Remaining cm on robot X-axis (st): ", robot_x
                    while abs(current_pixel_pos[1] - point_G[1]) >= 1:
                        tripodGait_full(goal_step, 0, 15, 1)
                        traveled_cm_dist[1] += dist_pr_full * slipage_factor
                        robot_x -= dist_pr_full * slipage_factor
                        print "Remaining cm on robot X-axis (full): ", robot_x

                        traveled_pixel_dist = [value / pixel_to_cm_ratio for value in traveled_cm_dist]
                        current_pixel_pos = [x - y for x, y in zip(starting_pixel_pos, traveled_pixel_dist)]
                        pixels[int(current_pixel_pos[0]), int(current_pixel_pos[1])] = 0
                        print "We are here now: ", current_pixel_pos
                    print "Goal position is reached! Quitting"
                    img.show()
                    quit()

        # Segment 2 : From Fridge line to Point A
        elif current_pixel_pos[0] <= point_F[0] and segment3_bool is False:  # if current Y is larger than fridge start
            print "Segment 2"
            tripodGait_finish(0, step, 15)
            degree_adjust(1)
            tripodGait_start(0, step, 15)
            traveled_cm_dist[0] += step_start_dist_cm * slipage_factor  # Distance til goal position Y
            robot_y -= step_start_dist_cm * slipage_factor
            print "Remaining cm on robot Y-axis (st): ", robot_y
            while current_pixel_pos[0] - point_A[0] > 1:
                tripodGait_full(0, step, 15, 1)
                traveled_cm_dist[0] += step_full_dist_cm * slipage_factor
                robot_y -= step_full_dist_cm * slipage_factor
                print "Remaining cm on robot Y-axis (full): ", robot_y
                traveled_pixel_dist = [value / pixel_to_cm_ratio for value in traveled_cm_dist]
                current_pixel_pos = [x - y for x, y in zip(starting_pixel_pos, traveled_pixel_dist)]
                pixels[int(current_pixel_pos[0]), int(current_pixel_pos[1])] = 0
                print "We are here: ", current_pixel_pos
                time.sleep(0.01)
            if current_pixel_pos[0] - point_A[0] < 1:  # ~6 cm away from goal on Y-axis
                degree_adjust(2)
                time.sleep(0.1)
                distance_adjust(1)
                time.sleep(0.1)
                for x in range(3):
                    yawRotation(-30)
                degree_adjust(3)
                time.sleep(0.1)
                distance_adjust(2)

                if point_G[1] <= point_FH[1] and point_G[0] <= point_F[0]:
                    if robot_y >= 0:  # map left side/ robot right side
                        goal_step = 20
                        dist_pr_start = step_start_dist_cm
                        dist_pr_full  = step_full_dist_cm
                    else:
                        goal_step = -20
                        dist_pr_start = -step_start_dist_cm
                        dist_pr_full  = -step_full_dist_cm

                    tripodGait_start(goal_step, 0, 15)
                    traveled_cm_dist[0] += dist_pr_start * slipage_factor  # Distance til goal position Y
                    robot_y -= dist_pr_start * slipage_factor
                    print "Remaining cm on robot Y-axis (st): ", robot_y
                    while abs(current_pixel_pos[0] - point_G[0]) >= 1:
                        tripodGait_full(goal_step, 0, 15, 1)
                        traveled_cm_dist[0] += dist_pr_full * slipage_factor
                        robot_y -= dist_pr_full * slipage_factor
                        print "Remaining cm on robot Y-axis (full): ", robot_y

                        traveled_pixel_dist = [value / pixel_to_cm_ratio for value in traveled_cm_dist]
                        current_pixel_pos = [x - y for x, y in zip(starting_pixel_pos, traveled_pixel_dist)]
                        pixels[int(current_pixel_pos[0]), int(current_pixel_pos[1])] = 0
                        print "We are here now: ", current_pixel_pos

                    if robot_x >= 0:  # map up side/ robot right side
                        goal_step = -20
                        dist_pr_start = step_start_dist_cm
                        dist_pr_full  = step_full_dist_cm
                    else:
                        goal_step = 20
                        dist_pr_start = -step_start_dist_cm
                        dist_pr_full  = -step_full_dist_cm

                    tripodGait_start(0, goal_step, 15)
                    traveled_cm_dist[1] += dist_pr_start * slipage_factor  # Distance til goal position Y
                    robot_x -= dist_pr_start * slipage_factor
                    print "Remaining cm on robot X-axis (st): ", robot_x
                    while abs(current_pixel_pos[1] - point_G[1]) >= 1:
                        tripodGait_full(0, goal_step, 15, 1)
                        traveled_cm_dist[1] += dist_pr_full * slipage_factor
                        robot_x -= dist_pr_full * slipage_factor
                        print "Remaining cm on robot X-axis (full): ", robot_x

                        traveled_pixel_dist = [value / pixel_to_cm_ratio for value in traveled_cm_dist]
                        current_pixel_pos = [x - y for x, y in zip(starting_pixel_pos, traveled_pixel_dist)]
                        pixels[int(current_pixel_pos[0]), int(current_pixel_pos[1])] = 0
                        print "We are here now: ", current_pixel_pos
                    print "Goal position is reached! Quitting"
                    img.show()
                    quit()

                else:
                    tripodGait_start(0, step, 15)
                    traveled_cm_dist[1] -= step_start_dist_cm * slipage_factor  # Distance til goal position Y
                    robot_x += step_start_dist_cm * slipage_factor
                    print "Remaining cm on robot X-axis (st): ", robot_x
                    while current_pixel_pos[1] <= point_FH[1]:
                        tripodGait_full(0, step, 15, 1)
                        traveled_cm_dist[1] -= step_full_dist_cm * slipage_factor
                        robot_x += step_full_dist_cm * slipage_factor
                        print "Remaining cm on robot X-axis (full): ", robot_x
                        traveled_pixel_dist = [value / pixel_to_cm_ratio for value in traveled_cm_dist]
                        current_pixel_pos = [x - y for x, y in zip(starting_pixel_pos, traveled_pixel_dist)]
                        pixels[int(current_pixel_pos[0]), int(current_pixel_pos[1])] = 0
                        print "We are here now: ", current_pixel_pos
                    segment3_bool = True

        # Segment 3 : From Fridge Horizontal line to Point B
        elif segment3_bool is True:
            print "Segment 3"
            tripodGait_finish(0, step, 15)
            tripodGait_start(0, step, 15)
            traveled_cm_dist[1] -= step_start_dist_cm * slipage_factor  # Distance til goal position Y
            robot_x += step_start_dist_cm * slipage_factor
            print "Remaining cm on robot X-axis (st): ", robot_x
            while current_pixel_pos[1] <= point_B[1]:
                tripodGait_full(0, step, 15, 1)
                traveled_cm_dist[1] -= step_full_dist_cm * slipage_factor
                robot_x += step_full_dist_cm * slipage_factor
                print "Remaining cm on robot X-axis (full): ", robot_x
                traveled_pixel_dist = [value / pixel_to_cm_ratio for value in traveled_cm_dist]
                current_pixel_pos = [x - y for x, y in zip(starting_pixel_pos, traveled_pixel_dist)]
                pixels[int(current_pixel_pos[0]), int(current_pixel_pos[1])] = 0
                print "We are here now: ", current_pixel_pos

                if current_pixel_pos[1] >= 60 and one_time_check is False:  # Past fridge start of plank checkpoint. TBC
                    degree_adjust(4)
                    distance_adjust(5)
                    one_time_check = True

                if check_goal(robot_x, 5, "X"):
                    if robot_y >= 0:  # if to map right = positive numbers
                        goal_step = 20
                        dist_pr_start = step_start_dist_cm
                        dist_pr_full  = step_full_dist_cm
                    else:             # if to map left = negative numbers
                        goal_step = -20
                        dist_pr_start = -step_start_dist_cm
                        dist_pr_full  = -step_full_dist_cm

                    tripodGait_start(goal_step, 0, 15)
                    traveled_cm_dist[0] += dist_pr_start * slipage_factor  # Distance til goal position Y
                    robot_y -= dist_pr_start * slipage_factor
                    print "Remaining cm on robot Y-axis (st): ", robot_y
                    while abs(current_pixel_pos[0] - point_G[0]) >= 1:
                        tripodGait_full(goal_step, 0, 15, 1)
                        traveled_cm_dist[0] += dist_pr_full * slipage_factor
                        robot_y -= dist_pr_full * slipage_factor
                        print "Remaining cm on robot Y-axis (full): ", robot_y

                        traveled_pixel_dist = [value / pixel_to_cm_ratio for value in traveled_cm_dist]
                        current_pixel_pos = [x - y for x, y in zip(starting_pixel_pos, traveled_pixel_dist)]
                        pixels[int(current_pixel_pos[0]), int(current_pixel_pos[1])] = 0
                        print "We are here now: ", current_pixel_pos

                    print "Goal position is reached! Quitting"
                    img.show()
                    quit()


def get_coordinates(goal, start):
    ''' Parameters: x,y goal pixel coordinates of <tuple>, and x,y start pixel coordinates of <list>
        Function:   plots goal location on a map with 50cm radius circle if region is available
        Return:     <tuple> with distance in cm on x and y from start to goal position
    '''
    if pixels[goal] < 126:
        print "Unavailable region:", pixels[goal]
    else:
        print "Available region:",  pixels[goal]
        pixels[goal[0], goal[1]] = 0
        draw = ImageDraw.Draw(image)
        draw.ellipse((goal[0] - 9, goal[1] - 9, goal[0] + 9, goal[1] + 9), outline='black')
        image.show()
        X_px = goal[0] - start[0]
        Y_px = goal[1] - start[1]
        X_cm = X_px * pixel_to_cm_ratio
        Y_cm = Y_px * pixel_to_cm_ratio
        print "X distance in cm:", X_cm
        print "Y distance in cm:", Y_cm
        return X_cm, Y_cm


def degree_adjust(case):
    ''' Parameter: Integer to specify which IR readings to take
        Function:  Rotate AntBot around z-axis to find shortest distance by IR distance
        Note:      function STRONGLY requires an optimization. Alpha version.
    '''
    if case == 1:    # Sum of right and left
        IR_reads = ir_sum_rg_lf
    elif case == 2:  # Sum of front and right
        IR_reads = ir_sum_fr_rg
    elif case == 3:  # Right IR
        IR_reads = ir_right
    elif case == 4:  # Left IR
        IR_reads = ir_left

    rotation_deg = 5
    IR = IR_reads()  # Gives [forward,right,left]
    print "First IR: ", IR
    prev_IR = IR  # Sum of front+right
    yawRotation(rotation_deg)
    time.sleep(0.2)
    IR = IR_reads()
    print "Second IR: ", IR
    curr_IR = IR
    trigger_cw  = False
    trigger_ccw = False
    ccw_bool    = False
    cw_bool     = False
    while trigger_cw is False or trigger_ccw is False:
        if curr_IR <= prev_IR and cw_bool is False:  # Clockwise
            trigger_cw = True
            prev_IR = curr_IR
            yawRotation(rotation_deg)
            time.sleep(0.1)
            IR = IR_reads()
            print "Clockwise IR: ", IR
            curr_IR = IR
            print "Rotating clockwise"
            while curr_IR <= prev_IR:
                prev_IR = curr_IR
                yawRotation(rotation_deg)
                time.sleep(0.1)
                IR = IR_reads()
                print "Clockwise IR: ", IR
                curr_IR = IR
                cw_bool = True

        elif curr_IR > prev_IR and ccw_bool is False:  # Counter-Clockwise
            trigger_ccw = True
            prev_IR = curr_IR
            yawRotation(-rotation_deg)
            time.sleep(0.1)
            IR = IR_reads()
            print "CounterClockwise IR: ", IR
            curr_IR = IR
            while curr_IR <= prev_IR:
                prev_IR = curr_IR
                yawRotation(-rotation_deg)
                time.sleep(0.1)
                IR = IR_reads()
                print "CounterClockwise IR: ", IR
                curr_IR = IR
                print "Rotating counter-clockwise"
                ccw_bool = True
        if ccw_bool is True:
            trigger_cw = True
            prev_IR = curr_IR
            yawRotation(rotation_deg)
            time.sleep(0.1)
            IR = IR_reads()
            print "Clockwise IR: ", IR
            curr_IR = IR
            print "Rotating clockwise"
        if cw_bool is True:
            trigger_ccw = True
            prev_IR = curr_IR
            yawRotation(-rotation_deg)
            time.sleep(0.1)
            IR = IR_reads()
            print "Counter-Clockwise IR: ", IR
            curr_IR = IR


def distance_adjust(case):
    ''' Parameter: Integer to specify which IR readings to take and which Segment
        Function:  Move AntBot perpendicularly to the wall to find desired distance
        Note:      function STRONGLY requires an optimization. Alpha version.
    '''
    # Segment 1 wall from middle line
    s1_left_cm  = 86
    s1_right_cm = 86
    # Segment 2 wall from point A
    s2_front_cm = 94
    s2_right_cm = 90
    # Segment 3 wall from point A
    s3_left_cm = 114

    if case == 1:  # Segment 2: front/right
        IR = readIR()
        fr_dist_to_move = IR[0] - s2_front_cm
        rg_dist_to_move = IR[1] - s2_right_cm
        fr_step = (fr_dist_to_move / 5) * 8
        rg_step = (rg_dist_to_move / 5) * 8
        tripodGait(rg_step / 5, fr_step / 5, 15, 5)
    elif case == 2:
        IR = readIR()  # Segment 2: right
        rg_dist_to_move = IR[1] - s2_right_cm
        rg_step = (rg_dist_to_move / 3) * 8
        tripodGait(rg_step / 3, 0, 15, 3)

    elif case == 3:  # Segment 2: right
        IR = readIR()
        rg_dist_to_move = IR[1] - s1_right_cm
        rg_step = (rg_dist_to_move / 3) * 8
        tripodGait(rg_step / 3, 0, 15, 3)
    elif case == 4:
        IR = readIR()  # Segment 1: left
        lf_dist_to_move = IR[2] - s1_left_cm
        lf_step = (lf_dist_to_move / 3) * 8
        tripodGait(-lf_step / 3, 0, 15, 3)
    elif case == 5:
        IR = readIR()  # Segment 3: left
        lf_dist_to_move = IR[2] - s3_left_cm
        lf_step = (lf_dist_to_move / 5) * 8
        tripodGait(-lf_step / 5, 0, 15, 5)


def distance_adjust2():
    ''' Function: Move AntBot perpendicularly to the wall to find desired distance (another variation)
        Return:   True if adjustment has been done. False if not
        Note:     Will be deprecated in the next iteration
    '''
    deviation, move_x, offset_rotz = calc_ir_params()
    time.sleep(0.1)
    if deviation < 0.7 or deviation > 1.3:
        deviation, move_x, offset_rotz = calc_ir_params()
        time.sleep(0.1)
        if deviation < 0.7 or deviation > 1.3:
            print "IR distance error correction:"
            tripodGait_finish(0, step, 15)
            time.sleep(1)
            pos = tripodGait_start(-move_x / 20 * 10, 0, 20)
            tripodGait_full(-move_x / 20 * 10, 0, 20, 2, pos)
            tripodGait_finish(-move_x / 20 * 10, 0, 20)
            time.sleep(1)
            degree_adjust(1)
            return True
    else:
        return False


def ir_sum_rg_lf():
    ''' Return: Sum of left and right IR sensor measurements on AntBot '''
    IR = readIR()
    return IR[1] + IR[2]


def ir_sum_fr_rg():
    ''' Return: Sum of front and right IR sensor measurements on AntBot '''
    IR = readIR()
    return IR[0] + IR[1]


def ir_right():
    ''' Return: Right IR sensor measurement on AntBot '''
    IR = readIR()
    return IR[1]


def ir_left():
    ''' Return: Right IR sensor measurement on AntBot '''
    IR = readIR()
    return IR[2]


def calc_ir_params():
    ''' Return: Some parameters for path planning algorithm '''
    IR_f, IR_r, IR_l = readIR()
    deviation   = float(IR_r) / float(IR_l)
    move_x      = IR_l - IR_r
    offset_rotz = IR_l + IR_r
    return deviation, move_x, offset_rotz


def check_goal(remaining_dist, proximity, axis=None):
    ''' Parameters: Integer distance from current position to goal point (one axis),
                    Integer proximity range to goal point
                    String axis name, for printing purpose only
    '''
    if  abs(remaining_dist) <= proximity:
        if axis:
            print "Goal is", abs(remaining_dist), "cm away on", axis, "axis"
        return True
    else:
        return False
