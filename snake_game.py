import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 20
FPS = 10

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

# Snake class
class Snake:
    def __init__(self):
        self.body = [(200, 200)]
        self.direction = 'RIGHT'

    def move(self):
        x, y = self.body[0]
        if self.direction == 'RIGHT':
            self.body.insert(0, ((x + BLOCK_SIZE) % SCREEN_WIDTH, y))
        elif self.direction == 'LEFT':
            self.body.insert(0, ((x - BLOCK_SIZE + SCREEN_WIDTH) % SCREEN_WIDTH, y))
        elif self.direction == 'UP':
            self.body.insert(0, (x, (y - BLOCK_SIZE + SCREEN_HEIGHT) % SCREEN_HEIGHT))
        elif self.direction == 'DOWN':
            self.body.insert(0, (x, (y + BLOCK_SIZE) % SCREEN_HEIGHT))

    def change_direction(self, new_direction):
        if (new_direction == 'UP' and self.direction != 'DOWN') or \
            (new_direction == 'DOWN' and self.direction != 'UP') or \
            (new_direction == 'LEFT' and self.direction != 'RIGHT') or \
                (new_direction == 'RIGHT' and self.direction != 'LEFT'):
            self.direction = new_direction

    def check_collision(self):
        if self.body[0] in self.body[1:]:
            return True
        return False

# Food class
class Food:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH // BLOCK_SIZE - 1) * BLOCK_SIZE
        self.y = random.randint(0, SCREEN_HEIGHT // BLOCK_SIZE - 1) * BLOCK_SIZE

    def respawn(self):
        self.x = random.randint(0, SCREEN_WIDTH // BLOCK_SIZE - 1) * BLOCK_SIZE
        self.y = random.randint(0, SCREEN_HEIGHT // BLOCK_SIZE - 1) * BLOCK_SIZE

# AI class that chases the player
class AI:
    def __init__(self, player):
        self.player = player

    def move(self):
        player_x, player_y = self.player.body[0]
        ai_x, ai_y = self.player.body[0]

        if player_x > ai_x:
            self.player.change_direction('RIGHT')
        elif player_x < ai_x:
            self.player.change_direction('LEFT')
        elif player_y > ai_y:
            self.player.change_direction('DOWN')
        else:
            self.player.change_direction('UP')

# Game Over function
def game_over():
    font = pygame.font.SysFont('Arial', 48)
    text = font.render('Game Over', True, RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

# Draw Score function
def draw_score(score):
    font = pygame.font.SysFont('Arial', 24)
    text = font.render('Score: {}'.format(score), True, BLUE)
    screen.blit(text, (10, 10))

# Initialize game objects
snake = Snake()
food = Food()
ai = AI(snake)

# Game loop
score = 0
clock = pygame.time.Clock()

while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction('UP')
            elif event.key == pygame.K_DOWN:
                snake.change_direction('DOWN')
            elif event.key == pygame.K_LEFT:
                snake.change_direction('LEFT')
            elif event.key == pygame.K_RIGHT:
                snake.change_direction('RIGHT')

    snake.move()
    ai.move()

    if snake.body[0] == food:
        score += 1
        snake.body.append((0, 0))  # Add a new block to the snake
        food.respawn()

    if snake.check_collision() or snake.body[0][0] not in range(SCREEN_WIDTH) or \
            snake.body[0][1] not in range(SCREEN_HEIGHT):
        game_over()

    # Draw the snake
    for block in snake.body:
        pygame.draw.rect(screen, GREEN, (block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))

    # Draw the food
    pygame.draw.rect(screen, RED, (food.x, food.y, BLOCK_SIZE, BLOCK_SIZE))

    draw_score(score)

    pygame.display.flip()
    clock.tick(FPS)