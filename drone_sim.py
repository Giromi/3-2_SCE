import pygame
import random
import math

# 초기화
pygame.init()

# 상수 설정
WIDTH, HEIGHT = 600, 1000
CELL_SIZE = 200  # 미로 셀 크기 증가
BACKGROUND_COLOR = (255, 255, 255)
WALL_COLOR = (0, 0, 0)
VISITED_COLOR = (255, 255, 255)
DRONE_COLOR = (0, 128, 255)
DRONE_RADIUS = 15
DRONE_SPEED = 5
DRONE_ROTATE_SPEED = 2
ARROW_LENGTH = 30
ARROW_WIDTH = 7
ARROW_OFFSET = 10  # 화살표의 시작점을 벽에서 얼마나 떨어지게 할지 결정
ARROW_HEAD_LENGTH = 10
ARROW_HEAD_WIDTH = 5


cols, rows = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

def dfs(cell, target, visited=[]):
    if cell == target:
        return [cell]

    visited.append(cell)
    
    neighbors = []

    top_idx = index(cell.x, cell.y - 1)
    right_idx = index(cell.x + 1, cell.y)
    bottom_idx = index(cell.x, cell.y + 1)
    left_idx = index(cell.x - 1, cell.y)

    if top_idx is not None and not grid[top_idx].visited and grid[top_idx] not in visited:
        neighbors.append(grid[top_idx])
    if right_idx is not None and not grid[right_idx].visited and grid[right_idx] not in visited:
        neighbors.append(grid[right_idx])
    if bottom_idx is not None and not grid[bottom_idx].visited and grid[bottom_idx] not in visited:
        neighbors.append(grid[bottom_idx])
    if left_idx is not None and not grid[left_idx].visited and grid[left_idx] not in visited:
        neighbors.append(grid[left_idx])

    for neighbor in neighbors:
        path = dfs(neighbor, target, visited)
        if path:
            return [cell] + path
    return None

def identify_corners(path):
    corners = []
    for i in range(1, len(path) - 1):
        prev_cell = path[i - 1]
        current_cell = path[i]
        next_cell = path[i + 1]

        prev_x, prev_y = prev_cell.x, prev_cell.y
        current_x, current_y = current_cell.x, current_cell.y
        next_x, next_y = next_cell.x, next_cell.y

        if (prev_x - current_x, prev_y - current_y) != (next_x - current_x, next_y - current_y):
            corners.append(current_cell)

    return corners

# 경로 찾기

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    def show(self, screen):
        x = self.x * CELL_SIZE
        y = self.y * CELL_SIZE

        if self.visited:
            pygame.draw.rect(screen, VISITED_COLOR, (x, y, CELL_SIZE, CELL_SIZE))

        # Always draw the top and left walls of a cell
        if self.walls['top']:
            pygame.draw.line(screen, WALL_COLOR, (x, y), (x + CELL_SIZE, y))
        if self.walls['left']:
            pygame.draw.line(screen, WALL_COLOR, (x, y), (x, y + CELL_SIZE))
        
        # For the last column, draw the right wall
        if self.x == cols - 1 and self.walls['right']:
            pygame.draw.line(screen, WALL_COLOR, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE))
        # For the last row, draw the bottom wall
        if self.y == rows - 1 and self.walls['bottom']:
            pygame.draw.line(screen, WALL_COLOR, (x + CELL_SIZE, y + CELL_SIZE), (x, y + CELL_SIZE))



    def draw_arrows(self, screen):
        if self not in path:  # 추가된 부분
            return
    # ... (나머지는 동일)


