import network,time
from umqtt.simple import MQTTClient 
from machine import I2C,Pin,Timer
import time
from lsm6dsox import LSM6DSOX
step1 = 0
from machine import Pin, I2C
lsm = LSM6DSOX(I2C(0, scl=Pin(13), sda=Pin(12)))



def WIFI_Connect():
    wlan = network.WLAN(network.STA_IF) 
    wlan.active(True)                   
    start_time=time.time()              

    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('13326-2GHz', 'iac-4701') 
        
    if wlan.isconnected():
        print('network information:', wlan.ifconfig())
        return True    

def MQTT_Send(tim):
    client.publish(TOPIC, 'Accelerometer: x:{:>8.3f} y:{:>8.3f} z:{:>8.3f}'.format(*lsm.read_accel()))
    print('Accelerometer: x:{:>8.3f} y:{:>8.3f} z:{:>8.3f}'.format(*lsm.read_accel()))
    print("")
    time.sleep_ms(100)

if WIFI_Connect():
    SERVER = '192.168.0.99'   # my rapa ip address , mqtt broker가 실행되고 있음
    PORT = 1883
    CLIENT_ID = 'Shin' # clinet id 이름
    TOPIC = 'Acceler' # TOPIC 이름
    client = MQTTClient(CLIENT_ID, SERVER, PORT,keepalive=30)
    client.connect()
    tim = Timer(-1)
    tim.init(period=1000, mode=Timer.PERIODIC,callback=MQTT_Send)