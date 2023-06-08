import pygame
import random
import argparse

pygame.init()
parser = argparse.ArgumentParser()
parser.add_argument("-F", help="set fullscreen mode", action="store_true")
args = parser.parse_args()

# Set up the display
fullscreen = args.F
screen_info = pygame.display.Info()
if fullscreen:
    WIDTH = screen_info.current_w
    HEIGHT = screen_info.current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
else:
    WIDTH = int(screen_info.current_w/1.5)
    HEIGHT = int(screen_info.current_h/1.5)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Flappy CubeSat")

# Set up the game variables
clock = pygame.time.Clock()
score = 0
game_over = False
pipe_width = int(WIDTH/20)
cubesat_width = int(HEIGHT/10)
started_game = False

# Load high scores
with open("high_scores.txt", "r") as f:
    high_score = int(f.read().strip())

# Load sounds
sound_effect = pygame.mixer.Sound("sound_design_effect_electricity_spark_002.mp3")
sound_effect.set_volume(0.05)
pygame.mixer.music.load("NyanCatoriginal.mp3")
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)

# Load images
bg_image = pygame.image.load("background.png").convert_alpha()
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
CubeSat_image = pygame.image.load("CubeSat.png").convert_alpha()
CubeSat_image = pygame.transform.scale(CubeSat_image, (cubesat_width, cubesat_width))
rainbow_image = pygame.image.load("walls.png").convert_alpha()

# Create masks
# CubeSat_mask = pygame.mask.from_surface(CubeSat_image, threshold=127)
# rainbow_mask = pygame.mask.from_surface(rainbow_image, threshold=127)

class Cubesat:
    def __init__(self):
        self.x = int(WIDTH/30)
        self.y = int(HEIGHT/2)
        self.velocity = -HEIGHT/73
        self.gravity = HEIGHT/2000
        self.width = cubesat_width
        self.height = cubesat_width

    def flap(self):
        self.velocity = int(-HEIGHT/73)
        sound_effect.play()

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

class Pipe:
    def __init__(self):
        self.x = WIDTH + 50
        self.y_gap = int(HEIGHT/2 - (score/69)*(HEIGHT/2))
        self.top_height = random.randint(75,HEIGHT-self.y_gap-75)
        self.bottom_height = HEIGHT - self.top_height - self.y_gap
        self.speed = WIDTH/60
        self.scored = False

    def off_screen(self):
        return self.x < -100

    def update(self):
        self.x -= self.speed
        self.top_rect = pygame.Rect(self.x, 0, pipe_width, self.top_height)
        self.bottom_rect = pygame.Rect(self.x, HEIGHT - self.bottom_height, pipe_width, self.bottom_height)
        self.top_invisible_rect = pygame.Rect(self.x, -100000, pipe_width, 100000)
        self.bottom_invisible_rect = pygame.Rect(self.x, HEIGHT, pipe_width, 100000)
        
        # self.top_pipe_mask = pygame.mask.from_surface(rainbow_image, threshold=127)
        # self.bottom_pipe_mask = pygame.mask.from_surface(rainbow_image, threshold=127)

    def collision(self, cubesat, pipe):
        if cubesat.rect.colliderect(self.top_rect) or cubesat.rect.colliderect(self.bottom_rect) or cubesat.rect.colliderect(self.top_invisible_rect) or cubesat.rect.colliderect(self.bottom_invisible_rect):
            #return True
            reset_game()
        # if CubeSat_mask.overlap_area(pipe.top_pipe_mask, (pipe.top_rect.x - cubesat.rect.x, pipe.top_rect.y - cubesat.rect.y)) > 0: #self.top_rect) or cubesat.rect.colliderect(self.bottom_rect) or cubesat.rect.colliderect(self.top_invisible_rect) or cubesat.rect.colliderect(self.bottom_invisible_rect):
        #     #return True
        #     reset_game()
        # elif CubeSat_mask.overlap_area(pipe.bottom_pipe_mask, (pipe.bottom_rect.x - cubesat.rect.x, pipe.bottom_rect.y - cubesat.rect.y)) > 0: #self.top_rect) or cubesat.rect.colliderect(self.bottom_rect) or cubesat.rect.colliderect(self.top_invisible_rect) or cubesat.rect.colliderect(self.bottom_invisible_rect):
        #     #return True
        #     reset_game()
        # elif CubeSat_mask.overlap_area(rainbow_mask, (pipe.top_invisible_rect.x - cubesat.rect.x, pipe.top_invisible_rect.y - cubesat.rect.y)) > 0: #self.top_rect) or cubesat.rect.colliderect(self.bottom_rect) or cubesat.rect.colliderect(self.top_invisible_rect) or cubesat.rect.colliderect(self.bottom_invisible_rect):
        #     #return True
        #     reset_game()
        # elif CubeSat_mask.overlap_area(rainbow_mask, (pipe.bottom_invisible_rect.x - cubesat.rect.x, pipe.bottom_invisible_rect.y - cubesat.rect.y)) > 0: #self.top_rect) or cubesat.rect.colliderect(self.bottom_rect) or cubesat.rect.colliderect(self.top_invisible_rect) or cubesat.rect.colliderect(self.bottom_invisible_rect):
        #     #return True
        #     reset_game()
        return False

