#!/bin/sh

if [ ! -d "/sys/class/gpio/gpio4" ];
then
       sudo bash -c "echo 4 > /sys/class/gpio/export"
       sleep 0.5
fi
sudo bash -c "echo out > /sys/class/gpio/gpio4/direction"
sleep 0.5
sudo bash -c "echo 0 > /sys/class/gpio/gpio4/value" #turn off switch
sleep 3
sudo bash -c "echo 1 > /sys/class/gpio/gpio4/value" #turn on switch
echo "-------------------------------------"
echo "Success. Waiting for switch resetting"
echo "-------------------------------------"