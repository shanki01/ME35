import time
import machine
import math


from secrets import Tufts_Wireless as wifi
from thetas import theta_1
from thetas import theta_2
import mqtt_CBR

mqtt_broker = '10.245.46.38' 
topic_sub = 'angles'
topic_pub = 'angles'
client_id = 'sophie'

mqtt_CBR.connect_wifi(wifi)

def blink(pin, delay = 0.1):
    led = machine.Pin(pin, machine.Pin.OUT)
    led.on()
    time.sleep(delay)
    led.off()
    
def whenCalled(topic, msg):
    print((topic.decode(), msg.decode()))
    blink(12)
    time.sleep(0.5)
        
def main():
    fred = mqtt_CBR.mqtt_client(client_id, mqtt_broker, whenCalled)
    fred.subscribe(topic_sub)

    old = 0
    i = 0
    while True:
        led_send = machine.Pin(13, machine.Pin.OUT)
        led_send.off()
        led_receive = machine.Pin(12, machine.Pin.OUT)
        led_receive.off()
        try:
            fred.check()
            if (time.time() - old) > 1:
                angle_1 = (180/math.pi)*theta_1[i]
                angle_2 = (180/math.pi)*theta_2[i]
                msg = '(' + str(angle_1) + ',' + str(angle_2) + ')'
                fred.publish(topic_pub, msg)
                blink(13)
                old = time.time()
                i += 1
        except OSError as e:
            print(e)
            fred.connect()
        except KeyboardInterrupt as e:
            fred.disconnect()
            print('done')
            break
    
main()

