import pygame
from typing import Tuple, List
from ..enums import Direction
from ..constants import *

class Snake:
    def __init__(self, start_x: int, start_y: int, color: Tuple[int, int, int], player_id: int):
        self.body = [(start_x, start_y)]
        self.direction = Direction.RIGHT
        self.color = color
        self.player_id = player_id
        self.score = 0
        self.speed_boost_end = 0
        self.alive = True
        self.death_time = 0
        self.death_reason = ""
        
    def move(self, grow: bool = False):
        """Move the snake, optionally growing"""
        if not self.alive:
            return
            
        head_x, head_y = self.body[0]
        dx, dy = self.direction.value
        new_x = head_x + dx
        new_y = head_y + dy
        
        # Wrap around walls (teleport to opposite side)
        if new_x < 0:
            new_x = GRID_WIDTH - 1
        elif new_x >= GRID_WIDTH:
            new_x = 0
            
        if new_y < 0:
            new_y = GRID_HEIGHT - 1
        elif new_y >= GRID_HEIGHT:
            new_y = 0
        
        # Add new head
        self.body.insert(0, (new_x, new_y))
        
        # Only remove tail if not growing
        if not grow:
            self.body.pop()
    
    def get_head(self) -> Tuple[int, int]:
        return self.body[0] if self.body else (0, 0)
    
    def change_direction(self, new_direction: Direction):
        # Prevent moving in the opposite direction
        current_dx, current_dy = self.direction.value
        new_dx, new_dy = new_direction.value
        
        if (current_dx, current_dy) != (-new_dx, -new_dy):
            self.direction = new_direction
    
    def check_self_collision(self) -> bool:
        head = self.get_head()
        return head in self.body[1:]
    
    def check_collision_with_snake(self, other_snake: 'Snake') -> bool:
        head = self.get_head()
        return head in other_snake.body
    
    def check_collision_with_obstacles(self, obstacles: List['Obstacle']) -> bool:
        head = self.get_head()
        return any(head == (obs.x, obs.y) for obs in obstacles)
    
    def grow(self, segments: int = 1):
        """Manually grow the snake by adding segments to the tail"""
        if not self.body:
            return
            
        tail = self.body[-1]
        for _ in range(segments):
            self.body.append(tail)
    
    def shrink(self, segments: int = 1):
        """Shrink the snake by removing segments from the tail"""
        if len(self.body) <= 1:
            return
            
        for _ in range(min(segments, len(self.body) - 1)):
            self.body.pop()
    
    def apply_speed_boost(self, duration: int = 3000):
        self.speed_boost_end = pygame.time.get_ticks() + duration
    
    def has_speed_boost(self) -> bool:
        return pygame.time.get_ticks() < self.speed_boost_end
    
    def kill(self, reason: str):
        """Kill the snake with a specific reason"""
        if self.alive:
            self.alive = False
            self.death_time = pygame.time.get_ticks()
            self.death_reason = reason
    
    def draw(self, screen: pygame.Surface):
        # Determine if snake should be visible (blinking effect when dead)
        visible = True
        if not self.alive:
            # Blinking effect - faster blinking for first 2 seconds, then slower
            time_since_death = pygame.time.get_ticks() - self.death_time
            if time_since_death < 2000:  # First 2 seconds - fast blink
                visible = (pygame.time.get_ticks() // 150) % 2 == 0
            elif time_since_death < 4000:  # Next 2 seconds - slower blink  
                visible = (pygame.time.get_ticks() // 300) % 2 == 0
            else:  # After 4 seconds - very slow blink
                visible = (pygame.time.get_ticks() // 500) % 2 == 0
        
        if not visible:
            return
            
        # Draw body
        for i, (x, y) in enumerate(self.body):
            if i == 0:  # Head
                # Make head brighter, or dim if dead
                if self.alive:
                    head_color = tuple(min(255, c + 50) for c in self.color)
                else:
                    head_color = tuple(max(0, c - 100) for c in self.color)  # Dim when dead
                
                pygame.draw.rect(screen, head_color, 
                               (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                
                # Draw eyes (X eyes when dead, normal when alive)
                if self.alive:
                    eye_size = 3
                    pygame.draw.circle(screen, BLACK, 
                                     (x * GRID_SIZE + 5, y * GRID_SIZE + 5), eye_size)
                    pygame.draw.circle(screen, BLACK, 
                                     (x * GRID_SIZE + GRID_SIZE - 5, y * GRID_SIZE + 5), eye_size)
                else:
                    # Draw X eyes when dead
                    pygame.draw.line(screen, RED, 
                                   (x * GRID_SIZE + 3, y * GRID_SIZE + 3),
                                   (x * GRID_SIZE + 9, y * GRID_SIZE + 9), 2)
                    pygame.draw.line(screen, RED, 
                                   (x * GRID_SIZE + 9, y * GRID_SIZE + 3),
                                   (x * GRID_SIZE + 3, y * GRID_SIZE + 9), 2)
                    pygame.draw.line(screen, RED, 
                                   (x * GRID_SIZE + GRID_SIZE - 9, y * GRID_SIZE + 3),
                                   (x * GRID_SIZE + GRID_SIZE - 3, y * GRID_SIZE + 9), 2)
                    pygame.draw.line(screen, RED, 
                                   (x * GRID_SIZE + GRID_SIZE - 3, y * GRID_SIZE + 3),
                                   (x * GRID_SIZE + GRID_SIZE - 9, y * GRID_SIZE + 9), 2)
            else:  # Body
                if self.alive:
                    body_color = self.color
                    # Add glowing effect during speed boost
                    if self.has_speed_boost():
                        glow = int(pygame.time.get_ticks() / 100) % 50
                        body_color = tuple(min(255, c + glow) for c in self.color)
                else:
                    # Dim body when dead
                    body_color = tuple(max(0, c - 100) for c in self.color)
                
                pygame.draw.rect(screen, body_color, 
                               (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)) 