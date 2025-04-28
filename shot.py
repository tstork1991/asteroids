#imports
import pygame
from circleshape import CircleShape
from constants import *

class Shot(CircleShape):
	def __init__(self,x, y):
		super().__init__(x, y, SHOT_RADIUS)
		self.velocity = pygame.Vector2(0, 0)

	def draw(self, screen):
		pygame.draw.circle(screen, "white", (int(self.position.x), int(self.position.y)), SHOT_RADIUS)

	def update(self, dt):
		self.position += self.velocity * dt

		#Update the rect position to match actual position
		self.rect.centerx = int(self.position.x)
		self.rect.centery = int(self.position.y)

		# Check if out of bounds
		if (self.position.x < 0 or 
			self.position.x > SCREEN_WIDTH or 
			self.position.y < 0 or 
			self.position.y > SCREEN_HEIGHT):
			self.kill()
