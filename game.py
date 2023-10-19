import pygame

# 초기화
pygame.init()

# 화면 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("블록 코딩 게임")

# 색깔 정의
white = (255, 255, 255)
red = (255, 0, 0)

# 블록 정보
blocks = [
    {"color": red, "shape": "circle", "x": 100, "y": 100},
    {"color": red, "shape": "rectangle", "x": 200, "y": 200},
    {"color": red, "shape": "triangle", "x": 300, "y": 300},
]

# 블록 드래그 상태 변수
dragging_block = None

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for block in blocks:
                # 블록을 클릭하여 드래그 상태로 전환
                if pygame.Rect(block["x"], block["y"], 50, 50).collidepoint(event.pos):
                    dragging_block = block
        elif event.type == pygame.MOUSEBUTTONUP:
            # 드래그 상태에서 블록을 놓음
            dragging_block = None

    # 블록 드래그 처리
    if dragging_block:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dragging_block["x"] = mouse_x
        dragging_block["y"] = mouse_y

    # 화면 지우기
    screen.fill(white)

    # 블록 그리기
    for block in blocks:
        pygame.draw.rect(screen, block["color"], (block["x"], block["y"], 50, 50))

    # 화면 업데이트
    pygame.display.update()

# 게임 종료
pygame.quit()
