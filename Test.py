import pygame

pygame.init()
TILE_SIZE = 100
CORPSE_SIZE = 200
W, H = 1300,800 
screen = pygame.display.set_mode((W, H))

# 加载两种瓦片
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
    (6, 10, 10),  # (row, column, item_type)
    (6, 5, 20)
]


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

            

clock = pygame.time.Clock()
running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0))
    draw_tile_map()
    draw_items()
    pygame.display.flip()
    clock.tick(60)
pygame.quit() 




