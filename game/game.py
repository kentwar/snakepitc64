import pygame
from .player import Player
from .snake import Snake
from .egg import Egg
from .sound import SoundManager


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.paused = False
        self.game_over = True  # Start with game over screen
        self.score = 0
        self.grid_size = 16  # Size of each grid cell
        self.grid_width = 40  # 40 eggs wide
        self.grid_height = 25  # 25 eggs high
        self.score_height = 32  # Height of score bar in pixels
        
        # Adjust screen size to accommodate score bar and grid
        self.play_area_width = self.grid_width * self.grid_size
        self.play_area_height = self.grid_height * self.grid_size
        self.screen = pygame.display.set_mode(
            (self.play_area_width, self.play_area_height + self.score_height)
        )
        
        # Initialize game objects
        self.snakes = []
        self.eggs = []
        self.sound_manager = SoundManager()
        
        # Timing variables
        self.tick_delay = 1000  # 1 second between ticks (1000ms)
        self.last_tick = pygame.time.get_ticks()
        # Snake movement is 4x faster than tick rate
        self.snake_move_delay = self.tick_delay / 4
        self.last_snake_move = pygame.time.get_ticks()
        # Player movement uses the same delay as snakes
        self.last_player_move = pygame.time.get_ticks()
        # Track current key being held down
        self.current_key_held = None
        
        # Initialize game state
        self.setup_level()
        
        # Create player at fixed position (8 from right, 8 from bottom)
        self.create_player()
        
    def setup_level(self):
        """Set up the initial level with eggs and snakes."""
        # Create egg walls first
        self.create_egg_walls()
        
        # Then create snakes in their enclosures
        self.create_snakes()
        
    def create_egg_walls(self):
        """Create the initial egg walls with precise holes for snakes."""
        # First fill the entire grid with eggs
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                self.eggs.append(Egg(x, y))
        
        # Define hole dimensions
        hole_width = 2
        hole_height = 3
        
        # Define spacing and margins
        vertical_gap = 5  # Gap between holes vertically
        horizontal_gap = 6  # Gap between holes horizontally
        top_margin = 2  # Gap from top edge
        left_margin = 3  # Gap from left edge
        
        # Calculate number of holes that can fit
        num_rows = 3  # 3 rows of holes
        num_cols = 5  # 5 columns of holes
        
        # Create holes for snakes (3 rows × 5 columns = 15 holes)
        for row in range(num_rows):
            for col in range(num_cols):
                # Calculate top-left corner of this hole
                hole_x = left_margin + (col * (hole_width + horizontal_gap))
                hole_y = top_margin + (row * (hole_height + vertical_gap))
                
                # Remove eggs to create the hole
                for y in range(hole_y, hole_y + hole_height):
                    for x in range(hole_x, hole_x + hole_width):
                        # Find and remove the egg at this position
                        for egg in self.eggs[:]:
                            if egg.position == (x, y):
                                self.eggs.remove(egg)
                                break
    
    def create_snakes(self):
        """Create the initial snakes in their holes."""
        # Define hole dimensions and spacing (same as in create_egg_walls)
        hole_width = 2
        hole_height = 3
        vertical_gap = 5
        horizontal_gap = 6
        top_margin = 2
        left_margin = 3
        
        num_rows = 3
        num_cols = 5
        
        # Create snakes in the center of each hole
        for row in range(num_rows):
            for col in range(num_cols):
                # Calculate center position for this snake
                snake_x = left_margin + (col * (hole_width + horizontal_gap))
                snake_y = top_margin + (row * (hole_height + vertical_gap)) + 1
                
                # Create snake - only the first snake can eat eggs
                can_eat = (row == 0 and col == 0)  # First snake can eat
                snake = Snake(snake_x, snake_y, can_eat=can_eat)
                snake.direction = (1, 0)  # Start moving right
                self.snakes.append(snake)
    
    def create_player(self):
        """Create player at fixed position (8 from right, 8 from bottom)."""
        player_x = self.grid_width - 8
        player_y = self.grid_height - 8
        
        # Make sure there's no egg at the player's position
        for egg in self.eggs[:]:
            if egg.position == (player_x, player_y):
                self.eggs.remove(egg)
                break
                
        self.player = Player(player_x, player_y)
    
    def handle_input(self, event):
        """Handle user input."""
        # If game is over, check for restart button click
        if self.game_over and event.type == pygame.MOUSEBUTTONDOWN:
            # Get restart button rect
            button_rect = self.get_restart_button_rect()
            if button_rect.collidepoint(event.pos):
                self.restart_game()
                return
        
        if event.type == pygame.KEYDOWN:
            # Store the key being held down
            arrow_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, 
                          pygame.K_DOWN]
            if event.key in arrow_keys:
                self.current_key_held = event.key
        
        elif event.type == pygame.KEYUP:
            # Clear the key if it's released
            if event.key == self.current_key_held:
                self.current_key_held = None
    
    def try_move_player(self, dx, dy):
        """Try to move player, checking for snake collisions and boundaries."""
        new_x = self.player.x + dx
        new_y = self.player.y + dy
        
        # Check if new position is within grid boundaries
        if (new_x < 0 or new_x >= self.grid_width or 
            new_y < 0 or new_y >= self.grid_height):
            return False  # Can't move outside the grid
        
        # Check if new position has a snake
        for snake in self.snakes:
            # Check snake head
            if snake.position == (new_x, new_y):
                return False  # Can't move onto a snake
            
            # Check snake body
            for segment in snake.body:
                if segment == (new_x, new_y):
                    return False  # Can't move onto a snake
        
        # If we get here, the move is valid
        self.player.move(dx, dy)
        self.last_player_move = pygame.time.get_ticks()
        return True
    
    def update(self):
        """Update game state."""
        if self.paused or self.game_over:
            return
        
        current_time = pygame.time.get_ticks()
        
        # Process player movement if a key is held down and enough time has passed
        time_since_move = current_time - self.last_player_move
        can_move = time_since_move >= self.snake_move_delay
        
        if self.current_key_held and can_move:
            if self.current_key_held == pygame.K_LEFT:
                self.try_move_player(-1, 0)
            elif self.current_key_held == pygame.K_RIGHT:
                self.try_move_player(1, 0)
            elif self.current_key_held == pygame.K_UP:
                self.try_move_player(0, -1)
            elif self.current_key_held == pygame.K_DOWN:
                self.try_move_player(0, 1)
        
        # Update snakes 4 times per tick (evenly spaced)
        if current_time - self.last_snake_move >= self.snake_move_delay:
            self.last_snake_move = current_time
            
            # Update each snake once
            for snake in self.snakes:
                snake.update(self.eggs, self.snakes, self.player)
            
            # Check for egg collection
            self.check_egg_collection()
            
            # Check for collisions
            self.check_collisions()
        
        # Play tick sound once per tick
        if current_time - self.last_tick >= self.tick_delay:
            self.last_tick = current_time
            self.sound_manager.play_tick()
    
    def check_egg_collection(self):
        """Check if player has collected any eggs."""
        player_pos = (self.player.x, self.player.y)
        for egg in self.eggs[:]:
            if egg.position == player_pos:
                self.eggs.remove(egg)
                self.score += 10
                self.sound_manager.play_egg_collect()
    
    def check_collisions(self):
        """Check for collisions between game objects."""
        player_pos = (self.player.x, self.player.y)
        
        # Check snake collisions
        for snake in self.snakes:
            if snake.position == player_pos:
                self.game_over = True
                self.running = False
                self.sound_manager.play_death()
                return
    
    def draw(self):
        """Draw all game objects."""
        # Draw white score bar
        score_bar = pygame.Rect(0, 0, self.play_area_width, self.score_height)
        pygame.draw.rect(self.screen, (255, 255, 255), score_bar)
        
        # Draw score on white background
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (0, 0, 0))
        score_rect = score_text.get_rect()
        score_rect.left = 10
        score_rect.centery = self.score_height // 2
        self.screen.blit(score_text, score_rect)
        
        # Draw black play area
        play_area = pygame.Rect(
            0, 
            self.score_height, 
            self.play_area_width, 
            self.play_area_height
        )
        pygame.draw.rect(self.screen, (0, 0, 0), play_area)
        
        # Draw eggs with offset for score bar
        for egg in self.eggs:
            egg.draw(self.screen, self.grid_size, y_offset=self.score_height)
        
        # Draw snakes with offset for score bar
        for snake in self.snakes:
            snake.draw(self.screen, self.grid_size, y_offset=self.score_height)
        
        # Draw player with offset for score bar
        self.player.draw(
            self.screen, 
            self.grid_size, 
            y_offset=self.score_height
        )
        
        # Draw game over screen if game is over
        if self.game_over:
            self.draw_game_over_screen()
    
    def draw_game_over_screen(self):
        """Draw the game over screen with final score and play button."""
        # Create semi-transparent overlay
        overlay = pygame.Surface(
            (self.play_area_width, self.play_area_height + self.score_height)
        )
        overlay.set_alpha(200)  # Semi-transparent
        overlay.fill((0, 0, 0))  # Black overlay
        self.screen.blit(overlay, (0, 0))
        
        # Draw title text (either "GAME OVER" or "SNAKEPIT")
        font_large = pygame.font.Font(None, 72)
        if self.score > 0:  # If we've played at least one game
            title_text = "GAME OVER"
            title_color = (255, 0, 0)  # Red for game over
        else:
            title_text = "SNAKEPIT"
            title_color = (0, 255, 0)  # Green for title screen
            
        game_over_text = font_large.render(title_text, True, title_color)
        game_over_rect = game_over_text.get_rect(
            center=(self.play_area_width // 2, 
                   (self.play_area_height + self.score_height) // 4)
        )
        self.screen.blit(game_over_text, game_over_rect)
        
        # Draw final score if we've played at least one game
        if self.score > 0:
            font_medium = pygame.font.Font(None, 48)
            score_text = font_medium.render(
                f"Final Score: {self.score}", True, (255, 255, 255)
            )
            score_rect = score_text.get_rect(
                center=(self.play_area_width // 2, 
                       (self.play_area_height + self.score_height) // 3)
            )
            self.screen.blit(score_text, score_rect)
        
        # Draw controls explainer
        font_small = pygame.font.Font(None, 28)
        controls_text = [
            "CONTROLS:",
            "Arrow Keys - Move player",
            "P - Pause game",
            "ESC - Quit game"
        ]
        
        # Position controls text in the middle of the screen
        controls_y = (self.play_area_height + self.score_height) // 2
        for i, text in enumerate(controls_text):
            control_surface = font_small.render(text, True, (255, 255, 255))
            control_rect = control_surface.get_rect(
                center=(self.play_area_width // 2, 
                       controls_y + (i * 30))
            )
            self.screen.blit(control_surface, control_rect)
        
        # Draw play button
        button_rect = self.get_restart_button_rect()
        pygame.draw.rect(self.screen, (0, 128, 0), button_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 2)
        
        # Draw button text
        font_button = pygame.font.Font(None, 36)
        restart_text = font_button.render("Play", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=button_rect.center)
        self.screen.blit(restart_text, restart_rect)
    
    def get_restart_button_rect(self):
        """Get the rectangle for the play button."""
        button_width = 200
        button_height = 50
        button_x = (self.play_area_width - button_width) // 2
        button_y = (self.play_area_height + self.score_height) * 3 // 4
        return pygame.Rect(button_x, button_y, button_width, button_height)
    
    def restart_game(self):
        """Restart the game."""
        # Reset game state
        self.running = True
        self.game_over = False
        self.score = 0
        self.snakes = []
        self.eggs = []
        
        # Reset timing variables
        self.last_tick = pygame.time.get_ticks()
        self.last_snake_move = pygame.time.get_ticks()
        self.last_player_move = pygame.time.get_ticks()
        self.current_key_held = None
        
        # Initialize game state
        self.setup_level()
        
        # Create player
        self.create_player()
    
    def toggle_pause(self):
        """Toggle game pause state."""
        self.paused = not self.paused 