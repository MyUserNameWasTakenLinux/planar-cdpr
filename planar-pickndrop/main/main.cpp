#include <stdio.h>
#include "driver/gpio.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "motor.h"

// Main application
void app_main() {
    Motor top_left_motor(1, 2, 3, 4); // This should be replaced with actual pins

    while (1) {
        top_left_motor.rotate_degrees(360, true, 1000); // Fix this
        vTaskDelay(500); // Fix this
    }
}
