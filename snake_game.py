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
    
    def draw(self, screen: pygame.Surface):
        if not self.alive:
            return
            
        # Draw body
        for i, (x, y) in enumerate(self.body):
            if i == 0:  # Head
                # Make head brighter
                head_color = tuple(min(255, c + 50) for c in self.color)
                pygame.draw.rect(screen, head_color, 
                               (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                # Draw eyes
                eye_size = 3
                pygame.draw.circle(screen, BLACK, 
                                 (x * GRID_SIZE + 5, y * GRID_SIZE + 5), eye_size)
                pygame.draw.circle(screen, BLACK, 
                                 (x * GRID_SIZE + GRID_SIZE - 5, y * GRID_SIZE + 5), eye_size)
            else:  # Body
                body_color = self.color
                # Add glowing effect during speed boost
                if self.has_speed_boost():
                    glow = int(pygame.time.get_ticks() / 100) % 50
                    body_color = tuple(min(255, c + glow) for c in self.color)
                
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

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Two-Player Snake Game")
        self.clock = pygame.time.Clock()
        
        # Initialize game objects
        self.snake1 = Snake(5, GRID_HEIGHT // 2, DARK_GREEN, 1)
        self.snake2 = Snake(GRID_WIDTH - 6, GRID_HEIGHT // 2, DARK_BLUE, 2)
        self.food = Food()
        self.power_ups: List[PowerUp] = []
        self.obstacles: List[Obstacle] = []
        
        # Game state
        self.base_speed = 120  # Lower is faster
        self.game_over = False
        self.winner = None
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Power-up spawn timer
        self.last_powerup_spawn = pygame.time.get_ticks()
        self.powerup_spawn_interval = 8000  # 8 seconds
        
        # Generate obstacles
        self.generate_obstacles()
        
        # Ensure food doesn't spawn on obstacles or snakes
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
        if self.snake1.check_self_collision():
            self.snake1.alive = False
        if self.snake2.check_self_collision():
            self.snake2.alive = False
        
        # Check collisions between snakes
        if self.snake1.check_collision_with_snake(self.snake2):
            self.snake1.alive = False
        if self.snake2.check_collision_with_snake(self.snake1):
            self.snake2.alive = False
        
        # Check obstacle collisions
        if self.snake1.check_collision_with_obstacles(self.obstacles):
            self.snake1.alive = False
        if self.snake2.check_collision_with_obstacles(self.obstacles):
            self.snake2.alive = False
        
        # Check for head-to-head collision (both snakes die)
        if (self.snake1.alive and self.snake2.alive and 
            self.snake1.get_head() == self.snake2.get_head()):
            self.snake1.alive = False
            self.snake2.alive = False
    
    def get_speed(self, snake: Snake) -> int:
        """Get current speed for a snake (accounts for speed boosts)"""
        if snake.has_speed_boost():
            return max(60, self.base_speed // 2)  # Double speed
        return self.base_speed
    
    def update_game_state(self):
        """Update win/lose conditions"""
        if not self.snake1.alive and not self.snake2.alive:
            self.game_over = True
            # Determine winner based on score
            if self.snake1.score > self.snake2.score:
                self.winner = "Player 1 (Green)"
            elif self.snake2.score > self.snake1.score:
                self.winner = "Player 2 (Blue)"
            else:
                self.winner = "Tie"
        elif not self.snake1.alive:
            self.game_over = True
            self.winner = "Player 2 (Blue)"
        elif not self.snake2.alive:
            self.game_over = True
            self.winner = "Player 1 (Green)"
    
    def draw_ui(self):
        """Draw score and game information"""
        # Scores
        score1_text = self.font.render(f"Player 1: {self.snake1.score}", True, WHITE)
        score2_text = self.font.render(f"Player 2: {self.snake2.score}", True, WHITE)
        
        self.screen.blit(score1_text, (10, 10))
        self.screen.blit(score2_text, (WINDOW_WIDTH - 200, 10))
        
        # Controls
        controls1 = self.small_font.render("P1: Arrow Keys", True, WHITE)
        controls2 = self.small_font.render("P2: WASD", True, WHITE)
        
        self.screen.blit(controls1, (10, WINDOW_HEIGHT - 50))
        self.screen.blit(controls2, (WINDOW_WIDTH - 150, WINDOW_HEIGHT - 50))
        
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
        winner_text = pygame.font.Font(None, 48).render(f"Winner: {self.winner}", True, WHITE)
        restart_text = self.font.render("Press R to restart or Q to quit", True, WHITE)
        
        # Center the text
        self.screen.blit(game_over_text, 
                        (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, 
                         WINDOW_HEIGHT // 2 - 100))
        self.screen.blit(winner_text, 
                        (WINDOW_WIDTH // 2 - winner_text.get_width() // 2, 
                         WINDOW_HEIGHT // 2 - 30))
        self.screen.blit(restart_text, 
                        (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, 
                         WINDOW_HEIGHT // 2 + 50))
    
    def restart_game(self):
        """Reset the game to initial state"""
        self.__init__()
    
    def run(self):
        """Main game loop"""
        running = True
        last_move_time1 = pygame.time.get_ticks()
        last_move_time2 = pygame.time.get_ticks()
        
        while running:
            current_time = pygame.time.get_ticks()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_r and self.game_over:
                        self.restart_game()
            
            if not self.game_over:
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
            
            # Draw everything
            self.screen.fill(BLACK)
            
            # Draw game objects
            for obstacle in self.obstacles:
                obstacle.draw(self.screen)
            
            self.food.draw(self.screen)
            
            for powerup in self.power_ups:
                powerup.draw(self.screen)
            
            self.snake1.draw(self.screen)
            self.snake2.draw(self.screen)
            
            # Draw UI
            self.draw_ui()
            
            # Draw game over screen if needed
            if self.game_over:
                self.draw_game_over()
            
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run() 