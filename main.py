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


	#Player setup
	player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

	#game loop
	while True:
		for event in pygame.event.get():
   		 	if event.type == pygame.QUIT:
        			return
		screen.fill("black")
		player.draw(screen)
		pygame.display.flip()
		dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
