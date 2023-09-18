# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 20:13:47 2022

@author: Hak
"""

# from tello_vib import tello_vib
from tello import tello
import time
import numpy as np

# Log
is_log = True
is_rec = True

# Tello 정의
Tello_1 = tello(is_log,is_rec)
Tello = Tello_1.tello

# check frame
frame_tmp = np.zeros((960,720,3))

#%%
# PID log
kp,kd,ki = 0,0,0
Tello_1.kp, Tello_1.kd, Tello_1.ki = kp,kd,ki
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
    
    move_right, move_up, move_front, yaw = 0, 0, 0,80
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
        
        """
        
        # class_no 1 : CAU, 2: Left, 3: Right
        x,y,w,h,label,conf,class_no = Tello_1.detect(frame, Tello_1.model)     # 타겟의 좌표(x,y), 크기(w,h), 정확도(conf), 종류(class_no)
        
        ##################################
        #### 학생들이 수정할 부분 시작 ####
        ##################################
        
        # x : -480 ~ 480
        # y : -360 ~ 360
        
        if y > 100:                                                            # 타겟의 좌표가 중심보다 높으면 고도 상승
            move_up = 15
        elif y < -100:
            move_up = -15
            
        if x > 100:                                                            # 타겟이 오른쪽에 있는 경우 오른쪽으로 이동
            move_right = 15
        elif x < -100:
            move_right = -15
            
        if w < 200:                                                            # 타겟이 멀리 있는 경우 앞으로 이동
            move_front = 15
        elif w > 250:
            move_front = -15

        vel = [move_right,move_front,move_up,yaw]
        Tello_1.update(vel)
        
        ##################################
        ##### 학생들이 수정할 부분 끝 #####
        ##################################
        
        # Plot
        Tello_1.plot_tracking(x)
    
    else: # Show plot
        Tello_1.plot_not_tracking()

    text = np.array([f"move_right : {move_right}", f"move_front : {move_front}",
                      f"move_up: {move_up}", f"yaw : {yaw}"])
    
    frame = Tello_1.write_txt(frame, text)
    Tello_1.log(x,y,w,h,move_right,move_front,move_up,yaw)
    
Tello_1.end()
