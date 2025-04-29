import pygame
import random

class ParallaxStarField:
    def __init__(self, screen_width, screen_height, layer_speeds, stars_per_layer=50):
        self.layers = []
        for speed in layer_speeds:
            stars = []
            for _ in range(stars_per_layer):
                x = random.randint(0, screen_width)
                y = random.randint(0, screen_height)
                stars.append(pygame.Vector2(x, y))
            self.layers.append({"speed": speed, "stars": stars})
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, dt):
        for layer in self.layers:
            for star in layer["stars"]:
                star.x -= layer["speed"] * dt
                if star.x < 0:
                    star.x = self.screen_width
                    star.y = random.randint(0, self.screen_height)

    def draw(self, screen):
        for i, layer in enumerate(self.layers):
            color = (255, 255, 255)  # white for all layers, or vary by layer if you want
            size = i + 1  # layer 0 = size 1, layer 1 = size 2, etc.
            for star in layer["stars"]:
                pygame.draw.circle(screen, color, (int(star.x), int(star.y)), size)
