import pygame
import sys

PASTEL_GREEN = (107, 125, 125)
LIGHT_PINK = (234, 212, 252)
PINK = (236, 130, 236)
BLACK = (0, 0, 0)

class GameMenu:
	def __init__(self, screen, font, width, height):
		self.screen = screen
		self.font = font
		self.width = width
		self.height = height

	def draw_button(self, text, x, y, width, height, inactive_color, active_color, action=None):
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()

		if x + width > mouse[0] > x and y + height > mouse[1] > y:
			pygame.draw.rect(self.screen, PINK, (x, y, width, height))

			if click[0] == 1 and action:
				return action()
		else:
			pygame.draw.rect(self.screen, LIGHT_PINK, (x, y, width, height))

		text_surface = self.font.render(text, True, BLACK)
		text_rect = text_surface.get_rect(center=(x + width	// 2, y + height // 2))
		self.screen.blit(text_surface, text_rect)

	def start_game(self, game_loop):
		game_loop()

	def how_to_play(self):
		running = True

		while running:
			self.screen.fill(PASTEL_GREEN)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
					running = False
	
		text_surface = self.font.render("How to play Sky Hop:", True, BLACK)
		text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
		self.screen.blit(text_surface, text_rect)

		pygame.display.update()

	def quit_game(self):
		pygame.quit()
		sys.exit()

	def main_menu(self, game_loop=None):
		while True:
			self.screen.fill(PASTEL_GREEN)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return "quit"

			start_action = self.draw_button("Start Game", self.width // 2 - 100, 200, 200, 50, (0, 255, 0), (173, 255, 47), lambda: "start")
			quit_action = self.draw_button("Quit", self.width // 2 - 100, 300, 200, 50, (255, 0, 0), (255, 69, 0), lambda: "quit")

			if start_action:
				return start_action
			if quit_action:
				return quit_action

			pygame.display.update()

