import pygame
import sys

pygame.init()

# 창 크기 및 색상 정의
window_width, window_height = 1600, 900
bg_color = (255, 255, 255)
runner_color = (255, 0, 0)

# 실행기 초기 위치 및 크기
runner_width, runner_height = 250, 700
runner_x = window_width - runner_width - 20
runner_y = (window_height - runner_height) // 2 + 20
runner_rect = pygame.Rect(runner_x, runner_y, runner_width, runner_height)

# 실행기 왼쪽 위쪽 끝 위치
runner_top_left = (runner_rect.left, runner_rect.top)

# 블록 초기 크기 및 간격
block_size = 50
block_spacing = 10
blocks = []

# Pygame 창 설정
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Arrow Key Blocks")

clock = pygame.time.Clock()

def create_block(color):
    global runner_top_left
    if not blocks or blocks[-1][0] + block_size + block_spacing < runner_top_left[0] - block_spacing:
        if not blocks:
            # 초기 블록 생성 위치
            new_block_x = runner_top_left[0] + block_spacing
            new_block_y = runner_top_left[1] + block_spacing
            blocks.append((new_block_x, new_block_y, color))
        else:
            # 이전 블록이 있는 경우, 현재 블록 위치 계산
            new_block_x = blocks[-1][0] + block_size + block_spacing
            new_block_y = blocks[-1][1]
            blocks.append((new_block_x, new_block_y, color))
    else:
        # 이전 블록이 있는 경우, 현재 블록 위치 계산
        new_block_x = runner_top_left[0] + block_spacing
        new_block_y = blocks[-1][1] - block_size - block_spacing
        blocks.append((new_block_x, new_block_y, color))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # 화살표 키 이벤트 처리
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                create_block((0, 0, 255))  # 파란색
            elif event.key == pygame.K_RIGHT:
                create_block((0, 255, 0))  # 초록색
            elif event.key == pygame.K_UP:
                create_block((0, 0, 0))  # 검정색
            elif event.key == pygame.K_DOWN:
                create_block((128, 0, 128))  # 보라색

    # 화면을 흰색으로 지우기
    screen.fill(bg_color)

    # 실행기 그리기
    pygame.draw.rect(screen, runner_color, runner_rect)

    # 블록 그리기
    for block in blocks:
        pygame.draw.rect(screen, block[2], (block[0], block[1], block_size, block_size))

    # 화면 업데이트
    pygame.display.flip()

    # 초당 프레임 수 설정
    clock.tick(60)
