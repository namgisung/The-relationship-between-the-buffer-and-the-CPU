import pygame
import sys
import os

# 현재 스크립트 파일의 디렉터리를 얻습니다.
script_directory = os.path.dirname(__file__)

# 'blocks' 디렉터리를 기준으로 상대 경로를 설정합니다.
block_folder = os.path.join(script_directory, 'blocks')


# 초기화
pygame.init()

# 화면 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("블록 코딩 게임")

# 색깔 정의
white = (255, 255, 255)

# 블록 폴더 경로
block_folder = "blocks"

# 블록 이미지 로드
block_images = {}
for filename in os.listdir(block_folder):
    if filename.endswith(".png"):
        block_name = os.path.splitext(filename)[0]
        block_images[block_name] = pygame.image.load(os.path.join(block_folder, filename))

# 실행 창 설정
terminal_text = ""
font = pygame.font.Font(None, 36)

# 실행 블록 실행 함수
def run_code(code):
    try:
        exec(code)
    except Exception as e:
        print(f"Error: {e}")

# 게임 루프
running = True
code = ""

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if 50 <= event.pos[0] <= 150 and 50 <= event.pos[1] <= 100:
                # 실행 블록 클릭
                run_code(code)

    # 화면 지우기
    screen.fill(white)

    # 블록 배치
    y = 200
    for block_name, block_image in block_images.items():
        screen.blit(block_image, (50, y))
        y += 100

    # 실행 창 그리기
    pygame.draw.rect(screen, (200, 200, 200), (250, 50, 500, 100))
    text_surface = font.render(terminal_text, True, (0, 0, 0))
    screen.blit(text_surface, (260, 60))

    # 화면 업데이트
    pygame.display.update()

# 게임 종료
pygame.quit()
sys.exit()