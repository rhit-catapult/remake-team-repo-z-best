import pygame

pygame.init()
TILE_SIZE = 100
W, H = 1300,800 
screen = pygame.display.set_mode((W, H))

# 加载两种瓦片
tile_floor_raw = pygame.image.load(("floor_tile_rescaled.png")).convert()
tile_floor = pygame.transform.scale(tile_floor_raw,(TILE_SIZE,TILE_SIZE))



tile_wall_raw = pygame.image.load(("brick_wall.png")).convert()
tile_wall = pygame.transform.scale(tile_wall_raw, (TILE_SIZE,TILE_SIZE))
tile_grass = pygame.image.load(("grass-tile.png"))


# 自定义地图：0草地，1石头
map_data = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0]
    
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




