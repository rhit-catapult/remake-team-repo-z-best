import pygame

pygame.init()
TILE_SIZE = 32
W, H = 640, 480
screen = pygame.display.set_mode((W, H))

# 加载两种瓦片
tile_grass = pygame.image.load(()))
tile_grass.fill((30, 120, 30))
tile_stone = pygame.Surface((TILE_SIZE, TILE_SIZE))
tile_stone.fill((80, 80, 80))

# 自定义地图：0草地，1石头
map_data = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0],
    [0,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0],
    [0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0],
    [0,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0],
    [0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0],
    
]

def draw_tile_map():
    for row_idx, row in enumerate(map_data):
        for col_idx, tile_id in enumerate(row):
            x = col_idx * TILE_SIZE
            y = row_idx * TILE_SIZE
            if tile_id == 0:
                screen.blit(tile_grass, (x, y))
            elif tile_id == 1:
                screen.blit(tile_stone, (x, y))

clock = pygame.time.Clock()
running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
    screen.fill((0,0,0))
    draw_tile_map()
    pygame.display.flip()
    clock.tick(60)
pygame.quit() 




