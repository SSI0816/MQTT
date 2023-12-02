import random
import time
import paho.mqtt.client as mqtt_client
import re
from pymata4 import pymata4
from gtts import gTTS 
import os 
import time 
import playsound 
import pygame

pygame.mixer.init()

board = pymata4.Pymata4()

servo = board.set_pin_mode_servo(11)

def move_servo(v):                  
    board.servo_write(11, v)
    time.sleep(1) 


def speak_save(text):
    tts = gTTS(lang='en', text=text ) #ko')
    filename='/home/pi/Desktop/Rapa_Mqtt/voice.mp3'
    tts.save(filename) 

def speaker_out():
    pygame.mixer.music.load("/home/pi/Desktop/Rapa_Mqtt/voice.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

global count
count = 0
global x_accel 
x_accel = 0
global y_accel 
y_accel = 0
global z_accel 
z_accel = 0

broker_address = "localhost"
broker_port = 1883

topic = "Acceler"
topic2 = 'ultra'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker")
        else:
            print(f"Failed to connect, Returned code: {rc}")

    def on_disconnect(client, userdata, flags, rc=0):
        print(f"disconnected result code {str(rc)}")

    def on_log(client, userdata, level, buf):
        print(f"log: {buf}")

    # client 생성
    client_id = f"mqtt_client_{random.randint(0, 1000)}"
    client = mqtt_client.Client(client_id)

    # 콜백 함수 설정
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_log = on_log

    # broker 연결
    client.connect(host=broker_address, port=broker_port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}")
        value = msg.payload.decode()
        numbers = re.findall(r'\d+.\d+', value)
        print(numbers)
        global count
        global x_accel 
        global y_accel 
        global z_accel 
        if count == 0:
            F_dis = float(numbers[0])
        if count == 10: 
            x_result = x_accel / 10
            y_result = y_accel / 10
            z_result = z_accel / 10
            print("============================================================")
            print(f"result : {x_result}', '{y_result}', '{z_result}")
            print("============================================================")
            x_accel = 0
            y_accel = 0
            z_accel = 0
            count = 0
            if x_result > 1.0:
              speak_save("I'm running.")
              speaker_out()
              move_servo(180)
              move_servo(0)  
              move_servo(180)
              move_servo(0) 
            if x_result < 1.0:
              speak_save("I'm walking.")
              speaker_out() 
              move_servo(90)
              move_servo(0)  
              move_servo(90)
              move_servo(0)   
        else :
            count = count +1 
        x_accel = x_accel + float(numbers[0])
        y_accel = y_accel + float(numbers[1])
        z_accel = z_accel + float(numbers[2])
    client.subscribe(topic) #1
    client.on_message = on_message



def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()