import pygame
import random

PLATFORM_WIDTH = 60
PLATFORM_HEIGHT = 10
BROWN = (139, 69, 19)

class Platform:
    def _init_(self, x, y):
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def generate_initial_platforms(num_platforms, screen_width, screen_height):
    platforms = []
    spacing = screen_height // num_platforms  # Spațiere uniformă
    for i in range(num_platforms):
        x = random.randint(0, screen_width - PLATFORM_WIDTH)  # Poziție aleatorie pe X
        y = screen_height - (i + 1) * spacing  # Distribuție pe Y
        platforms.append([x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT])  # reprezinta platformele ca liste
    return platforms

#def update_platforms(platforms, player, screen_width, screen_height):
def update_platforms(platforms, scroll_speed, screen_width, screen_height):
    for platform in platforms:
        platform[1] += scroll_speed
        #platform.rect.y += int(player.y_velocity)  # muta platformele în jos

    # elimina platformele care ies din ecran
    #platforms = [platform for platform in platforms if platform.rect.top < screen_height]
    platforms = [platform for platform in platforms if platform[1] < screen_height]

    # adauga platforme noi la partea de sus
    while len(platforms) < 6:
        x = random.randint(0, screen_width - PLATFORM_WIDTH)
        y = random.randint(-50, -10)
        platforms.append([x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT])
    return platforms

def draw_platforms(screen, platforms):
    for platform in platforms:
        pygame.draw.rect(screen, BROWN, (platform[0], platform[1], platform[2], platform[3]))