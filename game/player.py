import pygame


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = (0, 0)  # Current movement direction
        self.color = (255, 0, 0)  # Red color for the face
    
    def move(self, dx, dy):
        """Move the player in the given direction."""
        self.x += dx
        self.y += dy
        self.direction = (dx, dy)
    
    def update(self):
        """Update player position based on current direction."""
        self.x += self.direction[0]
        self.y += self.direction[1]
        self.direction = (0, 0)  # Reset direction after moving
    
    def draw(self, screen, grid_size, y_offset=0):
        """Draw the player character (red face) on the screen."""
        rect = pygame.Rect(
            self.x * grid_size + 1,
            self.y * grid_size + y_offset + 1,
            grid_size - 2,
            grid_size - 2
        )
        pygame.draw.rect(screen, self.color, rect)
    
    @property
    def position(self):
        """Get the current position of the player."""
        return (self.x, self.y) 