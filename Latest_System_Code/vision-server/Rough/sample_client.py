#!/usr/bin/env python3

import socket
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

# Connect to the server
server_address = "169.254.121.89"  # Replace with the server's IP address
port = 65432
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_address, port))
print("Connected to the server.")
print()

print("Starting Motion")
x_old = 30
y_old = 30
n = 1
try:
    while True:
        # Receive data from the server
        data = client_socket.recv(1024).decode().strip()
        
        if data:
            x_new, y_new = map(float, data.split(","))
            # print(f"Mouse position received: ({x_new}, {y_new})")
            
            # System Motion
            if (math.sqrt((x_new - x_old)**2 + (y_new - y_old)**2) >= 1) and (7 <= x_new <= 53 and 7 <= y_new <= 53):

                print("Movement ",n, "x: ",x_new, "y: ", y_new)  
                # Moving Only if the difference in position is >= 1 and the coordinates within bounds
                # system.update_target_using_coords((x_new, y_new))
                # system.update_command_buffer()
                # system.move_ee_vs()

                x_old = x_new
                y_old = y_new
        
        time.sleep(2)

except KeyboardInterrupt:
    print("Closing connection...")

finally:
    client_socket.close()
    print("Finished Following Target")