def draw_path_arrows(screen, path):
    arrow_length = ARROW_LENGTH
    arrow_angle = 45

    for i in range(len(path) - 1):
        cell = path[i]
        next_cell = path[i + 1]
        x1, y1 = cell.x * CELL_SIZE + CELL_SIZE // 2, cell.y * CELL_SIZE + CELL_SIZE // 2
        x2, y2 = next_cell.x * CELL_SIZE + CELL_SIZE // 2, next_cell.y * CELL_SIZE + CELL_SIZE // 2
        dx, dy = x2 - x1, y2 - y1

        if dx > 0:  # 다음 셀이 현재 셀의 오른쪽에 있음
            arrow_pos = (x1 + ARROW_OFFSET, y1)
            arrow_direction = (1, 0)
        elif dx < 0:  # 다음 셀이 현재 셀의 왼쪽에 있음
            arrow_pos = (x1 - ARROW_OFFSET, y1)
            arrow_direction = (-1, 0)
        elif dy > 0:  # 다음 셀이 현재 셀의 아래에 있음
            arrow_pos = (x1, y1 + ARROW_OFFSET)
            arrow_direction = (0, 1)
        else:  # 다음 셀이 현재 셀의 위에 있음
            arrow_pos = (x1, y1 - ARROW_OFFSET)
            arrow_direction = (0, -1)

        pygame.draw.line(screen, WALL_COLOR, arrow_pos, (arrow_pos[0] + arrow_direction[0] * arrow_length, arrow_pos[1] + arrow_direction[1] * arrow_length), ARROW_WIDTH)
        pygame.draw.polygon(screen, WALL_COLOR, [
            (arrow_pos[0] + arrow_direction[0] * arrow_length, arrow_pos[1] + arrow_direction[1] * arrow_length),
            (arrow_pos[0] + arrow_direction[0] * arrow_length - arrow_angle, arrow_pos[1] + arrow_direction[1] * arrow_length - ARROW_HEAD_WIDTH),
            (arrow_pos[0] + arrow_direction[0] * arrow_length - arrow_angle, arrow_pos[1] + arrow_direction[1] * arrow_length + ARROW_HEAD_WIDTH)
        ])



def index(i, j):
    if i < 0 or j < 0 or i >= cols or j >= rows:
        return None
    return i + j * cols

def remove_walls(a, b):
    x = a.x - b.x
    if x == 1:
        a.walls['left'] = False
        b.walls['right'] = False
    elif x == -1:
        a.walls['right'] = False
        b.walls['left'] = False

    y = a.y - b.y
    if y == 1:
        a.walls['top'] = False
        b.walls['bottom'] = False
    elif y == -1:
        a.walls['bottom'] = False
        b.walls['top'] = False

def generate_maze(grid):
    stack = []
    current = grid[0]

    while stack or current:
        current.visited = True
        next_cell = None

        neighbors = []

        top_idx = index(current.x, current.y - 1)
        right_idx = index(current.x + 1, current.y)
        bottom_idx = index(current.x, current.y + 1)
        left_idx = index(current.x - 1, current.y)

        if top_idx is not None and not grid[top_idx].visited:
            neighbors.append(grid[top_idx])
        if right_idx is not None and not grid[right_idx].visited:
            neighbors.append(grid[right_idx])
        if bottom_idx is not None and not grid[bottom_idx].visited:
            neighbors.append(grid[bottom_idx])
        if left_idx is not None and not grid[left_idx].visited:
            neighbors.append(grid[left_idx])

        if neighbors:
            next_cell = random.choice(neighbors)
            remove_walls(current, next_cell)
            stack.append(current)
            current = next_cell
        else:
            if stack:
                current = stack.pop()
            else:
                break

grid = [Cell(i, j) for j in range(rows) for i in range(cols)]
# 출발지점과 도착지점 지정
start_cell = grid[0]
end_cell = grid[-1]
START_COLOR = (0, 255, 0)  # 녹색으로 출발지점 표시
END_COLOR = (255, 0, 0)    # 빨간색으로 도착지점 표시
POINT_RADIUS = 25  # 출발 및 도착 지점의 원의 반지름



generate_maze(grid)
path = dfs(start_cell, end_cell) or []


