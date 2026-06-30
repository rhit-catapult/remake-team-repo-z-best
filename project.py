import pygame
import sys
import random
import math
from healthbar import HealthBar
from my_character import MainC
from zombie_module import Zombie
<<<<<<< HEAD
# from map import Rooms
=======
from map import Rooms
from maps import full_world_map, map_data_1, map_data_2, map2_rows_count, map1_start_row, items
from assets import TILE_SPRITES, ITEM_SPRITES
from config import TILE_SIZE
from collision import is_wall_collision, is_out_of_screen


>>>>>>> e1f0e403df598720668e61c86ef1ddf7a8dae8e7

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
                return  # start the game

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


# ---------------- MAP RENDERING ---------------- #

def draw_map(screen, view_offset_x, view_offset_y):
    """Draw the complete map with camera offset"""
    view_cols = 1300 // TILE_SIZE
    view_rows = 800 // TILE_SIZE
    start_col = int(view_offset_x)
    start_row = int(view_offset_y)
    
    for row_idx in range(start_row, start_row + view_rows + 1):
        if row_idx < 0 or row_idx >= len(full_world_map):
            continue
        row = full_world_map[row_idx]
        for col_idx in range(start_col, start_col + view_cols + 1):
            if col_idx < 0 or col_idx >= len(row):
                continue
            tile_id = row[col_idx]
            if tile_id in TILE_SPRITES:
                screen_x = col_idx * TILE_SIZE - view_offset_x * TILE_SIZE
                screen_y = row_idx * TILE_SIZE - view_offset_y * TILE_SIZE
                screen.blit(TILE_SPRITES[tile_id], (screen_x, screen_y))

def draw_map_items(screen, view_offset_x, view_offset_y):
    """Draw items on the map with camera offset"""
    for row, col, item_type in items:
        if item_type in ITEM_SPRITES:
            screen_x = col * TILE_SIZE - view_offset_x * TILE_SIZE
            screen_y = row * TILE_SIZE - view_offset_y * TILE_SIZE
            screen.blit(ITEM_SPRITES[item_type], (screen_x, screen_y))

def draw_popup(screen):
    """Draw unlock popup overlay"""
    overlay = pygame.Surface((1300, 800), pygame.SRCALPHA)
    overlay.fill((0, 0, 180, 150))
    screen.blit(overlay, (0, 0))
    
    popup_font = pygame.font.Font(None, 48)
    text1 = popup_font.render("Press E to Unlock Full Map Content", True, (220, 220, 220))
    text2 = popup_font.render("Before unlock: Map2 is hidden", True, (220, 220, 220))
    screen.blit(text1, (1300/2 - text1.get_width()/2, 800/2 - 40))
    screen.blit(text2, (1300/2 - text2.get_width()/2, 800/2 + 10))


# ---------------- MAIN GAME ---------------- #

def main():
    current_level = 1
    pygame.init()
    pygame.display.set_caption("peanut apocolypse")
    screen = pygame.display.set_mode((1300, 800))

    # FONT FOR LEVEL DISPLAY
    font = pygame.font.SysFont(None, 40)

    # Load level clear PNG AFTER display is created
    level_clear_img = pygame.image.load("level_complete.png").convert_alpha()
    level_clear_img = pygame.transform.scale(level_clear_img, (600, 300))

    # Show start screen first
    start_screen(screen)

    player = MainC(screen, 650, 950, "Character_Placeholder.png")
    healthbar = HealthBar(screen)
    
    # Camera and map state
    view_offset_x = player.x / TILE_SIZE - (1300 // TILE_SIZE) / 2
    view_offset_y = player.y / TILE_SIZE - (800 // TILE_SIZE) / 2
    is_unlocked = False
    show_popup = False
    trigger_pos = (TILE_SIZE * 6, TILE_SIZE * (map1_start_row) + 1)

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
            
            # E key to unlock map
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e and show_popup:
                is_unlocked = True
                show_popup = False

        pressed_keys = pygame.key.get_pressed()

        # Player movement with wall collision
        dx, dy = 0, 0
        if pressed_keys[pygame.K_w]:
            dy -= 5
        if pressed_keys[pygame.K_s]:
            dy += 5
        if pressed_keys[pygame.K_a]:
            dx -= 5
        if pressed_keys[pygame.K_d]:
            dx += 5
        
        # Check X movement collision
        new_x = player.x + dx
        if not is_wall_collision(new_x, player.y, player.radius * 2, player.radius * 2) and not is_out_of_screen(new_x, player.y, player.radius * 2, player.radius * 2):
            player.x = new_x
        
        # Check Y movement collision
        new_y = player.y + dy
        if not is_wall_collision(player.x, new_y, player.radius * 2, player.radius * 2) and not is_out_of_screen(player.x, new_y, player.radius * 2, player.radius * 2):
            player.y = new_y
        
        # Check popup trigger
        if not is_unlocked and not show_popup:
            if abs(player.x - trigger_pos[0]) < TILE_SIZE and abs(player.y - trigger_pos[1]) < TILE_SIZE:
                show_popup = True
        
        # Update camera to follow player
        view_offset_x = player.x / TILE_SIZE - (1300 // TILE_SIZE) / 2
        view_offset_y = player.y / TILE_SIZE - (800 // TILE_SIZE) / 2
        
        # Clamp camera to map bounds
        max_view_col = len(full_world_map[0]) - (1300 // TILE_SIZE)
        max_view_row = len(full_world_map) - (800 // TILE_SIZE)
        view_offset_x = max(0, min(view_offset_x, max_view_col))
        view_offset_y = max(0, min(view_offset_y, max_view_row))

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
        
        # Draw map first
        draw_map(screen, view_offset_x, view_offset_y)
        draw_map_items(screen, view_offset_x, view_offset_y)

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

        # ---------------- LEVEL CLEAR CHECK ---------------- #
        if len(zombies) == 0:
            # Draw level clear image
            screen.blit(level_clear_img, (350, 250))
            pygame.display.update()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_e:
                            waiting = False

                pygame.time.delay(50)

            # Start next level
            current_level += 1
            player.bullets.clear()  # optional but recommended
            zombies = spawn_zombies(screen, player, 5)

        healthbar.draw()
<<<<<<< HEAD

        # ---------------- DRAW LEVEL TEXT ---------------- #
        level_text = font.render(f"Level: {current_level}", True, (0, 0, 0))
        screen.blit(level_text, (20, 760))  # bottom-left corner

=======
        #big_r = Map(screen)
        #room_5 = Rooms(screen, 5)
        #big_r.draw()
        #room_5.draw()
        
        # Draw popup if needed
        if show_popup:
            draw_popup(screen)
        
>>>>>>> e1f0e403df598720668e61c86ef1ddf7a8dae8e7
        pygame.display.update()


main()