import pygame
import sys
import textwrap
import os

# Stickers with the character and the reward to be added on the screen
character = "features/final_character.png"
reward = "features/final_reward.png"

# Used colors in the game menu implementation
PASTEL_GREEN = (107, 125, 125)
LIGHT_PINK = (234, 212, 252)
PINK = (236, 130, 236)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DUSTY_ROSE = (134, 84, 103)
HUNTER_GREEN = (53, 94, 59)

# Centers the window on the screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()


def read_best_score():
    try:
        with open("features/best_score.txt", "r") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0


class GameMenu:
    # Initialize the game menu screen
    def __init__(self, screen, font, width, height):
        self.screen = screen
        self.font = font
        self.width = width
        self.height = height
        self.use_video_input = False

    # Draw text with different color margin (glowing effect)
    def draw_glowing_text(self, text, font, x, y, glow_color, text_color):
        # Creates the main text surface, in the desired color and centers it on the (x, y) coordinates
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(x, y))

        # Creates a glowing effect for the text by adding multiple layers with different offsets
        for offset in range(5, 0, -1):
            glow_surface = font.render(text, True, glow_color)

            # Creates glowing effect by adding layers to the left, right, top and bottom of the text
            self.screen.blit(glow_surface, (text_rect.x - offset, text_rect.y - offset))
            self.screen.blit(glow_surface, (text_rect.x + offset, text_rect.y - offset))
            self.screen.blit(glow_surface, (text_rect.x - offset, text_rect.y + offset))
            self.screen.blit(glow_surface, (text_rect.x + offset, text_rect.y + offset))

        self.screen.blit(text_surface, text_rect)

    # Draw rotated text with different color margin (glowing effect)
    def draw_rotated_text(self, text, x, y, angle, font, color, glow_color):
        # Creates the main text surface, in the desired color and marks the position where the text starts
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(topleft=(x, y))

        # Rotates the text with a specific angle
        rotated_text_surface = pygame.transform.rotate(text_surface, angle)
        rotated_text_rect = rotated_text_surface.get_rect()

        # Synchronizes the corner of the rect with the corner of the text to make an easier rotation
        rotated_text_rect.topright = text_rect.topright

        # Creates the glow surface and rotates it with the same angle as the main text
        glow_surface = font.render(text, True, glow_color)
        rotated_glow_surface = pygame.transform.rotate(glow_surface, angle)
        rotated_glow_rect = rotated_glow_surface.get_rect()

        rotated_glow_rect.topright = rotated_text_rect.topright

        # Creates a glowing effect for the text by adding multiple layers with different offsets
        for offset in range(3, 0, -1):
            glow_surface = font.render(text, True, glow_color)

            # Creates glowing effect by adding layers to the left, right, top and bottom of the text
            self.screen.blit(rotated_glow_surface, (rotated_glow_rect.x - offset, rotated_glow_rect.y - offset))
            self.screen.blit(rotated_glow_surface, (rotated_glow_rect.x + offset, rotated_glow_rect.y - offset))
            self.screen.blit(rotated_glow_surface, (rotated_glow_rect.x - offset, rotated_glow_rect.y + offset))
            self.screen.blit(rotated_glow_surface, (rotated_glow_rect.x + offset, rotated_glow_rect.y + offset))

        self.screen.blit(rotated_text_surface, rotated_text_rect.topleft)

    # Creates the buttons and the game menu logic
    def draw_button(self, text, x, y, width, height, inactive_color, active_color, action=None):
        # Takes the position of the mouse and checks if the click is pressed
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Checks if the mouse hovers over the button and if so, makes it darker to mark that it
        # can be selected, otherwise, the button stays in its initial color
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            pygame.draw.rect(self.screen, active_color, (x, y, width, height))

            # If the button is clicked, the selected action is performed
            if click[0] == 1 and action:
                return action()
        else:
            pygame.draw.rect(self.screen, inactive_color, (x, y, width, height))

        # Adds text to the buttons and aligns it in the button's space
        text_surface = self.font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text_surface, text_rect)

    # Starts the game, if the "Start" button is selected
    def start_game(self, game_loop):
        game_loop()

    # Toggles video input
    def toggle_video_input(self):
        self.use_video_input = not self.use_video_input

    # Creates "How to play" button logic, where the players can see the game instructions
    def how_to_play(self):
        running = True

        # Creates a reward sticker (only for design purposes)
        reward_sticker = pygame.image.load(reward)
        reward_sticker = pygame.transform.scale(reward_sticker, (80, 80))
        rotated_reward_sticker_right = pygame.transform.rotate(reward_sticker, 300)
        rotated_reward_sticker_left = pygame.transform.rotate(reward_sticker, -10)

        while running:
            self.screen.fill(PASTEL_GREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                    running = False

            # Creates the "How to play" screen design
            self.screen.fill(PASTEL_GREEN)

            # Creates the title of the page
            title_surface = self.font.render("How to play Sky Hop:", True, BLACK)
            title_rect = title_surface.get_rect(center=(self.width // 2, 100))
            self.screen.blit(title_surface, title_rect)

            # Adds the reward sticker on the screen
            rotated_reward_rect = rotated_reward_sticker_right.get_rect(bottomright=(self.width - 40, self.height - 40))
            self.screen.blit(rotated_reward_sticker_right, rotated_reward_rect.topleft)

            # Adds the reward sticker on the screen
            rotated_reward_rect = rotated_reward_sticker_left.get_rect(
                bottomleft=(self.width // 2 - 250, self.height - 45))
            self.screen.blit(rotated_reward_sticker_left, rotated_reward_rect.topleft)

            # Makes a smaller font for the instructions
            instructions_font = pygame.font.Font("features/PixelOperator-Bold.ttf", 20)

            instructions = [
                "",
                "1. Use left or right arrow keys or",
                "move your index finger through camera capture!",
                "2. For the index finger movement capture,",
                "it doesn't matter what hand you use, just make sure",
                "you move your finger somewhere in the middle of",
                "the space captured by the camera!",
                "3. Avoid falling off the platforms!:)",
                "4. Collect special items to increase your score!",
                "",
                "Press B to go back to the menu"
            ]

            wrapped_instructions = []
            for line in instructions:
                # Divides the text lines if they exceed a given width
                wrapped_lines = textwrap.wrap(line, width=50)
                wrapped_instructions.extend(wrapped_lines)

            # Draws each line on the screen and centers it
            for i, line in enumerate(instructions):
                line_surface = instructions_font.render(line, True, BLACK)
                line_rect = line_surface.get_rect(center=(self.width // 2, 150 + i * 30))
                self.screen.blit(line_surface, line_rect)

            pygame.display.update()

    # Quits the game if the "Quit" button is selected
    def quit_game(self):
        pygame.quit()
        sys.exit()

    # Creates the main menu
    def main_menu(self, game_loop=None):
        # Creates a character sticker (only for design purposes)
        character_sticker = pygame.image.load(character)
        character_sticker = pygame.transform.scale(character_sticker, (105, 105))
        rotated_character_sticker = pygame.transform.rotate(character_sticker, 15)

        # Creates a reward sticker (only for design purposes)
        reward_sticker = pygame.image.load(reward)
        reward_sticker = pygame.transform.scale(reward_sticker, (80, 80))
        rotated_reward_sticker = pygame.transform.rotate(reward_sticker, 300)

        # Extracts the best score from the file
        highscore = read_best_score()

        # Formats the high score so that it will be completed with 0s
        # (it will be displayed with 6 figures)
        formatted_highscore = str(highscore).zfill(6)

        while True:
            self.screen.fill(PASTEL_GREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

            title_font = pygame.font.Font("features/PixelOperator-Bold.ttf", 100)

            # Creates the text title with the glowing effect
            self.draw_glowing_text("Sky Hop", title_font, self.width // 2, 120, DUSTY_ROSE, WHITE)

            # Creates a message (only for design purposes)
            highscore_font = pygame.font.Font("features/ARCADECLASSIC.TTF", 30)
            self.draw_rotated_text("High Score", self.width // 2 + 120, 25, -20, highscore_font, WHITE, HUNTER_GREEN)
            self.draw_rotated_text(f"{formatted_highscore}", self.width // 2 + 140, 55, -20, highscore_font, WHITE,
                                   HUNTER_GREEN)

            # Adds the character sticker on the screen
            rotated_character_rect = rotated_character_sticker.get_rect(center=(self.width // 2 - 220, 180))
            self.screen.blit(rotated_character_sticker, rotated_character_rect.topleft)

            # Adds the reward sticker on the screen
            rotated_reward_rect = rotated_reward_sticker.get_rect(bottomright=(self.width - 40, self.height - 20))
            self.screen.blit(rotated_reward_sticker, rotated_reward_rect.topleft)

            # Extracts the action for the pressed button
            start_action = self.draw_button("Start Game", self.width // 2 - 100, 220, 200, 50, LIGHT_PINK, PINK,
                                            lambda: "start")
            how_to_play_action = self.draw_button("How to play", self.width // 2 - 100, 300, 200, 50, LIGHT_PINK, PINK,
                                                  lambda: "how to play")
            toggle_action = self.draw_button(
                f"{'Video' if self.use_video_input else 'Keys'}",
                self.width // 2 - 100,
                380, 200, 50,
                LIGHT_PINK,
                PINK,
                lambda: "toggle video input"
            )
            quit_action = self.draw_button("Quit", self.width // 2 - 100, 460, 200, 50, LIGHT_PINK, PINK,
                                           lambda: "quit")

            # Does the selected action
            if start_action:
                return start_action
            if how_to_play_action:
                self.how_to_play()
            if toggle_action:
                self.toggle_video_input()
            if quit_action:
                pygame.event.clear()
                return quit_action

            pygame.display.update()
