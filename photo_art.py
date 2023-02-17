# pinout used https://www.amazon.com/Reduction-Multiple-Replacement-Velocity-Measurement/dp/B08DKJT2XF/ref=d_pd_di_sccai_cn_sccl_3_1/145-8390281-0998129?pd_rd_w=jYBFm&content-id=amzn1.sym.e13de93e-5518-4644-8e6b-4ee5f2e0b062&pf_rd_p=e13de93e-5518-4644-8e6b-4ee5f2e0b062&pf_rd_r=KX5BJF96QMEVHE275AZD&pd_rd_wg=ZcRhn&pd_rd_r=57bc5303-8936-46a0-8b6d-3e1e6bd180ff&pd_rd_i=B08DKJT2XF&psc=1

import time
import math
from motorController import *

board = NanoMotorBoard()
def Init():
    print("reboot")
    board.reboot()
    time.sleep_ms(500)
    
    motors = []

    # at 50 it works as expected, at 60 shift sides and 
    #is too small duty to move, at 70 is very big duty.
    for i in range(2):
        motors.append(DCMotor(i))

    for motor in motors:  # initialize
        b = motor.setDuty(0)
        b = motor.resetEncoder(0)
    return motors

def Ramp(motors):
    for duty in range(-100,100,1):
        print("Motor Duty: %d" % duty)
        print('Battery: %0.1f' % board.battery(1))
        for motor in motors:
            b = motor.setDuty(duty)
            print(motor.readEncoder(),end=' ')
        print('')
        time.sleep_ms(100)

def Stop(motors):  
    for motor in motors:  # initialize
        b = motor.setDuty(0)

motors = Init()
Kp = 0.5
theta1 = [-8.51112586780829E-01, -7.87784354725638E-01, -6.33304744918922E-01, -4.50085831343468E-01, -3.04888140888271E-01, -2.45563350720786E-01, -2.7860105394487E-01, -3.68513987521974E-01, -5.38571516395467E-01, -8.07041704530205E-01, -1.13420706162197E+00, -1.33402349500851E+00, -1.36347818962529E+00, -1.42263093179253E+00, -1.60059670791357E+00, -1.81137944078365E+00, -1.95831240808852E+00, -2.05222661495436E+00, -2.14632786917196E+00, -2.24858289256303E+00, -2.28909335977597E+00]
theta2 = [3.1402059465568E+00, 3.04434905721348E+00, 2.79058481453655E+00, 2.51057340373427E+00, 2.274272316254E+00, 2.07526673909678E+00, 1.90058883189908E+00, 1.8045656129612E+00, 1.90301713355015E+00, 2.14905943488836E+00, 2.29823934837661E+00, 2.17247403860549E+00, 1.92479635168269E+00, 1.8037278039675E+00, 1.88578157035053E+00, 2.05666292625117E+00, 2.25290783571885E+00, 2.48495504060426E+00, 2.76166545780418E+00, 3.02384878780837E+00, 3.1402059465568E+00]
theta = [theta1, theta2]


desired1 = theta[0]
desired2 = theta[1]
motor1 = DCMotor(0)
motor2 = DCMotor(1) 
for n in range(len(theta1)):   
    desired_1 = desired1[n]*180/math.pi
    desired_2 = desired2[n]*180/math.pi
    while True:
        print('desired 1', desired_1)
        angle_1 = motor1.readEncoder()
        print(angle_1)
        error_1 = desired_1-angle_1
        print("error 1", error_1)
        speed_1 = int(Kp*(error_1))
        print("speed 1", speed_1)
        motor1.setDuty(speed_1)
        if abs(error_1)< 2:
            motor1.setDuty(0)
            break
        time.sleep_ms(6)
    while True:  
        print('desired 2', desired_2)
        angle_2 = motor2.readEncoder()
        print(angle_2)
        error_2 = desired_2-angle_2
        print("error 2", error_2)
        speed_2 = int(Kp*(error_2))
        print("speed 1", speed_2)
        motor2.setDuty(speed_2)
        if abs(error_2)< 2:
            motor1.setDuty(0)
            break
        time.sleep_ms(6)
motors = Init()
Stop(motors)