#!/usr/bin/env python3

from time import sleep
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_3
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.motor import SpeedRPM
from ev3dev2.motor import MoveDifferential
from ev3dev2.wheel import EV3EducationSetTire
from Rough.Matrix import *
import math
import threading
from Rough.Actuator import *

# TODO: 

# Set up motors on ports A, B, C, D
motor_a = LargeMotor(OUTPUT_D)
motor_b = LargeMotor(OUTPUT_A)
motor_c = LargeMotor(OUTPUT_B)
motor_d = LargeMotor(OUTPUT_C)

actuator_a = Actuator(cw_for_push=True , motor=motor_a)
actuator_b = Actuator(ccw_for_push=True, motor=motor_b)
actuator_c = Actuator(cw_for_push=True , motor=motor_c)
actuator_d = Actuator(ccw_for_push=True, motor=motor_d)

# def run_motor_a(velA, d):
#     motor_a.on_for_degrees(speed=velA, degrees=d)  # Run motor A

# def run_motor_b(velB, d):
#     motor_b.on_for_seconds(speed=velB, degrees=d)  # Run motor B

# def run_motor_c(velC, d):
#     motor_c.on_for_seconds(speed=velC, degrees=t)  # Run motor C

# def run_motor_d(velD, d):
#     motor_d.on_for_seconds(speed=velD, degrees=t)  # Run motor D

LA = 24
LB = 26
LC = 25
LD = 24
list_of_cables = [LA,LB,LC,LD]  # L1 by Motor A, L2 by Motor B, L3 by Motor C, L4 by Motor D

# 0

# End Effector Coordinates
x_base = 24.5 
y_base = 3

# Create threads for each motor task
thread_a = threading.Thread(target=actuator_a.push(5,10))
thread_b = threading.Thread(target=run_motor_b.pull(5,10))
thread_c = threading.Thread(target=run_motor_c.pull(5,10))
thread_d = threading.Thread(target=run_motor_d.pull(5,10))

# Start the threads (this will run motors concurrently)
thread_a.start()
thread_b.start()
thread_c.start()
thread_d.start()

# Wait for all threads to finish
thread_a.join()
thread_b.join()
thread_c.join()
thread_d.join()

print("All motors have finished running.")


# Current Position


