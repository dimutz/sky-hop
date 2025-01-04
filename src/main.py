import pygame
import random
from game_platform import generate_initial_platforms, update_platforms, create_initial_platform
from character import Character  # Character class
from game_menu import GameMenu
from reward import generate_rewards


WIDTH, HEIGHT = 500, 600
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
RED = (255, 182, 193)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (234, 212, 252)
DARK_PINK = (180, 90, 180)
GREEN = (152, 251, 152)
FPS = 60


def read_best_score():
	try:
		with open("features/best_score.txt", "r") as file:
			return int(file.read().strip())
	except (FileNotFoundError, ValueError):
		return 0

def save_best_score(score):
	with open("features/best_score.txt", "w") as file:
		file.write(str(score))

# Game over screen: Displays a message when the game ends
def game_over_screen(screen):
	# Load font
	font = pygame.font.Font("features/PixelOperator-Bold.ttf", 80)
	button_font = pygame.font.Font("features/PixelOperator-Bold.ttf", 28)

	# Render buttons
	restart_button = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
	quit_button = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + 70, BUTTON_WIDTH, BUTTON_HEIGHT)

	# Blinking variables
	blink = True
	blink_interval = 400
	last_blink_time = pygame.time.get_ticks()

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				# Handle button clicks
				if restart_button.collidepoint(event.pos):
					return "restart"
				if quit_button.collidepoint(event.pos):
					return "quit"

		# Get current time and toggle blinking
		current_time = pygame.time.get_ticks()
		if current_time - last_blink_time >= blink_interval:
			blink = not blink
			last_blink_time = current_time

		# Clear screen
		screen.fill(BLACK)

		# Blinking Game Over text
		if blink:
			text = font.render("GAME OVER", True, WHITE)  # Red text
			text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
			screen.blit(text, text_rect)

		# Draw buttons
		pygame.draw.rect(screen, GREEN, restart_button)
		pygame.draw.rect(screen, RED, quit_button)

		# Render button text
		restart_text = button_font.render("Restart", True, BLACK)
		quit_text = button_font.render("Quit", True, BLACK)
		screen.blit(restart_text, (restart_button.centerx - restart_text.get_width() // 2, restart_button.centery -
								   restart_text.get_height() // 2))
		screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2, quit_button.centery -
								quit_text.get_height() // 2))

		# Update display
		pygame.display.flip()
		pygame.time.Clock().tick(FPS)


# Main game loop: Handles game logic and updates
def game_loop(screen, clock):
	running = True
	score = 0
	best_score = read_best_score()

	# Create the initial platform
	initial_platform = create_initial_platform(WIDTH, HEIGHT)
	platforms = [initial_platform]

	# Create the character and position it on the initial platform
	character = Character(WIDTH, HEIGHT)
	character.y = initial_platform.rect.top - character.height

	# Generate additional platforms
	platforms = generate_initial_platforms(platforms, 5, WIDTH, HEIGHT)

	# Inițializarea listei de recompense
	rewards = []

	# Inițializarea listei de recompense
	rewards = []

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()
				exit()


		# Clear the game screen
		screen.fill(PINK, (0, 0, WIDTH, HEIGHT))

		# Draw menu
		font = pygame.font.Font("features/PixelOperator-Bold.ttf", 24)
		menu_font = pygame.font.Font("features/PixelOperator-Bold.ttf", 20)
		best_score_text = menu_font.render(f"Best Score: {best_score}", True, DARK_PINK)
		score_text = menu_font.render(f"Score: {score}", True, DARK_PINK)

		# Display menu elements
		screen.blit(score_text, (5, 20))  # Score text
		screen.blit(best_score_text, (5, 50))  # Score text

		# Handle user input
		keys = pygame.key.get_pressed()
		character.handle_movement(keys)

		# Update character position and check game over status
		character_status = character.update(platforms, HEIGHT, 1)

		# Increase score when touching a platform
		if character.check_collision_with_platform(platforms):
			score += 1

		if score > best_score:
			save_best_score(score)

		# Check game over status
		if character_status == "game_over":
			running = False
			result = game_over_screen(screen)
			if result == "restart":
				main()  # Restart the game
			elif result == "quit":
				pygame.quit()
				exit()

		# Update platform positions
		platforms = update_platforms(platforms, 0, WIDTH, HEIGHT)

		# Generate new rewards
		if random.random() < 0.005:
			generate_rewards(platforms, rewards)

		# Update rewards and remove those out of screen
		for reward in rewards:
			reward.update_position()

		# Check for rewards collection
		for reward in rewards[:]:
			if reward.is_collected(character):
				rewards.remove(reward)
				score += 5  # Increase score


		# Check for rewards out of screen
		for reward in rewards[:]:
			if reward.is_out_of_screen(HEIGHT):
				rewards.remove(reward)


		# Draw everything on the screen
		for platform in platforms:
			platform.draw(screen)
		for reward in rewards:
			reward.draw(screen)
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

	font = pygame.font.Font("features/PixelOperator-Bold.ttf", 35)
	menu = GameMenu(screen, font, WIDTH, HEIGHT)

	while True:
		menu_action = menu.main_menu()

		if menu_action == "quit":
			pygame.quit()
			exit()
		elif menu_action == "start":
			game_loop(screen, clock)

		# Run the game loop
		game_loop(screen, clock)

		# Quit the game
		pygame.quit()

# Entry point of the script
if __name__ == "__main__":
	main()