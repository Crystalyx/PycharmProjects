import pygame
import time
from pygame.locals import *
from SnakeCore import Snake
from numpy import *
import random
import math

width = 800
height = 600
count = 100
snakes = [Snake(width / 2, height / 2)]
snakes[0].copy(width, height)
snake_num = 25

for i in range(0, snake_num):
    snakes.append(
        Snake(random.randint(0, width - int(3 * width / count)), random.randint(0, height - int(3 * height / count))))

game_map = []

for i in range(0, count):
    t = []
    for j in range(0, count):
        t.append([0, 255, 0])
    game_map.append(t)

satur = []
for i in range(0, 256):
    satur.append(int(48 * ((i / 48) ** 10 + 2 ** 10) ** (1 / 10)))


def __main__():
    print('begin')
    pygame.init()

    screen = pygame.display.set_mode((width, height))

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        screen.blit(background, (0, 0))

        cell_x = width / count
        cell_y = height / count

        for i in range(0, count):
            for j in range(0, count):
                cell = pygame.Surface((cell_x, cell_y + 1))
                rect = cell.get_rect()
                rect.left = cell_x * i
                rect.top = cell_y * j
                food = game_map[i][j]
                # print((satur[food[0]], satur[food[1]], satur[food[2]]))
                # print(red_blue, green)
                if food != [-1, -1, -1]:
                    cell.fill((satur[food[0]], satur[food[1]], satur[food[2]]))
                else:
                    cell.fill((satur[0], satur[0], satur[0]))
                screen.blit(cell, rect)
        if len(snakes) == 0:
            break
        main_loop(screen)
        # time.sleep(0.001)

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False


def main_loop(screen):
    pressed_keys = pygame.key.get_pressed()

    for entity in snakes:
        entity.update(pressed_keys, game_map, width, height)
        screen.blit(entity.surface, entity.rect)
        if entity.food >= 100 and 70 > len(snakes) or entity.pregnant:
            snakes.append(entity.copy(width, height))
            entity.food = entity.food - 100
            entity.pregnant = False
        if entity.food < 0 or entity.dead:
            cx = int(count * (entity.x - 1) / width)
            cy = int(count * (entity.y - 1) / height)
            game_map[cx % count][cy % count][entity.hue] = game_map[cx][cy][entity.hue] + 20
            if game_map[cx % count][cy % count][entity.hue] > 250:
                game_map[cx % count][cy % count][entity.hue] = 250
            snakes.remove(entity)
            # print('removed', len(snakes), '/', snake_num, ' snakes left')

    # if len(snakes) < snake_num / 2:
    #     print('copied')
    #     new_snakes = []
    #     for snak in snakes:
    #         new_snakes.append(snak.copy(width, height))
    #     for i in new_snakes:
    #         snakes.append(i)

    pygame.display.flip()

    if random.randint(0, 625) < 8:
        for i in range(0, count):
            for j in range(0, count):
                # if game_map[i][j][0] < 250 and game_map[i][j][0] != -1:
                #     # print('restored')
                #     game_map[i][j][0] = game_map[i][j][0] + 1

                if game_map[i][j][1] < 250 and game_map[i][j][1] != -1:
                    # print('restored')
                    game_map[i][j][1] = game_map[i][j][1] + 1

                # if game_map[i][j][2] < 250 and game_map[i][j][2] != -1:
                #     # print('restored')
                #     game_map[i][j][2] = game_map[i][j][2] + 1
                # pass


# Standard boilerplate to call the main() function.
if __name__ == '__main__':
    __main__()
