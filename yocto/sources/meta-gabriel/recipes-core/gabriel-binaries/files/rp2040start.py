import time
import json
import serial
import os
import subprocess
from datetime import datetime

version = "0.0.2"

try:
    # Configure the UART settings
    uart = serial.Serial('/dev/ttyS0', 115200, timeout = 2, write_timeout = 2)  # Replace with the appropriate serial port and baud rate
except:
    print("ERROR: The Serial port is not available to open")
    exit()


def send_message(message):
    attempts = 0
    while attempts < 5:
        try:
            json_message = json.dumps(message)
            uart.write(json_message.encode())
            uart.write('\n'.encode())  # Add a newline character at the end
            return True
        except:
            attempts += 1
    print("ERROR: Fail to send message to RP2040!")
    return False

def receive_message():
    while uart.inWaiting():
        try:
            message = uart.readline().decode().rstrip()
            if message:
                print("Received Message:", message)
            try:
                jsonloads = json.loads(message) 
                return jsonloads
            except:
                return None
        except:
            return None
    return None

def burn_rp2040_firmware():
    attempts = 0
    while attempts < 5:
        burn_process = subprocess.Popen(['openocd', '-f', 'interface/raspberrypi-swd.cfg', '-f', 'target/rp2040.cfg', '-c', 'program /opt/gabriel/bin/firmware-rp2040/rp2040.elf verify reset exit'])
        try:
            burn_process.wait(10)
            #os.system("sudo openocd -f interface/raspberrypi-swd.cfg -f target/rp2040.cfg -c \"program /opt/gabriel/bin/firmware-rp2040/rp2040.elf verify reset exit\"")
            return True
        except:
            burn_process.kill()
            attempts += 1
    print("ERROR: Fail to burn firmware in RP2040!")
    return False

# Send a JSON message when started
start_message = {
    "version": version,
    "msgType": "COMMAND",
    "message": "START"
}
periodic_message = {
    "version": version,
    "msgType": "COMMAND",
    "message": "RUNNING"
}

logFilePath = "/home/gabriel/rp2040log.txt" # <= MODIFICAR CAMINHO?
if not os.path.isfile(logFilePath):
    logFile = open(logFilePath, "x")
logFile = open(logFilePath, "r")
timesRestarted = len(logFile.readlines())
logFile.close()

if send_message(start_message):
    time.sleep(0.1)
    received_message = receive_message()
else:
    print("ERROR: Fail to send initial message to RP2040!")
    exit()

if (not received_message) or (received_message.get("version") != version):
    if burn_rp2040_firmware():
        send_message(start_message)
        time.sleep(0.1)
        received_message = receive_message()
    else:
        exit()

while (received_message) and (received_message.get("msgType")=="ERROR"):
    if send_message(start_message):
        time.sleep(0.1)
        received_message = receive_message()
    else:
        print("ERROR: Fail to send start message to RP2040!")
        exit()

if (received_message) and (received_message.get("msgType")=="ACK") and (received_message.get("message")=="RESET_BY_RP2040"):
    logFile = open(logFilePath, "a")
    currentTime = datetime.now()
    logFile.write(f"{timesRestarted}\t{currentTime}\n")
    logFile.close()

# Send a JSON message every 300 seconds
while True:

    send_message(periodic_message)
    time.sleep(1)

    received_message = receive_message()
    if (received_message) and (received_message.get("msgType")=="ERROR"):
        if (received_message.get("message")=="NOT STARTED"):
            send_message(start_message)
        else:
            send_message(periodic_message)
    time.sleep(300)
