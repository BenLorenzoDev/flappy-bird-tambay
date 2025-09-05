import pygame
import random
import sys
from enum import Enum

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
GRID_SIZE = 15
GRID_HEIGHT = 11
CELL_SIZE = 40
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
BROWN = (139, 69, 19)

class CellType(Enum):
    EMPTY = 0
    WALL = 1
    BRICK = 2
    BOMB = 3
    EXPLOSION = 4
    POWER_UP = 5

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Player:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.x = x * CELL_SIZE + CELL_SIZE // 2
        self.y = y * CELL_SIZE + CELL_SIZE // 2
        self.speed = 2
        self.bomb_count = 1
        self.bomb_power = 2
        self.max_bombs = 1
        self.placed_bombs = []
        self.alive = True
        self.move_cooldown = 0
        
    def move(self, dx, dy, game_map):
        if self.move_cooldown > 0:
            return
            
        new_grid_x = self.grid_x + dx
        new_grid_y = self.grid_y + dy
        
        if (0 <= new_grid_x < GRID_SIZE and 
            0 <= new_grid_y < GRID_HEIGHT and
            game_map[new_grid_y][new_grid_x] in [CellType.EMPTY, CellType.POWER_UP]):
            
            if game_map[new_grid_y][new_grid_x] == CellType.POWER_UP:
                self.collect_powerup()
                game_map[new_grid_y][new_grid_x] = CellType.EMPTY
            
            self.grid_x = new_grid_x
            self.grid_y = new_grid_y
            self.x = self.grid_x * CELL_SIZE + CELL_SIZE // 2
            self.y = self.grid_y * CELL_SIZE + CELL_SIZE // 2
            self.move_cooldown = 8
    
    def collect_powerup(self):
        power_type = random.choice(['bombs', 'power'])
        if power_type == 'bombs':
            self.max_bombs += 1
        else:
            self.bomb_power += 1
    
    def place_bomb(self, game_map):
        if len(self.placed_bombs) < self.max_bombs:
            if game_map[self.grid_y][self.grid_x] == CellType.EMPTY:
                bomb = Bomb(self.grid_x, self.grid_y, self.bomb_power)
                self.placed_bombs.append(bomb)
                game_map[self.grid_y][self.grid_x] = CellType.BOMB
                return bomb
        return None
    
    def update(self):
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
    
    def draw(self, screen):
        if self.alive:
            pygame.draw.circle(screen, BLUE, (self.x, self.y), CELL_SIZE // 3)
            pygame.draw.circle(screen, WHITE, (self.x - 5, self.y - 5), 3)

class Enemy:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.x = x * CELL_SIZE + CELL_SIZE // 2
        self.y = y * CELL_SIZE + CELL_SIZE // 2
        self.speed = 1
        self.alive = True
        self.move_cooldown = 0
        self.direction = random.choice(list(Direction))
        
    def move(self, game_map):
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
            return
        
        if random.random() < 0.3:
            self.direction = random.choice(list(Direction))
        
        dx, dy = self.direction.value
        new_grid_x = self.grid_x + dx
        new_grid_y = self.grid_y + dy
        
        if (0 <= new_grid_x < GRID_SIZE and 
            0 <= new_grid_y < GRID_HEIGHT and
            game_map[new_grid_y][new_grid_x] == CellType.EMPTY):
            self.grid_x = new_grid_x
            self.grid_y = new_grid_y
            self.x = self.grid_x * CELL_SIZE + CELL_SIZE // 2
            self.y = self.grid_y * CELL_SIZE + CELL_SIZE // 2
            self.move_cooldown = 20
        else:
            self.direction = random.choice(list(Direction))
    
    def draw(self, screen):
        if self.alive:
            pygame.draw.circle(screen, RED, (self.x, self.y), CELL_SIZE // 3)
            pygame.draw.circle(screen, YELLOW, (self.x - 5, self.y - 5), 3)

class Bomb:
    def __init__(self, x, y, power):
        self.grid_x = x
        self.grid_y = y
        self.x = x * CELL_SIZE + CELL_SIZE // 2
        self.y = y * CELL_SIZE + CELL_SIZE // 2
        self.power = power
        self.timer = 180
        self.exploded = False
        
    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.exploded = True
            return True
        return False
    
    def draw(self, screen):
        if not self.exploded:
            size = CELL_SIZE // 3 + int(2 * abs(self.timer % 40 - 20) / 20)
            pygame.draw.circle(screen, BLACK, (self.x, self.y), size)
            pygame.draw.circle(screen, ORANGE, (self.x, self.y - size // 2), 3)

class Explosion:
    def __init__(self, positions):
        self.positions = positions
        self.timer = 30
        
    def update(self):
        self.timer -= 1
        return self.timer <= 0
    
    def draw(self, screen):
        for x, y in self.positions:
            center_x = x * CELL_SIZE + CELL_SIZE // 2
            center_y = y * CELL_SIZE + CELL_SIZE // 2
            size = CELL_SIZE // 2
            pygame.draw.circle(screen, YELLOW, (center_x, center_y), size)
            pygame.draw.circle(screen, ORANGE, (center_x, center_y), size - 5)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Bomberman")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.reset_game()
        
    def reset_game(self):
        self.game_map = self.generate_map()
        self.player = Player(1, 1)
        self.enemies = [
            Enemy(GRID_SIZE - 2, 1),
            Enemy(1, GRID_HEIGHT - 2),
            Enemy(GRID_SIZE - 2, GRID_HEIGHT - 2)
        ]
        self.bombs = []
        self.explosions = []
        self.game_over = False
        self.victory = False
        self.score = 0
        
    def generate_map(self):
        game_map = [[CellType.EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_HEIGHT)]
        
        for i in range(GRID_HEIGHT):
            for j in range(GRID_SIZE):
                if i == 0 or i == GRID_HEIGHT - 1 or j == 0 or j == GRID_SIZE - 1:
                    game_map[i][j] = CellType.WALL
                elif i % 2 == 0 and j % 2 == 0:
                    game_map[i][j] = CellType.WALL
                elif random.random() < 0.7:
                    if not ((i <= 2 and j <= 2) or 
                            (i >= GRID_HEIGHT - 3 and j >= GRID_SIZE - 3) or
                            (i <= 2 and j >= GRID_SIZE - 3) or
                            (i >= GRID_HEIGHT - 3 and j <= 2)):
                        game_map[i][j] = CellType.BRICK
        
        return game_map
    
    def handle_explosion(self, bomb):
        explosion_positions = [(bomb.grid_x, bomb.grid_y)]
        self.game_map[bomb.grid_y][bomb.grid_x] = CellType.EMPTY
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            for i in range(1, bomb.power + 1):
                x = bomb.grid_x + dx * i
                y = bomb.grid_y + dy * i
                
                if 0 <= x < GRID_SIZE and 0 <= y < GRID_HEIGHT:
                    if self.game_map[y][x] == CellType.WALL:
                        break
                    elif self.game_map[y][x] == CellType.BRICK:
                        explosion_positions.append((x, y))
                        if random.random() < 0.3:
                            self.game_map[y][x] = CellType.POWER_UP
                        else:
                            self.game_map[y][x] = CellType.EMPTY
                        self.score += 10
                        break
                    else:
                        explosion_positions.append((x, y))
                        
                        if self.player.grid_x == x and self.player.grid_y == y:
                            self.player.alive = False
                            self.game_over = True
                        
                        for enemy in self.enemies:
                            if enemy.alive and enemy.grid_x == x and enemy.grid_y == y:
                                enemy.alive = False
                                self.score += 100
        
        return Explosion(explosion_positions)
    
    def update(self):
        if self.game_over or self.victory:
            return
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.move(0, -1, self.game_map)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player.move(0, 1, self.game_map)
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move(-1, 0, self.game_map)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move(1, 0, self.game_map)
        
        self.player.update()
        
        for enemy in self.enemies:
            if enemy.alive:
                enemy.move(self.game_map)
                if enemy.grid_x == self.player.grid_x and enemy.grid_y == self.player.grid_y:
                    self.player.alive = False
                    self.game_over = True
        
        for bomb in self.bombs[:]:
            if bomb.update():
                explosion = self.handle_explosion(bomb)
                self.explosions.append(explosion)
                self.bombs.remove(bomb)
                if bomb in self.player.placed_bombs:
                    self.player.placed_bombs.remove(bomb)
        
        for explosion in self.explosions[:]:
            if explosion.update():
                self.explosions.remove(explosion)
        
        if all(not enemy.alive for enemy in self.enemies):
            self.victory = True
    
    def draw(self):
        self.screen.fill(BLACK)
        
        for i in range(GRID_HEIGHT):
            for j in range(GRID_SIZE):
                x = j * CELL_SIZE
                y = i * CELL_SIZE
                
                if self.game_map[i][j] == CellType.WALL:
                    pygame.draw.rect(self.screen, DARK_GRAY, (x, y, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(self.screen, GRAY, (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4))
                elif self.game_map[i][j] == CellType.BRICK:
                    pygame.draw.rect(self.screen, BROWN, (x, y, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(self.screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
                elif self.game_map[i][j] == CellType.POWER_UP:
                    pygame.draw.rect(self.screen, GREEN, (x + 10, y + 10, CELL_SIZE - 20, CELL_SIZE - 20))
                else:
                    pygame.draw.rect(self.screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
        
        for bomb in self.bombs:
            bomb.draw(self.screen)
        
        for explosion in self.explosions:
            explosion.draw(self.screen)
        
        self.player.draw(self.screen)
        
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        score_text = self.small_font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, GRID_HEIGHT * CELL_SIZE + 10))
        
        bombs_text = self.small_font.render(f"Bombs: {self.player.max_bombs}", True, WHITE)
        self.screen.blit(bombs_text, (150, GRID_HEIGHT * CELL_SIZE + 10))
        
        power_text = self.small_font.render(f"Power: {self.player.bomb_power}", True, WHITE)
        self.screen.blit(power_text, (280, GRID_HEIGHT * CELL_SIZE + 10))
        
        controls_text = self.small_font.render("Move: Arrow Keys/WASD | Bomb: Space | Restart: R", True, WHITE)
        self.screen.blit(controls_text, (10, GRID_HEIGHT * CELL_SIZE + 40))
        
        if self.game_over:
            game_over_text = self.font.render("GAME OVER! Press R to restart", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            pygame.draw.rect(self.screen, BLACK, text_rect.inflate(20, 10))
            self.screen.blit(game_over_text, text_rect)
        elif self.victory:
            victory_text = self.font.render(f"VICTORY! Score: {self.score} Press R to restart", True, GREEN)
            text_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            pygame.draw.rect(self.screen, BLACK, text_rect.inflate(20, 10))
            self.screen.blit(victory_text, text_rect)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not self.game_over and not self.victory:
                            bomb = self.player.place_bomb(self.game_map)
                            if bomb:
                                self.bombs.append(bomb)
                    elif event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
            
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()