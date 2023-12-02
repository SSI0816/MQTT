import random
import time
import paho.mqtt.client as mqtt_client
import re
from gtts import gTTS 
import os 
import time 
import playsound 
import pygame

from sklearn.datasets import load_digits

pygame.mixer.init()

def speak_save(text):
    tts = gTTS(lang='en', text=text ) #ko')
    filename='/home/pi/Desktop/vsc_ws/voice.mp3'
    tts.save(filename) 

def speaker_out():
    pygame.mixer.music.load("/home/pi/Desktop/vsc_ws/voice.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

global count
count = 0
global distance
distance = 0
global F_dis
F_dis = 0

broker_address = "localhost"
broker_port = 1883

topic = "ultra"


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
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        dis = msg.payload.decode()
        number = re.findall(r'\d+.\d+', dis)
        print(number)
        global count
        global distance
        global F_dis
        if count == 0:
            F_dis = float(number[0])
        if count == 3:
            L_dis = float(number[0])
            distance = F_dis - L_dis
            print("============================================================")
            print(f"result : {distance}'")
            print("============================================================")
            if distance > 0:
                print("I'm getting closer.")
                speak_save("I'm getting closer")
                speaker_out()
            if distance < 0:
                print("I'm moving away.")
                speak_save("I'm moving away.")
                speaker_out()
            distance = 0
            count = 0

        else :
            count = count + 1
        

    client.subscribe(topic) #1
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()