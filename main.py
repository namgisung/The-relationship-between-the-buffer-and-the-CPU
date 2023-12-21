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
extra_block_size = 50
extra_block_spacing = 5

# 딜레이 시간 설정
delay_time = 0.05  

bgsound = pygame.mixer.Sound("blocks/pop.mp3")
bgsound.set_volume(0.7)

# 마지막으로 실행한 시간
last_execution_time = time.time()

image_bg = pygame.image.load("blocks/background.png")

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
            remove_first_block()
            return self.stack.pop(0)  # 스택의 맨 앞에서 팝
        else:
            print("스택이 비어있습니다.")

    def clear(self):
        self.stack = []

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
    new_block_x = position[0] * (extra_block_size + extra_block_spacing) + extra_block_spacing
    new_block_y = position[1] * (extra_block_size + extra_block_spacing) + extra_block_spacing
    rect.topleft = (new_block_x, new_block_y)
    block_list.append((rect, image))

def create_block_map_floor(image_path, block_list, position):
    global runner_top_left, blocks
    image = pygame.image.load(image_path)
    rect = image.get_rect()
    new_block_x = position[0] * (extra_block_size + extra_block_spacing) + (extra_block_spacing/2)
    new_block_y = position[1] * (extra_block_size + extra_block_spacing) + (extra_block_spacing/2)
    rect.topleft = (new_block_x, new_block_y)
    block_list.append((rect, image))


def create_block_map_tree(image_path, block_list, position):
    global runner_top_left, blocks
    image = pygame.image.load(image_path)
    rect = image.get_rect()
    new_block_x = position[0] * (extra_block_size + extra_block_spacing) + extra_block_spacing + 9
    new_block_y = position[1] * (extra_block_size + extra_block_spacing) + extra_block_spacing
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

def remove_first_block():
    global blocks
    if blocks:
        blocks.pop(0)

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

def find_stop_position_in_array():
    global extra_map
    for row, line in enumerate(extra_map):
        for col, char in enumerate(line):
            if char == '-':
                return col, row
    return None  # '*'를 찾지 못한 경우 None 반환

def is_position_valid(position):
    # position이 맵 범위 내에 있는지 확인
    if 0 <= position[0] < len(extra_map[0]) and 0 <= position[1] < len(extra_map):
        # 해당 위치에 벽이 있는지 확인
        return extra_map[position[1]][position[0]] != 'X' and extra_map[position[1]][position[0]] != 'F' and extra_map[position[1]][position[0]] != '<'
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
    new_s_block_x = stone_position[0] * (extra_block_size + extra_block_spacing) + extra_block_spacing
    new_s_block_y = stone_position[1] * (extra_block_size + extra_block_spacing) + extra_block_spacing
    stone_s_position = (new_s_block_x, new_s_block_y)
    screen.blit(stone_image, stone_s_position)

def stop_stone(stone_position_array,stop_position):
    if (
        stone_position_array[0]  == stop_position[0]  and
        stone_position_array[1] == stop_position[1] and
        stone_position_array[0] +1 == stop_position[0] +1 and
        stone_position_array[1] +1 == stop_position[1] + 1
        ):
        return True

# 스테이지 전환 함수
def switch_stage():
    global current_stage_index
    direction_stack.clear()
    while len(blocks) != 0:
        remove_last_block() 
    current_stage_index = (current_stage_index + 1) % len(stages)
    initialize_extra_blocks()

current_direction = None
last_move_time = time.time()


# 현재 스테이지 인덱스
current_stage_index = 0

