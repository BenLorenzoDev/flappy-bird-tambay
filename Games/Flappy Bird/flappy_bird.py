import pygame
import sys
import random
import math
from abc import ABC, abstractmethod

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -8
PIPE_WIDTH = 70
PIPE_GAP = 180
PIPE_SPEED = 3
GROUND_HEIGHT = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
SKY_BLUE = (135, 206, 250)
BROWN = (139, 69, 19)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
SKIN_COLOR = (255, 220, 177)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

class Character(ABC):
    """Base class for all playable characters"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.size = 30
        
    def jump(self):
        self.velocity = JUMP_STRENGTH
        
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        
    @abstractmethod
    def draw(self, screen):
        pass
    
    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, 
                          self.size * 2, self.size * 2)

class Bird(Character):
    """Flappy Bird character"""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.wing_state = 0  # For wing animation
        self.wing_timer = 0
        
    def update(self):
        super().update()
        # Animate wings
        self.wing_timer += 1
        if self.wing_timer >= 10:
            self.wing_state = (self.wing_state + 1) % 3
            self.wing_timer = 0
    
    def draw(self, screen):
        # Draw bird body (circle)
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, ORANGE, (int(self.x), int(self.y)), self.size, 2)
        
        # Draw eye
        eye_x = self.x + 10
        eye_y = self.y - 5
        pygame.draw.circle(screen, WHITE, (int(eye_x), int(eye_y)), 8)
        pygame.draw.circle(screen, BLACK, (int(eye_x + 3), int(eye_y)), 4)
        
        # Draw beak
        beak_points = [
            (self.x + self.size, self.y),
            (self.x + self.size + 15, self.y + 3),
            (self.x + self.size, self.y + 8)
        ]
        pygame.draw.polygon(screen, ORANGE, beak_points)
        
        # Draw animated wings
        if self.wing_state == 0:  # Wings up
            wing_points = [
                (self.x - 10, self.y - 5),
                (self.x - 25, self.y - 20),
                (self.x - 30, self.y - 10),
                (self.x - 15, self.y + 5)
            ]
            pygame.draw.polygon(screen, YELLOW, wing_points)
            pygame.draw.polygon(screen, ORANGE, wing_points, 2)
        elif self.wing_state == 1:  # Wings middle
            wing_points = [
                (self.x - 10, self.y),
                (self.x - 30, self.y - 5),
                (self.x - 30, self.y + 5),
                (self.x - 15, self.y + 8)
            ]
            pygame.draw.polygon(screen, YELLOW, wing_points)
            pygame.draw.polygon(screen, ORANGE, wing_points, 2)
        else:  # Wings down
            wing_points = [
                (self.x - 10, self.y + 5),
                (self.x - 25, self.y + 15),
                (self.x - 30, self.y + 8),
                (self.x - 15, self.y)
            ]
            pygame.draw.polygon(screen, YELLOW, wing_points)
            pygame.draw.polygon(screen, ORANGE, wing_points, 2)
        
        # Draw tail
        tail_points = [
            (self.x - self.size + 5, self.y - 5),
            (self.x - self.size - 10, self.y - 10),
            (self.x - self.size - 10, self.y + 10),
            (self.x - self.size + 5, self.y + 5)
        ]
        pygame.draw.polygon(screen, ORANGE, tail_points)

class Mario(Character):
    """Super Mario character"""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.jump_frame = 0  # Animation frame when jumping
        self.is_jumping = False
        
    def jump(self):
        super().jump()
        self.is_jumping = True
        self.jump_frame = 0
        
    def update(self):
        super().update()
        if self.is_jumping:
            self.jump_frame += 1
            if self.jump_frame > 20:
                self.is_jumping = False
    
    def draw(self, screen):
        # Draw Mario's body
        body_rect = pygame.Rect(self.x - 20, self.y - 15, 40, 30)
        pygame.draw.rect(screen, RED, body_rect)
        
        # Draw overalls
        overall_rect = pygame.Rect(self.x - 20, self.y, 40, 15)
        pygame.draw.rect(screen, BLUE, overall_rect)
        
        # Draw buttons
        pygame.draw.circle(screen, YELLOW, (int(self.x - 8), int(self.y + 5)), 2)
        pygame.draw.circle(screen, YELLOW, (int(self.x + 8), int(self.y + 5)), 2)
        
        # Draw head
        head_center_y = self.y - 25
        pygame.draw.circle(screen, SKIN_COLOR, (int(self.x), int(head_center_y)), 15)
        
        # Draw cap
        cap_rect = pygame.Rect(self.x - 18, head_center_y - 15, 36, 12)
        pygame.draw.rect(screen, RED, cap_rect)
        # Cap brim
        brim_rect = pygame.Rect(self.x - 20, head_center_y - 8, 40, 3)
        pygame.draw.rect(screen, RED, brim_rect)
        
        # Draw 'M' on cap
        font = pygame.font.Font(None, 16)
        m_text = font.render("M", True, WHITE)
        m_rect = m_text.get_rect(center=(self.x, head_center_y - 9))
        screen.blit(m_text, m_rect)
        
        # Draw eyes
        eye_left_x = self.x - 5
        eye_right_x = self.x + 5
        eye_y = head_center_y - 2
        pygame.draw.circle(screen, BLACK, (int(eye_left_x), int(eye_y)), 2)
        pygame.draw.circle(screen, BLACK, (int(eye_right_x), int(eye_y)), 2)
        
        # Draw mustache
        mustache_points_left = [
            (self.x - 2, head_center_y + 5),
            (self.x - 10, head_center_y + 3),
            (self.x - 12, head_center_y + 5),
            (self.x - 10, head_center_y + 7),
            (self.x - 2, head_center_y + 7)
        ]
        mustache_points_right = [
            (self.x + 2, head_center_y + 5),
            (self.x + 10, head_center_y + 3),
            (self.x + 12, head_center_y + 5),
            (self.x + 10, head_center_y + 7),
            (self.x + 2, head_center_y + 7)
        ]
        pygame.draw.polygon(screen, BLACK, mustache_points_left)
        pygame.draw.polygon(screen, BLACK, mustache_points_right)
        
        # Draw arms (animated when jumping)
        if self.is_jumping:
            # Arms up when jumping
            left_arm_points = [
                (self.x - 20, self.y - 10),
                (self.x - 30, self.y - 20),
                (self.x - 28, self.y - 22),
                (self.x - 18, self.y - 12)
            ]
            right_arm_points = [
                (self.x + 20, self.y - 10),
                (self.x + 30, self.y - 20),
                (self.x + 28, self.y - 22),
                (self.x + 18, self.y - 12)
            ]
        else:
            # Arms down when falling
            left_arm_points = [
                (self.x - 20, self.y - 5),
                (self.x - 28, self.y),
                (self.x - 26, self.y + 2),
                (self.x - 18, self.y - 3)
            ]
            right_arm_points = [
                (self.x + 20, self.y - 5),
                (self.x + 28, self.y),
                (self.x + 26, self.y + 2),
                (self.x + 18, self.y - 3)
            ]
        
        pygame.draw.polygon(screen, SKIN_COLOR, left_arm_points)
        pygame.draw.polygon(screen, SKIN_COLOR, right_arm_points)
        
        # Draw gloves
        if self.is_jumping:
            pygame.draw.circle(screen, WHITE, (int(self.x - 29), int(self.y - 21)), 5)
            pygame.draw.circle(screen, WHITE, (int(self.x + 29), int(self.y - 21)), 5)
        else:
            pygame.draw.circle(screen, WHITE, (int(self.x - 27), int(self.y + 1)), 5)
            pygame.draw.circle(screen, WHITE, (int(self.x + 27), int(self.y + 1)), 5)
        
        # Draw shoes
        shoe_left_rect = pygame.Rect(self.x - 18, self.y + 13, 15, 7)
        shoe_right_rect = pygame.Rect(self.x + 3, self.y + 13, 15, 7)
        pygame.draw.rect(screen, BROWN, shoe_left_rect)
        pygame.draw.rect(screen, BROWN, shoe_right_rect)

class JetPlane:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction  # 1 for right, -1 for left
        self.speed = 2 if direction == 1 else -2
        self.contrail = []  # List of smoke trail positions
        self.contrail_timer = 0
        self.banner_offset = 0  # For banner wave animation
        self.banner_wave_timer = 0
        
    def update(self):
        self.x += self.speed
        
        # Update banner wave animation
        self.banner_wave_timer += 0.1
        self.banner_offset = math.sin(self.banner_wave_timer) * 3
        
        # Add to contrail
        self.contrail_timer += 1
        if self.contrail_timer >= 3:
            if self.direction == 1:
                self.contrail.append({'x': self.x - 35, 'y': self.y, 'opacity': 255})
            else:
                self.contrail.append({'x': self.x + 35, 'y': self.y, 'opacity': 255})
            self.contrail_timer = 0
        
        # Update contrail (fade out and remove old particles)
        for particle in self.contrail[:]:
            particle['opacity'] -= 3
            if particle['opacity'] <= 0:
                self.contrail.remove(particle)
    
    def draw(self, screen):
        # Draw contrail first (behind the plane)
        for particle in self.contrail:
            alpha = particle['opacity']
            if alpha > 0:
                # Draw white smoke circles with transparency
                smoke_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
                pygame.draw.circle(smoke_surface, (255, 255, 255, min(alpha, 100)), (10, 10), 10)
                screen.blit(smoke_surface, (particle['x'] - 10, particle['y'] - 10))
        
        # Draw cable/rope connecting plane to banner
        if self.direction == 1:  # Flying right
            cable_start = (self.x - 35, self.y)
            banner_x = self.x - 120
        else:  # Flying left
            cable_start = (self.x + 35, self.y)
            banner_x = self.x + 60
        
        banner_y = self.y + 5 + self.banner_offset
        cable_end = (banner_x + 60, banner_y)
        
        # Draw cable as multiple thin lines for rope effect
        for i in range(3):
            offset = i - 1
            pygame.draw.line(screen, DARK_GRAY, 
                           (cable_start[0], cable_start[1] + offset),
                           (cable_end[0], cable_end[1] + offset), 1)
        
        # Draw banner
        banner_width = 120
        banner_height = 30
        
        # Create banner shape with slight wave effect
        banner_points = [
            (banner_x, banner_y - banner_height // 2),
            (banner_x + banner_width, banner_y - banner_height // 2 + self.banner_offset),
            (banner_x + banner_width, banner_y + banner_height // 2 + self.banner_offset),
            (banner_x, banner_y + banner_height // 2)
        ]
        
        # Draw banner background
        pygame.draw.polygon(screen, RED, banner_points)
        pygame.draw.polygon(screen, WHITE, banner_points, 2)
        
        # Draw banner text
        font = pygame.font.Font(None, 20)
        text = font.render("Welcome Tambay", True, WHITE)
        text_rect = text.get_rect(center=(banner_x + banner_width // 2, banner_y))
        screen.blit(text, text_rect)
        
        # Draw jet plane
        if self.direction == 1:  # Flying right
            # Fuselage
            pygame.draw.ellipse(screen, GRAY, (self.x - 30, self.y - 8, 60, 16))
            pygame.draw.ellipse(screen, DARK_GRAY, (self.x - 30, self.y - 8, 60, 16), 2)
            
            # Cockpit
            pygame.draw.ellipse(screen, LIGHT_GRAY, (self.x + 15, self.y - 6, 15, 12))
            pygame.draw.ellipse(screen, BLACK, (self.x + 20, self.y - 4, 8, 8))
            
            # Wings
            wing_points = [
                (self.x - 5, self.y),
                (self.x - 20, self.y - 15),
                (self.x - 15, self.y - 15),
                (self.x + 5, self.y)
            ]
            pygame.draw.polygon(screen, GRAY, wing_points)
            pygame.draw.polygon(screen, DARK_GRAY, wing_points, 2)
            
            wing_points2 = [
                (self.x - 5, self.y),
                (self.x - 20, self.y + 15),
                (self.x - 15, self.y + 15),
                (self.x + 5, self.y)
            ]
            pygame.draw.polygon(screen, GRAY, wing_points2)
            pygame.draw.polygon(screen, DARK_GRAY, wing_points2, 2)
            
            # Tail
            tail_points = [
                (self.x - 25, self.y),
                (self.x - 35, self.y - 10),
                (self.x - 30, self.y - 10),
                (self.x - 20, self.y)
            ]
            pygame.draw.polygon(screen, GRAY, tail_points)
            pygame.draw.polygon(screen, DARK_GRAY, tail_points, 2)
            
            # Engine
            pygame.draw.circle(screen, DARK_GRAY, (int(self.x - 30), int(self.y)), 5)
            pygame.draw.circle(screen, RED, (int(self.x - 32), int(self.y)), 3)
            
        else:  # Flying left
            # Fuselage
            pygame.draw.ellipse(screen, GRAY, (self.x - 30, self.y - 8, 60, 16))
            pygame.draw.ellipse(screen, DARK_GRAY, (self.x - 30, self.y - 8, 60, 16), 2)
            
            # Cockpit
            pygame.draw.ellipse(screen, LIGHT_GRAY, (self.x - 30, self.y - 6, 15, 12))
            pygame.draw.ellipse(screen, BLACK, (self.x - 28, self.y - 4, 8, 8))
            
            # Wings
            wing_points = [
                (self.x + 5, self.y),
                (self.x + 20, self.y - 15),
                (self.x + 15, self.y - 15),
                (self.x - 5, self.y)
            ]
            pygame.draw.polygon(screen, GRAY, wing_points)
            pygame.draw.polygon(screen, DARK_GRAY, wing_points, 2)
            
            wing_points2 = [
                (self.x + 5, self.y),
                (self.x + 20, self.y + 15),
                (self.x + 15, self.y + 15),
                (self.x - 5, self.y)
            ]
            pygame.draw.polygon(screen, GRAY, wing_points2)
            pygame.draw.polygon(screen, DARK_GRAY, wing_points2, 2)
            
            # Tail
            tail_points = [
                (self.x + 25, self.y),
                (self.x + 35, self.y - 10),
                (self.x + 30, self.y - 10),
                (self.x + 20, self.y)
            ]
            pygame.draw.polygon(screen, GRAY, tail_points)
            pygame.draw.polygon(screen, DARK_GRAY, tail_points, 2)
            
            # Engine
            pygame.draw.circle(screen, DARK_GRAY, (int(self.x + 30), int(self.y)), 5)
            pygame.draw.circle(screen, RED, (int(self.x + 32), int(self.y)), 3)
    
    def is_off_screen(self):
        return self.x < -100 or self.x > SCREEN_WIDTH + 100

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, SCREEN_HEIGHT - GROUND_HEIGHT - PIPE_GAP - 100)
        self.passed = False
        
    def update(self):
        self.x -= PIPE_SPEED
        
    def draw(self, screen):
        # Top pipe
        pygame.draw.rect(screen, DARK_GREEN, 
                        (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(screen, GREEN, 
                        (self.x - 5, self.height - 30, PIPE_WIDTH + 10, 30))
        
        # Bottom pipe
        bottom_pipe_y = self.height + PIPE_GAP
        pygame.draw.rect(screen, DARK_GREEN, 
                        (self.x, bottom_pipe_y, PIPE_WIDTH, 
                         SCREEN_HEIGHT - bottom_pipe_y - GROUND_HEIGHT))
        pygame.draw.rect(screen, GREEN, 
                        (self.x - 5, bottom_pipe_y, PIPE_WIDTH + 10, 30))
        
    def get_rects(self):
        top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, 
                                 SCREEN_HEIGHT - self.height - PIPE_GAP - GROUND_HEIGHT)
        return top_rect, bottom_rect
    
    def is_off_screen(self):
        return self.x + PIPE_WIDTH < 0

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird - Choose Your Character!")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        self.tiny_font = pygame.font.Font(None, 24)
        
        self.character_selection = True
        self.selected_character = None
        self.jets = []  # List of jet planes
        self.jet_timer = 0
        self.reset_game()
        
    def reset_game(self):
        # Don't reset character if already selected
        if self.selected_character == "bird":
            self.character = Bird(100, SCREEN_HEIGHT // 2)
        elif self.selected_character == "mario":
            self.character = Mario(100, SCREEN_HEIGHT // 2)
        else:
            self.character = None
            
        self.pipes = []
        self.pipe_timer = 0
        self.score = 0
        self.game_over = False
        self.game_started = False
        
        # Don't reset jets when resetting game
        if not hasattr(self, 'jets'):
            self.jets = []
            self.jet_timer = 0
        
    def handle_character_selection(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.selected_character = "bird"
                self.character = Bird(100, SCREEN_HEIGHT // 2)
                self.character_selection = False
                pygame.display.set_caption("Flappy Bird - Playing as Bird")
            elif event.key == pygame.K_2:
                self.selected_character = "mario"
                self.character = Mario(100, SCREEN_HEIGHT // 2)
                self.character_selection = False
                pygame.display.set_caption("Flappy Bird - Playing as Mario")
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if self.character_selection:
                self.handle_character_selection(event)
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not self.game_started:
                            self.game_started = True
                        if not self.game_over:
                            self.character.jump()
                        else:
                            self.reset_game()
                    elif event.key == pygame.K_c and (self.game_over or not self.game_started):
                        # Allow changing character when game is over or not started
                        self.character_selection = True
                        self.selected_character = None
                        self.reset_game()
        return True
    
    def update(self):
        # Update jets even when not playing
        self.update_jets()
        
        if self.character_selection or not self.game_started or self.game_over:
            return
            
        # Update character
        self.character.update()
        
        # Check boundaries
        if self.character.y <= 0 or self.character.y >= SCREEN_HEIGHT - GROUND_HEIGHT:
            self.game_over = True
            
        # Spawn pipes
        self.pipe_timer += 1
        if self.pipe_timer >= 90:  # Spawn pipe every 1.5 seconds
            self.pipes.append(Pipe(SCREEN_WIDTH))
            self.pipe_timer = 0
            
        # Update pipes
        for pipe in self.pipes[:]:
            pipe.update()
            
            # Check collision
            character_rect = self.character.get_rect()
            top_rect, bottom_rect = pipe.get_rects()
            if character_rect.colliderect(top_rect) or character_rect.colliderect(bottom_rect):
                self.game_over = True
                
            # Check if character passed the pipe
            if not pipe.passed and pipe.x + PIPE_WIDTH < self.character.x:
                pipe.passed = True
                self.score += 1
                
            # Remove off-screen pipes
            if pipe.is_off_screen():
                self.pipes.remove(pipe)
    
    def update_jets(self):
        # Spawn new jets randomly
        self.jet_timer += 1
        if self.jet_timer >= random.randint(300, 600):  # Random interval between 5-10 seconds
            # Randomly choose direction and height
            if random.choice([True, False]):
                # Spawn from left, moving right
                jet_x = -50
                direction = 1
            else:
                # Spawn from right, moving left
                jet_x = SCREEN_WIDTH + 50
                direction = -1
            
            jet_y = random.randint(50, 200)  # Keep jets in upper portion of screen
            self.jets.append(JetPlane(jet_x, jet_y, direction))
            self.jet_timer = 0
        
        # Update existing jets
        for jet in self.jets[:]:
            jet.update()
            if jet.is_off_screen():
                self.jets.remove(jet)
    
    def draw_background(self, screen):
        # Sky
        screen.fill(SKY_BLUE)
        
        # Clouds (simple circles)
        for i in range(3):
            x = 50 + i * 150
            y = 50 + i * 30
            pygame.draw.circle(screen, WHITE, (x, y), 30)
            pygame.draw.circle(screen, WHITE, (x + 25, y), 25)
            pygame.draw.circle(screen, WHITE, (x - 20, y), 25)
        
        # Draw jets (behind everything else but in front of sky)
        for jet in self.jets:
            jet.draw(screen)
    
    def draw_ground(self, screen):
        # Ground
        pygame.draw.rect(screen, BROWN, 
                        (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
        # Grass
        pygame.draw.rect(screen, GREEN, 
                        (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, 20))
    
    def draw_character_selection(self, screen):
        # Draw background
        self.draw_background(screen)
        self.draw_ground(screen)
        
        # Title
        title_text = self.font.render("Choose Your Character", True, WHITE)
        title_shadow = self.font.render("Choose Your Character", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
        screen.blit(title_text, title_rect)
        
        # Draw Bird preview
        bird_preview = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 50)
        bird_preview.draw(screen)
        bird_text = self.small_font.render("1. Bird", True, WHITE)
        bird_shadow = self.small_font.render("1. Bird", True, BLACK)
        bird_rect = bird_text.get_rect(center=(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 20))
        screen.blit(bird_shadow, (bird_rect.x + 2, bird_rect.y + 2))
        screen.blit(bird_text, bird_rect)
        
        # Draw Mario preview
        mario_preview = Mario(3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 50)
        mario_preview.draw(screen)
        mario_text = self.small_font.render("2. Mario", True, WHITE)
        mario_shadow = self.small_font.render("2. Mario", True, BLACK)
        mario_rect = mario_text.get_rect(center=(3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 20))
        screen.blit(mario_shadow, (mario_rect.x + 2, mario_rect.y + 2))
        screen.blit(mario_text, mario_rect)
        
        # Instructions
        inst_text = self.tiny_font.render("Press 1 for Bird or 2 for Mario", True, WHITE)
        inst_shadow = self.tiny_font.render("Press 1 for Bird or 2 for Mario", True, BLACK)
        inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150))
        screen.blit(inst_shadow, (inst_rect.x + 1, inst_rect.y + 1))
        screen.blit(inst_text, inst_rect)
    
    def draw(self):
        if self.character_selection:
            self.draw_character_selection(self.screen)
        else:
            # Draw background
            self.draw_background(self.screen)
            
            # Draw pipes
            for pipe in self.pipes:
                pipe.draw(self.screen)
                
            # Draw ground
            self.draw_ground(self.screen)
            
            # Draw character
            if self.character:
                self.character.draw(self.screen)
            
            # Draw score
            score_text = self.font.render(str(self.score), True, WHITE)
            score_shadow = self.font.render(str(self.score), True, BLACK)
            self.screen.blit(score_shadow, (SCREEN_WIDTH // 2 - 18, 52))
            self.screen.blit(score_text, (SCREEN_WIDTH // 2 - 20, 50))
            
            # Draw game over or start message
            if not self.game_started:
                start_text = self.small_font.render("Press SPACE to Start", True, WHITE)
                start_shadow = self.small_font.render("Press SPACE to Start", True, BLACK)
                text_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(start_shadow, (text_rect.x + 2, text_rect.y + 2))
                self.screen.blit(start_text, text_rect)
                
                change_text = self.tiny_font.render("Press C to Change Character", True, WHITE)
                change_shadow = self.tiny_font.render("Press C to Change Character", True, BLACK)
                change_rect = change_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
                self.screen.blit(change_shadow, (change_rect.x + 1, change_rect.y + 1))
                self.screen.blit(change_text, change_rect)
            elif self.game_over:
                game_over_text = self.font.render("Game Over!", True, RED)
                game_over_shadow = self.font.render("Game Over!", True, BLACK)
                text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
                self.screen.blit(game_over_shadow, (text_rect.x + 2, text_rect.y + 2))
                self.screen.blit(game_over_text, text_rect)
                
                restart_text = self.small_font.render("Press SPACE to Restart", True, WHITE)
                restart_shadow = self.small_font.render("Press SPACE to Restart", True, BLACK)
                text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
                self.screen.blit(restart_shadow, (text_rect.x + 2, text_rect.y + 2))
                self.screen.blit(restart_text, text_rect)
                
                change_text = self.tiny_font.render("Press C to Change Character", True, WHITE)
                change_shadow = self.tiny_font.render("Press C to Change Character", True, BLACK)
                change_rect = change_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 45))
                self.screen.blit(change_shadow, (change_rect.x + 1, change_rect.y + 1))
                self.screen.blit(change_text, change_rect)
                
                final_score_text = self.small_font.render(f"Score: {self.score}", True, WHITE)
                final_score_shadow = self.small_font.render(f"Score: {self.score}", True, BLACK)
                text_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
                self.screen.blit(final_score_shadow, (text_rect.x + 2, text_rect.y + 2))
                self.screen.blit(final_score_text, text_rect)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()