import pygame
import random
import sys
from enum import Enum
from typing import List, Tuple

# Initialize Pygame
pygame.init()

# Game constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
GRAY = (128, 128, 128)
DARK_GREEN = (0, 150, 0)
DARK_BLUE = (0, 0, 150)

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class PowerUpType(Enum):
    SPEED_BOOST = "speed_boost"
    GROW = "grow"
    SHRINK_OPPONENT = "shrink_opponent"

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

class GameState(Enum):
    NAME_INPUT = "name_input"
    PLAYING = "playing"
    GAME_OVER = "game_over"

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Two-Player Snake Game")
        self.clock = pygame.time.Clock()
        
        # Game state management
        self.game_state = GameState.NAME_INPUT
        self.first_time = True
        
        # Player names
        self.player1_name = "Player 1"
        self.player2_name = "Player 2"
        self.current_input_player = 1  # Which player is currently inputting name
        self.name_input = ""
        self.input_active = True
        
        # Win tracking
        self.player1_wins = 0
        self.player2_wins = 0
        
        # Initialize game objects
        self.snake1 = None
        self.snake2 = None
        self.food = None
        self.power_ups: List[PowerUp] = []
        self.obstacles: List[Obstacle] = []
        
        # Game state
        self.base_speed = 120  # Lower is faster
        self.game_over = False
        self.winner = None
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)
        
        # Death effect timing
        self.death_delay = 3000  # 3 seconds delay before showing game over
        self.first_death_time = 0
        
        # Power-up spawn timer
        self.last_powerup_spawn = 0
        self.powerup_spawn_interval = 8000  # 8 seconds
    
    def initialize_game_objects(self):
        """Initialize game objects when starting a new game"""
        self.snake1 = Snake(5, GRID_HEIGHT // 2, DARK_GREEN, 1)
        self.snake2 = Snake(GRID_WIDTH - 6, GRID_HEIGHT // 2, DARK_BLUE, 2)
        self.food = Food()
        self.power_ups = []
        self.obstacles = []
        
        # Game state reset
        self.game_over = False
        self.winner = None
        self.last_powerup_spawn = pygame.time.get_ticks()
        
        # Generate obstacles and ensure safe food spawn
        self.generate_obstacles()
        self.respawn_food_safely()
    
    def generate_obstacles(self):
        """Generate random obstacles on the board"""
        num_obstacles = random.randint(8, 15)
        
        for _ in range(num_obstacles):
            max_attempts = 50
            for _ in range(max_attempts):
                x = random.randint(2, GRID_WIDTH - 3)
                y = random.randint(2, GRID_HEIGHT - 3)
                
                # Make sure obstacles don't spawn on snakes' starting positions
                if (x, y) not in [(5, GRID_HEIGHT // 2), (GRID_WIDTH - 6, GRID_HEIGHT // 2)]:
                    self.obstacles.append(Obstacle(x, y))
                    break
    
    def respawn_food_safely(self):
        """Respawn food in a safe location away from obstacles and snakes"""
        max_attempts = 100
        for _ in range(max_attempts):
            self.food.respawn()
            food_pos = self.food.get_position()
            
            # Check if position is safe
            safe = True
            
            # Check against snakes
            if (food_pos in self.snake1.body or 
                food_pos in self.snake2.body):
                safe = False
            
            # Check against obstacles
            if any(food_pos == obs.get_position() for obs in self.obstacles):
                safe = False
            
            # Check against power-ups
            if any(food_pos == pu.get_position() for pu in self.power_ups):
                safe = False
            
            if safe:
                break
    
    def spawn_powerup(self):
        """Spawn a random power-up"""
        if len(self.power_ups) >= 2:  # Limit number of power-ups on screen
            return
            
        power_type = random.choice(list(PowerUpType))
        powerup = PowerUp(power_type)
        
        # Make sure power-up doesn't spawn on snakes, food, or obstacles
        max_attempts = 50
        for _ in range(max_attempts):
            powerup.respawn()
            pu_pos = powerup.get_position()
            
            safe = True
            if (pu_pos in self.snake1.body or 
                pu_pos in self.snake2.body or
                pu_pos == self.food.get_position() or
                any(pu_pos == obs.get_position() for obs in self.obstacles)):
                safe = False
            
            if safe:
                break
        
        self.power_ups.append(powerup)
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Player 1 controls (Arrow keys)
        if keys[pygame.K_UP]:
            self.snake1.change_direction(Direction.UP)
        elif keys[pygame.K_DOWN]:
            self.snake1.change_direction(Direction.DOWN)
        elif keys[pygame.K_LEFT]:
            self.snake1.change_direction(Direction.LEFT)
        elif keys[pygame.K_RIGHT]:
            self.snake1.change_direction(Direction.RIGHT)
        
        # Player 2 controls (WASD)
        if keys[pygame.K_w]:
            self.snake2.change_direction(Direction.UP)
        elif keys[pygame.K_s]:
            self.snake2.change_direction(Direction.DOWN)
        elif keys[pygame.K_a]:
            self.snake2.change_direction(Direction.LEFT)
        elif keys[pygame.K_d]:
            self.snake2.change_direction(Direction.RIGHT)
    
    def check_will_eat_food(self, snake: Snake) -> bool:
        """Check if snake will eat food on next move"""
        head_x, head_y = snake.get_head()
        dx, dy = snake.direction.value
        new_x = head_x + dx
        new_y = head_y + dy
        
        # Handle wall wrapping
        if new_x < 0:
            new_x = GRID_WIDTH - 1
        elif new_x >= GRID_WIDTH:
            new_x = 0
        if new_y < 0:
            new_y = GRID_HEIGHT - 1
        elif new_y >= GRID_HEIGHT:
            new_y = 0
        
        return (new_x, new_y) == self.food.get_position()
    
    def check_powerup_collisions(self):
        """Check if either snake collected a power-up"""
        for powerup in self.power_ups[:]:  # Create a copy to iterate over
            powerup_pos = powerup.get_position()
            
            snake_that_collected = None
            other_snake = None
            
            if self.snake1.get_head() == powerup_pos:
                snake_that_collected = self.snake1
                other_snake = self.snake2
            elif self.snake2.get_head() == powerup_pos:
                snake_that_collected = self.snake2
                other_snake = self.snake1
            
            if snake_that_collected:
                # Apply power-up effect
                if powerup.power_type == PowerUpType.SPEED_BOOST:
                    snake_that_collected.apply_speed_boost()
                elif powerup.power_type == PowerUpType.GROW:
                    snake_that_collected.grow(2)  # Grow by 2 segments
                elif powerup.power_type == PowerUpType.SHRINK_OPPONENT:
                    other_snake.shrink(2)  # Shrink opponent by 2 segments
                
                snake_that_collected.score += 5  # Bonus points for power-ups
                self.power_ups.remove(powerup)
    
    def check_collisions(self):
        """Check all deadly collision scenarios"""
        # Check self collisions
        if self.snake1.alive and self.snake1.check_self_collision():
            self.snake1.kill(f"{self.player1_name} ran into themselves!")
            if self.first_death_time == 0:
                self.first_death_time = pygame.time.get_ticks()
                
        if self.snake2.alive and self.snake2.check_self_collision():
            self.snake2.kill(f"{self.player2_name} ran into themselves!")
            if self.first_death_time == 0:
                self.first_death_time = pygame.time.get_ticks()
        
        # Check for head-to-head collision FIRST (both snakes die)
        if (self.snake1.alive and self.snake2.alive and 
            self.snake1.get_head() == self.snake2.get_head()):
            self.snake1.kill(f"{self.player1_name} collided head-to-head!")
            self.snake2.kill(f"{self.player2_name} collided head-to-head!")
            if self.first_death_time == 0:
                self.first_death_time = pygame.time.get_ticks()
        
        # Check collisions between snakes (avoid head-to-head double-kill)
        elif self.snake1.alive and self.snake1.check_collision_with_snake(self.snake2):
            self.snake1.kill(f"{self.player1_name} ran into {self.player2_name}!")
            if self.first_death_time == 0:
                self.first_death_time = pygame.time.get_ticks()
                
        elif self.snake2.alive and self.snake2.check_collision_with_snake(self.snake1):
            self.snake2.kill(f"{self.player2_name} ran into {self.player1_name}!")  
            if self.first_death_time == 0:
                self.first_death_time = pygame.time.get_ticks()
        
        # Check obstacle collisions
        if self.snake1.alive and self.snake1.check_collision_with_obstacles(self.obstacles):
            self.snake1.kill(f"{self.player1_name} hit an obstacle!")
            if self.first_death_time == 0:
                self.first_death_time = pygame.time.get_ticks()
                
        if self.snake2.alive and self.snake2.check_collision_with_obstacles(self.obstacles):
            self.snake2.kill(f"{self.player2_name} hit an obstacle!")
            if self.first_death_time == 0:
                self.first_death_time = pygame.time.get_ticks()
    
    def get_speed(self, snake: Snake) -> int:
        """Get current speed for a snake (accounts for speed boosts)"""
        if snake.has_speed_boost():
            return max(60, self.base_speed // 2)  # Double speed
        return self.base_speed
    
    def update_game_state(self):
        """Update win/lose conditions"""
        if not self.snake1.alive and not self.snake2.alive:
            if not self.game_over:  # Only update wins on first game over
                # Determine winner based on score
                if self.snake1.score > self.snake2.score:
                    self.winner = "Player 1 (Green)"
                    self.player1_wins += 1
                elif self.snake2.score > self.snake1.score:
                    self.winner = "Player 2 (Blue)"
                    self.player2_wins += 1
                else:
                    self.winner = "Tie"
                    # No wins added for tie
            self.game_over = True
        elif not self.snake1.alive:
            if not self.game_over:  # Only update wins on first game over
                self.winner = "Player 2 (Blue)"
                self.player2_wins += 1
            self.game_over = True
        elif not self.snake2.alive:
            if not self.game_over:  # Only update wins on first game over
                self.winner = "Player 1 (Green)"
                self.player1_wins += 1
            self.game_over = True
    
    def draw_name_input_screen(self):
        """Draw the name input screen"""
        self.screen.fill(BLACK)
        
        # Title
        title = self.large_font.render("Snake Game 2 Players", True, WHITE)
        self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 100))
        
        if self.first_time:
            subtitle = self.font.render("Enter player names to start!", True, WHITE)
            self.screen.blit(subtitle, (WINDOW_WIDTH // 2 - subtitle.get_width() // 2, 150))
        else:
            subtitle = self.font.render("Edit player names", True, WHITE)
            self.screen.blit(subtitle, (WINDOW_WIDTH // 2 - subtitle.get_width() // 2, 150))
        
        # Current names and wins
        name1_label = self.font.render(f"Player 1: {self.player1_name} ({self.player1_wins} wins)", True, DARK_GREEN)
        name2_label = self.font.render(f"Player 2: {self.player2_name} ({self.player2_wins} wins)", True, DARK_BLUE)
        
        self.screen.blit(name1_label, (WINDOW_WIDTH // 2 - name1_label.get_width() // 2, 220))
        self.screen.blit(name2_label, (WINDOW_WIDTH // 2 - name2_label.get_width() // 2, 260))
        
        # Current input
        if self.input_active:
            current_player_text = f"Enter name for Player {self.current_input_player}:"
            current_label = self.font.render(current_player_text, True, WHITE)
            self.screen.blit(current_label, (WINDOW_WIDTH // 2 - current_label.get_width() // 2, 320))
            
            # Input box
            input_box_width = 300
            input_box_height = 40
            input_box_x = WINDOW_WIDTH // 2 - input_box_width // 2
            input_box_y = 360
            
            # Draw input box
            pygame.draw.rect(self.screen, WHITE, (input_box_x, input_box_y, input_box_width, input_box_height), 2)
            
            # Draw current input text
            input_text = self.font.render(self.name_input, True, WHITE)
            self.screen.blit(input_text, (input_box_x + 10, input_box_y + 10))
            
            # Draw cursor
            cursor_x = input_box_x + 10 + input_text.get_width()
            if pygame.time.get_ticks() % 1000 < 500:  # Blinking cursor
                pygame.draw.line(self.screen, WHITE, (cursor_x, input_box_y + 5), (cursor_x, input_box_y + 35), 2)
        
        # Instructions
        instructions = [
            "Press ENTER to confirm name",
            "Press TAB to skip to next player", 
            "Press SPACE to start game with current names",
            "Press C to reset win count",
            "Press ESC to start with default names" if self.first_time else "Press ESC to return to game"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = self.small_font.render(instruction, True, WHITE)
            self.screen.blit(inst_text, (WINDOW_WIDTH // 2 - inst_text.get_width() // 2, 450 + i * 25))
    
    def draw_ui(self):
        """Draw score and game information"""
        # Current game scores with player names
        score1_text = self.font.render(f"{self.player1_name}: {self.snake1.score}", True, WHITE)
        score2_text = self.font.render(f"{self.player2_name}: {self.snake2.score}", True, WHITE)
        
        self.screen.blit(score1_text, (10, 10))
        self.screen.blit(score2_text, (WINDOW_WIDTH - 250, 10))
        
        # Win tracking (overall wins)
        wins1_text = self.small_font.render(f"Wins: {self.player1_wins}", True, DARK_GREEN)
        wins2_text = self.small_font.render(f"Wins: {self.player2_wins}", True, DARK_BLUE)
        
        self.screen.blit(wins1_text, (10, 40))
        self.screen.blit(wins2_text, (WINDOW_WIDTH - 100, 40))
        
        # Controls  
        controls1 = self.small_font.render(f"{self.player1_name}: Arrow Keys", True, WHITE)
        controls2 = self.small_font.render(f"{self.player2_name}: WASD", True, WHITE)
        
        self.screen.blit(controls1, (10, WINDOW_HEIGHT - 50))
        self.screen.blit(controls2, (WINDOW_WIDTH - 200, WINDOW_HEIGHT - 50))
        
        # Speed boost indicators
        if self.snake1.has_speed_boost():
            boost1 = self.small_font.render("SPEED BOOST!", True, CYAN)
            self.screen.blit(boost1, (10, 50))
        
        if self.snake2.has_speed_boost():
            boost2 = self.small_font.render("SPEED BOOST!", True, CYAN)
            self.screen.blit(boost2, (WINDOW_WIDTH - 150, 50))
        
        # Power-up legend
        legend_y = WINDOW_HEIGHT - 120
        legend_items = [
            ("Speed Boost", CYAN),
            ("Grow", PURPLE),
            ("Shrink Enemy", ORANGE)
        ]
        
        legend_title = self.small_font.render("Power-ups:", True, WHITE)
        self.screen.blit(legend_title, (WINDOW_WIDTH // 2 - 50, legend_y))
        
        for i, (name, color) in enumerate(legend_items):
            y_pos = legend_y + 25 + i * 20
            pygame.draw.rect(self.screen, color, (WINDOW_WIDTH // 2 - 50, y_pos, 15, 15))
            text = self.small_font.render(name, True, WHITE)
            self.screen.blit(text, (WINDOW_WIDTH // 2 - 30, y_pos))
    
    def draw_game_over(self):
        """Draw game over screen"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = pygame.font.Font(None, 72).render("GAME OVER", True, WHITE)
        
        # Show winner with actual name
        winner_display = self.winner
        if self.winner == "Player 1 (Green)":
            winner_display = f"{self.player1_name} (Green)"
        elif self.winner == "Player 2 (Blue)":
            winner_display = f"{self.player2_name} (Blue)"
        
        winner_text = pygame.font.Font(None, 48).render(f"Winner: {winner_display}", True, WHITE)
        
        # Final scores
        final_score1 = self.font.render(f"{self.player1_name}: {self.snake1.score} points", True, DARK_GREEN)
        final_score2 = self.font.render(f"{self.player2_name}: {self.snake2.score} points", True, DARK_BLUE)
        
        # Overall win tracking
        overall_wins1 = self.font.render(f"{self.player1_name}: {self.player1_wins} wins", True, DARK_GREEN)
        overall_wins2 = self.font.render(f"{self.player2_name}: {self.player2_wins} wins", True, DARK_BLUE)
        
        # Instructions
        restart_text = self.font.render("Press R to restart", True, WHITE)
        name_text = self.font.render("Press N to change names", True, WHITE)
        reset_text = self.font.render("Press C to reset win count", True, WHITE)
        quit_text = self.font.render("Press Q to quit", True, WHITE)
        
        # Center the text
        self.screen.blit(game_over_text, 
                        (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, 
                         WINDOW_HEIGHT // 2 - 140))
        self.screen.blit(winner_text, 
                        (WINDOW_WIDTH // 2 - winner_text.get_width() // 2, 
                         WINDOW_HEIGHT // 2 - 70))
        
        # Final scores this game
        self.screen.blit(final_score1, 
                        (WINDOW_WIDTH // 2 - final_score1.get_width() // 2, 
                         WINDOW_HEIGHT // 2 - 30))
        self.screen.blit(final_score2, 
                        (WINDOW_WIDTH // 2 - final_score2.get_width() // 2, 
                         WINDOW_HEIGHT // 2))
        
        # Overall win counts
        self.screen.blit(overall_wins1, 
                        (WINDOW_WIDTH // 2 - overall_wins1.get_width() // 2, 
                         WINDOW_HEIGHT // 2 + 40))
        self.screen.blit(overall_wins2, 
                        (WINDOW_WIDTH // 2 - overall_wins2.get_width() // 2, 
                         WINDOW_HEIGHT // 2 + 70))
        
        # Instructions
        self.screen.blit(restart_text, 
                        (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, 
                         WINDOW_HEIGHT // 2 + 110))
        self.screen.blit(name_text, 
                        (WINDOW_WIDTH // 2 - name_text.get_width() // 2, 
                         WINDOW_HEIGHT // 2 + 140))
        self.screen.blit(reset_text, 
                        (WINDOW_WIDTH // 2 - reset_text.get_width() // 2, 
                         WINDOW_HEIGHT // 2 + 170))
        self.screen.blit(quit_text, 
                        (WINDOW_WIDTH // 2 - quit_text.get_width() // 2, 
                         WINDOW_HEIGHT // 2 + 200))
    
    def handle_name_input(self, event):
        """Handle text input for player names"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Enter - confirm current name
                if self.name_input.strip():
                    if self.current_input_player == 1:
                        self.player1_name = self.name_input.strip()
                    else:
                        self.player2_name = self.name_input.strip()
                
                self.name_input = ""
                if self.current_input_player == 1:
                    self.current_input_player = 2
                else:
                    self.current_input_player = 1
                    
            elif event.key == pygame.K_TAB:  # Tab - skip to next player
                self.current_input_player = 2 if self.current_input_player == 1 else 1
                self.name_input = ""
                
            elif event.key == pygame.K_SPACE:  # Space - start game with current names
                self.start_game()
                
            elif event.key == pygame.K_c:  # C - reset win count
                self.reset_win_count()
                
            elif event.key == pygame.K_ESCAPE:  # Escape - start with defaults or return
                if self.first_time:
                    self.start_game()
                else:
                    self.game_state = GameState.GAME_OVER
                    
            elif event.key == pygame.K_BACKSPACE:  # Backspace - delete character
                self.name_input = self.name_input[:-1]
                
            else:
                # Add character to input (limit length)
                if len(self.name_input) < 15 and event.unicode.isprintable():
                    self.name_input += event.unicode
    
    def start_game(self):
        """Start a new game"""
        self.game_state = GameState.PLAYING
        self.first_time = False
        self.input_active = False
        self.initialize_game_objects()
    
    def restart_game(self):
        """Restart the current game with same names"""
        self.initialize_game_objects()
        self.game_state = GameState.PLAYING
    
    def go_to_name_input(self):
        """Go to name input screen"""
        self.game_state = GameState.NAME_INPUT
        self.input_active = True
        self.current_input_player = 1
        self.name_input = ""
    
    def reset_win_count(self):
        """Reset win count for both players"""
        self.player1_wins = 0
        self.player2_wins = 0
    
    def run(self):
        """Main game loop"""
        running = True
        last_move_time1 = pygame.time.get_ticks()
        last_move_time2 = pygame.time.get_ticks()
        
        while running:
            current_time = pygame.time.get_ticks()
            
            # Handle events based on current state
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif self.game_state == GameState.NAME_INPUT:
                    self.handle_name_input(event)
                
                elif self.game_state == GameState.PLAYING:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            running = False
                
                elif self.game_state == GameState.GAME_OVER:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            running = False
                        elif event.key == pygame.K_r:
                            self.restart_game()
                        elif event.key == pygame.K_n:
                            self.go_to_name_input()
                        elif event.key == pygame.K_c:
                            self.reset_win_count()
            
            # Game logic based on current state
            if self.game_state == GameState.PLAYING and not self.game_over:
                # Handle continuous input
                self.handle_input()
                
                # Get current speeds
                speed1 = self.get_speed(self.snake1)
                speed2 = self.get_speed(self.snake2)
                
                # Check if snakes will eat food and move them accordingly
                if current_time - last_move_time1 >= speed1:
                    will_eat = self.check_will_eat_food(self.snake1)
                    self.snake1.move(grow=will_eat)
                    
                    if will_eat:
                        self.snake1.score += 10
                        self.respawn_food_safely()
                    
                    last_move_time1 = current_time
                
                if current_time - last_move_time2 >= speed2:
                    will_eat = self.check_will_eat_food(self.snake2)
                    self.snake2.move(grow=will_eat)
                    
                    if will_eat:
                        self.snake2.score += 10
                        self.respawn_food_safely()
                    
                    last_move_time2 = current_time
                
                # Check power-up collisions
                self.check_powerup_collisions()
                
                # Check deadly collisions
                self.check_collisions()
                
                # Spawn power-ups
                if current_time - self.last_powerup_spawn >= self.powerup_spawn_interval:
                    self.spawn_powerup()
                    self.last_powerup_spawn = current_time
                
                # Update game state
                self.update_game_state()
                if self.game_over:
                    self.game_state = GameState.GAME_OVER
            
            # Draw based on current state
            if self.game_state == GameState.NAME_INPUT:
                self.draw_name_input_screen()
            
            elif self.game_state == GameState.PLAYING:
                # Draw everything
                self.screen.fill(BLACK)
                
                # Draw game objects
                if self.obstacles:
                    for obstacle in self.obstacles:
                        obstacle.draw(self.screen)
                
                if self.food:
                    self.food.draw(self.screen)
                
                for powerup in self.power_ups:
                    powerup.draw(self.screen)
                
                if self.snake1:
                    self.snake1.draw(self.screen)
                if self.snake2:
                    self.snake2.draw(self.screen)
                
                # Draw UI
                self.draw_ui()
            
            elif self.game_state == GameState.GAME_OVER:
                # Draw game (faded) with game over overlay
                self.screen.fill(BLACK)
                
                # Draw faded game objects
                if self.obstacles:
                    for obstacle in self.obstacles:
                        obstacle.draw(self.screen)
                
                if self.food:
                    self.food.draw(self.screen)
                
                for powerup in self.power_ups:
                    powerup.draw(self.screen)
                
                if self.snake1:
                    self.snake1.draw(self.screen)
                if self.snake2:
                    self.snake2.draw(self.screen)
                
                # Draw UI
                self.draw_ui()
                
                # Draw game over screen
                self.draw_game_over()
            
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run() 