# 여러 스테이지의 맵 데이터
stages = [
    [
    "..................",
    "..................",
    "..................",
    "...........XXXXXXX",
    "...........X,,,,,X",
    "...........X,**,XX",
    "...........X,**,,X",
    "...........X,,,O,X",
    "...........X,,,--X",
    "...........X,X,--X",
    "...........XXXXXXX"
    ],
    [
    "..................",
    "..................",
    "..................",
    "..........XXXXXXXX",
    "..........X,,,,,,X",
    "..........X,,**,,X",
    "..........X,,**,,X",
    "..........X,,,,OXX",
    "..........X,,,F--X",
    "..........XX,,,--X",
    "..........X,,,,,,X",
    "..........X,,,,<,X",
    "..........X,,,,,,X",
    "..........XXXXXXXX"        
    ],
    [
    "...................",
    "...................",
    "...................",
    "........XXXXXXXXXXX",
    "........X,,,,,,,,,X",
    "........X,,,,,,**,X",
    "........X,,,,,,**,X",
    "........X,,,XXXXXXX",
    "........X,,,,,,,,<X",
    "........X,,,,O,,,,X",
    "........X,,,,,,,,,X",
    "........XXXXXXX,,,X",
    "........X--,,,,,,,X",
    "........X--,,,,,,FX",
    "........XXXXXXXXXXX"   
    ],
    [
    "...................",
    "...................",
    "...................",
    ".........XXXXXXXXXX",
    ".........X,,XFX,,,X",
    ".........X,,,,,,,,X",
    ".........X,X<,O,,,X",
    ".........X,,X,,,,,X",
    ".........X,**,,X--X",
    ".........X,**,,X--X",
    ".........X,,,,,,,,X",
    ".........XXXXXXXXXX"
    ],
    [
    "......X...X..XX.XXX.X",
    "......XXXX,XX,,X,,,X.",
    "......X,--,,,**,,,,,X",
    "......X,--,,O**,,,,,X",
    "......X,XXX,XX,XX,,,X",
    ".......XF,,X,,X<,,,X.",
    ".......X,,,,,,,X,,,X.",
    "......X,,,,,,,,,X,,XX",
    "......X,,,X,X,,,X,,X.",
    "......X,,,,X,,,XF,,X.",
    "......XX,,,X,,,,X,,X.",
    "......X,,,X,,,,,X,,,X",
    ".......X,,X,<,,X,,,X.",
    "......X,,,X,,,X,,,,X.",
    "......X,,,XXXX,XX,,,X",
    "......X,,,,,,,,,,,,,X",
    ".......X,,,,,,,,,,,X.",
    ".......X,,,X,X<X,,XX.",
    "......X.XXX.X.X.XX..X"
    ],
    [
    "...................",
    "...................",
    "...................",
    "........XXXXXXXXXXX",
    "........X,,,,,X,,X.",
    "........XX**,,,,,X.",
    "........XX**,,,,,X.",
    "........X,,,,X,,,,X",
    "........X,,,XFX,,,X",
    "........X,,X,,,,,XX",
    "........X,,,,,,,,OX",
    "........X,,,,,,,,,X",
    "........X,,,X<XXXX.",
    "........XX,,,X.....",
    "........X--,,X.....",
    "........X--,,X.....",
    "........XXXXXX....."
    ],
    [
    "......................",
    "......................",
    "......................",
    "......X.XXX...XXXX.XXX",
    ".....X,X,,,XXX,,,,X,<X",
    ".....X,,,X,,X,,X,,XF,X",
    ".....X,XX,,X,,X,,X,,,X",
    ".....X,,X,,,,X,,X,,,,X",
    ".....XX,,X,,,,,,,,,,,X",
    ".....X,X,X,,,,,,,,,X,X",
    ".....X,,,,,,XO,,X,,X,X",
    ".....X,,X,**,XX,X,,X,X",
    "......X,X,**,FX,,,,,,X",
    ".....X,,X,XX,X,,X--XXX",
    "......X,,,,X,,,X,--X..",
    ".....X.XXXX.XXX.XXXX..",
    ]
]

stage1 = pygame.image.load("blocks/stage1.png")
stage2 = pygame.image.load("blocks/stage2.png")
stage3 = pygame.image.load("blocks/stage3.png")
stage4 = pygame.image.load("blocks/stage4.png")
stage5 = pygame.image.load("blocks/stage5.png")
stage6 = pygame.image.load("blocks/stage6.png")
stage7 = pygame.image.load("blocks/stage7.png")
reset = pygame.image.load("blocks/reset.png")
def switch_stage1():
    global current_stage_index
    direction_stack.clear()
    while len(blocks) != 0:
        remove_last_block()
    current_stage_index = 0
    initialize_extra_blocks()

def switch_stage2():
    global current_stage_index
    direction_stack.clear()
    while len(blocks) != 0:
        remove_last_block()
    current_stage_index = 1
    initialize_extra_blocks()

def switch_stage3():
    global current_stage_index
    direction_stack.clear()
    while len(blocks) != 0:
        remove_last_block()
    current_stage_index = 2
    initialize_extra_blocks()

