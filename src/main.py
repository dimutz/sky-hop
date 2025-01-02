import pygame
from game_platform import generate_initial_platforms, update_platforms, create_initial_platform
from character import Character  # Clasa pentru personaj

WIDTH, HEIGHT = 500, 500
PINK = (234, 212, 252)
FPS = 60


def game_over_screen(screen):
	font = pygame.font.SysFont("Arial", 48, bold=True)
	text = font.render("GAME OVER", True, (255, 0, 0))
	screen.fill((0, 0, 0))
	screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3))

	pygame.display.flip()

	pygame.time.wait(2000)  # Așteaptă 2 secunde înainte de ieșire
	return False  # Închide jocul

def game_loop(screen, clock):
	running = True

	# Creează platforma inițială
	initial_platform = create_initial_platform(WIDTH, HEIGHT)

	# Creează personajul și poziționează-l pe platforma inițială
	character = Character(WIDTH, HEIGHT)
	character.y = initial_platform.rect.top - \
		character.height  # Poziționează deasupra platformei

	# Creează restul platformelor
	platforms = generate_initial_platforms(5, WIDTH, HEIGHT)
	# Adaugă platforma inițială în lista de platforme
	platforms.append(initial_platform)

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		keys = pygame.key.get_pressed()
		character.handle_movement(keys)

		# Actualizează poziția personajului
		character_status = character.update(platforms, HEIGHT, 1)
		if character_status == "game over":
			running = False

		# Test pentru Game Over
		if character_status == "game_over":
			running = False
			# Dacă utilizatorul decide să iasă din joc
			if not game_over_screen(screen):
				break

		# Actualizează platformele
		platforms = update_platforms(platforms, 1, WIDTH, HEIGHT)

		# Fundal
		screen.fill(PINK)

		# Desenează platformele și personajul
		for platform in platforms:
			platform.draw(screen)
		character.draw(screen)

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
