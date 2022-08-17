import pygame
import os
import time
import random

# Init the font to write on the screen
pygame.font.init()

# Screen
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Invaders')

# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_red_small.png'))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_green_small.png'))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_blue_small.png'))

# Player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_yellow.png'))

# Lasers
RED_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_red.png'))
GREEN_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_green.png'))
BLUE_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_blue.png'))
YELLOW_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_yellow.png'))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background-black.png')), (WIDTH, HEIGHT))

# Abstract/Base class
class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None # Allow to draw ship and laser but the class is abstract, so I put None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
    
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img) # creating a pixel=perfect hitbox
        self.max_health = health

class Enemy(Ship):
    # Color map
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
    
    def move(self, vel):
        self.y += vel


# Main loop
def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    player_vel = 10
    main_font = pygame.font.SysFont('comicsams', 50)
    lost_font = pygame.font.SysFont('comicsans', 100)

    # Enemies settings
    enemies = []
    wave_length = 5
    enemy_vel = 5

    player = Player(100, 100)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    # Updating the window
    def redraw_window():
        # First - blit the BG
        WIN.blit(BG, (0, 0))
        # Draw labels
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        WIN.blit(level_label, (10, 10))
        WIN.blit(lives_label, (WIDTH - level_label.get_width() - 10, 10))
        
        player.draw(WIN)
        
        for enemy in enemies:
            enemy.draw(WIN)

        if lost:
            lost_label = lost_font.render("YOU LOST", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, HEIGHT/2 - lost_label.get_height()/2))


        pygame.display.update()

    while run:
        # Setting FPS 
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
        
        if lost:
            if lost_count > FPS * 3: # 3 second timer
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-50), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        # Quitting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed() # return a dict of keys when they're pressed.
        if keys[pygame.K_a] and player.x + player_vel > 0: # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT: # down
            player.y += player_vel

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        

main()
                