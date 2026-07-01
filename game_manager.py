"""Main game manager and loop"""
import pygame
from config import screen, clock, TILE_SIZE, FPS, W, H
from assets import player
from maps import map1_start_row
from renderer import draw_full_map, draw_items, draw_player, draw_popup
from player import player_movement

class GameManager:
    """Main game manager class"""
    
    def __init__(self):
        self.player_x = TILE_SIZE * 6
        self.player_y = TILE_SIZE * (map1_start_row + 4)
        
        self.view_offset_x = self.player_x / TILE_SIZE - (W // TILE_SIZE) / 2
        self.view_offset_y = self.player_y / TILE_SIZE - (H // TILE_SIZE) / 2
        
        self.is_unlocked = False
        self.show_popup = False
        self.running = True
        self.trigger_y = TILE_SIZE * (map1_start_row + 1)
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_e and self.show_popup:
                self.is_unlocked = True
                self.show_popup = False
    
    def check_popup_trigger(self):
        """Check if player triggered popup"""
        self.show_popup = (not self.is_unlocked) and (self.player_y <= self.trigger_y)
    
    def update(self):
        """Update game state"""
        self.handle_events()
        self.check_popup_trigger()
        
        if not self.show_popup:
            self.player_x, self.player_y, self.view_offset_x, self.view_offset_y = \
                player_movement(self.player_x, self.player_y, self.view_offset_x, self.view_offset_y)
    
    def render(self):
        """Render game"""
        screen.fill((0, 0, 0))
        
        draw_full_map(self.view_offset_x, self.view_offset_y, self.is_unlocked)
        draw_items(self.view_offset_x, self.view_offset_y)
        draw_player(self.player_x, self.player_y, self.view_offset_x, self.view_offset_y, player)
        
        if self.show_popup:
            draw_popup()
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.update()
            self.render()
            clock.tick(FPS)
        
        pygame.quit()

def start_game():
    """Start the game"""
    game = GameManager()
    game.run()

if __name__ == "__main__":
    start_game()
