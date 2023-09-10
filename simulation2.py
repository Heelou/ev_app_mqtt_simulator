import paho.mqtt.client as mqtt
from datetime import datetime
import json
from random import random
import time

ChargingMode = False
Mode = True


class SoC_demo:
    def __init__(self, min_SoC, max_SoC):
        self.min_SoC = min_SoC
        self.max_SoC = max_SoC
        self.SoC_value = 0

    def sense(self):
        self.SoC_value = self.first_SoC_val()
        return self.SoC_value

    def first_SoC_val(self):
        SoC_value = random.randint(self.min_SoC, self.max_SoC)
        return SoC_value


def on_message(client, userdata, message):
    # In ra thông tin tin nhắn

    data = message.payload.decode()

    if data != None:
        print("On Message Global")
        s = Simulator(1.25)
        s.start()


class Simulator:
    def __init__(self, interval):
        self.interval = interval
    #
    begin = True

    def start(self):
        self.begin = True

        def on_message(client, userdata, message):
            print('Message topic {}'.format(message.topic))
            print('Message payload:')
            print(message.payload.decode())
            data = message.payload.decode()
            # lấy value vào begin
            print("On message in Class")
            if data != None:
                self.begin = False
                mqtt_publisher.disconnect()
        mqtt_publisher = mqtt.Client('Temperature publisher')
        mqtt_publisher.on_message = on_message
        mqtt_publisher.connect('171.244.57.88', 1883, 60)
        mqtt_publisher.loop_start()
        SoC_ran = SoC_demo(20, 60)
        SoC_send = SoC_ran.sense()
        while (SoC_send < 95) and (self.begin == True):
            SoC_send = SoC_send + 1
            SoC_messege = {"SoC": SoC_send}
            jmsg1 = json.dumps(SoC_messege, indent=1)

            mqtt_publisher.publish('evse_service/EVSE45678/SoC', jmsg1, 2)
            mqtt_publisher.subscribe("evse_service/EVSE45678/ChargeOff")
            # mqtt_publisher.on_message = on_message

            time.sleep(1)

        # SoC_messege = {"ChargingMode": "False"}
        # jmsg1 = json.dumps(SoC_messege, indent=1)
        # mqtt_publisher.publish(
        #     'evse_service/EVSE45678/ChargeOff', jmsg1, 2)
        # time.sleep(self.interval)


mqtt_subscriber = mqtt.Client('Temperature subscriber')
mqtt_subscriber.connect('171.244.57.88', 1883, 60)
mqtt_subscriber.on_message = on_message
mqtt_subscriber.subscribe('evse_service/EVSE45678/ChargeOn', qos=2)
mqtt_subscriber.loop_forever()
