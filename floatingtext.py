import pygame
import math
import random

class FloatingText(pygame.sprite.Sprite):
    def __init__(self, text, position, color=(255, 0, 0), lifespan=1.5):
        super().__init__()
        self.font = pygame.font.Font(None, 28)
        self.original_color = color
        self.text = text
        self.lifespan = lifespan
        self.age = 0

        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect(center=(int(position[0]), int(position[1])))

        self.start_position = pygame.Vector2(position)
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(0, -30)  # Floating upward

        # Wobble effect
        self.wobble_speed = random.uniform(3, 5)   # How fast it wiggles
        self.wobble_magnitude = random.uniform(5, 10)  # How wide the wiggle is

    def update(self, dt):
        self.age += dt
        if self.age >= self.lifespan:
            self.kill()
        else:
            # Move upward
            self.position += self.velocity * dt

            # Apply wobble horizontally
            wobble_offset = math.sin(self.age * self.wobble_speed) * self.wobble_magnitude
            self.rect.centerx = int(self.position.x + wobble_offset)
            self.rect.centery = int(self.position.y)

            # Fade out
            fade_factor = max(0, 1 - (self.age / self.lifespan))
            faded_color = (
                int(self.original_color[0] * fade_factor),
                int(self.original_color[1] * fade_factor),
                int(self.original_color[2] * fade_factor)
            )

            self.image = self.font.render(self.text, True, faded_color)

