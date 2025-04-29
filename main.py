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
    explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
    game_over_sound = pygame.mixer.Sound("sounds/game over.wav")

    pygame.mixer.music.load("sounds/music.ogg")
    pygame.mixer.music.play(-1)

    # Volume state
    music_volume = 0.5
    sfx_volume = 0.5
    muted = False
    volume_display_timer = 0
    volume_display_font = pygame.font.Font(None, 30)

    def apply_volume():
        if muted:
            shoot_sound.set_volume(0)
            explosion_sound.set_volume(0)
            pygame.mixer.music.set_volume(0)
            game_over_sound.set_volume(0)
        else:
            shoot_sound.set_volume(sfx_volume * 0.8)
            explosion_sound.set_volume(sfx_volume * 0.1)
            pygame.mixer.music.set_volume(music_volume * 0.5)
            game_over_sound.set_volume(sfx_volume * 0.7)

    apply_volume()

    # Pause system
    paused = False
    showing_instructions = False
    pause_font = pygame.font.Font(None, 48)
    pause_options = ["Resume", "Music Volume", "SFX Volume", "Instructions", "Quit"]
    selected_option = 0

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    BASE_SCORE = 50
    font = pygame.font.Font(None, 36)

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

    updatable = None
    drawable = None
    asteroids = None
    shots_group = None
    floating_texts = None
    player = None
    asteroid_field = None
    score = 0
    game_over = False
    music_stopped = False

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
        player.shoot_sound = shoot_sound

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

        if volume_display_timer > 0:
            volume_display_timer -= dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if showing_instructions:
                    if event.key == pygame.K_ESCAPE:
                        showing_instructions = False

                elif paused and not game_over:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(pause_options)
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(pause_options)
                    if event.key == pygame.K_LEFT:
                        if pause_options[selected_option] == "Music Volume":
                            music_volume = max(music_volume - 0.1, 0.0)
                            apply_volume()
                        if pause_options[selected_option] == "SFX Volume":
                            sfx_volume = max(sfx_volume - 0.1, 0.0)
                            apply_volume()
                    if event.key == pygame.K_RIGHT:
                        if pause_options[selected_option] == "Music Volume":
                            music_volume = min(music_volume + 0.1, 1.0)
                            apply_volume()
                        if pause_options[selected_option] == "SFX Volume":
                            sfx_volume = min(sfx_volume + 0.1, 1.0)
                            apply_volume()
                    if event.key == pygame.K_RETURN:
                        option = pause_options[selected_option]
                        if option == "Resume":
                            paused = False
                        elif option == "Quit":
                            pygame.quit()
                            sys.exit()
                        elif option == "Instructions":
                            showing_instructions = True

                else:
                    if event.key == pygame.K_p:
                        paused = not paused

                    if not paused and not game_over:
                        if event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                            sfx_volume = min(sfx_volume + 0.1, 1.0)
                            apply_volume()
                            volume_display_timer = 3
                        if event.key == pygame.K_MINUS:
                            sfx_volume = max(sfx_volume - 0.1, 0.0)
                            apply_volume()
                            volume_display_timer = 3
                        if event.key == pygame.K_m:
                            muted = not muted
                            apply_volume()
                            volume_display_timer = 3

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

        if not paused and not game_over:
            updatable.update(dt)
            floating_texts.update(dt)

            for asteroid in asteroids:
                if player.collides_with(asteroid):
                    game_over = True
                    if not music_stopped:
                        pygame.mixer.music.stop()
                        game_over_sound.play()
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

        if volume_display_timer > 0:
            vol_text = "Muted" if muted else f"SFX Volume: {int(sfx_volume * 100)}%"
            vol_render = volume_display_font.render(vol_text, True, (255, 255, 0))
            vol_rect = vol_render.get_rect(center=(SCREEN_WIDTH / 2, 30))
            screen.blit(vol_render, vol_rect)

        if paused and not game_over:
            if showing_instructions:
                # Draw Instructions
                title = pause_font.render("INSTRUCTIONS", True, (255, 255, 0))
                title_rect = title.get_rect(center=(SCREEN_WIDTH/2, 80))
                screen.blit(title, title_rect)

                instructions = [
                    "Move: W / A / S / D",
                    "Rotate: A / D",
                    "Shoot: SPACE",
                    "Pause: P",
                    "Increase Volume: +",
                    "Decrease Volume: -",
                    "Mute: M",
                    "",
                    "Press ESC to return"
                ]

                for i, line in enumerate(instructions):
                    line_text = font.render(line, True, (255, 255, 255))
                    line_rect = line_text.get_rect(center=(SCREEN_WIDTH/2, 150 + i * 40))
                    screen.blit(line_text, line_rect)

            else:
                # Draw normal Pause Menu
                title = pause_font.render("PAUSED", True, (255, 255, 0))
                title_rect = title.get_rect(center=(SCREEN_WIDTH/2, 100))
                screen.blit(title, title_rect)

                for idx, option in enumerate(pause_options):
                    if option == "Music Volume":
                        text = f"Music Volume: {int(music_volume * 100)}%"
                    elif option == "SFX Volume":
                        text = f"SFX Volume: {int(sfx_volume * 100)}%"
                    else:
                        text = option

                    color = (255, 255, 0) if idx == selected_option else (255, 255, 255)
                    option_text = font.render(text, True, color)
                    option_rect = option_text.get_rect(center=(SCREEN_WIDTH/2, 200 + idx * 40))
                    screen.blit(option_text, option_rect)

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
                restart_font = font.render("Press R to Restart", True, (255, 255, 255))
                restart_rect = restart_font.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 30))
                screen.blit(restart_text, restart_rect)

            hs_font = font.render(f"High Score: {highscore_name} {highscore_value}", True, (255, 255, 255))
            hs_rect = hs_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 80))
            screen.blit(hs_text, hs_rect)

        pygame.display.flip()

if __name__ == "__main__":
    main()
