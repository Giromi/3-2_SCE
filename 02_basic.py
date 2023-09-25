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

FRONTBIAS = 300
BACKBIAS = 600

FRONTFAR = 400 # 50m 보다 멀리 있는 경우

YAWTIME = 1000 # Yaw 제어 시간

''' --------------------------------------------- '''

'''
50m 기준 그림 정보
x = 480
y = 320
w = 450
h = 315
'''

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
startTime = time.time()
timePrev = time.time() - 1
moveRight, moveUp, moveFront, moveYaw = 0, 0, 0, 0
yawEndTime = 0

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
    moveYaw *= 0 if (time.time() * 1000 > yawEndTime) else 1  # Yaw 제어 시간이 지나면 0으로 만듦
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

        mainSpeed = 100
        subSpeed = 15

        ''' 치우침 보정 '''
        if y > UPBIAS:                                                            # 타겟의 좌표가 중심보다 높으면 고도 상승
            moveUp = subSpeed
        elif y < DOWNBIAS:
            moveUp = -subSpeed

        if x > RIGHTBIAS:                                                            # 타겟이 오른쪽에 있는 경우 오른쪽으로 이동
            moveRight = subSpeed
        elif x < LEFTBIAS:
            moveRight = -subSpeed

        ''' 타겟 접근 '''
        if w < FRONTFAR:                                                            # 타겟이 멀리 있는 경우 앞으로 이동
            moveFront = mainSpeed
        else:
            moveFront = 0

        ''' 타겟 발견 '''
        if (classNo == 1):                                  # CAU
            if (w < FRONTBIAS):
                moveFront = subSpeed
            elif (w > BACKBIAS):
                moveFront = -subSpeed
            if moveFront == 0:
                Tello_1.land()
        elif (classNo == 2):                                # Left
            yawEndTime = time.time() * 1000 + YAWTIME
            moveYaw = -mainSpeed
        elif (classNo == 3):                                # Right
            yawEndTime = time.time() * 1000 + YAWTIME
            moveYaw = mainSpeed

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
print("End time : ", time.time() - startTime, 's')



