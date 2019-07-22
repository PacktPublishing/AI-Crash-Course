#AI for Snake using Deep Q-Learning and Convolutional Neural Networks: Testing AI

from environment import Environment
from brain import Brain
import numpy as np

nLastStates = 4
filepathToOpen = 'model.h5'
slowdown = 75

env = Environment(slowdown)
brain = Brain((env.nRows, env.nColumns, nLastStates))
model = brain.loadModel(filepathToOpen)

def resetStates():
    currentState = np.zeros((1, env.nRows, env.nColumns, nLastStates))
    
    for i in range(nLastStates):
        currentState[:,:,:,i] = env.screenMap
   
    return currentState, currentState

while True:
    env.reset()
    currentState, nextState = resetStates()
    gameOver = False
    while not gameOver: 
        
        qvalues = model.predict(currentState)[0]
        action = np.argmax(qvalues)
        
        state, _, gameOver = env.step(action)

        state = np.reshape(state, (1, env.nRows, env.nColumns, 1))
        nextState = np.append(nextState, state, axis = 3)
        nextState = np.delete(nextState, 0, axis = 3)
        
        currentState = nextState
