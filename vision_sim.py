import pygame
import sys
import time as Time

FRONTFAR = 450 # 50m 보다 멀리 있는 경우

YawTime = 1300 # Yaw 제어 시간

subSpeed = 15

class TimeChecker:
    def __init__(self):
        self.endTime = 0

    def setEndTimeInMs(self, ms):
        current_time_ms = Time.time() * 1000  # 현재 시간을 밀리초(ms)로 변환
        self.endTime = current_time_ms + ms

    def hasTimeElapsed(self):
        current_time_ms = Time.time() * 1000  # 현재 시간을 밀리초(ms)로 변환
        return current_time_ms > self.endTime

moveRight, moveUp, moveFront, moveYaw = 0, 0, 0, 0
yawTimer = TimeChecker()
isLanding = False


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

################################################################################

# 초기화
pygame.init()

# x : -480 ~ 480
# y : -360 ~ 360

# 화면 크기 및 설정
WIDTH, HEIGHT = 960, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("마우스 따라가는 네모 박스")

# 색상
BLACK = (0, 0, 0)
GREY = (128, 128, 128)  # 회색 설정
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
INIT_WIDTH, INIT_HEIGHT = 164, 116
CYAN = (0, 255, 255)


# 네모 박스 초기 위치 및 크기
boxWidth, boxHeight = INIT_WIDTH, INIT_HEIGHT
imageWidth, imageHeight = INIT_WIDTH, INIT_HEIGHT
box_x, box_y = WIDTH // 2 - boxWidth // 2, HEIGHT // 2 - boxHeight // 2

# 이동 속도
move_speed = 9

# 최소 이동 거리
min_distance = 5

start_time = pygame.time.get_ticks()
font = pygame.font.Font(None, 36)

# imageWidth, imageHeight = 32, 32  # 이미지 크기 설정
originCauImage = pygame.image.load("cau.png")
cauImageRect = originCauImage.get_rect()


originLeftArrowImage = pygame.image.load("left.png")
originRightArrowImage = pygame.image.load("right.png")

cauImage = pygame.transform.scale(originCauImage, (imageWidth, imageHeight))
leftArrowImage = pygame.transform.scale(originLeftArrowImage, (imageWidth, imageHeight))
rightArrowImage = pygame.transform.scale(originRightArrowImage, (imageWidth, imageHeight))

scale_factor = 1.01 # 이미지 크기를 90%로 축소

# 메인 루프
while True:
    time = pygame.time.get_ticks() // 1000
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # 스크롤 업
                if imageWidth < WIDTH and imageHeight < HEIGHT:
                    imageWidth = min(WIDTH, imageWidth * scale_factor)
                    imageHeight = min(HEIGHT, imageHeight * scale_factor)
                    cauImage = pygame.transform.scale(originCauImage, (imageWidth, imageHeight))
                    leftArrowImage = pygame.transform.scale(originLeftArrowImage, (imageWidth, imageHeight))
                    rightArrowImage = pygame.transform.scale(originRightArrowImage, (imageWidth, imageHeight))
            elif event.button == 5:  # 스크롤 다운
                if imageWidth > 10 and imageHeight > 10:
                    imageWidth = max(10, imageWidth / scale_factor)
                    imageHeight = max(10, imageHeight / scale_factor)
                    cauImage = pygame.transform.scale(originCauImage, (imageWidth, imageHeight))
                    leftArrowImage = pygame.transform.scale(originLeftArrowImage, (imageWidth, imageHeight))
                    rightArrowImage = pygame.transform.scale(originRightArrowImage, (imageWidth, imageHeight))
    # 마우스 위치 가져오기
    mouseX, mouseY = pygame.mouse.get_pos()

    # # 마우스와 박스 사이의 거리 계산
    # dx = mouseX - box_x
    # dy = mouse_y - box_y
    #
    #
    # # 거리가 일정 이상일 때만 이동
    # if abs(dx) > min_distance or abs(dy) > min_distance:
    #     # 거리를 이동 속도로 나누어 박스를 이동
    #     distance = (dx ** 2 + dy ** 2) ** 0.5
    #     ratio = move_speed / distance
    #     box_x += int(dx * ratio)
    #     box_y += int(dy * ratio)

    elapsed_time = (current_time - start_time)

    # 화면 지우기
    screen.fill(GREY)

    # 네모 박스 그리기
    keys = pygame.key.get_pressed()
    pygame.draw.rect(screen, WHITE, (mouseX - imageWidth // 2, mouseY - imageHeight // 2, imageWidth, imageHeight))
    classNo = 0
    if keys[pygame.K_0]:
        imageWidth, imageHeight = INIT_WIDTH, INIT_HEIGHT
    if keys[pygame.K_1]:
        classNo = 1
        screen.blit(cauImage, (mouseX - imageWidth // 2, mouseY - imageHeight // 2))
    elif keys[pygame.K_2]:
        classNo = 2
        screen.blit(leftArrowImage, (mouseX - imageWidth // 2, mouseY - imageHeight // 2))
    elif keys[pygame.K_3]:
        classNo = 3
        screen.blit(rightArrowImage, (mouseX - imageWidth // 2, mouseY - imageHeight // 2))

    # 네모 박스 왼쪽 화살표 그리기
    
    infoText = f'x: {mouseX} y: {mouseY} width : {int(imageWidth)} height : {int(imageHeight)}'
    text = font.render(infoText, True, BLUE)
    screen.blit(text, (10, 10))

    timeText = f'time : {elapsed_time // 1000}s {elapsed_time % 1000} ms'
    text = font.render(timeText, True, YELLOW)
    screen.blit(text, (10, HEIGHT - 30))

    x, y, w, h = mouseX, HEIGHT - mouseY, imageWidth, imageHeight

    if (classNo == 0):
        w = 0

    ''' Start logic '''

    moveRight, moveUp, moveFront = 0, 0, 0
    if (yawTimer.hasTimeElapsed()):
        yawTimer.endTime = 0
        moveYaw = 0

    if (isLanding == False):
        if (moveYaw == 0):
            moveUp = isUpDownBiased(y) * subSpeed
            moveRight = isRightLeftBiased(x) * subSpeed
            moveFront = isFrontFar(w)
    else:
        moveFront = isFrontBackBiased(w) * subSpeed
        if moveFront == 0:
            print('Landing')
            break

    if (w > 450 and moveYaw == 0):
        switchDict.get(classNo, defaultCase)()

    vel = [moveRight, moveFront, moveUp, moveYaw]
    velText = f'move_right : {moveRight} move_front : {moveFront} move_up: {moveUp} yaw : {moveYaw}'
    text = font.render(velText, True, WHITE)
    screen.blit(text, (10, 40))

    targetText = f'classNo : {classNo} yawTimer : {yawTimer.endTime} isLanding : {isLanding}'
    text = font.render(targetText, True, CYAN)
    screen.blit(text, (10, 70))



    # 화면 업데이트
    pygame.display.flip()


