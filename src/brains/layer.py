"""This module contains the Layer class."""

from random import random


class Layer:
    """Layer class represents one layer of network."""

    def __init__(self, inputs_count: int, outputs_count: int) -> None:
        self.inputs_count = inputs_count
        self.outputs_count = outputs_count
        self.inputs = []
        self.outputs = [0] * self.outputs_count
        self.biases = []
        self.weights = []
        self._randomize()

    def _randomize(self) -> None:
        """Randomize the values (biases and weights) of the layer."""
        for i in range(self.inputs_count):
            self.weights.append([])
            for _ in range(self.outputs_count):
                self.weights[i].append(random() * 2 - 1)
        for _ in range(self.outputs_count):
            self.biases.append(random() * 2 - 1)

    def feedforward(self, inputs: list) -> list:
        """Feed given inputs to the layer and calculate outputs.

        Args:
            inputs (list): The inputs to feed the layer.

        Returns:
            list: A list of values that are outputs of the layer.
        """
        self.inputs = inputs
        for i in range(self.outputs_count):
            weighted_sum = 0
            for j in range(self.inputs_count):
                weighted_sum += self.inputs[j] * self.weights[j][i]
            if weighted_sum > self.biases[i]:
                self.outputs[i] = 1
            else:
                self.outputs[i] = 0
        return self.outputs
