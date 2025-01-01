import pygame
from game_platform import generate_initial_platforms, update_platforms
from character import Character  # Clasa pentru personaj

WIDTH, HEIGHT = 500, 500
BLUE = (0, 0, 255)
FPS = 60

def game_loop(screen, clock):
    running = True

    # Creează personajul
    character = Character(WIDTH, HEIGHT)

    # Creează platformele
    platforms = generate_initial_platforms(6, WIDTH, HEIGHT)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Obține tastele apăsate
        keys = pygame.key.get_pressed()

        # Mișcă și actualizează personajul
        character.handle_movement(keys)
        character.update()

        # Actualizează platformele
        platforms = update_platforms(platforms, 2, WIDTH, HEIGHT)

        # Verifică coliziunile cu platformele
        for platform in platforms:
            if (
                character.y + character.height >= platform.rect.y
                and character.y + character.height <= platform.rect.y + 10
                and character.x + character.width >= platform.rect.x
                and character.x <= platform.rect.x + platform.rect.width
                and character.velocity_y > 0
            ):
                character.velocity_y = character.jump_force

        # Fundal
        screen.fill(BLUE)

        # Desenează platformele și personajul
        for platform in platforms:
            platform.draw(screen)
        character.draw(screen)

        # Actualizează afișajul
        pygame.display.flip()
        clock.tick(FPS)


def main():
    # Inițializare pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sky Hop")
    clock = pygame.time.Clock()

    # Rulează bucla principală a jocului
    game_loop(screen, clock)

    # Închide jocul
    pygame.quit()

if __name__ == "__main__":
    main()
