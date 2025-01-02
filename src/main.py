import pygame
from game_platform import generate_initial_platforms, update_platforms, create_initial_platform
from character import Character  # Clasa pentru personaj

WIDTH, HEIGHT = 500, 500
PINK = (234, 212, 252)
FPS = 60

# Game over screen: Displays a message when the game ends
def game_over_screen(screen):
	font = pygame.font.SysFont("Arial", 48, bold=True)
	text = font.render("GAME OVER", True, (255, 0, 0))
	screen.fill((0, 0, 0))
	screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3))

	pygame.display.flip()

	# Wait 2 seconds before closing
	pygame.time.wait(2000)
	return False

# Main game loop: Handles game logic and updates
def game_loop(screen, clock):
	running = True

	# Create the initial platform
	initial_platform = create_initial_platform(WIDTH, HEIGHT)

	# Create the character and position it on the initial platform
	character = Character(WIDTH, HEIGHT)
	character.y = initial_platform.rect.top - \
		character.height

	# Generate additional platforms
	platforms = generate_initial_platforms(5, WIDTH, HEIGHT)
	platforms.append(initial_platform)

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		# Handle user input
		keys = pygame.key.get_pressed()
		character.handle_movement(keys)

		# Update character position and check game over status
		character_status = character.update(platforms, HEIGHT, 1)

		# Check game over status
		if character_status == "game_over":
			running = False
			if not game_over_screen(screen):
				break

		# Update platform positions
		platforms = update_platforms(platforms, 1, WIDTH, HEIGHT)

		# Draw everything on the screen
		screen.fill(PINK)
		for platform in platforms:
			platform.draw(screen)
		character.draw(screen)

		# Refresh the display
		pygame.display.flip()
		clock.tick(FPS)

# Main function: Initializes and starts the game
def main():
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Sky Hop")
	clock = pygame.time.Clock()

	# Run the game loop
	game_loop(screen, clock)

	# Quit the game
	pygame.quit()

# Entry point of the script
if __name__ == "__main__":
	main()
