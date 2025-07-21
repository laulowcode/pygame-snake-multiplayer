from enum import Enum

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class PowerUpType(Enum):
    SPEED_BOOST = "speed_boost"
    GROW = "grow"
    SHRINK_OPPONENT = "shrink_opponent"

class GameState(Enum):
    NAME_INPUT = "name_input"
    PLAYING = "playing"
    GAME_OVER = "game_over" 