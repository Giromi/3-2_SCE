# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 20:13:47 2022

@author: Hak
"""

from tello_vib import tello_vib
import time
import numpy as np



# Log
is_log = True
is_rec = True

YAWING_TIME = 1
yaw_begin_time = 0

# Tello 정의
Tello_1 = tello_vib(is_log,is_rec)
Tello = Tello_1.tello

# check frame
frame_tmp = np.zeros((960,720,3))

# PID log
kp,kd,ki = 0,0,0
Tello_1.kp, Tello_1.kd, Tello_1.ki = kp,kd,ki

## JG

kp = np.eye(4,4,dtype=np.float32)
kd = np.eye(4,4,dtype=np.float32)
ki = np.eye(4,4,dtype=np.float32)

kp[2,2] = -0.4
kd[2,2] = -0


kp[1,1] = -0.4
kd[1,1] = -0


kp[0,0] = -1
kd[0,0] = 0

kp = 0.1 * kp;
kd = 0.0 * kd;
ki = -0.3 * ki;

elapsedTime = 0
preTime = 0
_time = 0

        # vel = [move_right,move_front,move_up,yaw]
position_des = np.array([0, 440, 0, 0],dtype=np.float32)

##

flag = False
vel = [0, 0, 0, 0]

error_pre = np.zeros(4)

while not Tello_1.stop :
    _time = time.time()
    elapsedTime = (_time - preTime);
    preTime = _time
    frame = Tello_1.frame_read.frame
    text = np.array([])
    
    # check frame
    if np.sum(frame) == np.sum(frame_tmp):
        continue
    else:
        frame_tmp = frame
    
    move_right, move_up, move_front, yaw = 0, 0, 0, 0 
    x,y,w,h = 0,0,0,0
    
    if Tello_1.tracking:
        ##################### drone control #########################
        class_no =0
        # class_no 1 : CAU, 2: Left, 3: Right
        x,y,w,h,label,conf,class_no = Tello_1.detect(frame, Tello_1.model)     # 타겟의 좌표(x,y), 크기(w,h), 정확도(conf), 종류(class_no)
        
        ##################################
        #### 학생들이 수정할 부분 시작 ####
        ##################################
        
        # x : -480 ~ 480
        # y : -360 ~ 360
        # vel = [move_right,move_front,move_up,yaw]
        
        position = np.array([x, w, y, 0],dtype=np.float32)
        error_pre = error
        error = position_des - position
        pd = kp.dot(error) + kd.dot((error_pre-error)/elapsedTime)
        
        # class_no 1 : CAU, 2: Left, 3: Right
        if yaw_begin_time != 0:
            flag = False
            # 최소한의 회전 후 error detection
            if time.time() - yaw_begin_time > YAWING_TIME and abs(x) < 15:
                yaw_begin_time = 0
        elif vel[1] < 15 and flag:
            yaw_begin_time = time.time()
            if class_no == 1:
                Tello.land()
                break
            elif class_no == 2:
                vel = [0,0,0,-50]
            elif class_no == 3:
                vel = [0,0,0,50]
        else:
            flag = True
            vel = pd.tolist()

        vel = [int(i) for i in vel]
        vel = [min(90,i) for i in vel]
        vel = [max(-90,i) for i in vel]
        print(vel)
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


