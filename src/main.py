import cv2
import mediapipe as mp
import pygame
import random
import os

from game_platform import generate_initial_platforms, update_platforms, create_initial_platform
from character import Character
from game_menu import GameMenu
from video_capture_processing import capture_video
from reward import generate_rewards

day_bg = "features/first_background.jpg"
night_bg = "features/second_background.jpg"

WIDTH, HEIGHT = 600, 600
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
RED = (255, 123, 108)
DARK_RED = (234, 60, 83)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (234, 212, 252)
DARK_PINK = (180, 90, 180)
GREEN = (152, 251, 152)
DARK_GREEN = (76, 154, 42)
BLUE = (82, 178, 191)
DARK_BLUE = (40, 80, 194)

FPS = 60

# Centers the window on the screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sky Hop")


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
    back_to_menu_button = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + 70, BUTTON_WIDTH, BUTTON_HEIGHT)
    quit_button = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + 140, BUTTON_WIDTH, BUTTON_HEIGHT)

    # Blinking variables
    blink = True
    blink_interval = 400
    last_blink_time = pygame.time.get_ticks()

    running = True
    while running:
        # Takes the position of the mouse and checks if the click is pressed
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

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
                if back_to_menu_button.collidepoint(event.pos):
                    return "back to menu"

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
        pygame.draw.rect(screen, BLUE, back_to_menu_button)
        pygame.draw.rect(screen, RED, quit_button)

        # Checks if the mouse hovers over the button and if so, makes it darker to mark that it
        # can be selected, otherwise, the button stays in its initial color
        if restart_button.collidepoint(mouse):
            pygame.draw.rect(screen, DARK_GREEN, restart_button)

            if click[0] == 1:
                return "restart"
        else:
            pygame.draw.rect(screen, GREEN, restart_button)

        if quit_button.collidepoint(mouse):
            pygame.draw.rect(screen, DARK_RED, quit_button)

            if click[0] == 1:
                return "quit"
        else:
            pygame.draw.rect(screen, RED, quit_button)

        if back_to_menu_button.collidepoint(mouse):
            pygame.draw.rect(screen, DARK_BLUE, back_to_menu_button)

            if click[0] == 1:
                return "back to menu"
        else:
            pygame.draw.rect(screen, BLUE, back_to_menu_button)

        # Render button text
        restart_text = button_font.render("Restart", True, BLACK)
        quit_text = button_font.render("Quit", True, BLACK)
        back_to_menu_text = button_font.render("Back to Menu", True, BLACK)
        screen.blit(restart_text, (restart_button.centerx - restart_text.get_width() // 2,
                                   restart_button.centery - restart_text.get_height() // 2))
        screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2,
                                quit_button.centery - quit_text.get_height() // 2))
        screen.blit(back_to_menu_text, (back_to_menu_button.centerx - back_to_menu_text.get_width() // 2,
                                        back_to_menu_button.centery - back_to_menu_text.get_height() // 2))

        # Update display
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)


# Main game loop: Handles game logic and updates
def game_loop(screen, clock, use_video_input):
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

    # Initialize reward list
    rewards = []

    # Open camera if video input is enabled
    if use_video_input:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        # Create HandLandmarker detector
        detector = mp.solutions.hands.Hands(max_num_hands=1,
                                            min_detection_confidence=0.5,
                                            min_tracking_confidence=0.5)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
        # Adds a background image
        if score % 200 < 100:
            background_image = pygame.image.load(day_bg)
        else:
            background_image = pygame.image.load(night_bg)

        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        screen.blit(background_image, (0, 0))

        # Handle user key input
        if not use_video_input:
            keys = pygame.key.get_pressed()
            character.handle_movement(keys)

        # Handle user video input
        if use_video_input:
            capture_video(character, cap, detector)

        # Update character position and check game over status
        character_status = character.update(platforms, HEIGHT, 1)

        # Increase score when touching a platform
        for platform in platforms:
            if character.check_collision_with_platform([platform]):
                if not platform.is_jumped_on:
                    score += 1
                    # Mark it as jumped on
                    platform.jumped_on_platform()

        if score > best_score:
            save_best_score(score)

        # Check game over status
        if character_status == "game_over":
            running = False
            # Release video capture for the moment
            if use_video_input:
                cap.release()
            result = game_over_screen(screen)
            if result == "restart":
                pygame.event.clear()
                game_loop(screen, clock, use_video_input)  # Restart the game
            elif result == "quit":
                pygame.quit()
                exit()
            elif result == "back to menu":
                pygame.event.clear()
                main()

        # Update platform positions
        platforms = update_platforms(platforms, WIDTH, HEIGHT)

        if random.random() < 0.005:
            generate_rewards(platforms, rewards, character)

        # Update rewards and remove those out of screen
        for reward in rewards:
            reward.update_position()

        # Check for rewards collection
        for reward in rewards[:]:
            if reward.is_collected(character):
                rewards.remove(reward)
                # Increase score
                score += 5

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

        # Draw score
        menu_font = pygame.font.Font("features/ARCADECLASSIC.TTF", 30)
        best_score_text = menu_font.render(f"Highscore {best_score}", True, WHITE)
        score_text = menu_font.render(f"Score {score}", True, WHITE)

        # Display menu elements
        screen.blit(score_text, (5, 20))  # Score text
        screen.blit(best_score_text, (5, 50))  # Score text

        # Refresh the display
        pygame.display.flip()
        clock.tick(FPS)


# Main function: Initializes and starts the game
def main():
    clock = pygame.time.Clock()

    font = pygame.font.Font("features/PixelOperator-Bold.ttf", 35)
    menu = GameMenu(screen, font, WIDTH, HEIGHT)

    while True:
        menu_action = menu.main_menu()
        if menu_action == "quit":
            pygame.quit()
            exit()
        elif menu_action == "start":
            game_loop(screen, clock, menu.use_video_input)

        # Run the game loop
        game_loop(screen, clock, menu.use_video_input)

        # Quit the game
        pygame.quit()


# Entry point of the script
if __name__ == "__main__":
    main()
