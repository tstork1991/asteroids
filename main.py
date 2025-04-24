import pygame

#imports
from player import Player
from constants import *

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
	Player.containers = (updatable, drawable)

	#Player setup
	player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)



	#game loop
	while True:
		for event in pygame.event.get():
   		 	if event.type == pygame.QUIT:
        			return

		dt = clock.tick(60) / 1000
		updatable.update(dt)

		screen.fill("black")

		for drawable_object in drawable:
			drawable_object.draw(screen)

		pygame.display.flip()


if __name__ == "__main__":
    main()
