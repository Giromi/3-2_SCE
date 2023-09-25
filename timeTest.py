import time

class TimeChecker:
    def __init__(self):
        self.endTime = 0

    def setEndTimeInMs(self, ms):
        current_time_ms = time.time() * 1000  # 현재 시간을 밀리초(ms)로 변환
        self.endTime = current_time_ms + ms
        print("current_time_ms : ", current_time_ms, "endTime : ", self.endTime)

    def hasTimeElapsed(self):
        current_time_ms = time.time() * 1000  # 현재 시간을 밀리초(ms)로 변환
        print("current_time_ms : ", current_time_ms)
        return current_time_ms > self.endTime

# 사용 예시:
checker = TimeChecker()
checker.setEndTimeInMs(2100)  # 2초 뒤의 시간을 endTime으로 설정
timePrev = time.time()

# 2초 동안 대기
time.sleep(2)

# 시간이 경과했는지 확인
if checker.hasTimeElapsed():
    print("Time has elapsed!")
else:
    print("Time has not yet elapsed.")

print("End time : ", time.time() - timePrev, 's')


