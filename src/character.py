import pygame

chipmunk = "features/character.png"
class Character:
	def __init__(self, screen_width, screen_height):
		# Load the character image into the game window
		self.image = pygame.image.load(chipmunk)

		# Smoothly scale the image to the desired dimensions
		self.image = pygame.transform.smoothscale(self.image, (100, 100))

		self.width, self.height = self.image.get_size()
		
		# Initialize the starting position of the character (at the bottom center)
		self.x = (screen_width // 2) - (self.width // 2)
		self.y = screen_height - self.height - 10

		# Initialize values for the physics of the character
		self.velocity_y = 0
		self.gravity = 0.15
		self.jump_force = -8
		self.speed_x = 5	# Horizontal movement speed
		self.screen_width = screen_width

	def handle_movement(self, keys):
		if keys[pygame.K_LEFT]:
			self.x -= self.speed_x
		if keys[pygame.K_RIGHT]:
			self.x += self.speed_x

		# Prevent the character from moving outside the screen's boundaries
		self.x = max(0, min(self.x, self.screen_width - self.width))

	def handle_motion(self, new_x):
		if self.x > new_x:
			self.x -= self.speed_x
		if self.x < new_x:
			self.x += self.speed_x

		# Prevent the character from moving outside the screen's boundaries
		self.x = max(0, min(self.x, self.screen_width - self.width))

	def check_collision_with_platform(self, platforms):
		for platform in platforms:
			# Checks if the character collides with platforms when falling
			if self.velocity_y > 0 and self.x + self.width > platform.rect.left and \
				self.x < platform.rect.right and self.y + self.height >= platform.rect.top and \
					self.y + self.height <= platform.rect.top + 10:
				# Alling the character on top of the platform and reset the jump
				self.y = platform.rect.top - self.height
				self.velocity_y = self.jump_force
				return True
		return False

	def update(self, platforms, screen_height, scroll_speed):
		# Updates the character's position when he doesn't collide with a platform
		if not self.check_collision_with_platform(platforms):
			self.y += self.velocity_y
			self.velocity_y += self.gravity
			self.velocity_y = min(self.velocity_y, 5)

		# If the character moves past a value, an automatic scroll downward is made
		if self.y < screen_height // 4:
			for platform in platforms:
				platform.rect.y += abs(self.velocity_y) + scroll_speed
			self.y = screen_height // 4

		# If the character falls off, it's game over
		if self.y + self.height >= screen_height:
			return "game_over"

		return "ok"

	def draw(self, screen):
		# Render the character on the screen
		screen.blit(self.image, (self.x, self.y))
