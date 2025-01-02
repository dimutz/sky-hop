import pygame


class Character:
	def __init__(self, screen_width, screen_height):
		self.image = pygame.image.load("character.png")
		self.image = pygame.transform.smoothscale(self.image, (100, 100))

		self.width, self.height = self.image.get_size()
		self.x = (screen_width // 2) - (self.width // 2)
		self.y = screen_height - self.height - 10

		self.velocity_y = 0
		self.gravity = 0.15
		self.jump_force = -8
		self.speed_x = 5
		self.screen_width = screen_width

	def handle_movement(self, keys):
		if keys[pygame.K_LEFT]:
			self.x -= self.speed_x
		if keys[pygame.K_RIGHT]:
			self.x += self.speed_x

		self.x = max(0, min(self.x, self.screen_width - self.width))

	def check_collision_with_platform(self, platforms):
		for platform in platforms:
			if self.velocity_y > 0 and self.x + self.width > platform.rect.left and \
				self.x < platform.rect.right and self.y + self.height >= platform.rect.top and \
					self.y + self.height <= platform.rect.top + 10:
				self.y = platform.rect.top - self.height
				self.velocity_y = self.jump_force
				return True
		return False

	def update(self, platforms, screen_height, scroll_speed):
		if not self.check_collision_with_platform(platforms):
			self.y += self.velocity_y
			self.velocity_y += self.gravity
			self.velocity_y = min(self.velocity_y, 5)

		if self.y < screen_height // 3:
			for platform in platforms:
				platform.rect.y += abs(self.velocity_y) + scroll_speed
			self.y = screen_height // 3

		if self.y + self.height >= screen_height:
			return "game_over"

		return "ok"

	def draw(self, screen):
		screen.blit(self.image, (self.x, self.y))
