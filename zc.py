import pygame
import sys

pygame.init()

# 창 크기 및 색상 정의
window_width, window_height = 1920, 1080
bg_color = (255, 255, 255)
runner_color = (255, 0, 0)

# 실행기 초기 위치 및 크기
runner_width, runner_height = 350, 900
runner_x = window_width - runner_width - 20
runner_y = (window_height - runner_height) // 2 + 20
runner_rect = pygame.Rect(runner_x, runner_y, runner_width, runner_height)

# 실행기 왼쪽 위쪽 끝 위치
runner_top_left = (runner_rect.left, runner_rect.top)

# 블록 초기 크기 및 간격
block_size = 40
block_spacing = 9
blocks = []

# 최대 블록 수
max_blocks = 140

# 추가된 블록 초기 크기 및 간격
extra_block_size = 30
extra_block_spacing = 0  # 사이 간격

# 추가된 블록 리스트
extra_blocks = []

# Pygame 창 설정
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Arrow Key Blocks")

clock = pygame.time.Clock()

def create_block(image_path):
    global runner_top_left, blocks
    if len(blocks) < max_blocks:
        image = pygame.image.load(image_path)
        rect = image.get_rect()
        new_block_x = runner_top_left[0] + (len(blocks) % 7) * (block_size + block_spacing) + block_spacing
        new_block_y = runner_top_left[1] + (len(blocks) // 7) * (block_size + block_spacing) + block_spacing
        rect.topleft = (new_block_x, new_block_y)
        blocks.append((rect.topleft, image))

def create_block_map(image_path, block_list, position):
    global runner_top_left, blocks
    image = pygame.image.load(image_path)
    rect = image.get_rect()
    new_block_x = position[0] * (extra_block_size + block_spacing) + block_spacing
    new_block_y = position[1] * (extra_block_size + block_spacing) + block_spacing
    rect.topleft = (new_block_x, new_block_y)
    block_list.append((rect, image))

def remove_last_block(block_list):
    global blocks
    if block_list:
        block_list.pop()

def initialize_extra_blocks():
    global extra_blocks
    for row, line in enumerate(extra_map):
        for col, char in enumerate(line):
            if char == 'X':
                create_block_map("blocks/extra_block.png", extra_blocks, (col, row))

def draw_extra_blocks():
    global extra_blocks
    for block in extra_blocks:
        screen.blit(block[1], block[0])

# 추가된 블록을 위한 맵
extra_map = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X....X.....X...X.....X.--XX",
    "X.**.....X.X.X...X.....--.X",
    "X.**....X..X..XXX.X.......X",
    "XXXXX...X.X..X....X..X.XX.X",
    "X....X..X..X...XX.X..X....X",
    "X.X.X...X...XXX...X..XXXXXX",
    "X........XX.....XXX.......X",
    "XX.......X.XXX.X..........X",
    "X....XXXX.....X..X...X...XX",
    "X...X.....XXX..X.....XX...X",
    "XX...X...X...X..X.XXXX...XX",
    "X..........X..X..X........X",
    "X.......XXX.X.XX.X........X",
    "XXXXXX..X.....XX..X...X.X.X",
    "X....X..X.XXXX.X..X..XX...X",
    "X........XXXXX....X.......X",
    "XX.......X...XXXXX........X",
    "X....XX.X..X.....X.X.X...XX",
    "X....X.X..X.XXXX.X.X.XX...X",
    "X...X...X........X....X...X",
    "XX.......X.......XXXXX....X",
    "X...........X.X..........XX",
    "X............X............X",
    "X..X.........X........X..OX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

# 초기화
initialize_extra_blocks()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # 화살표 키 이벤트 처리
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                create_block("blocks/left.png")  # 파란색
            elif event.key == pygame.K_RIGHT:
                create_block("blocks/right.png")  # 초록색
            elif event.key == pygame.K_UP:
                create_block("blocks/up.png")  # 검정색
            elif event.key == pygame.K_DOWN:
                create_block("blocks/down.png")  # 보라색
            elif event.key == pygame.K_BACKSPACE:
                remove_last_block(extra_blocks)
                print(len(blocks))
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # 화면을 흰색으로 지우기
    screen.fill(bg_color)

    # 실행기 그리기
    pygame.draw.rect(screen, runner_color, runner_rect)

    # 블록 그리기
    for block in blocks:
        screen.blit(block[1], block[0])

    # 추가된 블록 그리기
    draw_extra_blocks()

    # 화면 업데이트
    pygame.display.flip()

    # 초당 프레임 수 설정
    clock.tick(60)
