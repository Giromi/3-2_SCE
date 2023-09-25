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

'''
50m 기준 그림 정보
x = 480
y = 320
w = 450
h = 315
'''


class TimeChecker:
    def __init__(self):
        self.endTime = 0

    def setEndTimeInMs(self, ms):
        current_time_ms = time.time() * 1000  # 현재 시간을 밀리초(ms)로 변환
        self.endTime = current_time_ms + ms

    def hasTimeElapsed(self):
        current_time_ms = time.time() * 1000  # 현재 시간을 밀리초(ms)로 변환
        return current_time_ms > self.endTime

def isRightLeftBiased(y):
    return 1 if y > RIGHTBIAS else (-1 if y < LEFTBIAS else 0)

def isUpDownBiased(x):
    return 1 if x > UPBIAS else (-1 if x < DOWNBIAS else 0)

def isFrontBackBiased(w):
    return 1 if w < FRONTBIAS else (-1 if w > BACKBIAS else 0)

def isFrontFar(w):
    return 1 if w < FRONTFAR else 0 # mainPath에서 뒤로 갈 필요 없음

def caseCAU():
    global moveFront, Tello_1, subSpeed
    print('Target CAU')
    moveFront = isFrontBackBiased(x) * subSpeed
    if moveFront == 0:
        Tello_1.land()

def caseLeft():
    global moveYaw, yawTimer, mainSpeed
    print('Target Left')
    yawTimer.setEndTimeInMs(YawTime)                   # Yaw 제어 시간 설정
    moveYaw = -mainSpeed


def caseRight():
    global moveYaw, yawTimer, mainSpeed
    print('Target Right')
    yawTimer.setEndTimeInMs(YawTime)                   # Yaw 제어 시간 설정   
    moveYaw = mainSpeed

def defaultCase():
    print('no Dectect any target')

switchDict = {
    1: caseCAU,
    2: caseLeft,
    3: caseRight
}

# Log
is_log = True
is_rec = True

# Tello 정의
Tello_1 = tello_vib(is_log,is_rec)
Tello = Tello_1.tello

# check frame
frame_tmp = np.zeros((960,720,3))

#%%
# PID log
kp,kd,ki = 0,0,0
Tello_1.kp, Tello_1.kd, Tello_1.ki = kp,kd,ki
timePrev = time.time() - 1
moveRight, moveUp, moveFront, moveYaw = 0, 0, 0, 0
yawTimer = TimeChecker()

while not Tello_1.stop :
    #%% control
    frame = Tello_1.frame_read.frame
    text = np.array([])
    
    # check frame
    if np.sum(frame) == np.sum(frame_tmp):
        continue
    else:
        frame_tmp = frame
    
    moveRight, moveUp, moveFront = 0, 0, 0
    moveYaw *= 0 if yawTimer.hasTimeElapsed() else 1  # Yaw 제어 시간이 지나면 0으로 만듦
    x,y,w,h = 0,0,0,0
    
    if Tello_1.tracking:
        ##################### drone control #########################
        """
        Drone velocities between -100~100
        define --> vel = [left_right_velocity, front_back_velocity, up_down_velocity, yaw_velocity]
        
        control by --> update(vel)
        
        front_back_velocity --> + : front, - : back
        left_right_velocity --> + : right, - : left
        up_down_velocity    --> + : up,    - : down
        yaw_velocity        --> + : cw,    - : ccw
        
        50m 기준 그림 정보
        x = 480
        y = 320
        w = 450
        h = 315
        """
        # class_no 1 : CAU, 2: Left, 3: Right
        x,y,w,h,label,conf,classNo = Tello_1.detect(frame, Tello_1.model)     # 타겟의 좌표(x,y), 크기(w,h), 정확도(conf), 종류(class_no)
        
        ##################################
        #### 학생들이 수정할 부분 시작 ####
        ##################################
        
        # x : -480 ~ 480
        # y : -360 ~ 360


        ''' 치우침 보정 '''
        moveUp = isUpDownBiased(x) * subSpeed
        moveRight = isRightLeftBiased(y) * subSpeed
        # moveFront = isFrontBackBiased() * subSpeed        # 타겟이 멀리 있는 경우 앞으로 이동

        ''' 타겟 접근 '''
        moveFront = isFrontFar(w) * mainSpeed

        ''' 타겟 발견 '''
        switchDict.get(classNo, defaultCase)()

        vel = [moveRight, moveFront, moveUp, moveYaw]
        Tello_1.update(vel)
        ##################################
        ##### 학생들이 수정할 부분 끝 #####
        ##################################
        
        # Plot
        Tello_1.plot_tracking(x)
    
    else: # Show plot
        Tello_1.plot_not_tracking()

    text = np.array([f"move_right : {moveRight}", f"move_front : {moveFront}",
                      f"move_up: {moveUp}", f"yaw : {moveYaw}"])
    
    frame = Tello_1.write_txt(frame, text)
    Tello_1.log(x,y,w,h,moveRight,moveFront,moveUp,moveYaw)
    
Tello_1.end()
print("End : ", time.time() - timePrev, 's')



# 딕셔너리에서 값을 가져와 함수를 호출


