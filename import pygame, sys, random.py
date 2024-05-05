import pygame, sys, random
from math import *

pygame.init()
width, height = 700, 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Balloon Shooter Game")
clock = pygame.time.Clock()

margin, lowerBound, score = 100, 100, 0
colors = [(230, 230, 230), (4, 27, 96), (231, 76, 60), (25, 111, 61), (40, 55, 71),
          (64, 178, 239), (35, 155, 86), (244, 208, 63), (46, 134, 193), (155, 89, 182), (243, 156, 18)]
font = pygame.font.SysFont("Snap ITC", 35)

class Balloon:
    def __init__(self, speed):
        self.a, self.b = random.randint(30, 40), random.randint(30, 50)
        self.x, self.y = random.randint(margin, width - self.a - margin), height - lowerBound
        self.angle, self.speed = 90, -speed
        self.proPool = [-1, 0, 1]
        self.length = random.randint(50, 100)
        self.color = random.choice(colors)

    def move(self):
        self.angle += random.choice(self.proPool) * 10
        self.y += self.speed * sin(radians(self.angle))
        self.x += self.speed * cos(radians(self.angle))
        if not (0 < self.x + self.a < width) or not (0 < self.y + self.b < height): self.reset()

    def show(self):
        pygame.draw.line(display, colors[5], (self.x + self.a/2, self.y + self.b), (self.x + self.a/2, self.y + self.b + self.length))
        pygame.draw.ellipse(display, self.color, (self.x, self.y, self.a, self.b))
        pygame.draw.ellipse(display, self.color, (self.x + self.a/2 - 5, self.y + self.b - 3, 10, 10))

    def burst(self):
        global score
        if (self.x < pygame.mouse.get_pos()[0] < self.x + self.a) and (self.y < pygame.mouse.get_pos()[1] < self.y + self.b):
            score += 1
            self.reset()

    def reset(self):
        self.__init__(random.choice([1, 2, 2, 3]))

balloons = [Balloon(random.choice([1, 2, 2, 3])) for _ in range(10)]

def pointer():
    pos = pygame.mouse.get_pos()
    pygame.draw.circle(display, colors[2], pos, 25, 4)
    for p in [(0, -20), (20, 0), (0, 20), (-20, 0)]:
        pygame.draw.line(display, colors[2], (pos[0] + p[0], pos[1] + p[1]), (pos[0] + p[0]*2, pos[1] + p[1]*2), 4)

def lowerPlatform():
    pygame.draw.rect(display, colors[4], (0, height - lowerBound, width, lowerBound))

def showScore():
    display.blit(font.render(f"Balloons Bursted: {score}", True, colors[0]), (150, height - lowerBound + 50))

def close():
    pygame.quit()
    sys.exit()

def game():
    global score
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q): close()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for balloon in balloons: balloon.burst()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r: score = 0

        display.fill(colors[1])
        for balloon in balloons: balloon.show(), balloon.move()
        pointer(), lowerPlatform(), showScore(), pygame.display.update(), clock.tick(60)

game()
