"""Test file - Original monolithic version (backup)"""
import pygame

pygame.init()
TILE_SIZE = 100
CORPSE_SIZE = 200
W, H = 1300, 800
screen = pygame.display.set_mode((W, H))

VIEW_COLS = W // TILE_SIZE
VIEW_ROWS = H // TILE_SIZE

view_offset_x = 0
view_offset_y = 0

def load_image(path, size, use_alpha=False):
    method = "convert_alpha" if use_alpha else "convert"
    img = pygame.image.load(path)
    img = getattr(img, method)()
    return pygame.transform.scale(img, size)

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

# 两张地图：map_data2在上，map_data1拼接在下方（图1在图2下面）
map_data_1 = [
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1],
]

map_data_2 = [
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
]

# 拼接总地图：map_data2在上，map_data1在下
full_world_map = map_data_2 + map_data_1
map2_rows_count = len(map_data_2)
map1_start_row = map2_rows_count

# Item types: 10=box, 20=corpse
ITEM_SPRITES = {10: box, 20: corpse}

#玩家初始位置，调整坐标防止出生在墙里/地图外
player_x = TILE_SIZE * 6
player_y = TILE_SIZE * (map1_start_row + 4)

#初始化镜头直接对准出生点
view_offset_x = player_x / TILE_SIZE - VIEW_COLS /2
view_offset_y = player_y / TILE_SIZE - VIEW_ROWS/ 2

# Items: (row, column, item_type)
items = [( map1_start_row + 6, 9, 10), (map1_start_row + 6, 6, 20)]

#解锁弹窗状态
is_unlocked = False
show_popup = False
popup_font = pygame.font.Font(None, 48)

#时钟
clock = pygame.time.Clock()
running = True

def draw_full_map():
    global view_offset_x, view_offset_y
    start_col = int(view_offset_x)
    start_row = int(view_offset_y)

    for row_idx in range(start_row, start_row + VIEW_ROWS + 1):
        if row_idx < 0 or row_idx >= len(full_world_map):
            continue
        row_data = full_world_map[row_idx]
        for col_idx in range(start_col, start_col + VIEW_COLS + 1):
            if col_idx < 0 or col_idx >= len(row_data):
                continue
            tile_id = row_data[col_idx]
            tile_img = TILE_SPRITES[tile_id].copy()

            if row_idx < map2_rows_count and not is_unlocked:
                tile_img.set_alpha(60)

            screen_x = col_idx * TILE_SIZE - view_offset_x * TILE_SIZE
            screen_y = row_idx * TILE_SIZE - view_offset_y * TILE_SIZE
            screen.blit(tile_img, (screen_x, screen_y))

def draw_items():
    global view_offset_x, view_offset_y
    for row, col, item_type in items:
        screen_x = col * TILE_SIZE - view_offset_x * TILE_SIZE
        screen_y = row * TILE_SIZE - view_offset_y * TILE_SIZE
        screen.blit(ITEM_SPRITES[item_type], (screen_x, screen_y))

def draw_popup():
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((0, 0, 180, 150))
    screen.blit(overlay, (0, 0))

    text1 = popup_font.render("Press E to Unlock Full Map Content", True, (220, 220, 220))
    text2 = popup_font.render("Before unlock: Only background image displays", True, (220, 220, 220))
    screen.blit(text1, (W/2 - text1.get_width()/2, H/2 - 40))
    screen.blit(text2, (W/2 - text2.get_width()/2, H/2 + 10))

#墙体碰撞检测 使用拼接后的完整地图
def is_wall_collision(x, y, w, h):
    left_col = int(x // TILE_SIZE)
    right_col = int((x + w - 1) // TILE_SIZE)
    top_row = int(y // TILE_SIZE)
    bottom_row = int((y + h - 1) // TILE_SIZE)

    for r in range(top_row, bottom_row + 1):
        if r < 0 or r >= len(full_world_map):
            continue
        for c in range(left_col, right_col + 1):
            if c < 0 or c >= len(full_world_map[r]):
                continue
            if full_world_map[r][c] == 1:
                return True
    return False

#窗口边界检测
def is_out_of_screen(x, y, w, h):
    map_width = len(full_world_map[0]) * TILE_SIZE
    map_height = len(full_world_map) * TILE_SIZE
    return x < 0 or y < 0 or (x + w) > map_width or (y + h) > map_height

def player_movement():
    global player_x, player_y, view_offset_x, view_offset_y
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0

    if keys[pygame.K_UP]:
        dy -= PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        dy += PLAYER_SPEED
    if keys[pygame.K_LEFT]:
        dx -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        dx += PLAYER_SPEED

    # 单独X轴移动检测碰撞
    new_x = player_x + dx
    if not is_wall_collision(new_x, player_y, TILE_SIZE, TILE_SIZE) and not is_out_of_screen(new_x, player_y, TILE_SIZE, TILE_SIZE):
        player_x = new_x

    # 单独Y轴移动检测碰撞
    new_y = player_y + dy
    if not is_wall_collision(player_x, new_y, TILE_SIZE, TILE_SIZE) and not is_out_of_screen(player_x, new_y, TILE_SIZE, TILE_SIZE):
        player_y = new_y

    # 相机跟随玩家居中
    view_offset_x = player_x / TILE_SIZE - VIEW_COLS / 2
    view_offset_y = player_y / TILE_SIZE - VIEW_ROWS / 2

    # 锁定相机边界，不超出整张地图
    max_view_col = len(full_world_map[0]) - VIEW_COLS
    max_view_row = len(full_world_map) - VIEW_ROWS
    view_offset_x = max(0, min(view_offset_x, max_view_col))
    view_offset_y = max(0, min(view_offset_y, max_view_row))

def draw_player():
    screen_x = player_x - view_offset_x * TILE_SIZE
    screen_y = player_y - view_offset_y * TILE_SIZE
    screen.blit(player, (screen_x, screen_y))

#主循环
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # 修复按键判断语法错误
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_e and show_popup:
            is_unlocked = True
            show_popup = False

    # 弹窗触发区域
    trigger_pos = (TILE_SIZE * 6, TILE_SIZE * (map1_start_row)+1)
    if not is_unlocked and not show_popup:
        if abs(player_x - trigger_pos[0]) < TILE_SIZE and abs(player_y - trigger_pos[1]) < TILE_SIZE:
            show_popup = True

    if not show_popup:
        player_movement()

    #渲染
    screen.fill((0, 0, 0))

    draw_full_map()
    draw_items()
    draw_player()

    if show_popup:
        draw_popup()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
