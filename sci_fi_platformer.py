import pyglet
from pyglet.window import key
import random

# Window dimensions
window = pyglet.window.Window(800, 600)

# Load player character
player_image = pyglet.resource.image('player.png')
player_sprite = pyglet.sprite.Sprite(player_image)

# Load enemy character
enemy_image = pyglet.resource.image('enemy.png')
enemy_sprite = pyglet.sprite.Sprite(enemy_image)

# Load spaceship
spaceship_image = pyglet.resource.image('spaceship.png')
spaceship_sprite = pyglet.sprite.Sprite(spaceship_image)

# Load car sound effect
car_sound = pyglet.resource.media('car.wav', streaming=False)

# Player and enemy positions
player_x, player_y = 50, 50
enemy_x, enemy_y = 600, 50
spaceship_x, spaceship_y = 750, 50

# Car variables
cars = []
car_speed = 5
car_interval = 100
next_car = car_interval

# Player movement variables
player_speed = 200
keys = key.KeyStateHandler()
window.push_handlers(keys)

# Game over variable
game_over = False

@window.event
def on_draw():
    window.clear()
    player_sprite.draw()
    enemy_sprite.draw()
    spaceship_sprite.draw()
    for car in cars:
        car.draw()

def update(dt):
    global player_x, player_y, enemy_x, enemy_y, game_over, next_car

    if not game_over:
        # Player movement
        if keys[key.LEFT]:
            player_x -= player_speed * dt
        if keys[key.RIGHT]:
            player_x += player_speed * dt
        if keys[key.UP]:
            player_y += player_speed * dt
        if keys[key.DOWN]:
            player_y -= player_speed * dt

        # Enemy movement towards the player
        if enemy_x > player_x:
            enemy_x -= player_speed * dt
        if enemy_x < player_x:
            enemy_x += player_speed * dt
        if enemy_y > player_y:
            enemy_y -= player_speed * dt
        if enemy_y < player_y:
            enemy_y += player_speed * dt

        # Check collision with cars
        for car in cars:
            if (player_x + 20 < car.x + 40 and player_x + 60 > car.x and
                player_y + 20 < car.y + 40 and player_y + 60 > car.y):
                game_over = True

        # Add new car
        next_car -= 1
        if next_car == 0:
            cars.append(pyglet.sprite.Sprite(pyglet.resource.image('car.png'), random.randint(0, window.width - 50), window.height))
            car_sound.play()
            next_car = car_interval

        # Update cars positions
        for car in cars:
            car.y -= car_speed
            if car.y < 0:
                cars.remove(car)

        # Check if player reached the spaceship
        if (player_x + 20 < spaceship_x + 50 and player_x + 60 > spaceship_x and
            player_y + 20 < spaceship_y + 50 and player_y + 60 > spaceship_y):
            game_over = True
            print("You escaped! You win!")

pyglet.clock.schedule_interval(update, 1/120)
pyglet.app.run()