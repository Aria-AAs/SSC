"""This module contains the NeuralNetwork class."""

from typing import Self
from math import floor
from random import random
from src.brains.layer import Layer
from src.maths.utils import lerp


class NeuralNetwork:
    """NeuralNetwork class represents a neural network."""

    def __init__(self, neuron_count: list) -> None:
        self.layers_count = len(neuron_count) - 1
        self.layers = []
        for i in range(len(neuron_count) - 1):
            self.layers.append(Layer(neuron_count[i], neuron_count[i + 1]))

    def feedforward(self, inputs: list) -> list:
        """Feed given inputs to the network and calculate outputs.

        Args:
            inputs (list): The inputs to feed the network.

        Returns:
            list: A list of values that are outputs of the network.
        """
        outputs = []
        outputs = self.layers[0].feedforward(inputs)
        for i in range(1, self.layers_count):
            outputs = self.layers[i].feedforward(outputs)
        return outputs

    def mix_networks(self, networks: list) -> None:
        """Mix all given networks.

        Args:
            networks (list): A list of networks to mix.
        """
        while 0 < len(networks):
            if len(networks) == 1:
                break
            index_1 = floor(random() * len(networks))
            network_1 = networks.pop(index_1)
            index_2 = floor(random() * len(networks))
            network_2 = networks.pop(index_2)
            network_1.crossover(network_2)
            networks.append(network_1)
        self.layers = networks[0].layers

    def crossover(self, other: Self, crossover_rate: float = 0.5) -> None:
        """Calculate the child network of two given parent networks.

        Args:
            other (Self): Other parent network to calculate the child network.
            crossover_rate (float, optional): The rate for selecting parents' genomes.
            Less rate means the child network is more similar to this network and
            more rate means the child network is more similar to the other given network.
            Defaults to 0.5.
        """
        for i in range(self.layers_count):
            j = 0
            while j < len(self.layers[i].biases):
                self.layers[i].biases[j] = lerp(
                    self.layers[i].biases[j], other.layers[i].biases[j], crossover_rate
                )
                j += 1
            j = 0
            while j < len(self.layers[i].weights):
                k = 0
                while k < len(self.layers[i].weights[j]):
                    self.layers[i].weights[j][k] = lerp(
                        self.layers[i].weights[j][k],
                        other.layers[i].weights[j][k],
                        crossover_rate,
                    )
                    k += 1
                j += 1

    def mutate(self, amount: float = 0.3, mutation_rate: float = 0.05) -> None:
        """Mutate the network.

        Args:
            amount (float, optional): The amount of randomness of mutated genomes.
            0 means no difference at all and 1 means random genome. Defaults to 0.3.
            mutation_rate (float, optional): This rate tells the percentage of genomes that can
            mutate. Defaults to 0.05.
        """
        for layer in self.layers:
            i = 0
            while i < len(layer.biases):
                if random() < mutation_rate:
                    layer.biases[i] = lerp(layer.biases[i], random() * 2 - 1, amount)
                i += 1
            i = 0
            while i < len(layer.weights):
                j = 0
                while j < len(layer.weights[i]):
                    if random() < mutation_rate:
                        layer.weights[i][j] = lerp(
                            layer.weights[i][j], random() * 2 - 1, amount
                        )
                    j += 1
                i += 1
