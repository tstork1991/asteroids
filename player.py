# imports
import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0

    # Define the triangle shape of the ship
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    # Draw the player
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    # Rotate the player
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    # Move the player
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    # Player shooting
    def shoot(self, shots_group):
        if self.shoot_timer > 0:
            return

        # Get the forward direction based on player's rotation
        forward = pygame.Vector2(0, 1).rotate(self.rotation)

        # Create the shot at the front of the ship
        shot_pos = self.position + forward * self.radius
        new_shot = Shot(shot_pos.x, shot_pos.y)

        # Set velocity in forward direction
        new_shot.velocity = forward * PLAYER_SHOOT_SPEED

        shots_group.add(new_shot)
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN

        # 🔫 Play shooting sound if available
        if hasattr(self, 'shoot_sound'):
            self.shoot_sound.play()

    # Player update location and actions
    def update(self, dt):
        self.shoot_timer -= dt
        self.shoot_timer = max(self.shoot_timer, 0)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE] and hasattr(self, "shots_group"):
            self.shoot(self.shots_group)
