import random
import pygame

##############################################################
# 기본 초기화 (반드시 해야 하는 것들)
pygame.init()

# 화면 크기 설정
screen_width = 480  # 가로 크기
screen_height = 640  # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Quiz")

# FPS
clock = pygame.time.Clock()
##############################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)
# 배경 만들기
background = pygame.image.load("ddong//background.png")

# 캐릭터 만들기
character = pygame.image.load("ddong\hoduman1.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height

# 이동 위치
to_x = 0
character_speed = 10

# 똥 만들기 함수
def create_ddongs(num_ddongs):
    ddongs = []
    for _ in range(num_ddongs):
        ddong = pygame.image.load("ddong/hodu3.png")
        ddong_size = ddong.get_rect().size
        ddong_width = ddong_size[0]
        ddong_height = ddong_size[1]
        ddong_x_pos = random.randint(0, screen_width - ddong_width)
        ddong_y_pos = random.randint(-100, -40)
        ddong_speed = random.randint(5, 15)
        ddongs.append({
            "image": ddong,
            "x_pos": ddong_x_pos,
            "y_pos": ddong_y_pos,
            "width": ddong_width,
            "height": ddong_height,
            "speed": ddong_speed
        })
    return ddongs

# 똥 리스트 초기화 (최대 5개)
ddongs = create_ddongs(random.randint(1, 5))

# 폰트 설정
game_font = pygame.font.Font(None, 40)

# 생존 시간 초기화
start_ticks = pygame.time.get_ticks()
elapsed_time = 0

# 게임 상태 관리 변수
game_over = False

def reset_game():
    global character_x_pos, character_y_pos, to_x, ddongs, start_ticks, elapsed_time, game_over
    character_x_pos = (screen_width / 2) - (character_width / 2)
    character_y_pos = screen_height - character_height
    to_x = 0
    ddongs = create_ddongs(random.randint(1, 5))
    start_ticks = pygame.time.get_ticks()
    elapsed_time = 0
    game_over = False

running = True
while running:
    dt = clock.tick(30)
    
    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                running = False
            elif event.key == pygame.K_SPACE and game_over:
                reset_game()
            
            if not game_over:
                if event.key == pygame.K_LEFT:
                    to_x -= character_speed
                elif event.key == pygame.K_RIGHT:
                    to_x += character_speed
            
        if event.type == pygame.KEYUP:
            if not game_over and (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                to_x = 0

    # 3. 게임 캐릭터 위치 정의
    if not game_over:
        character_x_pos += to_x

        if character_x_pos < 0:
            character_x_pos = 0
        elif character_x_pos > screen_width - character_width:
            character_x_pos = screen_width - character_width

        for ddong in ddongs:
            ddong["y_pos"] += ddong["speed"]
            if ddong["y_pos"] > screen_height:
                ddong["y_pos"] = random.randint(-100, -40)
                ddong["x_pos"] = random.randint(0, screen_width - ddong["width"])

    # 4. 충돌 처리
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ddong in ddongs:
        ddong_rect = ddong["image"].get_rect()
        ddong_rect.left = ddong["x_pos"]
        ddong_rect.top = ddong["y_pos"]

        if character_rect.colliderect(ddong_rect):
            game_over = True
            break

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))
    screen.blit(character, (character_x_pos, character_y_pos))
    for ddong in ddongs:
        screen.blit(ddong["image"], (ddong["x_pos"], ddong["y_pos"]))

    # 생존 시간 계산 및 표시
    if not game_over:
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Elapsed Time: {:.1f}".format(elapsed_time), True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    # 게임 오버 시 화면에 텍스트 표시
    if game_over:
        game_over_text = game_font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (screen_width / 2 - 80, screen_height / 2 - 50))
        elapsed_text = game_font.render("Survival Time: {:.1f}".format(elapsed_time), True, (255, 255, 255))
        screen.blit(elapsed_text, (screen_width / 2 - 130, screen_height / 2))
        restart_text = game_font.render("Press SPACE to restart", True, (255, 255, 255))
        screen.blit(restart_text, (screen_width / 2 - 150, screen_height / 2 + 50))

    pygame.display.update()

pygame.quit()
