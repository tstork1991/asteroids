import pygame

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
	print("CircleShape loaded!")
	def __init__(self, x, y, radius):
		# we will be using this later
		if hasattr(self, "containers"):
			super().__init__(self.containers)
		else:
			super().__init__()

		self.position = pygame.Vector2(x, y)
		self.velocity = pygame.Vector2(0, 0)
		self.radius = radius

		# Add this to CircleShape.__init__ after setting self.radius
		self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
		pygame.draw.circle(self.image, (255, 255, 255, 0), (radius, radius), radius)  # Transparent circle
		self.rect = self.image.get_rect()
		self.rect.centerx = int(x)
		self.rect.centery = int(y)


	def draw(self, screen):
		# sub-classes must override
		pass

	def update(self, dt):
		# sub-classes must override
		self.position += self.velocity * dt
		# Update rect position to match the actual position
		self.rect.centerx = int(self.position.x)
		self.rect.centery = int(self.position.y)

	def collides_with(self, other):
		distance = self.position.distance_to(other.position)
		sum_radius = self.radius + other.radius
		return  distance <= sum_radius


