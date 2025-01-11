import pygame
import random

PLATFORM_WIDTH = 60
PLATFORM_HEIGHT = 10
MIN_VERTICAL_SPACING = 40  # Minimum vertical distance between platforms
MIN_HORIZONTAL_SPACING = 60  # Minimum horizontal distance between platforms
BROWN = (139, 69, 19)

# Platform class: Represents individual platforms in the game
class Platform:
	def __init__(self, x, y):
		# Define the platform's rectangle and color
		self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
		self.image.fill(BROWN)
		self.rect = self.image.get_rect(topleft=(x, y))
		self.is_jumped_on = False

	# Draw the platform as a rectangle
	def draw(self, screen):
		screen.blit(self.image, self.rect)

	def jumped_on_platform(self):
		# Marchează platforma ca sărită
		self.is_jumped_on = True

	def reset(self):
		# Resetează platforma pentru a putea fi sărită din nou (pentru o posibilă logică de resetare)
		self.is_jumped_on = False

# Function to create an initial platform at the bottom center of the screen
def create_initial_platform(screen_width, screen_height):
	x = screen_width // 2 - PLATFORM_WIDTH // 2
	y = screen_height - PLATFORM_HEIGHT - 100
	return Platform(x, y)

# Function to generate initial platforms at the start of the game
def generate_initial_platforms(platforms, num_platforms, screen_width, screen_height):

	# Random horizontal and vertical position for each platform
	for i in range(num_platforms):
		valid_position = False
		attempts = 0

		while not valid_position and attempts < 100:
			# Generate random coordinates for the platform
			x = random.randint(0, screen_width - PLATFORM_WIDTH)
			y = random.randint(screen_height // 4, screen_height - 100)

			# Check the distance from other platforms
			valid_position = True
			for platform in platforms:
				if abs(y - platform.rect.y) < MIN_VERTICAL_SPACING or \
						abs(x - platform.rect.x) < MIN_HORIZONTAL_SPACING:
					valid_position = False
					break

			attempts += 1

			# If valid, create the platform
			if valid_position:
				platforms.append(Platform(x, y))

		if attempts >= 100:
			break

	return platforms

# Function to update platform positions and add/remove platforms as needed
def update_platforms(platforms, scroll_speed, screen_width, screen_height):
	# Move all platforms downward by the scroll speed
	for platform in platforms:
		platform.rect.y += scroll_speed

	# Remove platforms that move out of the screen
	platforms = [platform for platform in platforms if platform.rect.top < screen_height]

	# Add new platforms until there are at least 6 on the screen
	while len(platforms) < 6:
		valid_position = False
		attempts = 0
		max_attempts = 200  # Limit attempts to prevent infinite loops

		while not valid_position and attempts < max_attempts:
			x = random.randint(0, screen_width - PLATFORM_WIDTH)
			y = random.randint(-50, -10)

			new_platform = Platform(x, y)

			# Conditions for valid positions
			valid_position = all(
				abs(y - p.rect.y) >= MIN_VERTICAL_SPACING and
				abs(x - p.rect.x) >= MIN_HORIZONTAL_SPACING
				for p in platforms
			)
			attempts += 1

		if valid_position:
			platforms.append(new_platform)
		else:
			break

	return platforms