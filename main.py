import pygame
import sys
import os

# Imports
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
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()

    # Load sound effects
    shoot_sound = pygame.mixer.Sound("sounds/shoot.wav")
    shoot_sound.set_volume(0.4)

    explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
    explosion_sound.set_volume(0.1)

    game_over_sound = pygame.mixer.Sound("sounds/game over.wav")
    game_over_sound.set_volume(0.7)

    # Load and play background music
    pygame.mixer.music.load("sounds/music.ogg")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # Setup screen and clock
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    BASE_SCORE = 50
    font = pygame.font.Font(None, 36)

    # High score setup
    highscore_file = "highscore.txt"
    highscore_name = "AAA"
    highscore_value = 0

    if os.path.exists(highscore_file):
        with open(highscore_file, "r") as f:
            try:
                data = f.read().split()
                highscore_name = data[0]
                highscore_value = int(data[1])
            except:
                pass

    entering_initials = False
    player_initials = ""

    # Game state
    updatable = None
    drawable = None
    asteroids = None
    shots_group = None
    floating_texts = None
    player = None
    asteroid_field = None
    score = 0
    game_over = False
    music_stopped = False  # 🆕 Track if music already stopped

    def reset_game():
        nonlocal updatable, drawable, asteroids, shots_group, floating_texts
        nonlocal player, asteroid_field, score, game_over, music_stopped
        nonlocal entering_initials, player_initials

        updatable = pygame.sprite.Group()
        drawable = pygame.sprite.Group()
        asteroids = pygame.sprite.Group()
        shots_group = pygame.sprite.Group()
        floating_texts = pygame.sprite.Group()

        Player.containers = (updatable, drawable)
        Asteroid.containers = (asteroids, updatable, drawable)
        AsteroidField.containers = (updatable,)
        Shot.containers = (shots_group, updatable, drawable)

        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        player.shots_group = shots_group
        player.shoot_sound = shoot_sound  # 🔫 inject shoot sound

        asteroid_field = AsteroidField()

        score = 0
        game_over = False
        music_stopped = False
        entering_initials = False
        player_initials = ""

    reset_game()

    while True:
        dt = clock.tick(60) / 1000
        screen.fill("black")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if game_over:
                if entering_initials:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE and len(player_initials) > 0:
                            player_initials = player_initials[:-1]
                        elif event.key == pygame.K_RETURN and len(player_initials) == 3:
                            with open(highscore_file, "w") as f:
                                f.write(f"{player_initials.upper()} {score}")
                            entering_initials = False
                        elif len(player_initials) < 3 and event.unicode.isalpha():
                            player_initials += event.unicode.upper()
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            reset_game()
                        else:
                            return

        if not game_over:
            updatable.update(dt)
            floating_texts.update(dt)

            for asteroid in asteroids:
                if player.collides_with(asteroid):
                    print("Game over!")
                    game_over = True
                    if not music_stopped:
                        pygame.mixer.music.stop()  # 🛑 Stop background music
                        game_over_sound.play()     # 🔔 Play Game Over sound
                        music_stopped = True
                    if score > highscore_value:
                        entering_initials = True

            for asteroid in asteroids:
                for shot in shots_group:
                    if shot.collides_with(asteroid) or asteroid.collides_with(shot):
                        asteroid.split()
                        shot.kill()
                        explosion_sound.play()

                        multiplier = asteroid.radius / ASTEROID_MIN_RADIUS
                        points = int(BASE_SCORE * multiplier)
                        score += points

                        text = FloatingText(f"+{points}", asteroid.position)
                        floating_texts.add(text)
        else:
            floating_texts.update(dt)

        for drawable_object in drawable:
            drawable_object.draw(screen)

        for shot in shots_group:
            shot.draw(screen)

        for text in floating_texts:
            screen.blit(text.image, text.rect)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_font = pygame.font.Font(None, 72)
            game_over_text = game_over_font.render("GAME OVER!", True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
            screen.blit(game_over_text, game_over_rect)

            if entering_initials:
                initials_font = pygame.font.Font(None, 48)
                initials_text = initials_font.render(f"Enter Initials: {player_initials}", True, (255, 255, 255))
                initials_rect = initials_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 10))
                screen.blit(initials_text, initials_rect)
            else:
                restart_font = pygame.font.Font(None, 36)
                restart_text = restart_font.render("Press R to Restart", True, (255, 255, 255))
                restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 30))
                screen.blit(restart_text, restart_rect)

            hs_font = pygame.font.Font(None, 36)
            hs_text = hs_font.render(f"High Score: {highscore_name} {highscore_value}", True, (255, 255, 255))
            hs_rect = hs_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 80))
            screen.blit(hs_text, hs_rect)

        pygame.display.flip()

if __name__ == "__main__":
    main()
