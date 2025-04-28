#imports
import random
import pygame
from constants import *
from circleshape import CircleShape

class Asteroid(CircleShape):
	def __init__(self, x, y, radius=40, velocity=None):
		if velocity is None:
			angle =random.uniform(0, 360)
			velocity =pygame.Vector2(1, 0).rotate(angle) *100
		super().__init__( x, y, radius)
		self.velocity = velocity

	def draw(self, screen):
		pygame.draw.circle(screen, "white", tuple(map(int, self.position)), self.radius,  2)

	def update(self, dt):
		self.position += self.velocity * dt 

	def split(self):
		if self.radius <= ASTEROID_MIN_RADIUS:
			self. kill()
			return

		# Random angle between 20 and 50 degrees
		random_angle = random.uniform(20, 50)

		# Original velocity rotated to get diverging paths
		new_velocity1 = self.velocity.rotate(random_angle) * 1.2
		new_velocity2 = self.velocity.rotate(-random_angle) * 1.2

		# New radius (smaller asteroid)
		new_radius = self.radius - ASTEROID_MIN_RADIUS

		# Create 2 new smaller asteroids at the same position
		asteroid1 = Asteroid(self.position.x, self.position.y, new_radius, new_velocity1)
		asteroid2 = Asteroid(self.position.x, self.position.y, new_radius, new_velocity2)

		self.kill()
