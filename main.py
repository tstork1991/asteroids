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
    game_over = False

    #Create Screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 

    #Game clock-60fps
    clock = pygame.time.Clock() 
    dt = 0

    #Scoring system
    score = 0
    font = pygame.font.Font(None, 36)
    BASE_SCORE = 50

    # These need to exist BEFORE reset_game() so they can be nonlocal
    updatable = None
    drawable = None
    asteroids = None
    shots_group = None
    floating_texts = None
    player = None
    asteroid_field = None
    score = 0

    font = pygame.font.Font(None, 36)
    BASE_SCORE = 50

    def reset_game():
        nonlocal updatable, drawable, asteroids, shots_group, floating_texts
        nonlocal player, asteroid_field, score, game_over

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

        #Reset game state
        score = 0
        game_over = False

    reset_game()

    #game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                else:
                    return

        dt = clock.tick(60) / 1000

        if not game_over:
            updatable.update(dt)
            floating_texts.update(dt)

            for asteroid in asteroids:
                if player.collides_with(asteroid):
                    print("Game over!")
                    game_over = True

            # Kill the asteroids only if game is NOT over
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

        else:
            # Always update floating texts so they fade out
            floating_texts.update(dt)

        screen.fill("black")

        #drawing objects
        for drawable_object in drawable:
            drawable_object.draw(screen)


        # Draw score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_font = pygame.font.Font(None, 72)
            game_over_text = game_over_font.render("GAME OVER!", True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            screen.blit(game_over_text, game_over_rect)

            restart_font = pygame.font.Font(None, 36)
            restart_text = restart_font.render("Press R to Restart", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 30))
            screen.blit(restart_text, restart_rect)

        #floating text from kill
        for text in floating_texts:
            screen.blit(text.image, text.rect)

        pygame.display.flip()


if __name__ == "__main__":
    main()
