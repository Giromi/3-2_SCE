
RIGHTBIAS = 100
LEFTBIAS = -100

UPBIAS = 100
DOWNBIAS = -100

FRONTBIAS = 300
BACKBIAS = 600

FRONTFAR = 400 # 50m 보다 멀리 있는 경우

def isRightLeftBiased():
    return 1 if y > RIGHTBIAS else (-1 if y < LEFTBIAS else 0)

def isUpDownBiased():
    return 1 if x > UPBIAS else (-1 if x < DOWNBIAS else 0)

def isFrontBackBiased():
    return 1 if w < FRONTBIAS else (-1 if w > BACKBIAS else 0)

def isFrontFar():
    return 1 if w < FRONTFAR else 0 # mainPath에서 뒤로 갈 필요 없음


def test_isRightLeftBiased():
    global y
    y = 150
    assert isRightLeftBiased() == 1, f"Expected 1, but got {isRightLeftBiased()}"

    y = 50
    assert isRightLeftBiased() == 0, f"Expected 0, but got {isRightLeftBiased()}"

    y = -150
    assert isRightLeftBiased() == -1, f"Expected -1, but got {isRightLeftBiased()}"

    print("isRightLeftBiased() passed!")

def test_isUpDownBiased():
    global x
    x = 150
    assert isUpDownBiased() == 1, f"Expected 1, but got {isUpDownBiased()}"

    x = 50
    assert isUpDownBiased() == 0, f"Expected 0, but got {isUpDownBiased()}"

    x = -150
    assert isUpDownBiased() == -1, f"Expected -1, but got {isUpDownBiased()}"

    print("isUpDownBiased() passed!")

def test_isFrontBackBiased():
    global w
    w = 150
    assert isFrontBackBiased() == 1, f"Expected 1, but got {isFrontBackBiased()}"

    w = 500 
    assert isFrontBackBiased() == 0, f"Expected 0, but got {isFrontBackBiased()}"

    w = 700 
    assert isFrontBackBiased() == -1, f"Expected -1, but got {isFrontBackBiased()}"

    print("isFrontBackBiased() passed!")

def test_isFrontFar():
    global w
    w = 350
    assert isFrontFar() == 1, f"Expected 1, but got {isFrontFar()}"

    w = 500
    assert isFrontFar() == 0, f"Expected 0, but got {isFrontFar()}"

    print("isFrontFar() passed!")

# Run tests
test_isRightLeftBiased()
test_isUpDownBiased()
test_isFrontBackBiased()
test_isFrontFar()

