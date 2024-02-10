#!/bin/bash

if [ ! -d "/sys/class/gpio/gpio22" ];
then
       sudo bash -c "echo 22 > /sys/class/gpio/export"
       sleep 0.5
fi
sudo bash -c "echo out > /sys/class/gpio/gpio22/direction"
sleep 0.5
sudo bash -c "echo 1 > /sys/class/gpio/gpio22/value" #turn off PoE
sleep 3
sudo bash -c "echo 0 > /sys/class/gpio/gpio22/value" #turn on PoE

echo "-------------------------------------"
echo "Success... Waiting while system is reseting."
echo "-------------------------------------"
