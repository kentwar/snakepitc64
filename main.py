import pygame
import sys
from game.game import Game

def main():
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()

    # Set up the display
    WINDOW_SIZE = (800, 600)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Snakepit (C64 Remake)")
    
    # Set up the game clock
    clock = pygame.time.Clock()
    
    # Create game instance
    game = Game(screen)
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p and not game.game_over:
                    game.toggle_pause()
            game.handle_input(event)
        
        # Update game state
        game.update()
        
        # Draw everything
        game.draw()
        
        # Update display
        pygame.display.flip()
        
        # Cap the framerate
        clock.tick(60)
        
        # Check if game is over but we should keep running for the game over screen
        if not game.running and not game.game_over:
            running = False
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 