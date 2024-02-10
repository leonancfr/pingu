import time
import json
import serial

try:
    # Configure the UART settings
    uart = serial.Serial('/dev/ttyS0', 115200, timeout = 2)  # Replace with the appropriate serial port and baud rate
except:
    print("ERROR: The Serial port is not available to Open")
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

# Send a JSON message when CM4 will shutdown
stop_message = {
    "version": "0.0.2",
    "msgType": "COMMAND",
    "message": "STOP"
}
send_message(stop_message)