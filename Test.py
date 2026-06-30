import pygame

pygame.init()
TILE_SIZE = 100
CORPSE_SIZE = 200
W, H = 1300,800 
screen = pygame.display.set_mode((W, H))

# 加载两种瓦片

room_1_raw = pygame.image.load(("room1_map.png")).convert()
room_1_bg = pygame.transform.scale(room_1_raw, (W, H))
#room_1 = pygame.transform.scale(room_1_raw, ())

tile_floor_raw = pygame.image.load(("White_Tile.png")).convert()
tile_floor = pygame.transform.scale(tile_floor_raw,(TILE_SIZE,TILE_SIZE))

tile_floor_blood_raw = pygame.image.load(("Blood_Tile_fixed.png")).convert()
tile_floor_blood = pygame.transform.scale(tile_floor_blood_raw,(TILE_SIZE,TILE_SIZE))



tile_wall_raw = pygame.image.load(("brick_wall.png")).convert()
tile_wall = pygame.transform.scale(tile_wall_raw, (TILE_SIZE,TILE_SIZE))



tile_grass_raw = pygame.image.load(("grass-tile.png"))
tile_grass = pygame.transform.scale(tile_grass_raw, (TILE_SIZE, TILE_SIZE))

box_raw = pygame.image.load(("box.png")).convert_alpha()
box = pygame.transform.scale(box_raw,(TILE_SIZE,TILE_SIZE))

corpse_raw = pygame.image.load(("dead_Zombie.png")).convert_alpha()
corpse = pygame.transform.scale(corpse_raw, (CORPSE_SIZE, TILE_SIZE))

#玩家角色和图片
PLAYER_SPEED = 5
player_raw= pygame.image.load("Character_Placeholder.png").convert_alpha()
player = pygame.transform.scale(player_raw, (TILE_SIZE, TILE_SIZE))


# 自定义地图：0草地，1石头
map_data = [
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,3,0,0,0,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1]
]

items = [
    (6, 9, 10),  # (row, column, item_type)
    (6, 6, 20)
]

#玩家初始位置
player_x = TILE_SIZE*2
player_y = TILE_SIZE*2

#解锁弹窗状态
is_unlocked = False
show_popup = False
popup_font = pygame.font. SysFont(None,48)

#时钟
clock = pygame.time.Clock()
running = True


def draw_tile_map():
    for row_idx, row in enumerate(map_data):
        for col_idx, tile_id in enumerate(row):
            x = col_idx * TILE_SIZE
            y = row_idx * TILE_SIZE
            if tile_id == 0:
                screen.blit(tile_floor, (x, y))
            elif tile_id == 1:
                screen.blit(tile_wall, (x, y))
            elif tile_id ==2:
                screen.blit(tile_grass,(x,y))
            elif tile_id ==3:
                screen.blit(tile_floor_blood,(x,y))

def draw_items():
    for row, col, item_type in items:
        x = col * TILE_SIZE
        y = row * TILE_SIZE

        if item_type == 10:
            screen.blit(box, (x, y))
        elif item_type == 20:
            screen.blit(corpse, (x, y))

#绘制弹窗
def draw_popup():
    overlay = pygame.Surface((W, H),pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay,(0,0))

text_line1 = popup_font.render("Press E to Unlock Full Map Content")
text_line2 = popup_font.render("Before unlock: Only backgroundimage displays",True, (220, 220, 220))
screen.blit(text_line1, (W//2 - text_line1.get_width()//2, H//2 - 40))
screen.blit(text_line2, (W//2 - text_line2.get_width()//2, H//2 + 10))

#墙体碰撞检测
def is_wall_collision(x, y, w, h):
    left_col= int(x//TILE_SIZE)
    right_col = int((x+w-1)//TILE_SIZE)
    top_row = int(y//TILE_SIZE)
    bottom_row = int((y+h-1)//TILE_SIZE)

    for r in range(top_row,bottom_row +1):
        for c in range(left_col, right_col+1):
            if 0<=r <len(map_data) and 0 <= c < len(map_data[r]):
                if map_data[r][c] == 1:
                    return True
    return False

#窗口边界检测
def is_out_of_screen(x, y, w, h):
    if x<0 or y<0 or (x+ w)> W or (y+h)>H:
        return True
    return False

def player_movement():
    global player_x, player_y
    keys = pygame.key.get_pressed()
    dx, dy =0, 0 

    if keys[pygame.K_UP]:
        dy -= PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        dy += PLAYER_SPEED
    if keys[pygame.K_LEFT]:
        dx -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        dx += PLAYER_SPEED

    new_x = player_x +dx
    if not is_wall_collision(new_x, player_y, TILE_SIZE, TILE_SIZE) and not is_out_of_screen(new_x, player_y, TILE_SIZE, TILE_SIZE):
        player_x = new_x
    
    new_y = player_y +dy
    if not is_wall_collision(player_x, new_y, TILE_SIZE, TILE_SIZE) and not is_out_of_screen(player_x, new_y,TILE_SIZE, TILE_SIZE):
        player_y = new_y

    
def draw_player():
    screen.blit(player_x,player_y)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if show_popup and event.key == pygame.K_e:
                is_unlocked = True
                show_popup= False


    trigger_pos_x = TILE_SIZE*6
    trigger_pos_y = TILE_SIZE*6
    if not is_unlocked and not show_popup:
        if abs(player_x - trigger_pos_x) < TILE_SIZE and abs(player_y-trigger_pos_y) < TILE_SIZE:
            show_popup = True

    if not show_popup:
        player_movement()

    screen.fill((0,0,0))
    screen.blit(room_1_bg,(0,0))

    if is_unlocked:
        draw_tile_map()
        draw_items()

    draw_player()
    if show_popup:
        draw_popup()

    pygame.display.flip()
    clock.tick(60)
pygame.quit() 




