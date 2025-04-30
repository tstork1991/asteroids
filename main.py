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
from parallax import ParallaxStarField

print("Starting Asteroids!")
print(f"Screen width: {SCREEN_WIDTH}")
print(f"Screen height: {SCREEN_HEIGHT}")

def show_instructions(screen):
    font = pygame.font.Font(None, 36)
    lines = [
        "INSTRUCTIONS",
        "",
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
    while True:
        screen.fill("black")
        for i, line in enumerate(lines):
            txt = font.render(line, True, (255, 255, 255))
            screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH/2, 80 + i * 40)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
        pygame.display.flip()
        pygame.time.Clock().tick(60)

def show_high_scores(screen):
    font = pygame.font.Font(None, 36)
    highscore_file = "highscore.txt"
    highscores = []
    if os.path.exists(highscore_file):
        with open(highscore_file, "r") as f:
            for line in f:
                try:
                    name, value = line.strip().split()
                    highscores.append((name, int(value)))
                except:
                    continue
        highscores = sorted(highscores, key=lambda x: x[1], reverse=True)[:5]

    while True:
        screen.fill("black")
        title = font.render("HIGH SCORES", True, (255, 255, 0))
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH/2, 60)))
        for i, (name, score) in enumerate(highscores):
            line = font.render(f"{i+1}. {name} {score}", True, (255, 255, 255))
            screen.blit(line, line.get_rect(center=(SCREEN_WIDTH/2, 120 + i * 40)))
        prompt = font.render("Press ESC to return", True, (255, 255, 255))
        screen.blit(prompt, prompt.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT - 60)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        pygame.display.flip()
        pygame.time.Clock().tick(60)

def show_main_menu(screen):
    menu_font = pygame.font.Font(None, 60)
    menu_options = ["Start Game", "Instructions", "High Scores", "Quit"]
    selected = 0

    pygame.mixer.music.load("sounds/menu.wav")
    pygame.mixer.music.play(-1)

    while True:
        screen.fill("black")
        title = menu_font.render("ASTEROIDS", True, (255, 255, 0))
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH/2, 100)))

        for i, option in enumerate(menu_options):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            txt = menu_font.render(option, True, color)
            screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH/2, 200 + i * 60)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_UP]:
                    selected = (selected - 1) % len(menu_options)
                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    selected = (selected + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    choice = menu_options[selected]
                    if choice == "Start Game":
                        pygame.mixer.music.stop()
                        return
                    elif choice == "Instructions":
                        show_instructions(screen)
                    elif choice == "High Scores":
                        show_high_scores(screen)
                    elif choice == "Quit":
                        pygame.quit()
                        sys.exit()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

def main():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    show_main_menu(screen)

    # Load sounds
    shoot_sound = pygame.mixer.Sound("sounds/shoot.wav")
    explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
    game_over_sound = pygame.mixer.Sound("sounds/game over.wav")
    pygame.mixer.music.load("sounds/music.ogg")
    pygame.mixer.music.play(-1)

    music_volume = 0.5
    sfx_volume = 0.5
    muted = False
    def apply_volume():
        volume = 0 if muted else 1
        shoot_sound.set_volume(sfx_volume * 0.8 * volume)
        explosion_sound.set_volume(sfx_volume * 0.1 * volume)
        game_over_sound.set_volume(sfx_volume * 0.7 * volume)
        pygame.mixer.music.set_volume(music_volume * 0.5 * volume)
    apply_volume()

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    BASE_SCORE = 50

    highscore_file = "highscore.txt"
    highscores = []
    if os.path.exists(highscore_file):
        with open(highscore_file, "r") as f:
            for line in f:
                try:
                    name, value = line.strip().split()
                    highscores.append((name, int(value)))
                except:
                    continue
        highscores = sorted(highscores, key=lambda x: x[1], reverse=True)[:5]

    entering_initials = False
    player_initials = ""
    game_over = False
    music_stopped = False
    paused = False

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
    starfield = ParallaxStarField(SCREEN_WIDTH, SCREEN_HEIGHT, [10, 30, 60])

    score = 0

    while True:
        dt = clock.tick(60) / 1000
        screen.fill("black")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if game_over:
                    if entering_initials:
                        if event.key == pygame.K_BACKSPACE and len(player_initials) > 0:
                            player_initials = player_initials[:-1]
                        elif event.key == pygame.K_RETURN and len(player_initials) == 3:
                            highscores.append((player_initials.upper(), score))
                            highscores = sorted(highscores, key=lambda x: x[1], reverse=True)[:5]
                            with open(highscore_file, "w") as f:
                                for name, value in highscores:
                                    f.write(f"{name} {value}\n")
                            entering_initials = False
                        elif event.unicode.isalpha() and len(player_initials) < 3:
                            player_initials += event.unicode.upper()
                    else:
                        if event.key == pygame.K_r:
                            return main()
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                elif event.key == pygame.K_p:
                    paused = not paused

        if not game_over:
            starfield.update(dt)
            updatable.update(dt)
            floating_texts.update(dt)

            for asteroid in asteroids:
                if player.collides_with(asteroid):
                    game_over = True
                    if not music_stopped:
                        pygame.mixer.music.stop()
                        game_over_sound.play()
                        music_stopped = True
                    if score > 0 and (len(highscores) < 5 or score > highscores[-1][1]):
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

        starfield.draw(screen)
        for drawable_object in drawable:
            drawable_object.draw(screen)
        for shot in shots_group:
            shot.draw(screen)
        for text in floating_texts:
            screen.blit(text.image, text.rect)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        if game_over:
            title_font = pygame.font.Font(None, 72)
            title_text = title_font.render("GAME OVER!", True, (255, 0, 0))
            screen.blit(title_text, title_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50)))
            if entering_initials:
                enter_font = pygame.font.Font(None, 48)
                enter_text = enter_font.render(f"Enter Initials: {player_initials}", True, (255, 255, 255))
                screen.blit(enter_text, enter_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 10)))
            else:
                restart_font = font.render("Press R to Restart or ESC to Quit", True, (255, 255, 255))
                screen.blit(restart_font, restart_font.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 30)))
            for i, (name, value) in enumerate(highscores):
                hs_text = font.render(f"{i+1}. {name} {value}", True, (255, 255, 255))
                screen.blit(hs_text, hs_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 80 + i * 30)))

        pygame.display.flip()

if __name__ == "__main__":
    main()
