import pygame
import random

height = 500
class Reward:
	def __init__(self, platform):
		self.image = pygame.image.load("features/reward1.png")
		self.image = pygame.transform.smoothscale(self.image, (50, 50))
		self.width, self.height = self.image.get_size()
		self.platform = platform
		self.update_position()

	def update_position(self):
		self.x = self.platform.rect.x + (self.platform.rect.width // 2) - (self.width // 2)
		self.y = self.platform.rect.y - self.height

	def is_collected(self, character):
		# Check if character touches reward
		return (
			self.x < character.x + character.width and
			self.x + self.width > character.x and
			self.y < character.y + character.height and
			self.y + self.height > character.y
		)

	def draw(self, screen):
		screen.blit(self.image, (self.x, self.y))

	def is_out_of_screen(self, screen_height):
		# Check if reward is out of screen
		return self.y + self.height > screen_height

def generate_rewards(platforms, num_rewards):
	rewards = []
	selected_platforms = random.sample(platforms, min(num_rewards, len(platforms)))

	for platform in selected_platforms:
		reward = Reward(platform)
		rewards.append(reward)

	return rewards
