import pygame

pygame.init()
TILE_SIZE = 100
CORPSE_SIZE = 200
W, H = 1300, 800
screen = pygame.display.set_mode((W, H))

VIEW_COLS = W //TILE_SIZE
VIEW_ROWS = H //TILE_SIZE


view_offset_x = 0
view_offset_y = 0

def load_image(path, size, use_alpha = False):
    method = "convert_alpha" if use_alpha else"convert"
    img = pygame.image.load(path)
    img = getattr(img, method)()
    return pygame.transform.transform.scale(img, size)


# Load sprites
tile_floor = load_image("White_Tile.png", (TILE_SIZE, TILE_SIZE))
tile_floor_blood = load_image("Blood_Tile_fixed.png", (TILE_SIZE, TILE_SIZE))
tile_wall = load_image("brick_wall.png", (TILE_SIZE, TILE_SIZE))
tile_grass = load_image("grass-tile.png", (TILE_SIZE, TILE_SIZE))
box = load_image("box.png", (TILE_SIZE, TILE_SIZE), use_alpha=True)
corpse = load_image("dead_Zombie.png", (CORPSE_SIZE, TILE_SIZE), use_alpha=True)

PLAYER_SPEED = 5
player = load_image("Character_Placeholder.png", (TILE_SIZE, TILE_SIZE), use_alpha=True)

# Tile ID to sprite mapping
TILE_SPRITES = {0: tile_floor, 1: tile_wall, 2: tile_grass, 3: tile_floor_blood}


# 自定义地图：0草地，1石头
map_data_1 = [
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,3,0,0,0,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1]
]

map_data_2 = [
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,3,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1]
]

# Item types: 10=box, 20=corpse
ITEM_SPRITES = {10: box, 20: corpse}

#玩家初始位置
player_x = TILE_SIZE * 2
player_y = TILE_SIZE * 2

# Items: (row, column, item_type)
items = [(6, 9, 10), (6, 6, 20)]

#解锁弹窗状态
is_unlocked = False
show_popup = False
popup_font = pygame.font.Font(None, 48)

#时钟
clock = pygame.time.Clock()
running = True

def draw_tile_map():
    global view_offset_x, view_offset_y
    full_map = map_data_2

    start_col = int(view_offset_x)
    start_row = int(view_offset_y)

    for row_idx in range(start_row, start_row + VIEW_ROWS + 1):
        if row_idx < 0 or row_idx >=len (full_map):
            continue
        row = full_map[row_idx]
        for col_idx in range(start_col, start_col + VIEW_COLS + 1):
            if col_idx < 0 or col_idx >= len(row):
                continue
            tile_id = row [col_idx]
            screen_x = col_idx * TILE_SIZE - view_offset_x * TILE_SIZE
            screen_y = row_idx * TILE_SIZE - view_offset_y * TILE_SIZE
            screen.blit(TILE_SPRITES[tile_id]),


def draw_items():
    global view_offset_x, view_offset_y
    for row, col, item_type in items:
        screen_x = col * TILE_SIZE - view_offset_x * TILE_SIZE
        screen_y = row * TILE_SIZE - view_offset_y * TILE_SIZE
        screen.blit (ITEM_SPRITES[item_type], (screen_x, screen_y))

def draw_popup():
    """Draw semi-transparent overlay with unlock message"""
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    text1 = popup_font.render("Press E to Unlock Full Map Content", True, (220, 220, 220))
    text2 = popup_font.render("Before unlock: Only background image displays", True, (220, 220, 220))
    screen.blit(text1, (W//2 - text1.get_width()//2, H//2 - 40))
    screen.blit(text2, (W//2 - text2.get_width()//2, H//2 + 10))

#墙体碰撞检测
def is_wall_collision(x, y, w, h):
    left_col = int(x // TILE_SIZE)
    right_col = int((x + w - 1) // TILE_SIZE)
    top_row = int(y // TILE_SIZE)
    bottom_row = int((y + h - 1) // TILE_SIZE)
    full_map = map_data_2

    for r in range(top_row, bottom_row + 1):
       if r < 0 or r>=len(full_map):
           continue
       for c in range(left_col, right_col + 1):
           if c < 0 or c >=len(full_map[r]):
               continue
           if full_map[r][c] ==1:
               return True
    return False

#窗口边界检测
def is_out_of_screen(x, y, w, h):
    return x < 0 or y < 0 or (x + w) > W or (y + h) > H

def player_movement():
    global player_x, player_y
    keys = pygame.key.get_pressed()
    
    # Key to movement mapping
    moves = [
        (pygame.K_UP, 0, -PLAYER_SPEED),
        (pygame.K_DOWN, 0, PLAYER_SPEED),
        (pygame.K_LEFT, -PLAYER_SPEED, 0),
        (pygame.K_RIGHT, PLAYER_SPEED, 0)
    ]
    
    for key, dx, dy in moves:
        if keys[key]:
            new_x = player_x + dx
            new_y = player_y + dy
            if not is_wall_collision(new_x, new_y, TILE_SIZE, TILE_SIZE) and not is_out_of_screen(new_x, new_y, TILE_SIZE, TILE_SIZE):
                player_x = new_x
                player_y = new_y

               # 相机跟随玩家居中，实现视野扩张
            view_offset_x = player_x / TILE_SIZE - VIEW_COLS / 2
            view_offset_y = player_y / TILE_SIZE - VIEW_ROWS / 2

            # 限制相机不超出整张地图边界，防止黑边
            max_view_col = len(map_data_2[0]) - VIEW_COLS
            max_view_row = len(map_data_2) - VIEW_ROWS
            view_offset_x = max(0, min(view_offset_x, max_view_col))
            view_offset_y = max(0, min(view_offset_y, max_view_row))
    
def draw_player():
    screen_x = player_x - view_offset_x * TILE_SIZE
    screen_y = player_y - view_offset_y * TILE_SIZE
    screen.blit(player, (screen_x, screen_y))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_e and show_popup:
            is_unlocked = True
            show_popup = False

    # Check trigger zone for popup
    trigger_pos = (TILE_SIZE * 6, TILE_SIZE * 6)
    if not is_unlocked and not show_popup:
        if abs(player_x - trigger_pos[0]) < TILE_SIZE and abs(player_y - trigger_pos[1]) < TILE_SIZE:
            show_popup = True

    if not show_popup:
        player_movement()

    # Render
    screen.fill((0, 0, 0))

    
    if is_unlocked:
        draw_tile_map()
        draw_items()
    
    draw_player()
    if show_popup:
        draw_popup()

    pygame.display.flip()
    clock.tick(60)

pygame.quit() 




