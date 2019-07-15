#AI for Snake using Deep Q-Learning and Convolutional Neural Networks: DQN memory

import numpy as np

class Dqn(object):
    
    def __init__(self, maxMemory, discount = 0.9):
        self.maxMemory = maxMemory
        self.discount = discount
        self.memory = list()
        
    def remember(self, transition, gameOver):
        self.memory.append([transition, gameOver])
        if len(self.memory) > self.maxMemory:
            del self.memory[0]
    
    
    def getBatch(self, model, batchSize):
        lenMemory = len(self.memory)
        numOutputs = model.output_shape[-1]
        inputs = np.zeros((min(lenMemory, batchSize), self.memory[0][0][0].shape[1],self.memory[0][0][0].shape[2],self.memory[0][0][0].shape[3]))
        targets = np.zeros((min(lenMemory, batchSize), numOutputs))
        for i, inx in enumerate(np.random.randint(0, lenMemory, size = min(lenMemory, batchSize))):
            currentState, action, reward, nextState = self.memory[inx][0]
            gameOver = self.memory[inx][1]
            inputs[i] = currentState
            targets[i] = model.predict(currentState)[0]
            Qsa = np.max(model.predict(nextState)[0])
            if gameOver:
                targets[i, action] = reward
            else:
                targets[i, action] = reward + self.discount * Qsa
            
        return inputs, targets
    
   
