#imports
import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
	def __init__(self, x, y):
		super().__init__(x,y, PLAYER_RADIUS)
		self.rotation = 0
		self.shoot_timer = 0

	# in the player class
	def triangle(self):
    		forward = pygame.Vector2(0, 1).rotate(self.rotation)
    		right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
    		a = self.position + forward * self.radius
    		b = self.position - forward * self.radius - right
    		c = self.position - forward * self.radius + right
    		return [a, b, c]

	# draw player shape
	def draw(self, screen):
    		pygame.draw.polygon(screen, "white", self.triangle(), 2)

	# player rotation
	def rotate(self, dt):
		self.rotation += PLAYER_TURN_SPEED * dt

	#player movement
	def move(self, dt):
		forward = pygame.Vector2(0, 1).rotate(self.rotation)
		self.position += forward * PLAYER_SPEED * dt

	#player shooting
	def shoot(self, shots_group):
		if self.shoot_timer > 0:
			return
		new_shot = Shot(self.position.x, self.position.y)
		shot_direction = pygame.Vector2(0,-1)
		shot_direction = shot_direction.rotate(self.rotation)
		new_shot.velocity = shot_direction * PLAYER_SHOOT_SPEED
		shots_group.add(new_shot)
		self.shoot_timer = PLAYER_SHOOT_COOLDOWN

	# player update location 
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
