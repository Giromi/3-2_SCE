# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 20:13:47 2022

@author: Hak
"""

from tello_vib import tello_vib
import time
import numpy as np

'''           >>> 여기 수정하면 됨 <<<           '''

FRONTFAR = 450 # 50m 보다 멀리 있는 경우

YawTime = 1300 # Yaw 제어 시간

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

def isRightLeftBiased(x):
    if (x > 640):
        return -1
    elif (x < 300):
        return 1
    return 0

def isUpDownBiased(y):
    if (y > 440):
        return -1
    elif (y < 200):
        return 1
    return 0

def isFrontBackBiased(w):
    if (w < 400):
        return -1
    elif (w > 500):
        return 1
    return 0

def isFrontFar(w):
    if (moveYaw != 0):
        return 0
    if (w <= 300):
        return 80
    if (300 < w < 400):
        return 50
    if (w >= 400 and w <= 500):
        return 20
    return 0

def caseCAU():
    global moveFront, Tello_1, subSpeed, isLanding
    isLanding = True
    print('Target CAU')

def caseLeft():
    global moveYaw, yawTimer
    print('Target Left')
    yawTimer.setEndTimeInMs(YawTime)                   # Yaw 제어 시간 설정
    moveYaw = -80


def caseRight():
    global moveYaw, yawTimer
    print('Target Right')
    yawTimer.setEndTimeInMs(YawTime)                   # Yaw 제어 시간 설정   
    moveYaw = 80

def defaultCase():
    pass

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
isLanding = False

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
    if (yawTimer.hasTimeElapsed()):
        yawTimer.endTime = 0
        moveYaw = 0

    x,y,w,h, classNo = 0,0,0,0,0
    
    if Tello_1.tracking:
        x,y,w,h,label,conf,classNo = Tello_1.detect(frame, Tello_1.model)     # 타겟의 좌표(x,y), 크기(w,h), 정확도(conf), 종류(class_no)

        if (isLanding == False):
            if (moveYaw == 0):
                moveUp = isUpDownBiased(y) * subSpeed
                moveRight = isRightLeftBiased(x) * subSpeed
                moveFront = isFrontFar(w)
        else:
            moveFront = isFrontBackBiased(w) * subSpeed
            if moveFront == 0:
                print('Landing')
                Tello_1.land()
                break

        if (w > 450 and moveYaw == 0):
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



# 딕셔너리에서 값을 가져와 함수를 호출jo

