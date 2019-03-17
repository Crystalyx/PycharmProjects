from random import randint as next
import math
import copy

weights = []

for i in range(0, 33):
    weights.append(4)

weights[4] = 5
weights[5] = 6
weights[7] = 32
weights[8] = 6
weights[9] = 9
weights[14] = 32
weights[16] = 32
weights[17] = 32
weights[20] = 32
weights[21] = 1
weights[28] = 32
weights[30] = 32


def create_dna():
    values = []
    for i in range(0, 33):
        values.append(next(0, weights[i]))
    return DNA(values)


def make_average(dna1, dna2):
    values = []
    for i in range(0, 33):
        if next(0, 1) < 0.5:
            values.append(dna1.values[i])
        else:
            values.append(dna2.values[i])
    return DNA(values)


class DNA:
    def __init__(self, values):
        self.values = values

    def neural_depth(self):
        return self.values[3]

    def neural_neurons_at(self, layer):
        indexes = [7, 16, 28, 30]
        return self.values[indexes[layer]]

    def speech_depth(self):
        return self.values[2]

    def speech_neurons_at(self, layer):
        indexes = [7, 14, 17, 20]
        return self.values[indexes[layer]]

    def have_magic_abilities(self):
        mod = self.values[1] + 1
        return self.values[2] % mod == 0 and self.values[8] % mod != 0 and self.values[17] % mod != 0 or \
               self.values[2] % mod != 0 and self.values[8] % mod == 0 and self.values[17] % mod != 0 or \
               self.values[2] % mod != 0 and self.values[8] % mod != 0 and self.values[17] % mod == 0

    def magic_type(self):
        return self.values[21]

    def metabolism(self):
        return math.floor((self.values[4] + self.values[8] + self.values[9]) / 3)

    def hue(self):
        return max(self.values[3], self.values[5], self.values[17]) % 3

    def mutated_copy(self):
        new_values = copy.deepcopy(self.values)
        for i in range(next(1, 10)):
            pos = next(0, len(self.values) - 1)
            shift = next(0, weights[pos])
            new_values[pos] = (new_values[pos] + shift) % weights[pos]
        return DNA(new_values)
