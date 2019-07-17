# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 12:45:40 2019

@author: janwa
"""

from environment import Environment
from brain import Brain
from DQN import Dqn
import numpy as np
import matplotlib.pyplot as plt


memSize = 60000
batchSize = 32
learningRate = 0.0001
gamma = 0.9
nLastStates = 4
maxIterations = 40000

epsilon = 1.
epsilonDecayRate = 0.0002
minEpsilon = 0.05

filepathToSave = 'model2.h5'


env = Environment(0)
brain = Brain((env.nRows, env.nColumns, nLastStates), learningRate)
model = brain.model
dqn = Dqn(memSize, gamma)


def resetStates():
    currentState = np.zeros((1, env.nRows, env.nColumns, 1))
    
    for i in range(nLastStates):
        state = np.reshape(env.screenMap, (1, env.nRows, env.nColumns, 1))
        currentState = np.append(currentState, state, axis = 3)
    
    currentState = np.delete(currentState, 0, axis = 3)
    
    return currentState, currentState

epoch = 0
rewards = list()
maxNCollected = 0
nCollected = 0.
totNCollected = 0
while True:
    env.reset()
    currentState, nextState = resetStates()
    iteration = 0
    epoch += 1;
    gameOver = False
    
    while iteration < maxIterations and not gameOver: 
        iteration += 1
        
        if np.random.rand() < epsilon:
            action = np.random.randint(0, 4)
        else:
            qvalues = model.predict(currentState)[0]
            action = np.argmax(qvalues)
    
        
        state, reward, gameOver = env.step(action)

        
        state = np.reshape(state, (1, env.nRows, env.nColumns, 1))
        nextState = np.append(nextState, state, axis = 3)
        nextState = np.delete(nextState, 0, axis = 3)
        
        dqn.remember([currentState, action, reward, nextState], gameOver)
        inputs, targets = dqn.getBatch(model, batchSize)
        model.train_on_batch(inputs, targets)
        
        if env.collected:
            nCollected += 1
        
        currentState = nextState
    
    if nCollected > maxNCollected and nCollected > 2:
        maxNCollected = nCollected
        model.save(filepathToSave)
    
    totNCollected += nCollected
    nCollected = 0
    
    
    if epoch % 100 == 0 and epoch != 0:
        rewards.append(totNCollected / 100)
        totNCollected = 0
        plt.plot(rewards)
        plt.xlabel('Epoch / 100')
        plt.ylabel('Average Collected')
        plt.show()
        
    
    if epsilon > minEpsilon:
        epsilon -= epsilonDecayRate
    
    print('Epoch: ' + str(epoch) + ' Current Best: ' + str(maxNCollected) + ' Epsilon: {:.5f}'.format(epsilon))

    
    
