#include "motor.h"
#include "driver/gpio.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

uint32_t half_step_sequence[8][4] = {
    {1, 0, 0, 0},
    {1, 1, 0, 0},
    {0, 1, 0, 0},
    {0, 1, 1, 0},
    {0, 0, 1, 0},
    {0, 0, 1, 1},
    {0, 0, 0, 1},
    {1, 0, 0, 1}
};

Motor::Motor(uint8_t in1, uint8_t in2, uint8_t in3, uint8_t in4) {
    gpio_set_direction(static_cast<gpio_num_t>(in1), GPIO_MODE_OUTPUT);
    gpio_set_direction(static_cast<gpio_num_t>(in2), GPIO_MODE_OUTPUT);
    gpio_set_direction(static_cast<gpio_num_t>(in3), GPIO_MODE_OUTPUT);
    gpio_set_direction(static_cast<gpio_num_t>(in4), GPIO_MODE_OUTPUT);

    this->in1 = static_cast<gpio_num_t>(in1);
    this->in2 = static_cast<gpio_num_t>(in2);
    this->in3 = static_cast<gpio_num_t>(in3);
    this->in4 = static_cast<gpio_num_t>(in4);
}

void Motor::rotate_degrees(uint16_t angle, bool clockwise, uint16_t speed=1000) {
    uint16_t steps = (4800 / 360) * angle;

    for(uint16_t i = 0; i != steps; ++i) {
        uint16_t step_index = clockwise ? i % 8 : (7 - i % 8);
        gpio_set_level(in1, half_step_sequence[step_index][0]);
        gpio_set_level(in2, half_step_sequence[step_index][1]);
        gpio_set_level(in3, half_step_sequence[step_index][2]);
        gpio_set_level(in4, half_step_sequence[step_index][3]);
        esp_rom_delay_us(speed);
    }
}

Motor::~Motor() {

}

