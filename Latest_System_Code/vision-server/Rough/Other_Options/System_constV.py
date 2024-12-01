#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.motor import SpeedPercent
from threading import Thread
import math
import time

# Constant Velocity System

class System:
    
    # Contants (in cm)
    base_frame_length  = 60
    base_frame_width   = 60
    ee_frame_length    = 6
    ee_frame_width     = 5
    pradius            = 2.5/2

    # System Variables
    a = [0, base_frame_length]
    b = [base_frame_width, base_frame_length]
    c = [base_frame_width, 0]
    d = [0, 0]
    frame = [a,b,c,d]
    centre_of_system = [base_frame_width/2 , base_frame_length/2]

    # Defining End Effector Variables, Current Position
    o             = []  # End Effector Centre
    points        = []  # End Effector Frame Coordinates [[xP,yP],[xQ,yQ],[xR,yR],[xS,yS]]
    currentlength = []  # Cable lengths associated with current EE Position [LA,LB,LC,LD]

    # Defining Target Position
    disp = (0,0)        # Displacement from current EE Centre
    new  = []           # Target Position with respect to base frame
    new_points = []     # End Effector Frame Coordinates required for Target EE Position
    newlength  = []     # Cable lengths associated with EE for acheiving Target EE Position

    # Finding Movement Variables
    angles = [] # Absolute required Angles in degrees

    # Command Buffer
    min_vel = 5
    max_vel = 40
    motor_a = motor_b = motor_c = motor_d = None
    command_buffer = None

    def __init__(self, motor_a, motor_b, motor_c, motor_d):
        # Initializing End Effector Centre and Frame Coordinates Variables (Assuming EE at Centre of System)
        self.o = [self.base_frame_width/2 , self.base_frame_length/2]
        p = [self.o[0] - self.ee_frame_width/2 , self.o[1] + self.ee_frame_length/2]
        q = [self.o[0] + self.ee_frame_width/2 , self.o[1] + self.ee_frame_length/2]
        r = [self.o[0] + self.ee_frame_width/2 , self.o[1] - self.ee_frame_length/2]
        s = [self.o[0] - self.ee_frame_width/2 , self.o[1] - self.ee_frame_length/2]
        self.points = [p,q,r,s]
        # Initiliazing Cable lengths
        for i in range(0,4):
            diff_x = self.points[i][0] - self.frame[i][0]
            diff_y = self.points[i][1] - self.frame[i][1]
            self.currentlength.append(math.sqrt(diff_x**2 + diff_y**2))
        # Initialize motors and command buffer
        self.motor_a = motor_a
        self.motor_b = motor_b
        self.motor_c = motor_c
        self.motor_d = motor_d
        self.command_buffer = [
        [motor_a, self.min_vel, 0],
        [motor_b, self.min_vel, 0],
        [motor_c, self.min_vel, 0],
        [motor_d, self.min_vel, 0]
        ]

    def update_target_using_disp(self, displacement):
        self.disp = displacement # Displacement from System Centre
        self.new  = [self.base_frame_width/2 + displacement[0], self.base_frame_length/2 + displacement[1]]
        new_p = [self.new[0] - self.ee_frame_width/2 , self.new[1] + self.ee_frame_length/2]
        new_q = [self.new[0] + self.ee_frame_width/2 , self.new[1] + self.ee_frame_length/2]
        new_r = [self.new[0] + self.ee_frame_width/2 , self.new[1] - self.ee_frame_length/2]
        new_s = [self.new[0] - self.ee_frame_width/2 , self.new[1] - self.ee_frame_length/2]
        self.new_points = [new_p, new_q, new_r, new_s]
        newlength = []
        for i in range(0,4):
            diff_x = self.new_points[i][0] - self.frame[i][0]
            diff_y = self.new_points[i][1] - self.frame[i][1]
            newlength.append(math.sqrt(diff_x**2 + diff_y**2))
        self.newlength = newlength

    def update_target_using_coords(self, coords):
        self.new = coords   # Coordinates given already with respect to System Frame
        new_p = [self.new[0] - self.ee_frame_width/2 , self.new[1] + self.ee_frame_length/2]
        new_q = [self.new[0] + self.ee_frame_width/2 , self.new[1] + self.ee_frame_length/2]
        new_r = [self.new[0] + self.ee_frame_width/2 , self.new[1] - self.ee_frame_length/2]
        new_s = [self.new[0] - self.ee_frame_width/2 , self.new[1] - self.ee_frame_length/2]
        self.new_points = [new_p, new_q, new_r, new_s]
        newlength = []
        for i in range(0,4):
            diff_x = self.new_points[i][0] - self.frame[i][0]
            diff_y = self.new_points[i][1] - self.frame[i][1]
            newlength.append(math.sqrt(diff_x**2 + diff_y**2))
        self.newlength = newlength

    def update_req_angles(self):
        abs_req_angles = []
        for i in range(0,4):
            angle = abs(self.newlength[i] - self.currentlength[i]) / self.pradius
            deg_angle = math.degrees(angle)
            abs_req_angles.append(deg_angle)
        self.angles = abs_req_angles
        self.command_buffer = [
        [self.motor_a, 5, self.angles[0]],
        [self.motor_b, 5, self.angles[1]],
        [self.motor_c, 5, self.angles[2]],
        [self.motor_d, 5, self.angles[3]]
        ]

    def fix_command_buffer(self):
        # Correcting Command Buffer Angles to Push/Pull (+ve/-ve angles) with respect to Motor Orientation

        # MotorA
        command_a = self.command_buffer[0]
        if (self.newlength[0] > self.currentlength[0]):
            command_a[2] *= 1
        elif (self.newlength[0] < self.currentlength[0]):
            command_a[2] *= -1
        else:
            command_a[2] = 0

        # MotorB
        command_b = self.command_buffer[1]
        if (self.newlength[1] > self.currentlength[1]):
            command_b[2] *= 1
        elif (self.newlength[1] < self.currentlength[1]):
            command_b[2] *= -1
        else:
            command_b[2] = 0

        # MotorC
        command_c = self.command_buffer[2]
        if (self.newlength[2] > self.currentlength[2]):
            command_c[2] *= 1
        elif (self.newlength[2] < self.currentlength[2]):
            command_c[2] *= -1
        else:
            command_c[2] = 0

        # MotorD
        command_d = self.command_buffer[3]
        if (self.newlength[3] > self.currentlength[3]):
            command_d[2] *= -1
        elif (self.newlength[3] < self.currentlength[3]):
            command_d[2] *= 1
        else:
            command_d[2] = 0

        self.command_buffer = [command_a, command_b, command_c, command_d]
   
    def run_motor(motor, speed, degrees):
        motor.on_for_degrees(SpeedPercent(speed), degrees)

    def move_ee(self):
        threads = []
        for command in self.command_buffer:
            thread = Thread(target=self.run_motor, args=(command[0], command[1], command[2]))
            print(command[1], command[2])
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        # Update Current EE Position
        self.o = self.new
        self.points = self.new_points
        self.currentlength = self.newlength

        time.sleep(2)


