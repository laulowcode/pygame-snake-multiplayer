import pygame
from typing import Tuple
from ..constants import *

class Obstacle:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.color = GRAY
    
    def get_position(self) -> Tuple[int, int]:
        return (self.x, self.y)
    
    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, 
                        (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)) 