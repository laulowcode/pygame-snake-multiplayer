#!/usr/bin/env python3
"""
Two-Player Snake Game
A multiplayer snake game built with pygame featuring power-ups, obstacles, and player naming.
"""

import pygame
import sys
from game import Game

def main():
    """Main entry point for the snake game."""
    # Initialize Pygame
    pygame.init()
    
    try:
        # Create and run the game
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    finally:
        pygame.quit()

if __name__ == "__main__":
    main() 