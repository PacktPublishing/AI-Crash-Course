# AI for Games - Beat the Snake game
# Testing the AI

# Importing the libraries
from environment import Environment
from brain import Brain
import numpy as np

# Defining the parameters
nLastStates = 4
filepathToOpen = 'model.h5'
slowdown = 75

# Creating the Environment and the Brain
env = Environment(slowdown)
brain = Brain((env.nRows, env.nColumns, nLastStates))
model = brain.loadModel(filepathToOpen)

# Making a function that will reset game states
def resetStates():
    currentState = np.zeros((1, env.nRows, env.nColumns, nLastStates))
    
    for i in range(nLastStates):
        currentState[:,:,:,i] = env.screenMap
   
    return currentState, currentState

# Starting the main loop
while True:
    # Resetting the game and the game states
    env.reset()
    currentState, nextState = resetStates()
    gameOver = False
    
    # Playing the game
    while not gameOver: 
        
        # Choosing an action to play
        qvalues = model.predict(currentState)[0]
        action = np.argmax(qvalues)
        
        # Updating the environment
        state, _, gameOver = env.step(action)
        
        # Adding new game frame to next state and deleting the oldest one from next state
        state = np.reshape(state, (1, env.nRows, env.nColumns, 1))
        nextState = np.append(nextState, state, axis = 3)
        nextState = np.delete(nextState, 0, axis = 3)
        
        # Updating current state
        currentState = nextState
