#ifndef MOTOR_H
#define MOTOR_H

#include <cstdint>

class Motor {
private:
gpio_num_t in1, in2, in3, in4;

public:
    Motor(uint8_t in1, uint8_t in2, uint8_t in3, uint8_t in4);
    void rotate_degrees(uint16_t angle, bool clockwise, uint16_t speed); // angle in degrees
    ~Motor();
};


#endif