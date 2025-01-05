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
        return self.y + self.height >= screen_height


def generate_rewards(platforms, rewards, min_distance=200, max_attempts=5):
    for platform in platforms:
        valid_position = False
        attempts = 0
        while not valid_position and attempts < max_attempts:
            x = platform.rect.x + random.randint(0, platform.rect.width - 50)
            y = platform.rect.y - 50  # Reward's vertical position

            # Check distance between rewards
            valid_position = True
            for reward in rewards:
                if abs(reward.x - x) < min_distance and abs(reward.y - y) < min_distance:
                    valid_position = False
                    break

            attempts += 1  # Increase attempts

        # If `max_attempts` can not find valid position, stop
        if valid_position:
            reward = Reward(platform)
            reward.x = x
            reward.y = y
            rewards.append(reward)

    return rewards
