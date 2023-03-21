import pygame
from settings import *
from writer import *
from random import choice, randint
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
# other global variables
player = pygame.sprite.Sprite()
fallingItems = [] # list of falling item sprites
writer = Writer(screen)
writer.setText('Score: 0')

def update():
    for item in fallingItems:
        item.rect.centery += item.dy
        if item.rect.colliderect(player.rect):
            player.alive = False
        if item.rect.bottom >= HEIGHT:
            numItems = len(fallingItems)
            item.rect.centery -= numItems * ITEMGAP
            item.rect.centerx = randint(0, WIDTH)
            text = writer.getText()
            score = int(text[7:])
            score += 1
            text = text[0:7] + str(score)
            writer.setText(text)
    
def draw():
    screen.fill(BGCOLOR)
    screen.blit(player.image, player.rect)
    for item in fallingItems:
        screen.blit(item.image, item.rect)
    writer.writeText(50, 50)
    pygame.display.update()

def onMouseMove(x, y):
    player.rect.centerx = x

def initPlayer():
    player.image = pygame.Surface((PLAYERSIZE, PLAYERSIZE))
    player.image.fill(FIREBRICK)
    player.rect = player.image.get_rect()
    player.rect.bottom = HEIGHT
    player.rect.centerx = WIDTH // 2

def initItems():
    for i in range(STARTING_ITEMS):
        item = pygame.sprite.Sprite()
        item.image = pygame.Surface((ITEMSIZE, ITEMSIZE))
        item.image.fill(BGCOLOR)
        if i % 3 == 0:
            pygame.draw.circle(item.image, choice(ITEMCOLORS), (ITEMSIZE // 2, ITEMSIZE // 2), ITEMSIZE // 2)
        elif i % 3 == 1:
            item.image.fill(choice(ITEMCOLORS))
        else:
            points = [[ITEMSIZE // 2, 0],
                      [ITEMSIZE, ITEMSIZE // 2],
                      [ITEMSIZE // 2, ITEMSIZE],
                      [0, ITEMSIZE // 2]]
            pygame.draw.polygon(item.image, choice(ITEMCOLORS), points)
        item.rect = item.image.get_rect()
        item.rect.centerx = randint(0, WIDTH)
        item.rect.centery = 0 - ITEMGAP * i
        item.dy = ITEMSTARTSPEED
        fallingItems.append(item)
        
def mainloop():
    running = True
    clock = pygame.time.Clock()
    while running:
        update()
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.MOUSEMOTION:
                onMouseMove(event.pos[0], event.pos[1])
        clock.tick(FPS)
        
initItems()
initPlayer()
pygame.init()
mainloop()
