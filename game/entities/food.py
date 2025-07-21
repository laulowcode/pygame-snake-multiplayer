import pygame
import random
from typing import Tuple
from ..constants import *

class Food:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.color = RED
        self.respawn()
    
    def respawn(self):
        self.x = random.randint(0, GRID_WIDTH - 1)
        self.y = random.randint(0, GRID_HEIGHT - 1)
    
    def get_position(self) -> Tuple[int, int]:
        return (self.x, self.y)
    
    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, 
                        (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)) 