# 드론 위치 및 화면 설정
drone_pos = [CELL_SIZE / 2, HEIGHT - CELL_SIZE / 2]
target_pos = drone_pos.copy()
direction = [0, -1]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Drone Maze Simulation')
orientation = 0 
running = True
while running:
    screen.fill(BACKGROUND_COLOR)

    # for cell in grid:
    #     cell.show(screen)
    for cell in grid:
        cell.show(screen)
        cell.draw_arrows(screen)
    # 출발 및 도착 지점 그리기
    pygame.draw.circle(screen, START_COLOR, [CELL_SIZE // 2, HEIGHT - CELL_SIZE // 2], POINT_RADIUS)  # 시작 지점
    pygame.draw.circle(screen, END_COLOR, [WIDTH - CELL_SIZE // 2, CELL_SIZE // 2], POINT_RADIUS)  # 도착 지점

    draw_path_arrows(screen, path)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            target_pos = list(event.pos)
            direction = [(target_pos[0] - drone_pos[0]) / max(abs(target_pos[0] - drone_pos[0]), 1),
                         (target_pos[1] - drone_pos[1]) / max(abs(target_pos[1] - drone_pos[1]), 1)]

    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        running = False
    if keys[pygame.K_LEFT]:
        # Calculate the movement vector based on orientation
        radians = math.radians(orientation - 90)  # Rotate -90 degrees for left movement
        dx = math.sin(radians) * DRONE_SPEED
        dy = -math.cos(radians) * DRONE_SPEED
        # Update the drone's position
        target_pos[0] += dx
        target_pos[1] += dy
    if keys[pygame.K_RIGHT]:
        # Calculate the movement vector based on orientation
        radians = math.radians(orientation + 90)  # Rotate 90 degrees for right movement
        dx = math.sin(radians) * DRONE_SPEED
        dy = -math.cos(radians) * DRONE_SPEED
        # Update the drone's position
        target_pos[0] += dx
        target_pos[1] += dy
    if keys[pygame.K_UP]:
        # Calculate the movement vector based on orientation
        radians = math.radians(orientation)
        dx = math.sin(radians) * DRONE_SPEED
        dy = -math.cos(radians) * DRONE_SPEED
        # Update the drone's position
        target_pos[0] += dx
        target_pos[1] += dy
        print(target_pos)
    if keys[pygame.K_DOWN]:
        # Calculate the movement vector based on orientation
        radians = math.radians(orientation)
        dx = -math.sin(radians) * DRONE_SPEED
        dy = math.cos(radians) * DRONE_SPEED
        # Update the drone's position
        target_pos[0] += dx
        target_pos[1] += dy
    if keys[pygame.K_COMMA]:
        orientation -= DRONE_ROTATE_SPEED
    if keys[pygame.K_PERIOD]:
        orientation += DRONE_ROTATE_SPEED
    if keys[pygame.K_1]:
        direction = [1, 0]
    if keys[pygame.K_2]:
        direction = [-1, 0]
    if keys[pygame.K_3]:
        direction = [0, 1]
    if keys[pygame.K_4]:
        direction = [0, -1]


    # 드론 움직임
    dx = target_pos[0] - drone_pos[0]
    dy = target_pos[1] - drone_pos[1]

    if abs(dx) > DRONE_SPEED:
        drone_pos[0] += DRONE_SPEED if dx > 0 else -DRONE_SPEED

    if abs(dy) > DRONE_SPEED:
        drone_pos[1] += DRONE_SPEED if dy > 0 else -DRONE_SPEED

    pygame.draw.circle(screen, DRONE_COLOR, drone_pos, DRONE_RADIUS)

    # 드론 앞 방향을 표시하는 삼각형
    triangle_offset = 20
    angle_rad = math.radians(orientation)
    cos_angle = math.cos(angle_rad)
    sin_angle = math.sin(angle_rad)
    # 삼각형의 각 꼭지점을 드론의 방향에 따라 회전하여 계산

# 삼각형의 각 꼭지점을 드론의 방향에 따라 회전하여 계산
    triangle = [
            (drone_pos[0] + direction[0] * triangle_offset, drone_pos[1] + direction[1] * triangle_offset),
            (drone_pos[0] + direction[1] * triangle_offset/2, drone_pos[1] - direction[0] * triangle_offset/2),
            (drone_pos[0] - direction[1] * triangle_offset/2, drone_pos[1] + direction[0] * triangle_offset/2)
    ]
    pygame.draw.polygon(screen, WALL_COLOR, triangle)

    # 드론의 회전을 적용하여 드론을 그립니다.
    rotated_drone = pygame.transform.rotate(pygame.Surface((2*DRONE_RADIUS, 2*DRONE_RADIUS), pygame.SRCALPHA), math.degrees(orientation))
    rotated_drone_rect = rotated_drone.get_rect(center=drone_pos)
    screen.blit(rotated_drone, rotated_drone_rect)
    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()

