import pygame
import sys
import random
import math
from healthbar import HealthBar
from my_character import MainC
from zombie_module import Zombie
from map import Rooms
from maps import full_world_map, map_data_1, map_data_2, map2_rows_count, map1_start_row, items



# ---------------- START SCREEN ---------------- #

def start_screen(screen):
    start_img = pygame.image.load("Welcome_page.png").convert_alpha()
    start_img = pygame.transform.scale(start_img, (1300, 800))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # CLICK ANYWHERE TO START
            if event.type == pygame.MOUSEBUTTONDOWN:
                return  # start the game/

        screen.blit(start_img, (0, 0))
        pygame.display.update()

def death_screen(screen):
    death_img = pygame.image.load("you_died.png").convert_alpha()
    death_img = pygame.transform.scale(death_img, (1300, 800))

    start_time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Allow clicking to restart AFTER 1 second
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.time.get_ticks() - start_time > 1000:
                    return  # restart the game

        screen.blit(death_img, (0, 0))
        pygame.display.update()

# ---------------- ZOMBIE SPAWNING ---------------- #

def spawn_zombies(screen, player, count=5):
    zombies = []
    for _ in range(count):
        while True:
            x = random.randint(50, 1250)
            y = random.randint(50, 750)

            dx = player.x - x
            dy = player.y - y
            distance = math.hypot(dx, dy)

            if distance > (player.radius + 100):  # safe buffer
                zombie = Zombie(screen, x, y, "ZombieFIXED.png")
                zombie.hp = 3  # 3 hits to kill
                zombies.append(zombie)
                break

    return zombies


# ---------------- MAIN GAME ---------------- #

def main():
    pygame.init()
    pygame.display.set_caption("peanut apocolypse")
    screen = pygame.display.set_mode((1300, 800))

    # Show start screen first
    start_screen(screen)

    player = MainC(screen, 650, 680, "Character_Placeholder.png")
    healthbar = HealthBar(screen)

    zombies = spawn_zombies(screen, player, 5)

    clock = pygame.time.Clock()
    hurt_sound = pygame.mixer.Sound("Roblox - Oof Death (Sound Effect).mp3")

    while True:
        clock.tick(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                player.fire()

        pressed_keys = pygame.key.get_pressed()

        # Player movement
        if pressed_keys[pygame.K_w]:
            player.y -= 5
        if pressed_keys[pygame.K_s]:
            player.y += 5
        if pressed_keys[pygame.K_a]:
            player.x -= 5
        if pressed_keys[pygame.K_d]:
            player.x += 5

        # Map boundaries
        player.x = max(player.radius, min(1300 - player.radius, player.x))
        player.y = max(player.radius, min(800 - player.radius, player.y))

        player.mouse_x, player.mouse_y = pygame.mouse.get_pos()
        player.update_angle()

        current_time = pygame.time.get_ticks()

        # Zombie movement + collision with player
        for zombie in zombies:
            zombie.follow_player(player)
            zombie.update_angle(player)

            dx = player.x - zombie.x
            dy = player.y - zombie.y
            distance = math.hypot(dx, dy)

            if distance < (player.radius + zombie.radius):
                if current_time - player.last_hit_time > 1000:
                    player.hp -= 1
                    player.last_hit_time = current_time
                    healthbar.set_hp(player.hp)
                    hurt_sound.play()
            if player.hp <= 0:
                pygame.time.delay(1000)
                death_screen(screen)
                return main()  # restart the whole game
        # Drawing
        screen.fill((255, 255, 255))

        # Bullet → Zombie collision
        for bullet in player.bullets[:]:
            bullet.move()
            bullet.draw()

            for zombie in zombies[:]:
                dx = bullet.bullet_x - zombie.x
                dy = bullet.bullet_y - zombie.y
                distance = math.hypot(dx, dy)

                if distance < zombie.radius:
                    zombie.hp -= 1
                    player.bullets.remove(bullet)

                    if zombie.hp <= 0:
                        zombies.remove(zombie)

                    break  # stop checking other zombies for this bullet

        player.draw()

        for zombie in zombies:
            zombie.draw()

        healthbar.draw()
<<<<<<< HEAD
        #big_r = Map(screen)
        #room_5 = Rooms(screen, 5)
        #big_r.draw()
        #room_5.draw()
=======
        # big_r = Map(screen)
        # room_5 = Rooms(screen, 5)
        # big_r.draw()
        # room_5.draw()
>>>>>>> #730eab6dc868edb3d235d20d1205f8e9ab1e40bc
        pygame.display.update()


main()
