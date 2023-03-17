#10.245.148.227
import paho.mqtt.client as mqtt
import time
import matplotlib.pyplot as plt
import numpy as np
import math
import re

angle_read = mqtt.Client('hankin')
angle_read.connect('10.245.46.38')

L1 = 7
L2 = 13

def what(who,user,message):
    theta = re.findall(r'\d+',message.payload.decode())
    theta_1 = float(theta[0] + '.' + theta[1])
    theta_2 = float(theta[2] + '.' + theta[3])
    x = L1*math.cos(theta_1)+ L2*math.cos(theta_1 + theta_2)
    y = L1*math.sin(theta_1)+ L2*math.sin(theta_1 + theta_2)
    plt.plot(x,y,'o')
    plt.show()

fig = plt.figure()
angle_read.on_message = what
angle_read.loop_start()
angle_read.subscribe('angles')
time.sleep(20)
angle_read.loop_stop()
angle_read.disconnect()

