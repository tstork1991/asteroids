import pygame
import sys

#imports
from player import Player
from constants import *
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from floatingtext import FloatingText


print("Starting Asteroids!")
print(f"Screen width: {SCREEN_WIDTH}")
print(f"Screen height: {SCREEN_HEIGHT}")

def main():
	#Initialize pygame
	pygame.init() 
 
	#Create Screen
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 

	#Game clock-60fps
	clock = pygame.time.Clock() 
	dt = 0

	#Scoring system
	score = 0
	font = pygame.font.Font(None, 36)
	BASE_SCORE = 50

	#groups setup
	updatable = pygame.sprite.Group()
	drawable = pygame.sprite.Group()
	asteroids = pygame.sprite.Group()
	shots_group = pygame.sprite.Group()
	floating_texts = pygame.sprite.Group()


	#Group containers
	Player.containers = (updatable, drawable)
	Asteroid.containers = (asteroids, updatable, drawable)
	AsteroidField.containers = (updatable,)
	Shot.containers = (shots_group, updatable, drawable)

	#Player setup
	player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
	player.shots_group = shots_group

	#Asteroid Field setup
	asteroid_field = AsteroidField()


	#game loop
	while True:
		for event in pygame.event.get():
   		 	if event.type == pygame.QUIT:
        			return

		dt = clock.tick(60) / 1000
		updatable.update(dt)
		floating_texts.update(dt)
		screen.fill("black")

		for asteroid in asteroids:
			if player.collides_with(asteroid):
				print("Game over!")
				sys.exit()


		#kill the asteroids
		for asteroid in asteroids:
			for shot in shots_group:
				if shot.collides_with(asteroid) or asteroid.collides_with(shot):
					asteroid.split()
					shot.kill()

					multiplier = asteroid.radius / ASTEROID_MIN_RADIUS
					points = int(BASE_SCORE * multiplier)
					score += points

					text = FloatingText(f"+{points}", asteroid.position)
					floating_texts.add(text)


		#drawing objects
		for drawable_object in drawable:
			drawable_object.draw(screen)


		# Draw score
		score_text = font.render(f"Score: {score}", True, (255, 255, 255))
		screen.blit(score_text, (10, 10))

		#floating text from kill
		for text in floating_texts:
			screen.blit(text.image, text.rect)

		pygame.display.flip()


if __name__ == "__main__":
    main()
