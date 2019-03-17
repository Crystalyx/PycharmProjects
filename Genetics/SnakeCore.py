import pygame
import random
import numpy as np
import neurolab as nl
import math
import NeuralCore as nc
import DNACore as dnac
from MagicCore import *
from SexCore import *
import copy

count = 91


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
        self.partner_dna = 0

        # model.evaluate(x_test, y_test)

    def copy(self, width, height):
        snak = Snake(self.x, self.y)
        if self.partner_dna != 0:
            snak.dna = dnac.make_average(self.dna, self.partner_dna)
        else:
            snak.dna = self.dna
        snak.neuro_model = copy.deepcopy(self.neuro_model)
        snak.speech_model = copy.deepcopy(self.neuro_model)
        snak.mutate_mind()
        snak.mutate_genome()
        return snak

    def update(self, pressed_keys, world, width, height):
        cx = world.get_chunk_x(self.x)
        cy = world.get_chunk_y(self.y)
        # print(str(cx), str(cy))

        inputs = [[world.get_food_at_chunk_by_hue(cx, cy, self.hue) / 255,
                   world.get_food_at_chunk_by_hue(cx + 1, cy, self.hue) / 255,
                   world.get_food_at_chunk_by_hue(cx - 1, cy, self.hue) / 255,
                   world.get_food_at_chunk_by_hue(cx, cy + 1, self.hue) / 255,
                   world.get_food_at_chunk_by_hue(cx, cy - 1, self.hue) / 255,
                   world.get_food_at_chunk_by_hue(cx + 1, cy + 1, self.hue) / 255,
                   world.get_food_at_chunk_by_hue(cx - 1, cy + 1, self.hue) / 255,
                   world.get_food_at_chunk_by_hue(cx + 1, cy - 1, self.hue) / 255,
                   world.get_food_at_chunk_by_hue(cx - 1, cy - 1, self.hue) / 255,
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
        want_to_create_gamet = neuro_result[5] > 0.7 or self.food > 200
        self.dead = False

        if world.item_at(self.x, self.y):
            item = world.get_item_at(self.x, self.y)
            if item != 0:
                item.activate(world, self)
                world.set_item_at(self.x, self.y)

        if want_to_create_gamet:
            world.set_item_at(self.x, self.y, Gamet(self))
            self.food -= self.dna.metabolism() - 20

        yum = random.randint(2, 8)
        self.food = self.food - self.dna.metabolism() - 3
        if world.get_food_at_chunk_by_hue(cx, cy, self.hue) > yum and self.food < 255:
            world.refill(cx, cy, -yum * 4, self.hue)
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
                cast_light_spell(self, spell, world, count, cx, cy)
            else:
                spell = construct_dark_spell(id)
                cast_dark_spell(self, spell, world, count, cx, cy)

    def mutate_genome(self):
        self.dna = self.dna.mutated_copy()

    def mutate_mind(self):
        neuron_count = random.randint(0, 20)
        for i in range(0, neuron_count):
            target = random.randint(0, len(self.neuro_model.nn.layers[1].np['w']) - 1)
            self.neuro_model.nn.layers[1].np['w'][target] = \
                self.neuro_model.nn.layers[1].np['w'][target] + random.gauss(0, 0.125)

            for j in self.neuro_model.nn.layers[1].np['w'][target]:
                if j > 1:
                    j = 1
                if j < 0:
                    j = 0
        pass
