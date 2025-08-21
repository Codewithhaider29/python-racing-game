import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultimate Flying Car Racing Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 255, 0)
ROAD_COLOR = (50, 50, 50)

# Game variables
player_speed = 8
base_enemy_speed = 5
enemy_speed_increase = 0.1
enemy_speed = base_enemy_speed
score = 0
high_score = 0
game_over = False
game_started = False
level = 1

# Flying mode variables
is_flying = False
fly_mode_timer = 0
fly_mode_duration = 300  # 5 seconds at 60 FPS
door_angle = 0  # For door animation

# Clock
clock = pygame.time.Clock()

# Fonts
font_large = pygame.font.SysFont("arial", 48, bold=True)
font_medium = pygame.font.SysFont("arial", 32)
font_small = pygame.font.SysFont("arial", 24)

# Road settings
road_width = 400
road_left = (WIDTH - road_width) // 2
road_right = road_left + road_width
lane_width = road_width // 3
lane_1 = road_left + lane_width // 2
lane_2 = road_left + lane_width + lane_width // 2
lane_3 = road_left + 2 * lane_width + lane_width // 2
lanes = [lane_1, lane_2, lane_3]

# Player car
class PlayerCar:
    def __init__(self):
        self.width = 50
        self.height = 100
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 150
        self.speed = player_speed
        self.color = RED
        self.lane = 1  # Middle lane
        self.fly_height = 0
        
    def draw(self):
        # Draw shadow when flying
        if is_flying:
            shadow_y = HEIGHT - 50
            pygame.draw.ellipse(screen, (30, 30, 30, 128), 
                               (self.x - 10, shadow_y, self.width + 20, 20))
        
        # Car body
        car_y = self.y - self.fly_height
        pygame.draw.rect(screen, self.color, (self.x, car_y, self.width, self.height), 0, 5)
        
        # Windows
        pygame.draw.rect(screen, BLACK, (self.x + 5, car_y + 5, self.width - 10, 20), 0, 3)
        pygame.draw.rect(screen, BLACK, (self.x + 5, car_y + 40, self.width - 10, 40), 0, 3)
        
        # Wheels (only show when not flying)
        if not is_flying:
            pygame.draw.rect(screen, BLACK, (self.x - 3, car_y + 10, 5, 20), 0, 2)
            pygame.draw.rect(screen, BLACK, (self.x - 3, car_y + 70, 5, 20), 0, 2)
            pygame.draw.rect(screen, BLACK, (self.x + self.width - 2, car_y + 10, 5, 20), 0, 2)
            pygame.draw.rect(screen, BLACK, (self.x + self.width - 2, car_y + 70, 5, 20), 0, 2)
        
        # Draw doors if flying
        if is_flying and door_angle > 0:
            # Left door
            door_left = pygame.Surface((self.width//2, self.height), pygame.SRCALPHA)
            pygame.draw.rect(door_left, self.color, (0, 0, self.width//2, self.height), 0, 5)
            pygame.draw.rect(door_left, BLACK, (5, 5, self.width//2 - 10, 15), 0, 3)
            door_left = pygame.transform.rotate(door_left, door_angle)
            screen.blit(door_left, (self.x, car_y))
            
            # Right door
            door_right = pygame.Surface((self.width//2, self.height), pygame.SRCALPHA)
            pygame.draw.rect(door_right, self.color, (0, 0, self.width//2, self.height), 0, 5)
            pygame.draw.rect(door_right, BLACK, (5, 5, self.width//2 - 10, 15), 0, 3)
            door_right = pygame.transform.rotate(door_right, -door_angle)
            screen.blit(door_right, (self.x + self.width//2, car_y))
        
    def move(self, direction):
        if direction == "left" and self.lane > 0:
            self.lane -= 1
        if direction == "right" and self.lane < 2:
            self.lane += 1
            
        target_x = lanes[self.lane] - self.width // 2
        # Smooth movement between lanes
        if self.x < target_x:
            self.x += min(self.speed, target_x - self.x)
        elif self.x > target_x:
            self.x -= min(self.speed, self.x - target_x)
    
    def update_fly_mode(self):
        global door_angle
        if is_flying:
            # Animate flying up
            if self.fly_height < 150:
                self.fly_height += 5
            
            # Animate doors opening
            if door_angle < 45:
                door_angle += 3
        else:
            # Animate flying down
            if self.fly_height > 0:
                self.fly_height -= 5
            
            # Animate doors closing
            if door_angle > 0:
                door_angle -= 3

# Enemy car
class EnemyCar:
    def __init__(self, lane):
        self.width = 50
        self.height = 100
        self.lane = lane
        self.x = lanes[lane] - self.width // 2
        self.y = -self.height
        self.speed = enemy_speed
        self.color = random.choice([BLUE, GREEN, YELLOW, (200, 100, 0), (150, 0, 200)])
        
    def draw(self):
        # Car body
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0, 5)
        # Windows
        pygame.draw.rect(screen, BLACK, (self.x + 5, self.y + 5, self.width - 10, 20), 0, 3)
        pygame.draw.rect(screen, BLACK, (self.x + 5, self.y + 40, self.width - 10, 40), 0, 3)
        # Wheels
        pygame.draw.rect(screen, BLACK, (self.x - 3, self.y + 10, 5, 20), 0, 2)
        pygame.draw.rect(screen, BLACK, (self.x - 3, self.y + 70, 5, 20), 0, 2)
        pygame.draw.rect(screen, BLACK, (self.x + self.width - 2, self.y + 10, 5, 20), 0, 2)
        pygame.draw.rect(screen, BLACK, (self.x + self.width - 2, self.y + 70, 5, 20), 0, 2)
        
    def update(self):
        self.y += self.speed
        return self.y > HEIGHT

# Road markings
class RoadMarking:
    def __init__(self, y):
        self.width = 10
        self.height = 50
        self.x = WIDTH // 2 - self.width // 2
        self.y = y
        self.speed = enemy_speed
        
    def draw(self):
        pygame.draw.rect(screen, YELLOW, (self.x, self.y, self.width, self.height))
        
    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = -self.height
            return True
        return False

# Initialize game objects
player = PlayerCar()
enemies = []
road_markings = []

# Create initial road markings
for i in range(-1, 12):
    road_markings.append(RoadMarking(i * 100))

# Game functions
def draw_road():
    # Draw road
    pygame.draw.rect(screen, ROAD_COLOR, (road_left, 0, road_width, HEIGHT))
    
    # Draw road markings
    for marking in road_markings:
        marking.draw()
    
    # Draw road edges
    pygame.draw.rect(screen, YELLOW, (road_left - 5, 0, 5, HEIGHT))
    pygame.draw.rect(screen, YELLOW, (road_right, 0, 5, HEIGHT))

def draw_hud():
    # Draw score
    score_text = font_small.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (20, 20))
    
    # Draw high score
    high_score_text = font_small.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(high_score_text, (20, 60))
    
    # Draw level
    level_text = font_small.render(f"Level: {level}", True, WHITE)
    screen.blit(level_text, (20, 100))
    
    # Draw speed
    speed_text = font_small.render(f"Speed: {enemy_speed:.1f} mph", True, WHITE)
    screen.blit(speed_text, (WIDTH - 200, 20))
    
    # Draw fly mode status
    if is_flying:
        fly_text = font_small.render(f"FLY MODE: {fly_mode_timer//60}s", True, GREEN)
        screen.blit(fly_text, (WIDTH - 200, 60))

def draw_game_over():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    game_over_text = font_large.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
    
    score_text = font_medium.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    
    high_score_text = font_medium.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 50))
    
    restart_text = font_medium.render("Press SPACE to restart", True, GREEN)
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 120))

def draw_start_screen():
    screen.fill(BLACK)
    
    title_text = font_large.render("FLYING CAR RACER", True, RED)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 100))
    
    start_text = font_medium.render("Press SPACE to start", True, GREEN)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
    
    controls_text = font_small.render("Use LEFT/RIGHT arrows to change lanes", True, WHITE)
    screen.blit(controls_text, (WIDTH // 2 - controls_text.get_width() // 2, HEIGHT // 2 + 60))
    
    fly_text = font_small.render("Press UP arrow to activate FLY MODE", True, BLUE)
    screen.blit(fly_text, (WIDTH // 2 - fly_text.get_width() // 2, HEIGHT // 2 + 90))
    
    # Draw a sample car
    pygame.draw.rect(screen, RED, (WIDTH // 2 - 25, HEIGHT // 2 + 120, 50, 100), 0, 5)

def check_collision():
    if is_flying:  # No collisions when flying
        return False
        
    for enemy in enemies:
        # Simple collision detection
        if (player.x < enemy.x + enemy.width and
            player.x + player.width > enemy.x and
            player.y < enemy.y + enemy.height and
            player.y + player.height > enemy.y):
            return True
    return False

def reset_game():
    global score, enemy_speed, game_over, level, enemies, is_flying, fly_mode_timer, door_angle
    score = 0
    enemy_speed = base_enemy_speed
    game_over = False
    level = 1
    is_flying = False
    fly_mode_timer = 0
    door_angle = 0
    enemies.clear()
    player.x = WIDTH // 2 - player.width // 2
    player.y = HEIGHT - 150
    player.lane = 1
    player.fly_height = 0

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    reset_game()
                elif not game_started:
                    game_started = True
            if event.key == pygame.K_UP and game_started and not game_over:
                if not is_flying:  # Activate fly mode
                    is_flying = True
                    fly_mode_timer = fly_mode_duration
    
    # Get key states
    keys = pygame.key.get_pressed()
    if game_started and not game_over:
        if keys[pygame.K_LEFT]:
            player.move("left")
        if keys[pygame.K_RIGHT]:
            player.move("right")
    
    # Update fly mode
    if is_flying:
        fly_mode_timer -= 1
        if fly_mode_timer <= 0:
            is_flying = False
    
    player.update_fly_mode()
    
    # Draw background
    screen.fill(BLACK)
    
    if not game_started:
        draw_start_screen()
    else:
        # Update road markings
        for marking in road_markings:
            marking.speed = enemy_speed
            marking.update()
        
        # Draw road
        draw_road()
        
        # Draw player
        player.draw()
        
        # Spawn enemies
        if random.random() < 0.03:  # 3% chance each frame
            lane = random.randint(0, 2)
            # Don't spawn if there's already a car in that lane at the top
            can_spawn = True
            for enemy in enemies:
                if enemy.lane == lane and enemy.y < 100:
                    can_spawn = False
                    break
            if can_spawn:
                enemies.append(EnemyCar(lane))
        
        # Update and draw enemies
        for enemy in enemies[:]:
            if enemy.update():
                enemies.remove(enemy)
                score += 1
            else:
                enemy.draw()
        
        # Check for collisions
        if check_collision():
            game_over = True
            high_score = max(high_score, score)
        
        # Increase difficulty with score
        if score > level * 10:
            level += 1
            enemy_speed += enemy_speed_increase
        
        # Draw HUD
        draw_hud()
        
        # Draw game over screen if game is over
        if game_over:
            draw_game_over()
    
    # Update display
    pygame.display.update()
    
    # Cap the frame rate
    clock.tick(60)

pygame.quit()