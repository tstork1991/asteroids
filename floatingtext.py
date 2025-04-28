import pygame

class FloatingText(pygame.sprite.Sprite):
    def __init__(self, text, position, color=(255, 255, 255), lifespan=1.0):
        super().__init__()
        self.font = pygame.font.Font(None, 28)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect(center=position)

        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(0, -30)  # float upward
        self.age = 0
        self.lifespan = lifespan

    def update(self, dt):
        self.age += dt
        if self.age >= self.lifespan:
            self.kill()
        else:
            self.position += self.velocity * dt
            self.rect.center = (int(self.position.x), int(self.position.y))
