import pygame

#! i made a 2 projectile classes for each player to try and fix the clumping of the bullets with player 2
#! IT didnt work but i am going to leave it there becuase i feel it looks better like that


# initializes every command

pygame.init()
# Creates a game window
WIDTH, HEIGHT = 800, 500

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fight Or Die")
clock = pygame.time.Clock()
score = pygame.font.SysFont("arial", 50, True)
# The player1 class with  all the player1 attributes and functions


class P1(object):
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.hitbox = (self.x + 20, self.y + 16, 60, 54)
        self.health = self.original_health = 50
        self.right = False
        self.left = False

    def draw(self, win):
        win.fill((0, 0, 0))
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.height))
        self.hitbox = (self.x - 14, self.y - 6.5, 90, 75)
        if self.health >= 0:
            pygame.draw.rect(
                win, (255, 255, 255), (self.x + 7, self.y - 15, self.health, 10)
            )

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.health = self.original_health


# The player2 class with all the enemy attributes and functions
class P2(object):
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.jumpCount = 10
        self.isJump = False
        self.hitbox = (self.x + 20, self.y + 16, 60, 54)
        self.health = self.original_health = 50
        self.right = False
        self.left = False

    def draw(self, win):
        pygame.draw.rect(win, (255, 155, 0), (self.x, self.y, self.width, self.height))
        self.hitbox = (self.x - 14, self.y - 6.5, 90, 75)
        if self.health >= 0:
            pygame.draw.rect(
                win, (255, 255, 255), (self.x + 7, self.y - 15, self.health, 10)
            )

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.health = self.original_health


# The projectile class for all player 1 throwable weapons
class Projectile1(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, (255, 0, 0), (self.x, self.y), self.radius)


# The projectile for all player 2 throwable objects
class Projectile2(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, (255, 155, 0), (self.x, self.y), self.radius)


# Make sure every things comes on screen
def redrawgamewindow():
    player1.draw(win)
    player2.draw(win)
    for dagger in daggers:
        dagger.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


# The classes allocated into one name
player1 = P1(550, 400, 64, 64)
player2 = P2(500, 400, 64, 64)
shootcycle = 0
shootloop = 0
daggers = []
bullets = []

# The main loop
run = True
while run:
    clock.tick(55)
    # Code for the bullet movement
    if shootcycle > 0:
        shootcycle += 1
    if shootcycle > 3:
        shootcycle = 0
    if shootloop > 0:
        shootloop += 1
    if shootloop > 3:
        shootloop = 0

    if player1.health <= 0:
        player1.reset()

    if player2.health <= 0:
        player2.reset()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for dagger in daggers:
        if (
            dagger.y - dagger.radius < player2.hitbox[1] + player2.hitbox[3]
            and dagger.y + dagger.radius > player2.hitbox[1]
        ):
            if (
                dagger.x + dagger.radius > player2.hitbox[0]
                and dagger.x - dagger.radius < player2.hitbox[0] + player2.hitbox[2]
            ):
                player2.health -= 1
                daggers.pop(daggers.index(dagger))

        if dagger.x < 800 and dagger.x > 0:
            dagger.x += dagger.vel
        else:
            daggers.pop(daggers.index(dagger))

    for bullet in bullets:
        if (
            bullet.y - bullet.radius < player1.hitbox[1] + player1.hitbox[3]
            and bullet.y + bullet.radius > player1.hitbox[1]
        ):
            if (
                bullet.x + bullet.radius > player1.hitbox[0]
                and bullet.x - bullet.radius < player1.hitbox[0] + player1.hitbox[2]
            ):
                player1.health -= 1
                bullets.pop(bullets.index(bullet))

        if bullet.x < 800 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    # Key mapping code
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT] and player1.x < WIDTH - player1.width - player1.vel:
        player1.x += player1.vel
        player1.right = True
        player1.left = False
    elif keys[pygame.K_LEFT] and player1.x > player1.vel:
        player1.x -= player1.vel
        player1.left = True
        player1.right = False
    elif keys[pygame.K_RCTRL]:
        if (
            player1.x + player1.width > player2.hitbox[0]
            and player1.x - player1.width < player2.hitbox[0] + player2.hitbox[2]
        ):
            player2.health -= 0.5  # type: ignore

    elif keys[pygame.K_SEMICOLON]:
        if (
            player1.x + player1.width > player2.hitbox[0]
            and player1.x - player1.width < player2.hitbox[0] + player2.hitbox[2]
        ):
            player2.health -= 0.5  # type: ignore

    elif keys[pygame.K_DOWN]:
        if (
            player1.x + player1.width > player2.hitbox[0]
            and player1.x - player1.width < player2.hitbox[0] + player2.hitbox[2]
        ):
            player2.health -= 0.5  # type: ignore

    elif keys[pygame.K_RSHIFT] and shootcycle == 0:
        if player1.left:
            facing = -1
        else:
            facing = 1
        if len(daggers) < 10:
            daggers.append(
                Projectile1(
                    round(player1.x + player1.width // 2),
                    round(player1.y + player1.height // 2),
                    6,
                    (0, 0, 0),
                    facing,
                )
            )

        shootcycle = 1

    if not (player1.isJump):
        if keys[pygame.K_UP]:
            player1.isJump = True

    else:
        if player1.jumpCount >= -10:
            player1.y -= (player1.jumpCount * abs(player1.jumpCount)) * 0.5  # type: ignore
            player1.jumpCount -= 1
        else:
            player1.isJump = False
            player1.jumpCount = 10

    if keys[pygame.K_d] and player2.x < WIDTH - player2.width - player2.vel:
        player2.x += player2.vel
        player2.right = True
        player2.left = False

    elif keys[pygame.K_a] and player2.x > player2.vel:
        player2.x -= player2.vel
        player2.left = True
        player2.right = False

    elif keys[pygame.K_LCTRL]:
        if (
            player2.x + player2.width > player1.hitbox[0]
            and player2.x - player2.width < player1.hitbox[0] + player1.hitbox[2]
        ):
            player1.health -= 0.5  # type: ignore

    elif keys[pygame.K_SPACE]:
        if (
            player2.x + player2.width > player1.hitbox[0]
            and player2.x - player2.width < player1.hitbox[0] + player2.hitbox[2]
        ):
            player1.health -= 0.5  # type: ignore
    elif keys[pygame.K_LSHIFT] and shootloop == 0:
        if player2.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 10:
            bullets.append(
                Projectile2(
                    round(player2.x + player2.width // 2),
                    round(player2.y + player2.height // 2),
                    6,
                    (0, 0, 0),
                    facing,
                )
            )

        shootLoop = 1

    if not (player2.isJump):
        if keys[pygame.K_w]:
            player2.isJump = True

    else:
        if player2.jumpCount >= -10:
            player2.y -= (player2.jumpCount * abs(player2.jumpCount)) * 0.5  # type: ignore
            player2.jumpCount -= 1
        else:
            player2.isJump = False
            player2.jumpCount = 10

    # Calling the callable functions
    redrawgamewindow()
pygame.quit()
