import pygame

pygame.init()
TILE_SIZE = 100
CORPSE_SIZE = 200
W, H = 1300, 800
screen = pygame.display.set_mode((W, H))

def load_image(path, size, use_alpha=False):
    """Load and scale image"""
    method = "convert_alpha" if use_alpha else "convert"
    img = pygame.image.load(path)
    img = getattr(img, method)()
    return pygame.transform.scale(img, size)

# Load sprites
room_1_bg = load_image("room1_map.png", (W, H))
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
    """Draw both map layers"""
    for map_data in [map_data_1, map_data_2]:
        for row_idx, row in enumerate(map_data):
            for col_idx, tile_id in enumerate(row):
                x, y = col_idx * TILE_SIZE, row_idx * TILE_SIZE
                screen.blit(TILE_SPRITES[tile_id], (x, y))

def draw_items():
    """Draw all items"""
    for row, col, item_type in items:
        screen.blit(ITEM_SPRITES[item_type], (col * TILE_SIZE, row * TILE_SIZE))

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

    for r in range(top_row, bottom_row + 1):
        for c in range(left_col, right_col + 1):
            if 0 <= r < len(map_data_1) and 0 <= c < len(map_data_1[r]):
                if map_data_1[r][c] == 1:
                    return True
            if 0 <= r < len(map_data_2) and 0 <= c < len(map_data_2[r]):
                if map_data_2[r][c] == 1:
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
            new_x, new_y = player_x + dx, player_y + dy
            if not is_wall_collision(new_x, player_y, TILE_SIZE, TILE_SIZE) and not is_out_of_screen(new_x, player_y, TILE_SIZE, TILE_SIZE):
                player_x = new_x
            if not is_wall_collision(player_x, new_y, TILE_SIZE, TILE_SIZE) and not is_out_of_screen(player_x, new_y, TILE_SIZE, TILE_SIZE):
                player_y = new_y
    
def draw_player():
    screen.blit(player, (player_x, player_y))


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
    screen.blit(room_1_bg, (0, 0))
    
    if is_unlocked:
        draw_tile_map()
        draw_items()
    
    draw_player()
    if show_popup:
        draw_popup()

    pygame.display.flip()
    clock.tick(60)

pygame.quit() 




