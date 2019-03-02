import neurolab as nl
import numpy as np


class NeuroModel:
    def __init__(self, dna):
        neural_layers = dna.neural_depth()
        inputs = [[0, 256],
                  [0, 256],
                  [0, 256],
                  [0, 256],
                  [0, 256],
                  [0, 256],
                  [0, 256],
                  [0, 256],
                  [0, 256],
                  [0, 255],
                  [0, 255],
                  [0, 255],
                  [0, 255],
                  [0, 1]]
        self.nn = nl.net.newff(inputs, [16, 7])
        self.nn.init()

    def sim(self, data):
        return self.nn.sim(data)[0]


class SpeechModel:
    def __init__(self, dna):
        speech_layers = dna.speech_depth()
        layers = []
        inputs = [[0, 256],
                  [0, 256],
                  [0, 256],
                  [0, 256],
                  [0, 256],
                  [0, 256],
                  [0, 256],
                  [0, 256],
                  [0, 256],
                  [0, 255],
                  [0, 255],
                  [0, 255],
                  [0, 255],
                  [0, 1]]
        self.nn = nl.net.newff(inputs, [32, 32, 9])
        self.nn.init()

    def sim(self, data):
        return self.nn.sim(data)[0]
