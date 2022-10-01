import pygame

# TODO get or make a spritesheet(pixilated) for the character movement

print("hellow world")
# initializes every command

pygame.init()
# Creates a game window
WIDTH, HEIGHT = 800, 600

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fight Or Die")
clock = pygame.time.Clock()
score = pygame.font.SysFont("arial", 50, True)
# The player class with  all the player attributes and functions
class Jack(object):
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
        win.fill((0,0,0))
        pygame.draw.rect(win,(255,0,0), (self.x, self.y, self.width, self.height))
        self.hitbox = (self.x - 14, self.y - 6.5, 90, 75)
        if self.health >= 0:
            pygame.draw.rect(
                win, (255, 255, 255), (self.x + 7, self.y - 15, self.health, 10)
            )

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.health = self.original_health


# The enemy class with all the enemy attributes and functions
class Enemy(object):

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


# The projectile class for all the throwable weapons
class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, (255, 255, 255), (self.x, self.y), self.radius)


# Make sure every things comes on screen
def redrawgamewindow():
    player.draw(win)
    rubi.draw(win)
    for dagger in daggers:
        dagger.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


# The classes allocated into one name
player = Jack(550, 400, 64, 64)
rubi = Enemy(500, 400, 64, 64)
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

    if player.health <= 0:
        player.reset()

    if rubi.health <= 0:
        rubi.reset()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for dagger in daggers:
        if (
            dagger.y - dagger.radius < rubi.hitbox[1] + rubi.hitbox[3]
            and dagger.y + dagger.radius > rubi.hitbox[1]
        ):
            if (
                dagger.x + dagger.radius > rubi.hitbox[0]
                and dagger.x - dagger.radius < rubi.hitbox[0] + rubi.hitbox[2]
            ):
                rubi.health -= 1
                daggers.pop(daggers.index(dagger))

        if dagger.x < 800 and dagger.x > 0:
            dagger.x += dagger.vel
        else:
            daggers.pop(daggers.index(dagger))

    for bullet in bullets:
        if (
            bullet.y - bullet.radius < player.hitbox[1] + player.hitbox[3]
            and bullet.y + bullet.radius > player.hitbox[1]
        ):
            if (
                bullet.x + bullet.radius > player.hitbox[0]
                and bullet.x - bullet.radius < player.hitbox[0] + player.hitbox[2]
            ):
                player.health -= 1
                bullets.pop(bullets.index(bullet))

        if bullet.x < 800 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    # Key mapping code
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT] and player.x < WIDTH - player.width - player.vel:
        player.x += player.vel
        player.right = True
        player.left = False
    elif keys[pygame.K_LEFT] and player.x > player.vel:
        player.x -= player.vel
        player.left = True
        player.right = False
    elif keys[pygame.K_b]:
        if (
            player.x + player.width > rubi.hitbox[0]
            and player.x - player.width < rubi.hitbox[0] + rubi.hitbox[2]
        ):
            rubi.health -= 0.5

    elif keys[pygame.K_TAB]:
        if (
            player.x + player.width > rubi.hitbox[0]
            and player.x - player.width < rubi.hitbox[0] + rubi.hitbox[2]
        ):
            rubi.health -= 0.5

    elif keys[pygame.K_DOWN]:
        if (
            player.x + player.width > rubi.hitbox[0]
            and player.x - player.width < rubi.hitbox[0] + rubi.hitbox[2]
        ):
            rubi.health -= 0.5

    elif keys[pygame.K_LSHIFT] and shootcycle == 0:
        if player.left:
            facing = -1
        else:
            facing = 1
        if len(daggers) < 10:
            daggers.append(
                Projectile(
                    round(player.x + player.width // 2),
                    round(player.y + player.height // 2),
                    6,
                    (0, 0, 0),
                    facing,
                )
            )

        shootcycle = 1

    if not (player.isJump):
        if keys[pygame.K_UP]:
            player.isJump = True

    else:
        if player.jumpCount >= -10:
            player.y -= (player.jumpCount * abs(player.jumpCount)) * 0.5
            player.jumpCount -= 1
        else:
            player.isJump = False
            player.jumpCount = 10

    if keys[pygame.K_d] and rubi.x < WIDTH - rubi.width - rubi.vel:
        rubi.x += rubi.vel
        rubi.right = True
        rubi.left = False

    elif keys[pygame.K_a] and rubi.x > rubi.vel:
        rubi.x -= rubi.vel
        rubi.left = True
        rubi.right = False

    elif keys[pygame.K_k]:
        if (
            rubi.x + rubi.width > player.hitbox[0]
            and rubi.x - rubi.width < player.hitbox[0] + player.hitbox[2]
        ):
            player.health -= 0.5

    elif keys[pygame.K_SPACE]:
        if (
            rubi.x + rubi.width > player.hitbox[0]
            and rubi.x - rubi.width < player.hitbox[0] + rubi.hitbox[2]
        ):
            player.health -= 0.5
    elif keys[pygame.K_RSHIFT] and shootloop == 0:
        if rubi.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 10:
            bullets.append(
                Projectile(
                    round(rubi.x + rubi.width // 2),
                    round(rubi.y + rubi.height // 2),
                    6,
                    (0, 0, 0),
                    facing,
                )
            )

        shootLoop = 1

    if not (rubi.isJump):
        if keys[pygame.K_w]:
            rubi.isJump = True

    else:
        if rubi.jumpCount >= -10:
            rubi.y -= (rubi.jumpCount * abs(rubi.jumpCount)) * 0.5
            rubi.jumpCount -= 1
        else:
            rubi.isJump = False
            rubi.jumpCount = 10

    # Calling the callable functions
    redrawgamewindow()
pygame.quit()
