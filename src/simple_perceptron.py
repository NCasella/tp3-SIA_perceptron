import numpy as np
import random
import math
class SimplePerceptron():
    def __init__(self,learning_rate:float=1e-4,training_input:list=None,training_output: list=None): 
        self.learning_rate=learning_rate
        self.training_input=self._get_input_with_bias(training_input)
        self.weights=[ random.uniform(-0.5,0.5) for w in range(self.training_input.shape[1]) ]
        self.training_output=np.array(training_output)
    
    def _get_input_with_bias(self, training_input):
        training_input = np.array(training_input)
        if training_input.ndim == 1:  
            training_input = training_input.reshape(1, -1)
        bias = np.ones((training_input.shape[0], 1), dtype=int)  
        return np.hstack([bias, training_input])  
        
    def calculate_error(self,expected,output):
        return abs(expected-output)
    
    def compute_activation(self,hμ):
        return 1 if hμ>=0 else -1
    
    def calculate_derivate(self,hµ):
        return 1
    
    def predict_output(self, input):
        x_with_bias = self._get_input_with_bias(input)
        return self.compute_activation(float(x_with_bias @ self.weights))

    
    def train_perceptron(self,epochs:int,epsilon:float):
        error_history=[]
        convergence:bool=True
        convergence_epoch = -1
        convergence_amount = 0
        first_convergence = False
        for epoch in range(epochs):
            total_error=0
            for µ in range(len(self.training_input)): #cada x^µ
                hµ:float=self.training_input[μ]@self.weights
                o_h=self.compute_activation(hμ)
                for i,w_i in enumerate(self.weights):
                    self.weights[i]=w_i+self.learning_rate*(self.training_output[µ]-o_h)*self.calculate_derivate(hμ)*self.training_input[μ][i]
                error=self.calculate_error(expected=self.training_output[μ],output=o_h)                                      #^^^^^^^^^^^^^^^^^^ (x^µ)_i
                total_error+=error
            error_history.append(total_error)
            convergence=total_error<epsilon #TODO: ver si esta bien?
            if convergence:
                convergence_amount+=1
            else:
                convergence_amount=0
            if convergence_amount>10 and not first_convergence:
                first_convergence=True
                convergence_epoch=epoch
            p=np.random.permutation(len(self.training_input))
            self.training_input=self.training_input[p]
            self.training_output=self.training_output[p]
            
        print(f"learning rate {self.learning_rate}: ")
        if first_convergence:
            print(f"se llego a convergencia en epoch {convergence_epoch}")
        else:
            print("no se llego a convergencia :(")
        return error_history, convergence_epoch