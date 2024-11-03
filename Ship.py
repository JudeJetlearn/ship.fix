import pgzrun
import random

WIDTH = 1200
HEIGHT = 650

Blue = (0, 0, 255)
White = (255, 255, 255)

gameover = False

ship = Actor("galaga")
ship.pos = (WIDTH // 2, HEIGHT - 60)
ship.dead = False
ship.countdown = 90

bug = Actor("bug")
speed = 5
direction = 1
bullets = []
enemies = []
score = 0

# Set up enemies in a grid
for x in range(8):
    for y in range(4):
        enemy = Actor("bug")
        enemy.x = 100 + 50 * x
        enemy.y = 80 + 50 * y
        enemies.append(enemy)

def display_score():
    screen.draw.text(f"Score: {score}", (30, 50), color=White)

def on_key_down(key):
    if key == keys.SPACE and not ship.dead:
        bullet = Actor("bullet")
        bullet.x = ship.x
        bullet.y = ship.y - 50
        bullets.append(bullet)

def update():
    global score, direction, gameover
    move_down = False
   
    # Move ship
    if not ship.dead:
        if keyboard.left and ship.x > 0:
            ship.x -= speed
        elif keyboard.right and ship.x < WIDTH:
            ship.x += speed

    # Move bullets
    for bullet in bullets[:]:
        bullet.y -= 10
        if bullet.y < 0:
            bullets.remove(bullet)

    # Check if game should be over
    if len(enemies) == 0:
        game_over()

    # Move enemies
    if len(enemies) > 0 and (enemies[-1].x > WIDTH - 80 or enemies[0].x < 80):
        move_down = True
        direction *= -1
    for enemy in enemies[:]:
        enemy.x += 5 * direction
        if move_down:
            enemy.y += 20
        if enemy.y > HEIGHT:
            enemies.remove(enemy)

    # Check for bullet collisions with enemies
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                score += 100
                bullets.remove(bullet)
                enemies.remove(enemy)
                break  # Stop checking other enemies for this bullet

    # Check if enemy collides with the ship
    for enemy in enemies:
        if enemy.colliderect(ship):
            ship.dead = True
            break

    # Handle ship respawn countdown
    if ship.dead:
        ship.countdown -= 1
        if ship.countdown == 0:
            ship.dead = False
            ship.countdown = 90

def game_over():
    global gameover
    gameover = True

def draw():
    screen.clear()
    screen.fill(Blue)
   
    if gameover:
        screen.draw.text("Game Over", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color=White)
    else:
        for bullet in bullets:
            bullet.draw()
        for enemy in enemies:
            enemy.draw()
        if not ship.dead:
            ship.draw()
        display_score()

pgzrun.go()
