import pygame
from pygame.locals import USEREVENT
import os
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 447
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Danger Run')

bg = pygame.image.load(os.path.join('images', 'bg.png')).convert()
bgX = 0
bgX2 = bg.get_width()

clock = pygame.time.Clock()

color_light = (170, 170, 170)
color_dark = (100, 100, 100)


class Player(object):
    run = [pygame.image.load(os.path.join('images', str(x) + '.png'))
           for x in range(8, 16)]
    jump = [pygame.image.load(os.path.join('images', str(x) + '.png'))
            for x in range(1, 8)]
    slide = [pygame.image.load(os.path.join('images', 'S1.png')), pygame.image.load(os.path.join('images', 'S2.png')),
             pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),
             pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),
             pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),
             pygame.image.load(os.path.join('images', 'S3.png')), pygame.image.load(os.path.join('images', 'S4.png')),
             pygame.image.load(os.path.join('images', 'S5.png'))]
    fall = pygame.image.load(os.path.join('images', '0.png'))
    jumpList = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4,
                4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1,
                -1, -1, -1, -1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3,
                -3, -3, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4]

    def __init__(self, x, y, width, height):
        self.x = x
        self. y = y
        self.width = width
        self. height = height
        self.jumping = False
        self.sliding = False
        self.slideUp = False
        self.falling = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.hitbox = (x, y, width, height)

    def draw(self, display):
        if self.falling:
            display.blit(self.fall, (self.x, self.y + 35))
        elif self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.2
            display.blit(self.jump[self.jumpCount // 18], (self.x, self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)

        elif self.sliding or self.slideUp:
            if self.slideCount < 20:
                self.y += 1
            elif self.slideCount == 80:
                self.y -= 19
                self.sliding = False
                self.slideUp = True
            elif self.slideCount > 20 and self.slideCount < 80:
                self.hitbox = (self.x, self.y + 3, self.width - 8, self.height - 35)
            if self.slideCount >= 110:
                self.slideCount = 0
                self.slideUp = False
                self.runCount = 0
                self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)
            display.blit(self.slide[self.slideCount // 10], (self.x, self.y))
            self.slideCount += 1

        # elif self.falling:
        #     display.blit(self.fall, (self.x, self.y + 35))

        else:
            if self.runCount > 42:
                self.runCount = 0
            display.blit(self.run[self.runCount // 6], (self.x, self.y))
            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 13)
            self.runCount += 1
        pygame.draw.rect(display, (255, 0, 0), self.hitbox, 2)


class ObstacleSaw(object):
    img = [pygame.image.load(os.path.join('images', 'SAW0.PNG')),
           pygame.image.load(os.path.join('images', 'SAW1.PNG')),
           pygame.image.load(os.path.join('images', 'SAW2.PNG')),
           pygame.image.load(os.path.join('images', 'SAW3.PNG'))]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x, y, width, height)
        self.count = 0

    def draw(self, display):
        self.hitbox = (self.x + 5, self.y + 5, self.width - 10, self.height)
        if self.count >= 8:
            self.count = 0
        display.blit(pygame.transform.scale(self.img[self.count // 2], (64, 64)), (self.x, self.y))
        self.count += 1
        pygame.draw.rect(display, (255, 0, 0), self.hitbox, 2)

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False


class ObstacleSpike(ObstacleSaw):
    img = pygame.image.load(os.path.join('images', 'spike.png'))

    def draw(self, display):
        self.hitbox = (self.x + 10, self.y, 28, 315)
        win.blit(self.img, (self.x, self.y))
        pygame.draw.rect(display, (255, 0, 0), self.hitbox, 2)

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        return False


def redraw_window():
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2, 0))
    runner.draw(win)
    for obj1 in objects:
        obj1.draw(win)

    font = pygame.font.SysFont('comicsans', 30)
    text = font.render('Score: ' + str(score), 1, (255, 255, 255))
    win.blit(text, (700, 10))
    pygame.display.update()


def update_file():
    f = open('prevscores.txt', 'r')
    file = f.readlines()
    last = int(file[0])

    if last < int(score):
        f.close()
        file = open('prevscores.txt', 'w')
        file.write(str(score))
        file.close()

        return score

    return last


def end_screen():
    global pause, objects, speed, score
    pause = 0
    objects = []
    speed = 30

    play = True
    while play:
        pygame.time.delay(100)
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                play = False
                pygame.quit()
                sys.exit()
            if events.type == pygame.MOUSEBUTTONDOWN:
                play = False
                start_screen()
        win.blit(bg, (0, 0))
        largefont = pygame.font.SysFont('comicsans', 80)
        prevscore = largefont.render('Best Score: ' + str(update_file()), 1, (255, 255, 55))
        win.blit(prevscore, (WIDTH/2 - prevscore.get_width() / 2, 150))
        newscore = largefont.render('Score: ' + str(score), 1, (255, 255, 55))
        win.blit(newscore, (WIDTH/2 - newscore.get_width() / 2, 240))
        pygame.display.update()

    score = 0
    runner.falling = False


def start_screen():
    mouse = pygame.mouse.get_pos()
    play = True
    while play:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                play = False
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if WIDTH/2 - 200 <= mouse[0] <= WIDTH/2 - 60 and HEIGHT/2 <= mouse[1] <= HEIGHT/2 + 40:
                    play = False
                    return True
                elif WIDTH/2 + 200 <= mouse[0] <= WIDTH/2 + 340 and HEIGHT/2 <= mouse[1] <= HEIGHT/2 + 40:
                    play = False
                    pygame.quit()
                    sys.exit()

        win.blit(bg, (0, 0))
        smallfont = pygame.font.SysFont('comicsans', 35)
        starttext = smallfont.render('START', True, (255, 255, 255))
        quittext = smallfont.render('QUIT', True, (255, 255, 255))

        mouse = pygame.mouse.get_pos()

        if WIDTH/2 - 200 <= mouse[0] <= WIDTH/2 - 60 and HEIGHT/2 <= mouse[1] <= HEIGHT/2 + 40:
            pygame.draw.rect(win, color_light, (WIDTH/2 - 200, HEIGHT/2, 140, 40))
        else:
            pygame.draw.rect(win, color_dark, (WIDTH/2 - 200, HEIGHT/2, 140, 40))
        win.blit(starttext, (WIDTH/2 - 170, HEIGHT/2 + 12))

        if WIDTH/2 + 200 <= mouse[0] <= WIDTH/2 + 340 and HEIGHT/2 <= mouse[1] <= HEIGHT/2 + 40:
            pygame.draw.rect(win, color_light, (WIDTH/2 + 200, HEIGHT/2, 140, 40))
        else:
            pygame.draw.rect(win, color_dark, (WIDTH / 2 + 200, HEIGHT / 2, 140, 40))
        win.blit(quittext, (WIDTH/2 + 240, HEIGHT/2 + 12))
        pygame.display.update()


runner = Player(200, 313, 64, 64)
pygame.time.set_timer(USEREVENT + 1, 500)
pygame.time.set_timer(USEREVENT + 2, random.randrange(3000, 7000))
speed = 30
run = True

startthegame = True
pause = 0
fallspeed = 0
objects = []

while run:
    if startthegame:
        start = start_screen()
        startthegame = False
    if start:
        score = speed//5 - 6
        if pause > 0:
            pause += 1
            if pause > fallspeed * 2:
                end_screen()

        for obj in objects:
            if obj.collide(runner.hitbox):
                runner.falling = True
                if pause == 0:
                    fallspeed = speed
                    pause = 1

            obj.x -= 1.4
            if obj.x < obj.width * -1:
                objects.pop(objects.index(obj))

        bgX -= 1.4
        bgX2 -= 1.4
        if bgX < bg.get_width() * -1:
            bgX = bg.get_width()
        if bgX2 < bg.get_width() * -1:
            bgX2 = bg.get_width()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == USEREVENT + 1:
                speed += 1
            if event.type == USEREVENT + 2:
                r = random.randrange(0, 2)
                if r == 0:
                    objects.append(ObstacleSaw(810, 310, 64, 64))
                else:
                    objects.append(ObstacleSpike(810, 0, 48, 320))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if not runner.jumping:
                runner.jumping = True
        if keys[pygame.K_DOWN]:
            if not runner.sliding:
                runner.sliding = True

        clock.tick(speed)
        redraw_window()
