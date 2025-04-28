import pygame
import sys

#imports
from player import Player
from constants import *
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

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

	#groups setup
	updatable = pygame.sprite.Group()
	drawable = pygame.sprite.Group()
	asteroids = pygame.sprite.Group()
	shots_group = pygame.sprite.Group()

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


		#drawing objects
		for drawable_object in drawable:
			drawable_object.draw(screen)


		pygame.display.flip()


if __name__ == "__main__":
    main()
