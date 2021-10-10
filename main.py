import pygame


class Game:
    pygame.display.set_caption("Space Invaders")
    screen = None
    aliens = []
    rockets = []
    lost = False

    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        done = False

        hero = Hero(self, width / 2, height - 20)
        generator = Generator(self)
        rocket = None

        while not done:
            if len(self.aliens) == 0:
                self.displayText("You Won!")

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                hero.x -= 3 if hero.x > 20 else 0
            elif pressed[pygame.K_RIGHT]:
                hero.x += 3 if hero.x < width - 20 else 0
            if pressed[pygame.K_UP]:
                hero.y -= 3 if hero.y > 20 else 0
            elif pressed[pygame.K_DOWN]:
                hero.y += 3 if hero.y < width - 20 else 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.lost:
                    self.rockets.append(Rocket(self, hero.x, hero.y))

            pygame.display.flip()
            self.clock.tick(60)
            self.screen.fill((0, 0, 0))

            for alien in self.aliens:
                alien.draw()
                alien.checkCollision(self)
                if alien.y > height:
                    self.lost = True
                    self.displayText("You Lost!")

            for rocket in self.rockets:
                rocket.draw()

            if not self.lost:
                hero.draw()

    def displayText(self, text):
        pygame.font.init()
        font = pygame.font.SysFont('Times New Roman', 50, "bold")
        textsurface = font.render(text, False, (44, 0, 62))
        self.screen.blit(textsurface, (110, 160))


class Alien:
    def __init__(self, game, x, y):
        self.x = x
        self.game = game
        self.y = y
        self.size = 15

    def draw(self):
        pygame.draw.rect(self.game.screen,
                         (81, 43, 88),
                         pygame.Rect(self.x, self.y, self.size, self.size))
        self.y += 0.3

    def checkCollision(self, game):
        for rocket in game.rockets:
            if (self.x + self.size > rocket.x > self.x - self.size and
                    self.y + self.size > rocket.y > self.y - self.size):
                game.rockets.remove(rocket)
                game.aliens.remove(self)


class Hero:
    def __init__(self, game, x, y):
        self.x = x
        self.game = game
        self.y = y

    def draw(self):
        pygame.draw.rect(self.game.screen,
                         "white",
                         pygame.Rect(self.x, self.y, 10, 7))


class Generator:
    def __init__(self, game):
        margin = 25
        width = 35
        for x in range(margin, game.width - margin, width):
            for y in range(margin, int(game.height / 3), width):
                game.aliens.append(Alien(game, x, y))


class Rocket:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game

    def draw(self):
        pygame.draw.rect(self.game.screen,
                         (254, 52, 110),
                         pygame.Rect(self.x, self.y, 4, 8))
        self.y -= 4


if __name__ == '__main__':
    game = Game(1000, 1000)
