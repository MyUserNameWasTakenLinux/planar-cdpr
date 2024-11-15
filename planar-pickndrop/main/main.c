#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "esp_timer.h"

#define IN1_GPIO 27
#define IN2_GPIO 26
#define IN3_GPIO 25
#define IN4_GPIO 33

// Delay per step in microseconds for 30 RPM
#define STEP_DELAY_US 1

void setup_gpio() {
    gpio_set_direction(IN1_GPIO, GPIO_MODE_OUTPUT);
    gpio_set_direction(IN2_GPIO, GPIO_MODE_OUTPUT);
    gpio_set_direction(IN3_GPIO, GPIO_MODE_OUTPUT);
    gpio_set_direction(IN4_GPIO, GPIO_MODE_OUTPUT);
}

void step_motor(int step) {
    switch (step) {
        case 0:
            gpio_set_level(IN1_GPIO, 1);
            gpio_set_level(IN2_GPIO, 0);
            gpio_set_level(IN3_GPIO, 0);
            gpio_set_level(IN4_GPIO, 0);
            break;
        case 1:
            gpio_set_level(IN1_GPIO, 1);
            gpio_set_level(IN2_GPIO, 1);
            gpio_set_level(IN3_GPIO, 0);
            gpio_set_level(IN4_GPIO, 0);
            break;
        case 2:
            gpio_set_level(IN1_GPIO, 0);
            gpio_set_level(IN2_GPIO, 1);
            gpio_set_level(IN3_GPIO, 0);
            gpio_set_level(IN4_GPIO, 0);
            break;
        case 3:
            gpio_set_level(IN1_GPIO, 0);
            gpio_set_level(IN2_GPIO, 1);
            gpio_set_level(IN3_GPIO, 1);
            gpio_set_level(IN4_GPIO, 0);
            break;
        case 4:
            gpio_set_level(IN1_GPIO, 0);
            gpio_set_level(IN2_GPIO, 0);
            gpio_set_level(IN3_GPIO, 1);
            gpio_set_level(IN4_GPIO, 0);
            break;
        case 5:
            gpio_set_level(IN1_GPIO, 0);
            gpio_set_level(IN2_GPIO, 0);
            gpio_set_level(IN3_GPIO, 1);
            gpio_set_level(IN4_GPIO, 1);
            break;
        case 6:
            gpio_set_level(IN1_GPIO, 0);
            gpio_set_level(IN2_GPIO, 0);
            gpio_set_level(IN3_GPIO, 0);
            gpio_set_level(IN4_GPIO, 1);
            break;
        case 7:
            gpio_set_level(IN1_GPIO, 1);
            gpio_set_level(IN2_GPIO, 0);
            gpio_set_level(IN3_GPIO, 0);
            gpio_set_level(IN4_GPIO, 1);
            break;
    }
}

void app_main() {
    setup_gpio();

    int step = 0;
    while (true) {
        step_motor(step);
        step = (step + 1) % 8;  // Cycle through steps 0 to 7
        esp_rom_delay_us(STEP_DELAY_US);  // Delay in microseconds for precise control
        vTaskDelay(1);  // Yield to allow the watchdog to reset
    }
}