def switch_stage4():
    global current_stage_index
    direction_stack.clear()
    while len(blocks) != 0:
        remove_last_block()
    current_stage_index = 3
    initialize_extra_blocks()

def switch_stage5():
    global current_stage_index
    direction_stack.clear()
    while len(blocks) != 0:
        remove_last_block()
    current_stage_index = 4
    initialize_extra_blocks()

def switch_stage6():
    global current_stage_index
    direction_stack.clear()
    while len(blocks) != 0:
        remove_last_block()
    current_stage_index = 5
    initialize_extra_blocks()

def switch_stage7():
    global current_stage_index
    direction_stack.clear()
    while len(blocks) != 0:
        remove_last_block()
    current_stage_index = 6
    initialize_extra_blocks()

def reset_l():
    direction_stack.clear()
    while len(blocks) != 0:
        remove_last_block()

class Button:
    def __init__(self, x, y, image, action=None):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        
        self.action = action

    def draw(self):
        
        screen.blit(self.image, (self.rect.x,self.rect.y))

    def check_click(self, mouse_pos):
        
        if self.rect.collidepoint(mouse_pos):
            if self.action:
                self.action()
                
reset_but = Button(runner_top_left[0] - 110,runner_top_left[1],"blocks/reset.png",reset_l)
stage1_but = Button(runner_top_left[0] - 110,runner_top_left[1] + 50,"blocks/stage1.png",switch_stage1)        
stage2_but = Button(runner_top_left[0] - 110,runner_top_left[1] + 100,"blocks/stage2.png",switch_stage2)
stage3_but = Button(runner_top_left[0] - 110,runner_top_left[1] + 150,"blocks/stage3.png",switch_stage3)
stage4_but = Button(runner_top_left[0] - 110,runner_top_left[1] + 200,"blocks/stage4.png",switch_stage4)
stage5_but = Button(runner_top_left[0] - 110,runner_top_left[1] + 250,"blocks/stage5.png",switch_stage5)
stage6_but = Button(runner_top_left[0] - 110,runner_top_left[1] + 300,"blocks/stage6.png",switch_stage6)
stage7_but = Button(runner_top_left[0] - 110,runner_top_left[1] + 350,"blocks/stage7.png",switch_stage7)
def o_find():
    global o_position_array, o_position, o_image
    # O의 위치 찾기 (2차원 배열에서)
    o_position_array = find_o_position_in_array()

    if o_position_array is not None:
        print(f"2차원 배열에서 O의 위치: {o_position_array}")
        o_position = o_position_array
        o_position_s = o_position_array

        o_image = pygame.image.load("blocks/o2.png")
        o_rect = o_image.get_rect()
        return o_position, o_position_s


def stone_find():
    global stone_position_array, stone_position, stone_image
    # *의 위치 찾기 (2차원 배열에서)
    stone_position_array = find_stone_position_in_array()
    if stone_position_array is not None:
        print(f"2차원 배열에서 *의 위치: {stone_position_array}")
        stone_position = stone_position_array
        stone_position_s = stone_position_array

        stone_image = pygame.image.load("blocks/stone.png")
        stone_rect = stone_image.get_rect()
        return stone_position, stone_position_s

def stop_find():
    global stop_position_array, stop_position, stop_image
    # -의 위치 찾기 (2차원 배열에서)
    stop_position_array = find_stop_position_in_array()
    if stop_position_array is not None:
        print(f"2차원 배열에서 -의 위치: {stop_position_array}")
        stop_position = stop_position_array
        stop_position_s = stop_position_array

        stop_image = pygame.image.load("blocks/stop.png")
        return stop_position, stop_position_s

def initialize_extra_blocks():
    global extra_blocks, extra_map, current_stage_index , o_position, o_position_s, stone_position, stone_position_s, stop_position, stop_position_s
    extra_map = stages[current_stage_index]
    extra_blocks = []
    for row, line in enumerate(extra_map):
        for col, char in enumerate(line):
            if char == 'X':
                create_block_map_floor("blocks/s.png", extra_blocks, (col, row))
                create_block_map("blocks/extra_block.png", extra_blocks, (col, row))

            elif char == '<':
                create_block_map_floor("blocks/floor.png", extra_blocks, (col, row))
                create_block_map_tree("blocks/tree.png", extra_blocks, (col, row))

            elif char == 'F':
                create_block_map_floor("blocks/floor.png", extra_blocks, (col, row))
                create_block_map("blocks/fire.png", extra_blocks, (col, row))
            elif char != '.':
                create_block_map_floor("blocks/floor.png", extra_blocks, (col, row))


    o_position, o_position_s = o_find()
    stone_position, stone_position_s = stone_find()
    stop_position, stop_position_s = stop_find()

