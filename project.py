import pygame
import sys
import random
import math
from healthbar import HealthBar
from my_character import MainC
from zombie_module import Zombie
from map import Rooms
from maps import full_world_map, map1_start_row, map2_start_row, map3_start_row, map4_start_row, map5_start_row, map5_start_col, map5_rows_count, map5_cols_count, items
from assets import TILE_SPRITES, ITEM_SPRITES
from config import TILE_SIZE
from collision import is_wall_collision, is_out_of_screen
from boss_module import Boss_class

# ---------------- START SCREEN ---------------- #

def start_screen(screen):
    start_img = pygame.image.load("Welcome_page.png").convert_alpha()
    start_img = pygame.transform.scale(start_img, (1300, 800))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                return

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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.time.get_ticks() - start_time > 1000:
                    return

        screen.blit(death_img, (0, 0))
        pygame.display.update()


# ---------------- ZOMBIE SPAWNING ---------------- #

def spawn_zombies(screen, player, count=5):
    zombies = []
    spawn_radius = 40
    for _ in range(count):
        while True:
            x = random.randint(50, 1250)
            y = random.randint(50, 750)

            dx = player.x - x
            dy = player.y - y
            distance = math.hypot(dx, dy)

<<<<<<< HEAD
            if distance > (player.radius + 100):
=======
            collides_with_map = is_wall_collision(
                x - spawn_radius,
                y - spawn_radius,
                spawn_radius * 2,
                spawn_radius * 2,
            )

            if distance > (player.radius + 100) and not collides_with_map:  # safe buffer + valid spawn tile
>>>>>>> 6f8a55e8a833222b2c2a80bb274c30da3d1462bc
                zombie = Zombie(screen, x, y, "ZombieFIXED.png")
                zombie.hp = 3
                zombies.append(zombie)
                break

    return zombies


# ---------------- MAP RENDERING ---------------- #

def _is_fence_tile(row_idx, col_idx):
    """Return True when the map tile exists and is a fence tile."""
    if row_idx < 0 or row_idx >= len(full_world_map):
        return False
    row = full_world_map[row_idx]
    if col_idx < 0 or col_idx >= len(row):
        return False
    return row[col_idx] == 4


def _get_fence_overlay(row_idx, col_idx):
    """Rotate fence sprite to match neighbor direction where possible."""
    up = _is_fence_tile(row_idx - 1, col_idx)
    down = _is_fence_tile(row_idx + 1, col_idx)
    left = _is_fence_tile(row_idx, col_idx - 1)
    right = _is_fence_tile(row_idx, col_idx + 1)

    fence_img = TILE_SPRITES[4].copy()

    # If this segment connects mostly vertically, rotate the fence texture.
    if (up or down) and not (left or right):
        fence_img = pygame.transform.rotate(fence_img, 90)

    return fence_img

def draw_map(screen, view_offset_x, view_offset_y, unlocked_min_row, room5_unlocked):
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
<<<<<<< HEAD
                tile_img = TILE_SPRITES[tile_id].copy()
                if row_idx < unlocked_min_row:
                    tile_img.set_alpha(55)
=======
                should_darken = False
                # Darken any map rows that are still locked.
                if row_idx < unlocked_min_row:
                    should_darken = True
                # Keep room 5 dark until it is explicitly unlocked.
>>>>>>> 6f8a55e8a833222b2c2a80bb274c30da3d1462bc
                if (not room5_unlocked) and row_idx >= map5_start_row and row_idx < (map5_start_row + map5_rows_count) and col_idx >= map5_start_col:
                    should_darken = True

                # Fence tile uses grass as base with a transparent fence overlay.
                if tile_id == 4:
                    base_img = TILE_SPRITES[2].copy()
                    fence_img = _get_fence_overlay(row_idx, col_idx)
                    if should_darken:
                        base_img.set_alpha(55)
                        fence_img.set_alpha(55)
                    screen.blit(base_img, (screen_x, screen_y))
                    # Slight overlap helps hide seams at tile boundaries.
                    screen.blit(fence_img, (screen_x - 1, screen_y - 1))
                else:
                    tile_img = TILE_SPRITES[tile_id].copy()
                    if should_darken:
                        tile_img.set_alpha(55)
                    screen.blit(tile_img, (screen_x, screen_y))


