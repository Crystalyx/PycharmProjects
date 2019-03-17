import pygame
import time
from pygame.locals import *
from SnakeCore import Snake
from numpy import *
import random
import math
from WorldCore import World
from SexCore import Gamet

width = 800
height = 600
count = 100
snakes = [Snake(random.randint(0, width - int(3 * width / count)), random.randint(0, height - int(3 * height / count)))]
snake_num = 25

for i in range(0, snake_num):
    snakes.append(
        Snake(random.randint(0, width - int(3 * width / count)), random.randint(0, height - int(3 * height / count))))

world = World(width, height, [0, 255, 0], count)

world.set_item_at(50, 50, Gamet(snakes[0]))
satur = []
for i in range(0, 256):
    satur.append(int(48 * ((i / 48) ** 10 + 2 ** 10) ** (1 / 10)))


def __main__():
    print('begin')
    print(101 % count)
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
                if world.get_food_at_chunk_by_hue(i, j, 0) > 250:
                    world.set_food_at_chunk_by_hue(i, j, 250, 0)
                if world.get_food_at_chunk_by_hue(i, j, 1) > 250:
                    world.set_food_at_chunk_by_hue(i, j, 250, 1)
                if world.get_food_at_chunk_by_hue(i, j, 2) > 250:
                    world.set_food_at_chunk_by_hue(i, j, 250, 2)

                cell = pygame.Surface((world.cell_width, world.cell_height))
                rect = cell.get_rect()
                rect.left = cell_x * i
                rect.top = cell_y * j
                food = world.get_food_at_chunk(i, j)
                # print((satur[food[0]], satur[food[1]], satur[food[2]]))
                # print(red_blue, green)
                if food != [-1, -1, -1]:
                    cell.fill((satur[food[0]], satur[food[1]], satur[food[2]]))
                else:
                    cell.fill((satur[0], satur[0], satur[0]))
                screen.blit(cell, rect)

        for i in range(0, count):
            for j in range(0, count):
                if world.item_at(i * world.cell_width, j * world.cell_height):
                    item = world.get_item_at(i * world.cell_width, j * world.cell_height)
                    if item != 0:
                        if item.timer < 0:
                            world.set_item_at(i * world.cell_width, j * world.cell_height, 0)
                            world.refill(i, j, 4, item.snak.hue)
                            continue
                        item.timer = item.timer - 1
                        gamX = pygame.Surface((2, 6))
                        gamY = pygame.Surface((6, 2))
                        gamX.fill((item.snak.red*0.5, item.snak.green*0.5, item.snak.blue*0.5))
                        gamY.fill((item.snak.red*0.5, item.snak.green*0.5, item.snak.blue*0.5))
                        xRect = gamX.get_rect()
                        yRect = gamY.get_rect()
                        xRect.left = cell_x * i + 2
                        xRect.top = cell_y * j
                        yRect.left = cell_x * i
                        yRect.top = cell_y * j + 2
                        screen.blit(gamX, xRect)
                        screen.blit(gamY, yRect)
        # if len(snakes) == 0:
        #     break
        main_loop(screen)
        # time.sleep(0.1)

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False


def main_loop(screen):
    pressed_keys = pygame.key.get_pressed()

    world.update()
    for entity in snakes:
        if len(snakes) > 50:
            if random.randint(0, len(snakes)) > 0.5 * len(snakes):
                snakes.remove(entity)
                continue
        entity.update(pressed_keys, world, width, height)
        screen.blit(entity.surface, entity.rect)
        if entity.pregnant:  # and 70 > len(snakes):
            snakes.append(entity.copy(width, height))
            entity.food = entity.food - 80
            entity.pregnant = False
            entity.partner_dna = 0
        if entity.food < 0 or entity.dead:
            # new_food = world.get_food_by_hue(entity.x, entity.y, entity.hue) + 20
            # world.set_food_by_hue(entity.x, entity.y, new_food, entity.hue)

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
    world.update()


# Standard boilerplate to call the main() function.
if __name__ == '__main__':
    __main__()
