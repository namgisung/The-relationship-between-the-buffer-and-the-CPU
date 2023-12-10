import pygame
import sys
import time

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

# 딜레이 시간 설정
delay_time = 0.2

# 마지막으로 실행한 시간
last_execution_time = time.time()

class DirectionStack:
    def __init__(self):
        self.stack = []

    def push(self, direction):
        self.stack.append(direction)

    def pop(self):
        if self.stack:
            return self.stack.pop()
        return None

    def peek(self):
        if self.stack:
            return self.stack[-1]
        return None

    def is_empty(self):
        return len(self.stack) == 0
    
    def pop_(self):
        if not self.is_empty():
            return self.stack.pop(0)  # 스택의 맨 앞에서 팝
        else:
            print("스택이 비어있습니다.")

direction_stack = DirectionStack()


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

def remove_last_block_with_direction():
    removed_direction = direction_stack.pop()
    if removed_direction:
        print(f"Removed direction: {removed_direction}")
        remove_last_block()

def remove_last_block():
    global blocks
    if blocks:
        blocks.pop()

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

def find_o_position_in_array():
    global extra_map
    for row, line in enumerate(extra_map):
        for col, char in enumerate(line):
            if char == 'O':
                return col, row
    return None  # 'O'를 찾지 못한 경우 None 반환

def find_stone_position_in_array():
    global extra_map
    for row, line in enumerate(extra_map):
        for col, char in enumerate(line):
            if char == '*':
                return col, row
    return None  # '*'를 찾지 못한 경우 None 반환

def is_position_valid(position):
    # position이 맵 범위 내에 있는지 확인
    if 0 <= position[0] < len(extra_map[0]) and 0 <= position[1] < len(extra_map):
        # 해당 위치에 벽이 있는지 확인
        return extra_map[position[1]][position[0]] != 'X'
    return False

def is_collision(player_position, stone_position):
    player_x, player_y = player_position
    stone_x, stone_y = stone_position

    # 플레이어와 돌의 충돌 감지
    if (
        player_x < stone_x + 2 and
        player_x + 1 > stone_x and
        player_y < stone_y + 2 and
        player_y + 1 > stone_y
    ):
        return True
    return False


def move_player_and_stone(player_position, stone_position, direction):
    global stone_position_array

    # 움직이려는 새로운 위치 계산
    new_player_position = (player_position[0], player_position[1])
    new_stone_position = (stone_position[0], stone_position[1])

    if direction == 'UP':
        new_player_position = (player_position[0], player_position[1] - 1)
        new_stone_position = (stone_position[0], stone_position[1] - 1)

    elif direction == 'DOWN':
        new_player_position = (player_position[0], player_position[1] + 1)
        new_stone_position = (stone_position[0], stone_position[1] + 1)

    elif direction == 'LEFT':
        new_player_position = (player_position[0] - 1, player_position[1])
        new_stone_position = (stone_position[0] - 1, stone_position[1])

    elif direction == 'RIGHT':
        new_player_position = (player_position[0] +1, player_position[1])
        new_stone_position = (stone_position[0] + 1, stone_position[1])

    # 새로운 위치에 벽이 있는지 확인
    if (
        stone_position_array[0]  <= new_player_position[0] <= stone_position_array[0] + 1 and
        stone_position_array[1] <= new_player_position[1] <= stone_position_array[1] + 1
    ):
        if is_position_valid(new_stone_position) and is_position_valid((new_stone_position[0]+1,new_stone_position[1])) and is_position_valid((new_stone_position[0]+1,new_stone_position[1]+1)) and is_position_valid((new_stone_position[0],new_stone_position[1]+1)):

            # 플레이어와 돌을 새로운 위치로 이동
            player_position = new_player_position
            stone_position = new_stone_position
            stone_position_array = new_stone_position
            print("충돌")

    elif is_position_valid(new_player_position):
        player_position = new_player_position
        

    else:
        # 벽이 있으면 이동 취소
        print("이동 취소")
        

    return player_position, stone_position

def draw_stone(stone_position):
    new_s_block_x = stone_position[0] * (extra_block_size + block_spacing) + block_spacing
    new_s_block_y = stone_position[1] * (extra_block_size + block_spacing) + block_spacing
    stone_s_position = (new_s_block_x, new_s_block_y)
    screen.blit(stone_image, stone_s_position)

    

direction_stack = DirectionStack()
current_direction = None
last_move_time = time.time()

# 추가된 블록을 위한 맵
extra_map = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X....X.....X...X.....X.--.X",
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

# O의 위치 찾기 (2차원 배열에서)
o_position_array = find_o_position_in_array()

if o_position_array is not None:
    print(f"2차원 배열에서 O의 위치: {o_position_array}")
    o_position = o_position_array

o_image = pygame.image.load("blocks/o.png")
o_rect = o_image.get_rect()

# -의 위치 찾기 (2차원 배열에서)
stone_position_array = find_stone_position_in_array()
if stone_position_array is not None:
    print(f"2차원 배열에서 -의 위치: {stone_position_array}")
    stone_position = stone_position_array

stone_image = pygame.image.load("blocks/stone.png")
stone_rect = stone_image.get_rect()

clock = pygame.time.Clock()
frame_rate = 10  # 초당 프레임 수 설정


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # 화살표 키 이벤트 처리
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction_stack.push('LEFT')
                create_block("blocks/left.png")
            elif event.key == pygame.K_RIGHT:
                direction_stack.push('RIGHT')
                new_position = (o_position_array[0] + 1, o_position_array[1])
                create_block("blocks/right.png")
            elif event.key == pygame.K_UP:
                direction_stack.push('UP')
                create_block("blocks/up.png")
            elif event.key == pygame.K_DOWN:
                direction_stack.push('DOWN')
                create_block("blocks/down.png")
                    
            elif event.key == pygame.K_BACKSPACE:
                remove_last_block_with_direction()
                print(len(blocks))
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_RETURN:
                while not direction_stack.is_empty():
                    current_direction = direction_stack.pop_()
                    print(f"Executing direction: {current_direction}")
                    o_position_array, stone_position_array = move_player_and_stone(o_position_array, stone_position_array, current_direction)
                    pygame.display.flip()
                    time.sleep(delay_time)
                print("Stack is empty.")
    
    

    # 화면을 흰색으로 지우기
    screen.fill(bg_color)

    # 실행기 그리기
    pygame.draw.rect(screen, runner_color, runner_rect)

    # 블록 그리기
    for block in blocks:
        screen.blit(block[1], block[0])

    # 추가된 블록 그리기
    draw_extra_blocks()

    # O 이미지 그리기
    new_block_x = o_position_array[0] * (extra_block_size + block_spacing) + block_spacing
    new_block_y = o_position_array[1] * (extra_block_size + block_spacing) + block_spacing
    o_position = (new_block_x, new_block_y)
    screen.blit(o_image, o_position)

    # 돌 이미지 그리기
    draw_stone(stone_position_array)


    # 화면 업데이트
    pygame.display.flip()

    # 초당 프레임 수 설정
    clock.tick(60)
