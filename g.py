import pygame
import sys

# Pygame 초기화
pygame.init()

# 화면 설정
width, height = 800, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Block Organizer")

# 색상 정의
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# 블록 클래스
class Block:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.width = 50
        self.height = 50
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.dragging = False
        self.fixed = False  # 고정 여부

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self):
        if self.dragging and not self.fixed:
            self.x, self.y = pygame.mouse.get_pos()
            self.x -= self.width / 2
            self.y -= self.height / 2
            self.rect.x = self.x
            self.rect.y = self.y

# 실행기 클래스
class Executor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = red  # 배경을 빨간색으로 변경
        self.width = 150
        self.height = 300
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.holding_block = None

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.holding_block:
            self.holding_block.x = self.x + 20
            self.holding_block.y = self.y + 20
            self.holding_block.rect.x = self.holding_block.x
            self.holding_block.rect.y = self.holding_block.y
            self.holding_block.draw()

# 블록들과 실행기 생성
blocks = [
    Block(50, 50, black), Block(150, 50, black), Block(250, 50, black),
    Block(50, 150, black), Block(150, 150, black), Block(250, 150, black)
]
executors = [
    Executor(500, 50), Executor(600, 50), Executor(700, 50),
    Executor(500, 150), Executor(600, 150), Executor(700, 150)
]

# 게임 루프
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for block in blocks:
                    if block.rect.collidepoint(event.pos) and not block.fixed:
                        block.dragging = True
                for executor in executors:
                    if executor.holding_block:
                        if executor.holding_block.rect.collidepoint(event.pos):
                            executor.holding_block.fixed = False
                            for block in blocks:
                                if abs(block.x - executor.x) <= 30 and abs(block.y - executor.y) <= 30:
                                    executor.holding_block = block
                                    block.fixed = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for block in blocks:
                    block.dragging = False
                for executor in executors:
                    if executor.rect.collidepoint(event.pos) and executor.holding_block in blocks and not executor.holding_block.fixed:
                        executor.holding_block.fixed = True

    screen.fill(white)

    for executor in executors:
        executor.draw()

    for block in blocks:
        block.update()
        block.draw()

    pygame.display.flip()

# 게임 종료
pygame.quit()
sys.exit()
