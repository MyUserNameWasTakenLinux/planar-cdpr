#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.motor import SpeedPercent
from threading import Thread
import math
import time

#TODO

def run_motor(motor, speed, degrees):
    motor.on_for_degrees(SpeedPercent(speed), degrees)

motor_a = LargeMotor(OUTPUT_D)
motor_b = LargeMotor(OUTPUT_A)
motor_c = LargeMotor(OUTPUT_B)
motor_d = LargeMotor(OUTPUT_C)

# Defining Constants
# ===================

base_frame_length = 70.9
base_frame_width  = 57.5

ee_frame_length   = 6
ee_frame_width    = 5
pradius = 2.5/2

o = [base_frame_width/2 , base_frame_length/2]

p = [o[0] - ee_frame_width/2 , o[1] + ee_frame_length/2]
q = [o[0] + ee_frame_width/2 , o[1] + ee_frame_length/2]
r = [o[0] + ee_frame_width/2 , o[1] - ee_frame_length/2]
s = [o[0] - ee_frame_width/2 , o[1] - ee_frame_length/2]
points = [p,q,r,s]

a = [0, base_frame_length]
b = [base_frame_width, base_frame_length]
c = [base_frame_width, 0]
d = [0, 0]
frame = [a,b,c,d]

currentlength = []
for i in range(0,4):
    diff_x = points[i][0] - frame[i][0]
    diff_y = points[i][1] - frame[i][1]
    currentlength.append(math.sqrt(diff_x**2 + diff_y**2))

# Constant V

displacement = (10 ,-10)

new = [base_frame_width/2 + displacement[0], base_frame_length/2 + displacement[1]]

new_p = [new[0] - ee_frame_width/2 , new[1] + ee_frame_length/2]
new_q = [new[0] + ee_frame_width/2 , new[1] + ee_frame_length/2]
new_r = [new[0] + ee_frame_width/2 , new[1] - ee_frame_length/2]
new_s = [new[0] - ee_frame_width/2 , new[1] - ee_frame_length/2]
new_points = [new_p, new_q, new_r, new_s]

newlength = []
for i in range(0,4):
    diff_x = new_points[i][0] - frame[i][0]
    diff_y = new_points[i][1] - frame[i][1]
    newlength.append(math.sqrt(diff_x**2 + diff_y**2))

# [LA,LB,LC,LD]
# [LA,LB,LC,LD]

abs_req_angles = [] # angle in degrees 

for i in range(0,4):
    angle = abs(newlength[i] - currentlength[i]) / pradius
    deg_angle = math.degrees(angle)
    abs_req_angles.append(deg_angle)
    
command_buffer = [
[motor_a, 5, abs_req_angles[0]],
[motor_b, 5, abs_req_angles[1]],
[motor_c, 5, abs_req_angles[2]],
[motor_d, 5, abs_req_angles[3]]
]

# MotorA
command_a = command_buffer[0]
if (newlength[0] > currentlength[0]):
    command_a[2] *= 1
elif (newlength[0] < currentlength[0]):
    command_a[2] *= -1
else:
    command_a[2] = 0

# MotorB
command_b = command_buffer[1]
if (newlength[1] > currentlength[1]):
    command_b[2] *= 1
elif (newlength[1] < currentlength[1]):
    command_b[2] *= -1
else:
    command_b[2] = 0

# MotorC
command_c = command_buffer[2]
if (newlength[2] > currentlength[2]):
    command_c[2] *= 1
elif (newlength[2] < currentlength[2]):
    command_c[2] *= -1
else:
    command_c[2] = 0

# MotorD
command_d = command_buffer[3]
if (newlength[3] > currentlength[3]):
    command_d[2] *= -1
elif (newlength[3] < currentlength[3]):
    command_d[2] *= 1
else:
    command_d[2] = 0

command_buffer = [command_a, command_b, command_c, command_d]

threads = []
for command in command_buffer:
    thread = Thread(target=run_motor, args=(command[0], command[1], command[2]))
    print(command[1], command[2])
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

time.sleep(5)

# Return to Original Place
# ========================