import pygame
import random
from typing import Tuple
from ..enums import PowerUpType
from ..constants import *

class PowerUp:
    def __init__(self, power_type: PowerUpType):
        self.x = 0
        self.y = 0
        self.power_type = power_type
        self.duration = 5000  # Duration in milliseconds
        
        # Set color based on power-up type
        if power_type == PowerUpType.SPEED_BOOST:
            self.color = CYAN
        elif power_type == PowerUpType.GROW:
            self.color = PURPLE
        elif power_type == PowerUpType.SHRINK_OPPONENT:
            self.color = ORANGE
        
        self.respawn()
    
    def respawn(self):
        self.x = random.randint(0, GRID_WIDTH - 1)
        self.y = random.randint(0, GRID_HEIGHT - 1)
    
    def get_position(self) -> Tuple[int, int]:
        return (self.x, self.y)
    
    def draw(self, screen: pygame.Surface):
        # Draw power-up with a pulsing effect
        pulse = int(pygame.time.get_ticks() / 200) % 2
        size = GRID_SIZE if pulse else GRID_SIZE - 4
        offset = (GRID_SIZE - size) // 2
        pygame.draw.rect(screen, self.color, 
                        (self.x * GRID_SIZE + offset, self.y * GRID_SIZE + offset, size, size)) 