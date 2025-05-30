import random
import sys
import json

from src.optimizers.optimizers import get_optimizer
from src.sigmoid_functions import get_sigmoid_function_and_derivate
from src.multilayer_perceptron import MultilayerPerceptron
from src.confusion_matrix import ConfusionMatrix
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def read_number_files(file,block_size=35):
    with open(file, 'r') as f:
        text = f.read() 
    numbers = text.strip().split()  
    numbers = [int(num) for num in numbers]  
    blocks = [numbers[i:i+block_size] for i in range(0, len(numbers), block_size)]  
    blocks = [block for block in blocks if len(block) == block_size]    
    return blocks

def gather_data(name, learning_rate, training_input, training_output, activation_function, activation_derivate, layers, optimizer):
    epoch_step = 10
    sets = int(epochs / epoch_step)

    accuracy_sum = np.zeros(sets)
    current_epoch = [i * epoch_step for i in range(sets)]

    num_runs = 100

    for run in range(num_runs):
        perc = MultilayerPerceptron(learning_rate, training_input, training_output,
                                     activation_function, activation_derivate, layers, optimizer)
        accuracy = []

        for i in range(sets):
            perc.train_perceptron(epochs=epoch_step, epsilon=epsilon)
            confusion_matrix = ConfusionMatrix(labels)
            for j, input in enumerate(input_dataset):
                confusion_matrix.increment(j % 2, np.argmax(perc.predict_output(input)))
            accuracy.append(confusion_matrix.accuracy())

        accuracy_sum += np.array(accuracy)

    average_accuracy = accuracy_sum / num_runs
    return current_epoch, average_accuracy



if __name__ == "__main__":

    expected_outputs = [(1, 0) if i % 2 == 0 else (0, 1) for i in range(10)]
    input_dataset = read_number_files("training/TP3-ej3-digitos.txt")
    layers = [8, 6, 4, 1, 2]
    input_size = len(input_dataset[0])

    layer_shapes = []
    current_size = input_size + 1
    for layer_size in layers:
        layer_shapes.append((current_size, layer_size))
        current_size = layer_size + 1

    labels = [0, 1]

    epochs = 1000
    epsilon = 0.02
    learning_rate = 0.001
    beta = 1
    optimizer_name = "adam"
    optimizer_alpha = 0.001
    optimizer_beta1 = 0.9
    optimizer_beta2 = 0.999
    optimizer_epsilon = 0.00000008

    optimizer = get_optimizer(
        optimizer_name,
        0.0001,
        optimizer_alpha,
        optimizer_beta1,
        optimizer_beta2,
        optimizer_epsilon,
        layer_shapes
    )

    activations = ["tanh", "logistic", "relu", "softplus"]
    plt.figure()

    for activation_function in activations:
        function, derivate = get_sigmoid_function_and_derivate(beta, activation_function)
        current_epoch, average_accuracy = gather_data(
            activation_function,
            learning_rate,
            input_dataset,
            expected_outputs,
            function,
            derivate,
            layers,
            optimizer
        )
        plt.plot(current_epoch, average_accuracy, label=activation_function)

    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.title('Comparación de funciones de activación')
    plt.grid(True)
    plt.legend()
    plt.ylim(0.0, 1.0)
    plt.xlim(0, epochs)

    folder = "output"
    filename = "accuracy_comparison.png"
    plt.savefig(folder + '/' + filename)
    plt.show()
