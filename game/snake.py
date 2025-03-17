import pygame
import random
import math


class Snake:
    # Define possible snake colors
    COLORS = [
        (255, 255, 255),  # White
        (255, 0, 255),    # Purple
        (0, 255, 255),    # Cyan
        (255, 255, 0),    # Yellow
    ]
    
    def __init__(self, x, y, can_eat=False):
        self.x = x
        self.y = y
        self.direction = (1, 0)  # Start moving right
        self.color = random.choice(Snake.COLORS)  # Random snake color
        self.can_eat_eggs = can_eat  # Only one snake can eat eggs
        # Initialize body with multiple segments
        self.body = [(x, y)] * 20  # Start with length 20
        self.length = 20  # Fixed length
        
    def update(self, eggs, all_snakes=None, player=None):
        """Update snake position and behavior."""
        # Get possible directions
        forward = self.direction
        left = self.rotate_left(self.direction)
        right = self.rotate_right(self.direction)
        back = self.rotate_left(self.rotate_left(self.direction))
        
        # Check what's blocking each direction
        forward_blocked = self.check_direction(forward, eggs, all_snakes)
        left_blocked = self.check_direction(left, eggs, all_snakes)
        right_blocked = self.check_direction(right, eggs, all_snakes)
        
        # Decide movement based on rules
        moved = False
        
        # With 10% probability, try to turn toward the player
        if player and random.random() < 0.10:
            # Calculate direction to player
            player_dir = self.direction_to_player(player)
            
            # If we're not already moving in that direction, try to turn
            if player_dir != self.direction:
                # Try to move in the direction of the player
                if not self.check_direction(player_dir, eggs, all_snakes):
                    self.direction = player_dir
                # If blocked, try to turn in a direction that gets us closer
                else:
                    # Calculate which turn gets us closer to player
                    left_dist = self.distance_after_turn(left, player)
                    right_dist = self.distance_after_turn(right, player)
                    
                    if left_dist < right_dist and not left_blocked:
                        self.direction = left
                    elif right_dist < left_dist and not right_blocked:
                        self.direction = right
        
        # If this snake can eat eggs, try to eat in the current direction
        if self.can_eat_eggs:
            # Try to eat in the current direction first
            if self.try_eat_egg(eggs, forward):
                moved = True
            # If forward is blocked, consider turning
            elif forward_blocked:
                # Collect available directions (not blocked by other snakes)
                available_turns = []
                if not left_blocked:
                    available_turns.append(left)
                if not right_blocked:
                    available_turns.append(right)
                
                # If we have available directions, choose one randomly
                if available_turns:
                    self.direction = random.choice(available_turns)
                # If completely blocked, try going back as last resort
                elif not self.check_direction(back, eggs, all_snakes):
                    self.direction = back
                
                # Try to eat in the new direction
                if self.try_eat_egg(eggs, self.direction):
                    moved = True
        
        # If we haven't moved yet, try normal movement
        if not moved:
            # Go forward if possible
            if not forward_blocked:
                # Keep going forward
                pass
            # If forward is blocked, try turning
            else:
                # Collect available directions (not blocked by other snakes)
                available_turns = []
                if not left_blocked:
                    available_turns.append(left)
                if not right_blocked:
                    available_turns.append(right)
                
                # If we have available directions, choose one randomly
                if available_turns:
                    self.direction = random.choice(available_turns)
                # If completely blocked, try going back as last resort
                elif not self.check_direction(back, eggs, all_snakes):
                    self.direction = back
                # If truly trapped, don't move
                else:
                    # We're completely trapped - don't move this turn
                    return
        
        # If we haven't explicitly moved yet, move in the chosen direction
        if not moved:
            self.move()
        
        # Update body segments - add new head position
        self.body.insert(0, (self.x, self.y))
        
        # Remove tail if body is longer than length
        while len(self.body) > self.length:
            self.body.pop()
    
    def direction_to_player(self, player):
        """Calculate the direction to move toward the player."""
        dx = player.x - self.x
        dy = player.y - self.y
        
        # Determine primary direction (horizontal or vertical)
        if abs(dx) > abs(dy):
            # Horizontal movement is more important
            return (1 if dx > 0 else -1, 0)
        else:
            # Vertical movement is more important
            return (0, 1 if dy > 0 else -1)
    
    def distance_after_turn(self, direction, player):
        """Calculate distance to player after moving in a direction."""
        new_x = self.x + direction[0]
        new_y = self.y + direction[1]
        return math.sqrt((new_x - player.x)**2 + (new_y - player.y)**2)
    
    def rotate_left(self, direction):
        """Rotate direction 90 degrees counter-clockwise."""
        x, y = direction
        return (y, -x)
    
    def rotate_right(self, direction):
        """Rotate direction 90 degrees clockwise."""
        x, y = direction
        return (-y, x)
    
    def check_direction(self, direction, eggs, all_snakes=None):
        """Check if a direction is blocked by other snakes or boundaries."""
        next_x = self.x + direction[0]
        next_y = self.y + direction[1]
        
        # Check if next position is outside the play area
        if next_x < 0 or next_x >= 40 or next_y < 0 or next_y >= 25:
            return True
        
        # Check if next position has another snake
        if all_snakes:
            for other_snake in all_snakes:
                # Skip self
                if other_snake is self:
                    continue
                    
                # Check other snake's head
                if other_snake.position == (next_x, next_y):
                    return True
                
                # Check other snake's body
                for segment in other_snake.body:
                    if segment == (next_x, next_y):
                        return True
        
        # For non-eating snakes, eggs block movement
        if not self.can_eat_eggs:
            for egg in eggs:
                if egg.position == (next_x, next_y):
                    return True
        
        # Note: We no longer check for our own body - snakes can move over themselves
        
        return False
    
    def try_eat_egg(self, eggs, direction):
        """Try to eat an egg in the specified direction."""
        # If this snake can't eat eggs, return False
        if not self.can_eat_eggs:
            return False
            
        next_x = self.x + direction[0]
        next_y = self.y + direction[1]
        
        # Check if next position is outside the play area
        if next_x < 0 or next_x >= 40 or next_y < 0 or next_y >= 25:
            return False
        
        for egg in eggs[:]:  # Create a copy to safely modify during iteration
            if egg.position == (next_x, next_y):
                eggs.remove(egg)
                # Move to the position after eating
                self.x = next_x
                self.y = next_y
                return True
        return False
    
    def move(self):
        """Move the snake in its current direction."""
        self.x += self.direction[0]
        self.y += self.direction[1]
    
    def draw(self, screen, grid_size, y_offset=0):
        """Draw the snake on the screen."""
        # Draw body segments first (except head and tail)
        for i in range(1, len(self.body) - 1):
            segment_x, segment_y = self.body[i]
            
            # Body segments are slightly darker
            r, g, b = self.color
            darkness = 0.8  # 80% brightness for body
            color = (
                int(r * darkness), 
                int(g * darkness), 
                int(b * darkness)
            )
            
            # Draw body segment as a square
            rect = pygame.Rect(
                segment_x * grid_size + 1,
                segment_y * grid_size + y_offset + 1,
                grid_size - 2,
                grid_size - 2
            )
            pygame.draw.rect(screen, color, rect)
        
        # Draw tail (if there are enough segments)
        if len(self.body) > 1:
            tail_x, tail_y = self.body[-1]
            
            # Tail is even darker
            r, g, b = self.color
            darkness = 0.6  # 60% brightness for tail
            tail_color = (
                int(r * darkness), 
                int(g * darkness), 
                int(b * darkness)
            )
            
            # Draw tail as a triangle pointing in the direction it came from
            # Calculate direction from second-to-last segment to tail
            if len(self.body) > 2:
                prev_x, prev_y = self.body[-2]
                dx = tail_x - prev_x
                dy = tail_y - prev_y
            else:
                # If only head and tail, use inverse of head direction
                dx = -self.direction[0]
                dy = -self.direction[1]
            
            # Calculate triangle points
            center_x = (tail_x * grid_size) + (grid_size // 2)
            center_y = (tail_y * grid_size) + (grid_size // 2) + y_offset
            
            # Triangle base is perpendicular to movement direction
            if dx != 0:  # Moving horizontally
                # Triangle points up and down
                points = [
                    (center_x, center_y - grid_size // 3),  # Top
                    (center_x, center_y + grid_size // 3),  # Bottom
                    (center_x + (dx * grid_size // 3), center_y),  # Tip
                ]
            else:  # Moving vertically
                # Triangle points left and right
                points = [
                    (center_x - grid_size // 3, center_y),  # Left
                    (center_x + grid_size // 3, center_y),  # Right
                    # Tip pointing in the direction of movement
                    (center_x, center_y + (dy * grid_size // 3)),
                ]
            
            pygame.draw.polygon(screen, tail_color, points)
        
        # Draw head last (on top of everything)
        head_x, head_y = self.body[0]
        
        # Head is full brightness
        head_color = self.color
        
        # Draw head as a circle
        center_x = (head_x * grid_size) + (grid_size // 2)
        center_y = (head_y * grid_size) + (grid_size // 2) + y_offset
        radius = (grid_size - 2) // 2
        
        pygame.draw.circle(screen, head_color, (center_x, center_y), radius)
        
        # Draw eyes on the head
        eye_radius = radius // 3
        eye_color = (0, 0, 0)  # Black eyes
        
        # Position eyes based on direction
        if self.direction == (1, 0):  # Right
            left_eye = (center_x + radius // 2, center_y - radius // 2)
            right_eye = (center_x + radius // 2, center_y + radius // 2)
        elif self.direction == (-1, 0):  # Left
            left_eye = (center_x - radius // 2, center_y - radius // 2)
            right_eye = (center_x - radius // 2, center_y + radius // 2)
        elif self.direction == (0, 1):  # Down
            left_eye = (center_x - radius // 2, center_y + radius // 2)
            right_eye = (center_x + radius // 2, center_y + radius // 2)
        else:  # Up
            left_eye = (center_x - radius // 2, center_y - radius // 2)
            right_eye = (center_x + radius // 2, center_y - radius // 2)
        
        pygame.draw.circle(screen, eye_color, left_eye, eye_radius)
        pygame.draw.circle(screen, eye_color, right_eye, eye_radius)
        
        # Draw egg-eating indicator if active
        if self.can_eat_eggs:
            rect = pygame.Rect(
                head_x * grid_size + 1,
                head_y * grid_size + y_offset + 1,
                grid_size - 2,
                grid_size - 2
            )
            pygame.draw.rect(screen, (255, 0, 0), rect, 1)  # Red outline
    
    @property
    def position(self):
        """Get the current position of the snake."""
        return (self.x, self.y) 