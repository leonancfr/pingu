#!/bin/sh

get_board_rev() {
    gpioset -B pull-up gpiochip0 7=0
    gpioset -B pull-up gpiochip0 16=0
    gpioset -B pull-up gpiochip0 17=0
    gpioset -B pull-up gpiochip0 27=0

    gpio_value_7=$(gpioget gpiochip0 7)
    gpio_value_16=$(gpioget gpiochip0 16)
    gpio_value_17=$(gpioget gpiochip0 17)
    gpio_value_27=$(gpioget gpiochip0 27)

    if [ "$gpio_value_7" = "1" ] && [ "$gpio_value_16" = "1" ] && [ "$gpio_value_17" = "1" ] && [ "$gpio_value_27" = "1" ]; then
        echo "rev4"
    elif [ "$gpio_value_7" = "0" ] && [ "$gpio_value_16" = "1" ] && [ "$gpio_value_17" = "1" ] && [ "$gpio_value_27" = "1" ]; then
        echo "rev5"
    else
        echo "Unknown board revision"
    fi
}