def draw_map_items(screen, view_offset_x, view_offset_y):
    for row, col, item_type in items:
        if item_type in ITEM_SPRITES:
            screen_x = col * TILE_SIZE - view_offset_x * TILE_SIZE
            screen_y = row * TILE_SIZE - view_offset_y * TILE_SIZE
            screen.blit(ITEM_SPRITES[item_type], (screen_x, screen_y))


def draw_unlock_prompt(screen, next_map_number):
    prompt_bg = pygame.Surface((420, 54), pygame.SRCALPHA)
    prompt_bg.fill((15, 15, 15, 190))
    screen.blit(prompt_bg, (1300 / 2 - 210, 24))

    popup_font = pygame.font.Font(None, 42)
    prompt_text = popup_font.render(f"Press E to unlock Map {next_map_number}", True, (230, 230, 230))
    screen.blit(prompt_text, (1300 / 2 - prompt_text.get_width() / 2, 35))


def draw_level2_popup(screen):
    overlay = pygame.Surface((1300, 800), pygame.SRCALPHA)
    overlay.fill((10, 25, 40, 120))
    screen.blit(overlay, (0, 0))

    popup_font = pygame.font.Font(None, 120)
    level_text = popup_font.render("LEVEL 2", True, (240, 240, 240))
    screen.blit(level_text, (1300 / 2 - level_text.get_width() / 2, 800 / 2 - level_text.get_height() / 2))


