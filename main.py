import asyncio
import pygame  
from cubesat import Cubesat
from pipe import Pipe
  
pygame.init() 

WIDTH = 1024 # 3072
HEIGHT = 640 # 1920
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pipe_width = int(WIDTH/20)
cubesat_width = int(HEIGHT/10)

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

bg_image = pygame.image.load("assets/background.png").convert_alpha()
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
CubeSat_image = pygame.image.load("assets/CubeSat.png").convert_alpha()
CubeSat_image = pygame.transform.scale(CubeSat_image, (cubesat_width, cubesat_width))
rainbow_image = pygame.image.load("assets/walls.png").convert_alpha()

async def main():
    global score, game_over, high_score, started_game, screen, HEIGHT, WIDTH, bg_image, rainbow_image, CubeSat_image, pipe_width

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

    # Set up the objects
    cubesat = Cubesat(WIDTH,HEIGHT)
    pipes = [Pipe(WIDTH,HEIGHT,score)]

    while not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cubesat.flap(HEIGHT)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    cubesat.flap(HEIGHT)

        # Update objects
        cubesat.update()
        for pipe in pipes:
            pipe.update(WIDTH,HEIGHT)

            if pipe.off_screen():
                pipes.remove(pipe)
            elif pipe.collision(cubesat):
                game_over = True
                reset_game()

            if pipe.x < cubesat.x and not pipe.scored:
                score += 1
                pipe.scored = True

            if pipe.x < -100 and len(pipes) < 3:
                pipes.append(Pipe(WIDTH,HEIGHT,score))

        if score > high_score:
            high_score = score

        # Draw objects
        screen.blit(bg_image, (0,0))
        for pipe in pipes:
            top_rainbow_image_temp = pygame.transform.scale(rainbow_image, (pipe_width, pipe.top_height))
            bottom_rainbow_image_temp = pygame.transform.scale(rainbow_image, (pipe_width, pipe.bottom_height))

            top_pipe_rect = top_rainbow_image_temp.get_rect(midbottom=(pipe.x, pipe.top_height))
            bottom_pipe_rect = bottom_rainbow_image_temp.get_rect(midtop=(pipe.x, HEIGHT-pipe.bottom_height))

            screen.blit(top_rainbow_image_temp, top_pipe_rect)
            screen.blit(pygame.transform.rotate(bottom_rainbow_image_temp,180), bottom_pipe_rect)
        screen.blit(CubeSat_image, (cubesat.x, cubesat.y))
        draw_score()

        # Update the display and tick the clock
        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0) # very important, and keep it 0

    # Draw the game over text and update the display one last time before quitting
    draw_game_over()
    pygame.display.update()
    pygame.time.wait(2000)

asyncio.run(main())