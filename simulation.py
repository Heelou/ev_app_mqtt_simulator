import paho.mqtt.client as mqtt
from datetime import datetime
import json
from random import random
import time

class TemperatureSensor:
    sensor_type='temperature'
    units='celcius'
    instance_id='SN123'

    def __init__(self, average_temperature, temperature_variation, min_temperature, max_temperature):
        self.average_temperature=average_temperature
        self.temperature_variation=temperature_variation
        self.min_temperature=min_temperature
        self.max_temperature=max_temperature
        self.value=0.0

    def sense(self):
        self.value= self.simple_random()
        return self.value

    def simple_random(self):
        value = self.min_temperature + (random() * (self.max_temperature - self.min_temperature))
        return value


class Simulator:
    def __init__(self, interval):
        self.interval = interval

    begin = True

    def start(self):
        ts= TemperatureSensor(20,10,16,35)

        def on_message(client, userdata, message):
            print('Message topic {}'.format(message.topic))
            print('Message payload:')
            print(message.payload.decode())
            sig = message.payload.decode()
            if sig == '0':
                self.begin = False 

        mqtt_publisher = mqtt.Client('Temperature publisher')
        mqtt_publisher.on_message = on_message
        mqtt_publisher.connect('127.0.0.1',1883,60)
        mqtt_publisher.loop_start()


        while self.begin:
            dt = datetime.now().strftime("%d-%m-%YT%H:%M:%S")
            message = {
                "type-id": "de.uni-stuttgart.iaas.sc." + ts.sensor_type,
                "instance-id": ts.instance_id,
                "timestamp": dt,
                "value":{
                ts.units: ts.sense()
                }
            }

            jmsg = json.dumps(message, indent=4)
            mqtt_publisher.publish('TopicID', jmsg, 2)

            print(ts.sensor_type , ts.sense())
            time.sleep(self.interval)
            mqtt_publisher.subscribe('TopicID/stop', qos=2)


def on_message(client, userdata, message):
    print('Message topic {}'.format(message.topic))
    print('Message payload:')
    print(message.payload.decode())
    sig = message.payload.decode()
    if sig == '0':
        mqtt_subscriber.disconnect() 
        s = Simulator(5)
        s.start() 

mqtt_subscriber = mqtt.Client('Temperature subscriber')
mqtt_subscriber.on_message = on_message
mqtt_subscriber.connect('127.0.0.1',1883,60)
mqtt_subscriber.subscribe('TopicID', qos=2)

mqtt_subscriber.loop_forever()
