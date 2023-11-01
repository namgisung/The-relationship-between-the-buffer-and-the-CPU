import pygame
import sys

# Pygame 초기화
pygame.init()

# 화면 설정
width, height = 1600, 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Block Organizer")

# 색상 정의
white = (255, 255, 255)
red = (255, 0, 0)

# 블록 클래스
class Block:
    def __init__(self, x, y, image_path, index):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.dragging = False
        self.offset_x = 0  # 마우스와 이미지 중심의 x 좌표 차이
        self.offset_y = 0  # 마우스와 이미지 중심의 y 좌표 차이
        self.index = index  # 블록의 인덱스
        self.fixed = False

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

    def update(self):
        if self.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.rect.center = (mouse_x + self.offset_x, mouse_y + self.offset_y)

    def start_drag(self, mouse_x, mouse_y):
        if self.rect.collidepoint(mouse_x, mouse_y):
            self.dragging = True
            self.offset_x = self.rect.centerx - mouse_x
            self.offset_y = self.rect.centery - mouse_y
    
    def stop_drag(self):
        self.dragging = False

# 실행기 클래스
class Executor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = red
        self.width = 200
        self.height = 600
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.dragging = False

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

# 블록들과 실행기 생성
blocks = [Block(50, 50, "blocks/jump.png", 0), Block(150, 50, "blocks/start.png", 1)]
executor = Executor(1360, 150)

# 게임 루프
running = True
fixed_block = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if fixed_block is None:
                    for block in blocks:
                        if block.rect.collidepoint(event.pos):
                            block.start_drag(*pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for block in blocks:
                    if block.rect.colliderect(executor.rect) and block.dragging:
                        block.rect.topleft = (executor.x + 20, executor.y + 20)
                        block.fixed = True
                        fixed_block = block
                    block.stop_drag()
                if executor.dragging:
                    executor.dragging = False

    screen.fill(white)

    executor.draw()
    
    for block in blocks:
        if not block.fixed:
            block.update()
        block.draw()

    pygame.display.flip()

# 게임 종료
pygame.quit()
sys.exit()
