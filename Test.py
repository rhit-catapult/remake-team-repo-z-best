import pygame
import random

WIDTH, HEIGHT = 1300,800
TILE_SIZE = 30
FPS=60

GRASS = (40,80,30)
ROAD = (60,60,60)
WALL = (90,70,50)
PLAYER_COLOR = (0,200,255)
ZOMBIE_COLOR = (80,140,20)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Pixel Apocalypse")
clock = pygame.time.Clock()

map_data = [
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,2,2,2,0,0,0,0,1,1,1,1,1,1,0,0,0,0,2,2,2,0,0,0],
[0,0,2,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,2,0,2,0,0,0],
[0,0,2,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,2,0,2,0,0,0],
[0,0,2,2,2,0,0,0,0,1,1,1,1,1,1,0,0,0,0,2,2,2,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
]



def draw_background():
    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile == 0:
                pygame.draw.rect(screen, GRASS, rect)
            elif tile ==1:
                pygame.draw.rect(screen, ROAD, rect)
            elif tile ==2:
                pygame.draw.rect(screen, WALL, rect)
                pygame.draw.rect(screen,(0,0,0),rect, 1)


class Player:
    def __init__(self):
        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.size = 24
        self.speed = 4
        self.keys_pressed = set()
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.keys_pressed.add(event.key)
        elif event.type == pygame.KEYUP:
            self.keys_pressed.discard(event.key)
    
    def update(self):
        if pygame.K_w in self.keys_pressed and self.y - self.speed >= 0:
            self.y -= self.speed
        if pygame.K_s in self.keys_pressed and self.y + self.speed <= HEIGHT - self.size:
            self.y += self.speed
        if pygame.K_a in self.keys_pressed and self.x - self.speed >= 0:
            self.x -= self.speed
        if pygame.K_d in self.keys_pressed and self.x + self.speed <= WIDTH - self.size:
            self.x += self.speed
    
    def draw(self):
        pygame.draw.rect(screen, PLAYER_COLOR, (self.x, self.y, self.size,self.size))

class Zombie:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = 22
        self.speed = 1.2
    def update(self, player):
        
        if self.x < player.x:
            self.x += self.speed
        elif self.x > player.x:
            self.x -= self.speed
        if self.y < player.y:
            self.y += self.speed
        elif self.y > player.y:
            self.y -= self.speed
    def draw(self):
        pygame.draw.rect(screen, ZOMBIE_COLOR, (self.x, self.y, self.size, self.size))


player=Player()
zombies = [Zombie() for _ in range(8)]  

running=True
while running:
    clock.tick(FPS)
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        player.handle_event(event)

    draw_background()
    
    player.update()
    player.draw()

    for z in zombies:
        z.update(player)
        z.draw()

    pygame.display.flip()

pygame.quit()