def draw_score():
    font = pygame.font.Font(None, 50)
    score_text = font.render(f"Score: {score} High Score: {high_score}", True, (255, 255, 255))
    screen.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

def draw_game_over():
    font = pygame.font.Font(None, 70)
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))

def reset_game():
    global score, started_game
    if score > 1:
        draw_game_over()
        pygame.display.update()
        pygame.time.wait(2000)
    score = 0
    started_game = False

def main():
    global score, game_over, high_score, started_game, screen, fullscreen, HEIGHT, WIDTH, bg_image, rainbow_image, CubeSat_image, pipe_width

    # Set up the objects
    cubesat = Cubesat()
    pipes = [Pipe()]

    while not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cubesat.flap()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    cubesat.flap()

        # Update objects
        cubesat.update()
        for pipe in pipes:
            pipe.update()

            if pipe.off_screen():
                pipes.remove(pipe)
            elif pipe.collision(cubesat, pipe):
                game_over = True

            if pipe.x < cubesat.x and not pipe.scored:
                score += 1
                pipe.scored = True

            if pipe.x < -100 and len(pipes) < 3:
                pipes.append(Pipe())

        if score > high_score:
            high_score = score
            with open("high_scores.txt", "w") as f:
                f.write(str(high_score))


        # Draw objects
        screen.blit(bg_image, (0,0))
        for pipe in pipes:
            top_rainbow_image_temp = pygame.transform.scale(rainbow_image, (pipe_width, pipe.top_height))
            bottom_rainbow_image_temp = pygame.transform.scale(rainbow_image, (pipe_width, pipe.bottom_height))
            
            # pipe.top_pipe_mask = pygame.mask.from_surface(top_rainbow_image_temp, threshold=127)
            # pipe.bottom_pipe_mask = pygame.mask.from_surface(bottom_rainbow_image_temp, threshold=127)

            top_pipe_rect = top_rainbow_image_temp.get_rect(midbottom=(pipe.x, pipe.top_height))
            bottom_pipe_rect = bottom_rainbow_image_temp.get_rect(midtop=(pipe.x, HEIGHT-pipe.bottom_height))

            screen.blit(top_rainbow_image_temp, top_pipe_rect)
            screen.blit(pygame.transform.rotate(bottom_rainbow_image_temp,180), bottom_pipe_rect)
        screen.blit(CubeSat_image, (cubesat.x, cubesat.y))
        draw_score()

        # Update the display and tick the clock
        pygame.display.update()
        if started_game == False:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        break
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        break
                    if event.type == pygame.QUIT:
                        game_over = True
                        draw_game_over()
                        break
                else:
                    continue
                started_game = True
                sound_effect.play()
                break
        else:
            clock.tick(60)

    # Draw the game over text and update the display one last time before quitting
    draw_game_over()
    pygame.display.update()
    pygame.time.wait(2000)

if __name__ == "__main__":
    main()
