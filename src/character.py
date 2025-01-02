import pygame

class Character:
    def __init__(self, screen_width, screen_height):
        self.image = pygame.image.load("character.png")
        self.image = pygame.transform.smoothscale(self.image, (100, 100))

        self.width, self.height = self.image.get_size()
        self.x = (screen_width // 2) - (self.width // 2)
        self.y = screen_height - self.height - 10
        self.initial_y = self.y

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
        if keys[pygame.K_SPACE] and self.y == self.initial_y:
            self.velocity_y = self.jump_force

        self.x = max(0, min(self.x, self.screen_width - self.width))



    def update(self, screen_height):
        self.y += self.velocity_y
        self.velocity_y += self.gravity
        self.velocity_y = min(self.velocity_y, 5)

        if self.y >= self.initial_y:
            self.y = self.initial_y
            self.velocity_y = self.jump_force

        if self.y + self.height >= screen_height:
            return "game_over"

        return "ok"

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
