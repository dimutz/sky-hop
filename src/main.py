import pygame
import sys
from game_platform import Platform, generate_initial_platforms, update_platforms, draw_platforms

WIDTH, HEIGHT = 400, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
#PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
PLATFORM_WIDTH, PLATFORM_HEIGHT = 60, 10
FPS = 60

def game_loop(screen, clock):
    running = True
   # player = Player()
    platforms = generate_initial_platforms(6, WIDTH, HEIGHT)

    while running:
        # Evenimente
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Actualizări personaj
        #player.update()
        #platforms = update_platforms(platforms, player)
        platforms = update_platforms(platforms, 2, WIDTH, HEIGHT)

        # Coliziuni
       # for platform in platforms:
        #    if player.rect.colliderect(platform.rect) and player.y_velocity > 0:
        #        player.jump()

        # Desenează pe ecran
        screen.fill(BLUE)
        draw_platforms(screen, platforms)
        #screen.blit(player.image, player.rect)
        pygame.display.flip()
        clock.tick(FPS)

# Funcția main
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sky Hop")
    clock = pygame.time.Clock()

    # Rulează jocul
    game_loop(screen, clock)

    # Închide jocul
    pygame.quit()
    sys.exit()

# Punctul de intrare
if __name__ == "__main__":
    main()