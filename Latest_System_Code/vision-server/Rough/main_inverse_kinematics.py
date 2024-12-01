#!/usr/bin/env python3

import math
import time
from threading import Thread
from System_constT import *
from ev3dev2.motor import SpeedPercent
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D

def run_motor(motor, speed, degrees):
        motor.on_for_degrees(SpeedPercent(speed), degrees)

# TODO:

motor_a = LargeMotor(OUTPUT_B)
motor_b = LargeMotor(OUTPUT_C)
motor_c = LargeMotor(OUTPUT_D)
motor_d = LargeMotor(OUTPUT_A)

print("Initializing the System")
system = System(motor_a, motor_b, motor_c, motor_d)
print()

print("Status: Setting up Motion 1")
system.update_target_using_coords((40,40))
system.update_command_buffer()
system.move_ee()
print("Status: Motion 1 Completed" + "\n")

print("Status: Setting up Motion 2")
system.update_target_using_coords((20,40))
system.update_command_buffer()
system.move_ee()
print("Status: Motion 2 Completed" + "\n")

print("Status: Setting up Motion 3")
system.update_target_using_coords((30,20))
system.update_command_buffer()
system.move_ee()
print("Status: Motion 3 Completed" + "\n")

print("Setting up Motion 4")
system.move_ee_to_centre()
print("Motion 4 Completed" + "\n")