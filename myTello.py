# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 20:13:47 2022

@author: Hak
"""

from tello_vib import tello_vib
import time
import numpy as np
from enum import Enum

class Tag(Enum):
    CAU = 1,
    Left = 2, 
    Right = 3

class MyTello(tello_vib):
    def __init__(self, is_log, is_rec):
        super().__init__(is_log, is_rec)
        start = time.time()
        self.endTime = {
            "FRONT" : start,
            "BACK"  : start,
            "LEFT"  : start,
            "RIGHT" : start,
            "UP"    : start,
            "DOWN"  : start,
            "CW"    : start,
            "CCW"   : start}

    def initPid(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def initDetection(self):
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0

    def initMoveAllVelocity(self):
        currentTime = time.time()
        self.moveFront *= (currentTime <= self.endTime["FRONT" if self.moveFront > 0 else "BACK"])
        self.moveRight *= (currentTime <= self.endTime["RIGHT" if self.moveRight > 0 else "LEFT"])
        self.moveUp *= (currentTime <= self.endTime["UP" if self.moveUp > 0 else "DOWN"])
        self.moveYaw *= (currentTime <= self.endTime["CW" if self.moveYaw > 0 else "CCW"])

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

    # setAction 함수 포인터 사용
    def registerActionWithTime(self, setAction, time):
        endTime = time.time() + time
        setAction()

# --------------------------------------------------------------------------- #

# Tello 정의 : is_log, is_rec
Tello_1 = MyTello(True, True)
Tello = Tello_1.tello

# check frame
frame_tmp = np.zeros((960,720,3))

# PID log : kp, ki, kd 
Tello_1.initPid(0, 0, 0)
time_prev = time.time() - 1

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
    Tello_1.initMoveAllVelocity()
    # x, y, w, h 초기화
    x, y, w, h = 0, 0, 0, 0 # Tello_1.initDetection() 
    
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
        x,y,w,h,label,conf,class_no = Tello_1.detect(frame, Tello_1.model)     # 타겟의 좌표(x,y), 크기(w,h), 정확도(conf), 종류(class_no)
        
        ##################################
        #### 학생들이 수정할 부분 시작 ####
        ##################################
        
        # x : -480 ~ 480
        # y : -360 ~ 360
        
        if y > 100:                                                            # 타겟의 좌표가 중심보다 높으면 고도 상승
            Tello_1.setMoveUpVelocity(15)
        elif y < -100:
            Tello_1.setMoveDownVelocity(15)
            
        if x > 100:                                                            # 타겟이 오른쪽에 있는 경우 오른쪽으로 이동
            Tello_1.setMoveRightVelocity(15)
        elif x < -100:
            Tello_1.setMoveLeftVelocity(15)
            
        if w < 200:                                                            # 타겟이 멀리 있는 경우 앞으로 이동
            Tello_1.setMoveFrontVelocity(15)
        elif w > 250:
            Tello_1.setMoveBackVelocity(15)


        vel = Tello_1.getMoveAllVelocity();
        Tello_1.update(vel)
        
        ##################################
        ##### 학생들이 수정할 부분 끝 #####
        ##################################
        
        # Plot
        Tello_1.plot_tracking(x)
    
    else: # Show plot
        Tello_1.plot_not_tracking()

    text = np.array([f"move_right : {Tello_1.moveRight}", f"move_front : {Tello_1.moveFront}",
                      f"move_up: {Tello_1.moveUp}", f"yaw : {Tello_1.moveYaw}"])
    
    frame = Tello_1.write_txt(frame, text)
    Tello_1.log(x, y,
        Tello_1.moveRight,
        Tello_1.moveFront,
        Tello_1.moveUp,
        Tello_1.moveYaw)
    
Tello_1.end()


"""
50m 기준 그림 정보
x = 480
y = 320
w = 450
h = 315
"""

