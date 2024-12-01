from ev3dev2.motor import LargeMotor, SpeedPercent

class Actuator:

    initial_cable_length = None
    clockwise_for_push = False
    counterclock_for_push = False
    motor = None

    def __init__(self, initial_cl, motor, cw_for_push=False, ccw_for_push=False):
        self.initial_cable_length = initial_cl
        self.clockwise_for_push = cw_for_push
        self.counterclock_for_push = ccw_for_push
        self.motor = motor  # Motor is initialized here

    def push(self, vel, d):
        # Use the instance variables with self
        if self.clockwise_for_push:
            self.motor.on_for_degrees(speed=SpeedPercent(vel), degrees=d)
        elif self.counterclock_for_push:
            self.motor.on_for_degrees(speed=SpeedPercent(vel), degrees=-d)
        else:
            print("Actuator not initialized for pushing")

    def pull(self, vel, d):
        # Use the instance variables with self
        if self.clockwise_for_push:
            self.motor.on_for_degrees(speed=SpeedPercent(vel), degrees=-d)
        elif self.counterclock_for_push:
            self.motor.on_for_degrees(speed=SpeedPercent(vel), degrees=d)
        else:
            print("Actuator not initialized for pulling")
