# AI for Games - Beat the Snake game
# Training the AI

# Importing the libraries
from environment import Environment
from brain import Brain
from DQN import Dqn
import numpy as np
import matplotlib.pyplot as plt

# Defining the parameters
memSize = 60000
batchSize = 32
learningRate = 0.0001
gamma = 0.9
nLastStates = 4

epsilon = 1.
epsilonDecayRate = 0.0002
minEpsilon = 0.05

filepathToSave = 'model2.h5'

# Creating the Environment, the Brain and the Experience Replay Memory
env = Environment(0)
brain = Brain((env.nRows, env.nColumns, nLastStates), learningRate)
model = brain.model
dqn = Dqn(memSize, gamma)

# Making a function that will initialize game states
def resetStates():
    currentState = np.zeros((1, env.nRows, env.nColumns, nLastStates))
    
    for i in range(nLastStates):
        currentState[:,:,:,i] = env.screenMap
    
    return currentState, currentState

# Starting the main loop
epoch = 0
scores = list()
maxNCollected = 0
nCollected = 0.
totNCollected = 0
while True:
    # Resetting the environment and game states
    env.reset()
    currentState, nextState = resetStates()
    epoch += 1
    gameOver = False
    
    # Starting the second loop in which we play the game and teach our AI
    while not gameOver: 
        
        # Choosing an action to play
        if np.random.rand() < epsilon:
            action = np.random.randint(0, 4)
        else:
            qvalues = model.predict(currentState)[0]
            action = np.argmax(qvalues)
        
        # Updating the environment
        state, reward, gameOver = env.step(action)
        
        # Adding new game frame to the next state and deleting the oldest frame from next state
        state = np.reshape(state, (1, env.nRows, env.nColumns, 1))
        nextState = np.append(nextState, state, axis = 3)
        nextState = np.delete(nextState, 0, axis = 3)
        
        # Remembering the transition and training our AI
        dqn.remember([currentState, action, reward, nextState], gameOver)
        inputs, targets = dqn.get_batch(model, batchSize)
        model.train_on_batch(inputs, targets)
        
        # Checking whether we have collected an apple and updating the current state
        if env.collected:
            nCollected += 1
        
        currentState = nextState
    
    # Checking if a record of apples eaten in a around was beaten and if yes then saving the model
    if nCollected > maxNCollected and nCollected > 2:
        maxNCollected = nCollected
        model.save(filepathToSave)
    
    totNCollected += nCollected
    nCollected = 0
    
    # Showing the results each 100 games
    if epoch % 100 == 0 and epoch != 0:
        scores.append(totNCollected / 100)
        totNCollected = 0
        plt.plot(scores)
        plt.xlabel('Epoch / 100')
        plt.ylabel('Average Score')
        plt.savefig('stats.png')
        plt.close()
    
    # Lowering the epsilon
    if epsilon > minEpsilon:
        epsilon -= epsilonDecayRate
    
    # Showing the results each game
    print('Epoch: ' + str(epoch) + ' Current Best: ' + str(maxNCollected) + ' Epsilon: {:.5f}'.format(epsilon))
