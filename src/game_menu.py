import pygame
import sys
import textwrap

# Used colors in the game menu implementation
PASTEL_GREEN = (107, 125, 125)
LIGHT_PINK = (234, 212, 252)
PINK = (236, 130, 236)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DUSTY_ROSE = (134, 84, 103)


class GameMenu:
    # Initialize the game menu screen
    def __init__(self, screen, font, width, height):
        self.screen = screen
        self.font = font
        self.width = width
        self.height = height
        self.use_video_input = False

    # Draw text with different color margin (glowing effect)
    def draw_glowing_text(self, screen, text, font, x, y, glow_color, text_color):
        # Create main text surface, in the desired color and centers it on the (x, y) coordinates
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(x, y))

        # Creates a glowing effect for the text by adding multiple layers with different offsets
        for offset in range(5, 0, -1):
            glow_surface = font.render(text, True, glow_color)

            # Creates glowing effect by adding layers to the left, right, top and bottom of the text
            screen.blit(glow_surface, (text_rect.x - offset, text_rect.y - offset))
            screen.blit(glow_surface, (text_rect.x + offset, text_rect.y - offset))
            screen.blit(glow_surface, (text_rect.x - offset, text_rect.y + offset))
            screen.blit(glow_surface, (text_rect.x + offset, text_rect.y + offset))

        screen.blit(text_surface, text_rect)

    # Creates the buttons and the game menu logic
    def draw_button(self, text, x, y, width, height, inactive_color, active_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Checks if the mouse hovers over the button and if so, makes it darker to mark that it
        # can be selected, otherwise, the button stays in its initial color
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            pygame.draw.rect(self.screen, PINK, (x, y, width, height))

            # If the button is clicked, the selected action is performed
            if click[0] == 1 and action:
                return action()
        else:
            pygame.draw.rect(self.screen, LIGHT_PINK, (x, y, width, height))

        # Adds text to the buttons and alligns it in the button's space
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

            # Makes a smaller font for the instructions
            instructions_font = pygame.font.Font("features/PixelOperator-Bold.ttf", 20)

            instructions = [
                "1. Use left or right arrow keys or",
                "move your index finger through camera capture!",
                "2. For the index finger movement capture,",
                "it doesn't matter what hand you use, just make sure",
                "you move your finger somewhere in the middle of",
                "the space captured by the camera!",
                "3. Avoid falling off the platforms!:)",
                "4. Collect special items to increase your score!",
                "5. Press B to go back to the menu!"
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
        while True:
            self.screen.fill(PASTEL_GREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

            title_font = pygame.font.Font("features/PixelOperator-Bold.ttf", 80)

            # Creates the text title with the glowing effect
            self.draw_glowing_text(self.screen, "Sky Hop", title_font, self.width // 2, 100, DUSTY_ROSE, WHITE)

            # Extracts the action for the pressed button
            start_action = self.draw_button("New Game", self.width // 2 - 100, 180, 200, 50, LIGHT_PINK, PINK,
                                            lambda: "start")
            how_to_play_action = self.draw_button("How to play", self.width // 2 - 100, 260, 200, 50, LIGHT_PINK, PINK,
                                                  lambda: "how to play")
            toggle_action = self.draw_button(
                f"{'Video' if self.use_video_input else 'Keys'}",
                self.width // 2 - 100,
                340, 200, 50,
                LIGHT_PINK,
                PINK,
                lambda: "toggle video input"
            )
            quit_action = self.draw_button("Quit", self.width // 2 - 100, 420, 200, 50, LIGHT_PINK, PINK,
                                           lambda: "quit")

            # Does the selected action
            if start_action:
                return start_action
            if how_to_play_action:
                self.how_to_play()
            if toggle_action:
                self.toggle_video_input()
            if quit_action:
                return quit_action

            pygame.display.update()
