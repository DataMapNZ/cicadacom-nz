#!/usr/bin/env python
import cayenne.client
import datetime
import time
import serial
# import random

def main():
    # Delay Start
    # print "Time now = ", datetime.datetime.now().strftime("%H-%M-%S")
    # time.sleep(60)
    # print "Starting now = ", datetime.datetime.now().strftime("%H-%M-%S")

    # Cayenne authentication info. This should be obtained from the Cayenne Dashboard.
    MQTT_USERNAME = ""
    MQTT_PASSWORD = ""
    MQTT_CLIENT_ID = ""

    channels = {
        "A": {"chan_num": 1, "devisor": 10},
        "B": {"chan_num": 1, "devisor": 10},
        "C": {"chan_num": 1, "devisor": 100},
        "D": {"chan_num": 1, "devisor": 1},
        "E": {"chan_num": 1, "devisor": 1},
        "F": {"chan_num": 1, "devisor": 1},
        "G": {"chan_num": 1, "devisor": 1000},
        "H": {"chan_num": 1, "devisor": 1},
        "I": {"chan_num": 1, "devisor": 1},
        "J": {"chan_num": 1, "devisor": 1},
        "K": {"chan_num": 1, "devisor": 1},
        "L": {"chan_num": 1, "devisor": 1000}
    }

    # Other settings that seem to be embedded in Cayenne's libraries
    # MQTT_URL =    "mqtt.mydevices.com"
    # MQTT_PORT =   "1883"

    # Default location of serial port on Pi models 1 and 2
    #SERIAL_PORT =  "/dev/ttyAMA0"

    # Default location of serial port on Pi models 3 and Zero
    SERIAL_PORT = "/dev/ttyS0"

    # How often shall we write values to Cayenne? (Seconds + 1)
    interval = 5

    # This sets up the serial port specified above. baud rate is the bits per second timeout seconds
    #port = serial.Serial(SERIAL_PORT, baudrate=2400, timeout=5)

    # This sets up the serial port specified above. baud rate.  This WAITS for any cr/lf (new blob of data from picaxe)
    port = serial.Serial(SERIAL_PORT, baudrate=2400)

    # The callback for when a message is received from Cayenne.


    def on_message(message):
        print("def on_message reply back, message received: " + str(message))
        # If there is an error processing the message return an error string, otherwise returns nothing.


    client = cayenne.client.CayenneMQTTClient()
    client.on_message = on_message
    client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID)

    # Predefine Data Packet objects for python prior to trying to look for them :)
    node = ":01"
    channel = "A"
    data = 123
    cs = 0

    while True:
        try:
            rcv = port.readline()  # read buffer until cr/lf
            #print("Serial Readline Data = " + rcv)
            rcv = rcv.rstrip("\r\n")
            node, channel, data, cs = rcv.split(",")
            # Test Point print("rcv.split Data = : " + node + channel + data + cs)
            if cs == '0':
                # if cs = Check Sum is good = 0 then do the following
                if channel in channels:
                    data = float(data)/channels[channel]["devisor"]
                    client.virtualWrite(channels[channel]["chan_num"], data, "analog_sensor", "null")
                    client.loop()

        except ValueError:
            # if Data Packet corrupt or malformed then...
            print("Data Packet corrupt or malformed")

if __name__ == "__main__":
    main()