font1 = pygame.font.Font(None, 30)

# 초기화
initialize_extra_blocks()

clock = pygame.time.Clock()
frame_rate = 10  # 초당 프레임 수 설정

execute_moves = False
move_interval = 0.05
time_since_last_move =0

while True:
    dt = clock.tick(60) / 1000.0
    time_since_last_move += dt


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # 화살표 키 이벤트 처리
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction_stack.push('LEFT')
                create_block("blocks/left.png")
                print(len(blocks))
            elif event.key == pygame.K_RIGHT:
                direction_stack.push('RIGHT')    
                create_block("blocks/right.png")
                print(len(blocks))
            elif event.key == pygame.K_UP:
                direction_stack.push('UP')
                create_block("blocks/up.png")
                print(len(blocks))
            elif event.key == pygame.K_DOWN:
                direction_stack.push('DOWN')
                create_block("blocks/down.png")
                print(len(blocks))
            elif event.key == pygame.K_BACKSPACE:
                remove_last_block_with_direction()
                print(len(blocks))
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_RETURN:
                execute_moves = True
                print("실행")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            stage1_but.check_click(mouse_pos) 
            stage2_but.check_click(mouse_pos)
            stage3_but.check_click(mouse_pos) 
            stage4_but.check_click(mouse_pos) 
            stage5_but.check_click(mouse_pos) 
            stage6_but.check_click(mouse_pos) 
            stage7_but.check_click(mouse_pos)
            reset_but.check_click(mouse_pos)       
            print("yes")
    if direction_stack.is_empty() and execute_moves:
        execute_moves = False
        o_position_array = o_position_s
        stone_position_array = stone_position_s
        pygame.display.flip()
        print("A")


    if execute_moves and time_since_last_move >= delay_time:
        if not direction_stack.is_empty():
            current_direction = direction_stack.pop_()
            print(f"Executing direction: {current_direction}")
            o_position_array, stone_position_array = move_player_and_stone(o_position_array, stone_position_array, current_direction)
            pygame.display.flip()
            time_since_last_move = 0
            print(execute_moves)

            stop_position_array = find_stop_position_in_array()

            # 스테이지 클리어 체크
            if stop_stone(stone_position_array,stop_position_array):  # CLEAR_POSITION은 스테이지 클리어 조건에 맞는 위치
                execute_moves = False
                print("성공")
                text1 = font1.render('collision_num : {}'.format(stages), True, (255, 255, 255))
                screen.blit(text1, (110, 10))
                
                switch_stage()
                # 초기화 함수 호출
                initialize_extra_blocks()
                
            
   
        
            
        
    
    

    # 화면을 흰색으로 지우기
    screen.fill(bg_color)


    screen.blit(image_bg, (0,0))
    # 실행기 그리기
    pygame.draw.rect(screen, runner_color, runner_rect)

    stage1_but.draw()
    stage2_but.draw()
    stage3_but.draw()
    stage4_but.draw()
    stage5_but.draw()
    stage6_but.draw()
    stage7_but.draw()
    reset_but.draw()
    # 블록 그리기
    for block in blocks:
        screen.blit(block[1], block[0])

    # 추가된 블록 그리기
    draw_extra_blocks()
    # 도착지점 이미지 그리기
    new_block_x = stop_position_array[0] * (extra_block_size + extra_block_spacing) + extra_block_spacing
    new_block_y = stop_position_array[1] * (extra_block_size + extra_block_spacing) + extra_block_spacing
    stop_position = (new_block_x, new_block_y)
    screen.blit(stop_image,stop_position)
    # O 이미지 그리기
    new_block_x = o_position_array[0] * (extra_block_size + extra_block_spacing) + extra_block_spacing
    new_block_y = o_position_array[1] * (extra_block_size + extra_block_spacing) + extra_block_spacing
    o_position = (new_block_x, new_block_y)
    screen.blit(o_image, o_position)

    # 돌 이미지 그리기
    draw_stone(stone_position_array)

    

    # 화면 업데이트
    pygame.display.flip()

    # 초당 프레임 수 설정
    clock.tick(60)
