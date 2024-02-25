from random import random


class Layer:
    def __init__(self, inputs_count: int, outputs_count: int) -> None:
        self.inputs_count = inputs_count
        self.outputs_count = outputs_count
        self.inputs = []
        self.outputs = [0] * self.outputs_count
        self.biases = []
        self.weights = []
        self.randomize()

    def randomize(self) -> None:
        for i in range(self.inputs_count):
            self.weights.append([])
            for _ in range(self.outputs_count):
                self.weights[i].append(random() * 2 - 1)
        for i in range(self.outputs_count):
            self.biases.append(random() * 2 - 1)

    def feedforward(self, inputs: list) -> list:
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
