from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.motor import SpeedPercent
from threading import Thread

motor_a = LargeMotor(OUTPUT_A)
motor_b = LargeMotor(OUTPUT_B)
motor_c = LargeMotor(OUTPUT_C)
motor_d = LargeMotor(OUTPUT_D)

def run_motor(motor, speed, degrees):
    motor.on_for_degrees(SpeedPercent(speed), degrees)



# Structure
# (Motor name, speed, degrees
command_buffer = [
(motor_a, 5, 50),
(motor_a, 5, 50),
(motor_a, 5, 50),
(motor_a, 5, 50)
]

threads = []
for command in command_buffer:
    thread = Thread(target=run_motor, args=(command[0], command[1], command[2])
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
    
