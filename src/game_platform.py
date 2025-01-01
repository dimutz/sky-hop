import pygame
import random

PLATFORM_WIDTH = 60
PLATFORM_HEIGHT = 10
BROWN = (139, 69, 19)

class Platform:
    def __init__(self, x, y):
        # Creează suprafața platformei
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def generate_initial_platforms(num_platforms, screen_width, screen_height):
    platforms = []
    spacing = screen_height // num_platforms
    for i in range(num_platforms):
        x = random.randint(0, screen_width - PLATFORM_WIDTH)
        y = screen_height - (i + 1) * spacing
        platforms.append(Platform(x, y))  # Creează obiecte Platform
    return platforms

def update_platforms(platforms, scroll_speed, screen_width, screen_height):
    for platform in platforms:
        platform.rect.y += scroll_speed

    # Elimină platformele care ies din ecran
    platforms = [platform for platform in platforms if platform.rect.top < screen_height]

    # Adaugă platforme noi
    while len(platforms) < 6:
        x = random.randint(0, screen_width - PLATFORM_WIDTH)
        y = random.randint(-50, -10)
        platforms.append(Platform(x, y))

    return platforms
