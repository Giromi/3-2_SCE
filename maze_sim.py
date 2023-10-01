import pygame
import random

# 초기화
pygame.init()

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
BACKGROUND_COLOR = (255, 255, 255)
WALL_COLOR = (0, 0, 0)
VISITED_COLOR = (255, 255, 255)

cols, rows = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

# Cell 클래스
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

        if self.walls['top']:
            pygame.draw.line(screen, WALL_COLOR, (x, y), (x + CELL_SIZE, y))
        if self.walls['right']:
            pygame.draw.line(screen, WALL_COLOR, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE))
        if self.walls['bottom']:
            pygame.draw.line(screen, WALL_COLOR, (x + CELL_SIZE, y + CELL_SIZE), (x, y + CELL_SIZE))
        if self.walls['left']:
            pygame.draw.line(screen, WALL_COLOR, (x, y + CELL_SIZE), (x, y))

def index(i, j):
    if i < 0 or j < 0 or i > cols - 1 or j > rows - 1:
        return None
    return i + j * cols

def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False

    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False

grid = []
for j in range(rows):
    for i in range(cols):
        cell = Cell(i, j)
        grid.append(cell)

current = grid[0]

stack = []

# 화면 설정
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Maze Generation')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND_COLOR)

    for cell in grid:
        cell.show(screen)

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

    if len(neighbors) > 0:
        next_cell = random.choice(neighbors)
        stack.append(current)

        remove_walls(current, next_cell)
        current = next_cell
    elif len(stack) > 0:
        current = stack.pop()

    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()

