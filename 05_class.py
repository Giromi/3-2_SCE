# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 20:13:47 2022

@author: Hak
"""

from tello_vib import tello_vib
import time
import numpy as np

'''           >>> 여기 수정하면 됨 <<<           '''

RIGHTBIAS = 100
LEFTBIAS = -100

UPBIAS = 100
DOWNBIAS = -100

FRONTBIAS = 400
BACKBIAS = 500 

FRONTFAR = 400 # 50m 보다 멀리 있는 경우

YawTime = 1000 # Yaw 제어 시간

mainSpeed = 100

subSpeed = 15

''' --------------------------------------------- '''



class TimeChecker:
    def __init__(self):
        self.endTime = 0

    def setEndTimeInMs(self, ms):
        current_time_ms = time.time() * 1000  # 현재 시간을 밀리초(ms)로 변환
        self.endTime = current_time_ms + ms

    def hasTimeElapsed(self):
        current_time_ms = time.time() * 1000  # 현재 시간을 밀리초(ms)로 변환
        return current_time_ms > self.endTime

class Drone:
    def __init__(self):
        self.yawTimer = TimeChecker()

    def initPid(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        return self.kp, self.ki, self.kd

    def initDetection(self):
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.label = 0
        self.conf = 0
        self.classNo = 0

    def initMove(self):
        self.moveFront = 0
        self.moveRight = 0
        self.moveUp = 0
        self.moveYaw = 0

    def initMoveAllVelocity(self):
        self.moveFront = 0
        self.moveRight = 0
        self.moveUp = 0
        self.moveYaw *= 0 if self.yawTimer.hasTimeElapsed() else 1  # Yaw 제어 시간이 지나면 0으로 만듦

    def getMoveAllVelocityList(self):
        return [self.moveRight, self.moveFront, self.moveUp, self.moveYaw]

    def setMoveUpVelocity(self, velocity):
        self.moveUp = velocity
    def setMoveDownVelocity(self, velocity):
        self.moveUp = -velocity

    def setMoveFrontVelocity(self, velocity):
        self.moveFront = velocity
    def setMoveBackVelocity(self, velocity):
        self.moveFront = -velocity

    def setMoveRightVelocity(self, velocity):
        self.moveRight = velocity
    def setMoveLeftVelocity(self, velocity):
        self.moveRight = -velocity

    def setTurnRightVelocity(self, velocity):
        self.moveYaw = velocity
    def setTurnLeftVelocity(self, velocity):
        self.moveYaw = -velocity

    def isRightLeftBiased(self):
        return 1 if self.y > RIGHTBIAS else (-1 if self.y < LEFTBIAS else 0)

    def isUpDownBiased(self):
        return 1 if self.x > UPBIAS else (-1 if self.x < DOWNBIAS else 0)

    def isFrontBackBiased(self):
        return 1 if self.w < FRONTBIAS else (-1 if self.w > BACKBIAS else 0)

    def isFrontFar(self):
        return 1 if self.w < FRONTFAR else 0 # mainPath에서 뒤로 갈 필요 없음
    def tunningRightLeft(self):
        self.moveRight = self.isRightLeftBiased() * subSpeed

    def tunningUpDown(self):
        self.moveUp = self.isUpDownBiased() * subSpeed

    def goFront(self):
        self.moveFront = self.isFrontFar() * mainSpeed

    def caseCAU(self):
        global moveFront, Tello_1
        print('Target CAU')
        moveFront = self.isFrontBackBiased() * subSpeed
        if moveFront == 0:
            Tello_1.land()

    def caseLeft(self):
        global moveYaw, yawTimer
        print('Target Left')
        self.yawTimer.setEndTimeInMs(YawTime)                   # Yaw 제어 시간 설정
        self.moveYaw = -mainSpeed


    def caseRight(self):
        global moveYaw, yawTimer
        print('Target Right')
        self.yawTimer.setEndTimeInMs(YawTime)                   # Yaw 제어 시간 설정   
        moveYaw = mainSpeed

    def defaultCase(self):
        print('no Dectect any target')

# --------------------------------------------------------------------------- #


# Tello 정의 : is_log, is_rec
is_log = True
is_rec = True
Tello_1 = tello_vib(is_log,is_rec)
Tello = Tello_1.tello

# Tello 정의
# check frame
frame_tmp = np.zeros((960,720,3))

# PID log : kp, ki, kd 
drone = Drone()
Tello_1.kp, Tello_1.kd, Tello_1.ki = drone.initPid(0,0,0)
timePrev = time.time() - 1
drone.initMove()

switchDict = {
    1: drone.caseCAU,
    2: drone.caseLeft,
    3: drone.caseRight
}

while not Tello_1.stop :
    #%% control
    frame = Tello_1.frame_read.frame
    text = np.array([])
    
    # check frame
    if np.sum(frame) == np.sum(frame_tmp):
        continue
    else:
        frame_tmp = frame

    # moveRight, moveUp, moveFront, moveYaw 초기화
    drone.initMoveAllVelocity()

    # x, y, w, h 초기화
    drone.initDetection()
    
    if Tello_1.tracking:
        """                        >>> drone control <<<                     """

        """
        Drone velocities between -100~100
        define --> vel = [left_right_velocity, front_back_velocity, up_down_velocity, yaw_velocity]
        
        control by --> update(vel)
        
        front_back_velocity --> + : front, - : back
        left_right_velocity --> + : right, - : left
        up_down_velocity    --> + : up,    - : down
        yaw_velocity        --> + : cw,    - : ccw
        
        """
        
        # class_no 1 : CAU, 2: Left, 3: Right
        drone.x, drone.y, drone.w, drone.h, drone.label, drone.conf, drone.classNo = Tello_1.detect(frame, Tello_1.model)     # 타겟의 좌표(x,y), 크기(w,h), 정확도(conf), 종류(class_no)
        
        ##################################
        #### 학생들이 수정할 부분 시작 ####
        ##################################
        
        # x : -480 ~ 480
        # y : -360 ~ 360
        
        ''' 치우침 보정 '''
        drone.tunningRightLeft()
        drone.tunningUpDown()

        ''' 타겟 접근 '''
        drone.isFrontFar()

        ''' 타겟 발견 '''
        switchDict.get(drone.classNo, drone.defaultCase)()

        vel = drone.getMoveAllVelocityList();
        Tello_1.update(vel)
        
        ##################################
        ##### 학생들이 수정할 부분 끝 #####
        ##################################
        
        # Plot
        Tello_1.plot_tracking(drone.x)
    
    else: # Show plot
        Tello_1.plot_not_tracking()

    text = np.array([f"move_right : {Tello_1.moveRight}", f"move_front : {Tello_1.moveFront}",
                      f"move_up: {Tello_1.moveUp}", f"yaw : {Tello_1.moveYaw}"])
    
    frame = Tello_1.write_txt(frame, text)
    Tello_1.log(drone.x, drone.y,
        drone.moveRight,
        drone.moveFront,
        drone.moveUp,
        drone.moveYaw)
    
Tello_1.end()


"""
50m 기준 그림 정보
x = 480
y = 320
w = 450
h = 315
"""

