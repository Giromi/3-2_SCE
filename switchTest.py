# 코드 일부...
import time

mainSpeed = 100
subSpeed = 15

RIGHTBIAS = 100
LEFTBIAS = -100

UPBIAS = 100
DOWNBIAS = -100

FRONTBIAS = 400
BACKBIAS = 500 

FRONTFAR = 400 # 50m 보다 멀리 있는 경우

YAWTIME = 1000 # Yaw 제어 시간


class TimeChecker:
    def __init__(self):
        self.endTime = 0

    def setEndTimeInMs(self, ms):
        current_time_ms = time.time() * 1000  # 현재 시간을 밀리초(ms)로 변환
        self.endTime = current_time_ms + ms

    def hasTimeElapsed(self):
        current_time_ms = time.time() * 1000  # 현재 시간을 밀리초(ms)로 변환
        return current_time_ms > self.endTime

def isFrontBackBiased(x):
    return 1 if x < FRONTBIAS else (-1 if x > BACKBIAS else 0)

def caseCAU():
    global moveFront, subSpeed
    print('Target CAU')
    moveFront = isFrontBackBiased(w) * subSpeed
    print("moveFront:", moveFront)

def caseLeft():
    global moveYaw, yawTimer, mainSpeed
    print('Target Left')
    yawTimer.setEndTimeInMs(YAWTIME)                   
    moveYaw = -mainSpeed
    print("moveYaw:", moveYaw)

def caseRight():
    global moveYaw, yawTimer, mainSpeed
    print('Target Right')
    yawTimer.setEndTimeInMs(YAWTIME)                   
    moveYaw = mainSpeed
    print("moveYaw:", moveYaw)

def default_case():
    print('no Dectect any target')

switchDict = {
    1: caseCAU,
    2: caseLeft,
    3: caseRight
}

# 테스트 코드
w = 480 
yawTimer = TimeChecker()
moveFront, moveYaw = 0, 0
for classNo in [1, 2, 3, 4]:
    print(f"\nTesting with classNo: {classNo}")
    switchDict.get(classNo, default_case)()

time.sleep(2)

moveYaw *= 0 if yawTimer.hasTimeElapsed() else 1  # Yaw 제어 시간이 지나면 0으로 만듦
print("moveYaw:", moveYaw)