def draw_minimap(screen, player, zombies, unlocked_min_row, room5_unlocked, x, y):
    """Draw a full-map minimap with player/zombie markers and lock shading."""
    map_rows = len(full_world_map)
    map_cols = len(full_world_map[0])

    panel_w = 250
    panel_h = 200
    padding = 8

    playable_w = panel_w - padding * 2
    playable_h = panel_h - padding * 2
    cell_size = min(playable_w / map_cols, playable_h / map_rows)

    minimap_w = map_cols * cell_size
    minimap_h = map_rows * cell_size
    map_x = x + (panel_w - minimap_w) / 2
    map_y = y + (panel_h - minimap_h) / 2

    panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    panel.fill((10, 10, 10, 165))
    screen.blit(panel, (x, y))
    pygame.draw.rect(screen, (210, 210, 210), (x, y, panel_w, panel_h), 2)

    tile_colors = {
        0: (205, 205, 205),
        1: (95, 95, 95),
        2: (85, 155, 85),
        3: (150, 75, 75),
        4: (100, 140, 80),
    }

    for row_idx, row_data in enumerate(full_world_map):
        for col_idx, tile_id in enumerate(row_data):
            color = tile_colors.get(tile_id, (120, 120, 120))

            # Match main-map lock behavior: locked rooms remain dark on minimap.
            if row_idx < unlocked_min_row:
                color = (color[0] // 4, color[1] // 4, color[2] // 4)
            if (not room5_unlocked) and row_idx >= map5_start_row and row_idx < (map5_start_row + map5_rows_count) and col_idx >= map5_start_col:
                color = (color[0] // 4, color[1] // 4, color[2] // 4)

            tile_rect = pygame.Rect(
                map_x + col_idx * cell_size,
                map_y + row_idx * cell_size,
                max(1, cell_size + 0.2),
                max(1, cell_size + 0.2),
            )
            pygame.draw.rect(screen, color, tile_rect)

    # Draw zombies first so player marker stays visible on top.
    for zombie in zombies:
        zx = map_x + (zombie.x / TILE_SIZE) * cell_size
        zy = map_y + (zombie.y / TILE_SIZE) * cell_size
        pygame.draw.circle(screen, (210, 55, 55), (int(zx), int(zy)), 3)

    px = map_x + (player.x / TILE_SIZE) * cell_size
    py = map_y + (player.y / TILE_SIZE) * cell_size
    pygame.draw.circle(screen, (70, 200, 255), (int(px), int(py)), 4)


# ---------------- MAIN GAME ---------------- #

def main():
    current_level = 1
    boss_spawned = False
    boss = None

    pygame.init()
    pygame.display.set_caption("peanut apocolypse")
    screen = pygame.display.set_mode((1300, 800))

    font = pygame.font.Font(None, 40)

    level_clear_img = pygame.image.load("level_complete.png").convert_alpha()
    level_clear_img = pygame.transform.scale(level_clear_img, (600, 300))

    start_screen(screen)

    player = MainC(screen, TILE_SIZE * 6, TILE_SIZE * (map1_start_row + 4), "Character_Placeholder.png")
    healthbar = HealthBar(screen)
    minimap_x = 20
    minimap_y = 20 + healthbar.images[4].get_height() + 12
    
    view_offset_x = player.x / TILE_SIZE - (1300 // TILE_SIZE) / 2
    view_offset_y = player.y / TILE_SIZE - (800 // TILE_SIZE) / 2
    unlocked_min_row = map1_start_row
    room5_unlocked = False
    show_popup = False
    next_map_number = 2
    show_level2_popup = False
    level2_popup_started_at = 0
    level2_popup_duration_ms = 1800

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
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e and show_popup:
                if unlocked_min_row == map1_start_row:
                    unlocked_min_row = map2_start_row
                    next_map_number = 3
                elif unlocked_min_row == map2_start_row:
                    unlocked_min_row = map3_start_row
                    next_map_number = 4
                elif unlocked_min_row == map3_start_row:
                    unlocked_min_row = map4_start_row
                    next_map_number = 5
                elif next_map_number == 5:
                    room5_unlocked = True
                    next_map_number = None
                    show_level2_popup = True
                    level2_popup_started_at = pygame.time.get_ticks()
                show_popup = False

        pressed_keys = pygame.key.get_pressed()

        dx, dy = 0, 0
        if pressed_keys[pygame.K_w]:
            dy -= 5
        if pressed_keys[pygame.K_s]:
            dy += 5
        if pressed_keys[pygame.K_a]:
            dx -= 5
        if pressed_keys[pygame.K_d]:
            dx += 5
        
        new_x = player.x + dx
        enters_locked_room5_x = (not room5_unlocked) and (new_x + player.radius >= map5_start_col * TILE_SIZE) and (player.y + player.radius >= map5_start_row * TILE_SIZE) and (player.y - player.radius < (map5_start_row + map5_rows_count) * TILE_SIZE)
        if not enters_locked_room5_x and not is_wall_collision(new_x - player.radius, player.y - player.radius, player.radius * 2, player.radius * 2) and not is_out_of_screen(new_x - player.radius, player.y - player.radius, player.radius * 2, player.radius * 2):
            player.x = new_x
        
        new_y = player.y + dy
        entering_locked_rows = (new_y - player.radius) < (unlocked_min_row * TILE_SIZE)
        enters_locked_room5_y = (not room5_unlocked) and (player.x + player.radius >= map5_start_col * TILE_SIZE) and (new_y + player.radius >= map5_start_row * TILE_SIZE) and (new_y - player.radius < (map5_start_row + map5_rows_count) * TILE_SIZE)
        if not entering_locked_rows and not enters_locked_room5_y and not is_wall_collision(player.x - player.radius, new_y - player.radius, player.radius * 2, player.radius * 2) and not is_out_of_screen(player.x - player.radius, new_y - player.radius, player.radius * 2, player.radius * 2):
            player.y = new_y
        
        if next_map_number in (2, 3, 4):
            unlock_prompt_y = TILE_SIZE * (unlocked_min_row + 1)
            show_popup = player.y <= unlock_prompt_y
        elif next_map_number == 5:
            near_room5_gate_x = player.x >= (map5_start_col * TILE_SIZE - TILE_SIZE)
            near_room5_gate_y = player.y <= (map5_start_row + map5_rows_count) * TILE_SIZE
            show_popup = near_room5_gate_x and near_room5_gate_y
        else:
            show_popup = False

        if show_level2_popup and (pygame.time.get_ticks() - level2_popup_started_at >= level2_popup_duration_ms):
            show_level2_popup = False
        
        view_offset_x = player.x / TILE_SIZE - (1300 // TILE_SIZE) / 2
        view_offset_y = player.y / TILE_SIZE - (800 // TILE_SIZE) / 2
        
        max_view_col = len(full_world_map[0]) - (1300 // TILE_SIZE)
        max_view_row = len(full_world_map) - (800 // TILE_SIZE)
        view_offset_x = max(0, min(view_offset_x, max_view_col))
        view_offset_y = max(0, min(view_offset_y, max_view_row))

        player.mouse_x, player.mouse_y = pygame.mouse.get_pos()
        player.mouse_x += int(view_offset_x * TILE_SIZE)
        player.mouse_y += int(view_offset_y * TILE_SIZE)
        player.update_angle()

        current_time = pygame.time.get_ticks()

        # ---------------- ZOMBIE MOVEMENT ---------------- #
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
                return main()

        # ---------------- BOSS MOVEMENT ---------------- #
        if boss_spawned and boss is not None:
            boss.follow_player(player)
            boss.update_angle(player)

            dx = player.x - boss.x
            dy = player.y - boss.y
            distance = math.hypot(dx, dy)

            if distance < (player.radius + boss.radius):
                if current_time - player.last_hit_time > 1000:
                    player.hp -= 1
                    player.last_hit_time = current_time
                    healthbar.set_hp(player.hp)
                    hurt_sound.play()

            if player.hp <= 0:
                pygame.time.delay(1000)
                death_screen(screen)
                return main()

        # ---------------- DRAWING ---------------- #
        screen.fill((255, 255, 255))
        
        draw_map(screen, view_offset_x, view_offset_y, unlocked_min_row, room5_unlocked)
        draw_map_items(screen, view_offset_x, view_offset_y)

        # ---------------- BULLET COLLISION ---------------- #
        for bullet in player.bullets[:]:
            bullet.move()
            screen.blit(bullet.peanut, (bullet.bullet_x - view_offset_x * TILE_SIZE, bullet.bullet_y - view_offset_y * TILE_SIZE))

            # Bullet → Zombie
            for zombie in zombies[:]:
                dx = bullet.bullet_x - zombie.x
                dy = bullet.bullet_y - zombie.y
                distance = math.hypot(dx, dy)

                if distance < zombie.radius:
                    zombie.hp -= 1
                    player.bullets.remove(bullet)

                    if zombie.hp <= 0:
                        zombies.remove(zombie)

                    break

            # Bullet → Boss
            if boss_spawned and boss is not None:
                dx = bullet.bullet_x - boss.x
                dy = bullet.bullet_y - boss.y
                distance = math.hypot(dx, dy)

                if distance < boss.radius:
                    boss.hp -= 1
                    player.bullets.remove(bullet)

                    if boss.hp <= 0:
                        boss = None
                        boss_spawned = False
                        current_level += 1

                    continue

        # Draw player
        player.rect.center = (player.x - view_offset_x * TILE_SIZE, player.y - view_offset_y * TILE_SIZE)
        player.draw()

        # Draw zombies
        for zombie in zombies:
            old_x, old_y = zombie.rect.x, zombie.rect.y
            zombie.rect.center = (zombie.x - view_offset_x * TILE_SIZE, zombie.y - view_offset_y * TILE_SIZE)
            zombie.draw()
            zombie.rect.x, zombie.rect.y = old_x, old_y

        # Draw boss
        if boss_spawned and boss is not None:
            old_x, old_y = boss.rect.x, boss.rect.y
            boss.rect.center = (boss.x - view_offset_x * TILE_SIZE, boss.y - view_offset_y * TILE_SIZE)
            boss.draw()
            boss.rect.x, boss.rect.y = old_x, old_y

        # ---------------- LEVEL CLEAR CHECK ---------------- #
        if len(zombies) == 0 and not boss_spawned:
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

            current_level += 1
            player.bullets.clear()

            # Spawn boss at Level 5
            if current_level == 5:
                boss = Boss_class(screen, player.x + 300, player.y + 300, "Boss_Jose.png", 20, 4)
                boss.hp = 20
                boss.radius = 70
                boss_spawned = True
            else:
                zombies = spawn_zombies(screen, player, 5)

        healthbar.draw()
        draw_minimap(screen, player, zombies, unlocked_min_row, room5_unlocked, minimap_x, minimap_y)

        if show_popup:
            draw_unlock_prompt(screen, next_map_number)

        if show_level2_popup:
            draw_level2_popup(screen)

        level_text = font.render(f"Level: {current_level}", True, (0, 0, 0))
        screen.blit(level_text, (20, 760))

        pygame.display.update()


main()