import pygame
import random

class Egg:
    # Define possible egg colors
    COLORS = [
        (255, 255, 255),  # White
        (0, 0, 255),      # Blue
        (255, 0, 255),    # Purple
        (255, 0, 0),      # Red
    ]
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (0, 255, 0)  # Green color for walls
    
    def draw(self, screen, grid_size, y_offset=0):
        """Draw the egg (green wall) on the screen."""
        # Calculate center position of the cell
        center_x = (self.x * grid_size) + (grid_size // 2)
        center_y = (self.y * grid_size) + y_offset + (grid_size // 2)
        radius = (grid_size // 2) - 1  # Slightly smaller than half the grid size
        
        # Draw egg as a circle
        pygame.draw.circle(screen, self.color, (center_x, center_y), radius)
    
    @property
    def position(self):
        """Get the current position of the egg."""
        return (self.x, self.y) 