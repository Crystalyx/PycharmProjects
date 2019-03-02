import pygame
import random
import numpy as np
import neurolab as nl
import math
import NeuralCore as nc
import DNACore as dnac
from MagicCore import *

count = 100


def get_food(game_map, cx, cy, hue):
    # if count > cx > 0 and count > cy > 0:
    return game_map[cx % len(game_map)][cy % len(game_map[0])][hue]
    # return 0


class Snake(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Snake, self).__init__()
        self.surface = pygame.Surface((4, 4))
        self.surface.fill((0, 0, 255))
        self.rect = self.surface.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.x = x
        self.y = y
        self.dir = 0
        self.speed = 4
        self.food = 20
        self.red = 0
        self.green = 0
        self.blue = 255
        self.dna = dnac.create_dna()
        self.neuro_model = nc.NeuroModel(self.dna)
        self.speech_model = nc.SpeechModel(self.dna)
        self.hue = self.dna.hue()
        self.dead = False
        self.pregnant = False

        # model.evaluate(x_test, y_test)

    def copy(self, width, height):
        snak = Snake(random.randint(0, width - int(3 * width / count)),
                     random.randint(0, height - int(3 * height / count)))
        snak.dna = self.dna
        snak.neuro_model = nc.NeuroModel(self.dna)
        snak.speech_model = nc.SpeechModel(self.dna)
        snak.mutate_mind()
        snak.mutate_genome()
        return snak

    def update(self, pressed_keys, game_map, width, height):
        x = self.x
        y = self.y
        cx = int(count * (x - 5) / width)
        cy = int(count * (y - 5) / height)

        # print(str(cx), str(cy))

        inputs = [[get_food(game_map, cx, cy, self.hue) / 255,
                   get_food(game_map, cx + 1, cy, self.hue) / 255,
                   get_food(game_map, cx - 1, cy, self.hue) / 255,
                   get_food(game_map, cx, cy + 1, self.hue) / 255,
                   get_food(game_map, cx, cy - 1, self.hue) / 255,
                   get_food(game_map, cx + 1, cy + 1, self.hue) / 255,
                   get_food(game_map, cx - 1, cy + 1, self.hue) / 255,
                   get_food(game_map, cx + 1, cy - 1, self.hue) / 255,
                   get_food(game_map, cx - 1, cy - 1, self.hue) / 255,
                   self.food,
                   self.red,
                   self.green,
                   self.blue,
                   1
                   ]]

        # self.hue = ord(self.genome[2]) - ord('a')
        # if self.hue == 3:
        #     self.hue = 1
        neuro_result = self.neuro_model.sim(inputs)
        self.dir = int(neuro_result[0] * math.pi * 4)
        self.red = math.fabs(neuro_result[1] * 255)
        self.green = math.fabs(neuro_result[2] * 255)
        self.blue = math.fabs(neuro_result[3] * 255)
        self.speed = int(neuro_result[4] * 3) + 3
        self.dead = False

        yum = random.randint(12, 15)
        self.food = self.food - self.dna.metabolism()
        if game_map[cx % count][cy % count][self.hue] > yum and self.food < 255:
            game_map[cx % count][cy % count][self.hue] = \
                game_map[cx % count][cy % count][self.hue] - yum
            self.food = self.food + yum

        if self.food > 0:
            # print(10 + self.food)
            self.surface.fill((self.red, self.green, self.blue))
            self.rect = self.surface.get_rect()
            self.rect.top = self.y
            self.rect.left = self.x

        if self.dir != -1:
            dx = math.cos(self.dir) * self.speed
            dy = math.sin(self.dir) * self.speed
            self.rect.move_ip(dx, dy)
            self.x = self.x + dx
            self.y = self.y + dy

        # Keep player on the screen
        if self.rect.left <= 0:
            self.rect.right = width
            self.x = width - 4
        elif self.rect.right >= width:
            self.rect.left = 0
            self.x = 4
        if self.rect.top <= 0:
            self.rect.bottom = height
            self.y = height - 4
        elif self.rect.bottom >= height:
            self.rect.top = 0
            self.y = 4

        if self.dna.have_magic_abilities():
            letter = self.speech_model.sim(inputs)
            id = []
            for i in letter:
                id.append(round(math.fabs(i)))
            if self.dna.magic_type() == 0:
                spell = construct_light_spell(id)
                cast_light_spell(self, spell, game_map, count, cx, cy)
            else:
                spell = construct_dark_spell(id)
                cast_dark_spell(self, spell, game_map, count, cx, cy)

    def mutate_genome(self):
        # new_genome = ''
        # # print('old: ',self.genome)
        # gene_count = random.randint(0, 3)
        # for i in range(0, gene_count + 1):
        #     order = ord(self.genome[i])
        #     # print('rand')
        #     new_order = (order + random.randint(-3, 3))
        #     if new_order > ord('d'):
        #         new_order = ord('d')
        #     if new_order < ord('a'):
        #         new_order = ord('a')
        #     new_genome = new_genome + chr(new_order)
        # self.genome = new_genome + self.genome[gene_count + 1:]
        # # print(self.genome)
        # # if self.genome[3] == 'a':
        # #     print('caster', self.genome)
        pass

    def mutate_mind(self):
        # neuron_count = random.randint(0, 20)
        # for i in range(0, neuron_count):
        #     target = random.randint(0, len(self.neuro_model.nn.layers[1].np['w']) - 1)
        #     self.neuro_model.nn.layers[1].np['w'][target] = \
        #         self.neuro_model.nn.layers[1].np['w'][target] + random.gauss(0, 0.125)
        #
        #     for j in self.neuro_model.nn.layers[1].np['w'][target]:
        #         if j > 1:
        #             j = 1
        #         if j < 0:
        #             j = 0
        pass
