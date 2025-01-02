import pygame
import random

PLATFORM_WIDTH = 60
PLATFORM_HEIGHT = 10
BROWN = (139, 69, 19)

# Platform class: Represents individual platforms in the game
class Platform:
	def __init__(self, x, y):
		# Define the platform's rectangle and color
		self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
		self.image.fill(BROWN)
		self.rect = self.image.get_rect(topleft=(x, y))

	# Draw the platform as a rectangle
	def draw(self, screen):
		screen.blit(self.image, self.rect)

# Function to create an initial platform at the bottom center of the screen
def create_initial_platform(screen_width, screen_height):
	x = screen_width // 2 - PLATFORM_WIDTH // 2
	y = screen_height - PLATFORM_HEIGHT - 100
	return Platform(x, y)

# Function to generate initial platforms at the start of the game
def generate_initial_platforms(num_platforms, screen_width, screen_height):
	platforms = []
	spacing = screen_height // num_platforms

	# Random horizontal and vertical position for each platform
	for i in range(num_platforms):
		x = random.randint(0, screen_width - PLATFORM_WIDTH)
		y = screen_height - (i + 1) * spacing
		# Create a Platform object and add it to the list
		platforms.append(Platform(x, y))
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
		x = random.randint(0, screen_width - PLATFORM_WIDTH)
		y = random.randint(-50, -10)

		# Create a new platform and ensure it doesn't overlap existing platforms
		new_platform = Platform(x, y)
		if not any(p.rect.colliderect(new_platform.rect) for p in platforms):
			platforms.append(new_platform)

	return platforms
