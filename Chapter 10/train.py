#Hardest Game Ever AI: Train

from environment import Environment
import cv2
from DQN import DQN
import numpy as np
import matplotlib.pyplot as plt
import pygame
from brain import Brain


def prepareFrame(frame, scalFa):
    newY = int(frame.shape[1]*scalFa)
    newX = int(frame.shape[0]*scalFa)
    frame = cv2.resize(frame, (newY, newX))
    frame = frame / 255
    return frame

def initializeState(env):
    currentState = env.observe()
    currentState = prepareFrame(currentState, scalingFactor)
    initState = currentState
    for i in range(nLastFrames - 1):
        initState = np.append(initState, currentState, axis = 2)
    initState = np.reshape(initState, (1, initState.shape[0], initState.shape[1], initState.shape[2]))
    return initState

defReward = -0.04
posReward = 1
negReward = -2
observingDistance = 5
maxIterations = 400
batchSize = 32
maxMemory = 50000
gamma = 0.9
learningRate = 0.0001
nLastFrames = 3
scalingFactor = 0.2
epsilon = 0.
minEpsilon = 0.01
epsilonDecay = 0.002
filepathToSave = 'model2.h5'
saveRate = 100

rewards = []
env = Environment(defReward, posReward, negReward, observingDistance)
dqn = DQN(maxMemory, gamma)
epoch = 0
editFromHere = False
while True:
    if env.editEnabled:
        env.edit()
    else:
        
        currentState = initializeState(env)
        if not editFromHere:
            brain = Brain(learningRate, (currentState.shape[1], currentState.shape[2], currentState.shape[3]), 9)
            model = brain.loadModel('modelwithSlidingWindow3.h5')
        
        while not env.editEnabled:
            epoch += 1
            iteration = 0
            env.reset()
            currentState = initializeState(env)
            nextState = currentState
            gameOver = False
            totReward = 0
            env.finished = False
            while not gameOver and iteration < maxIterations:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_e:
                            env.editEnabled = True
                            editFromHere = True
                            env.reset()
                            
                if env.editEnabled:
                    break
                
                iteration += 1
                if np.random.rand() < epsilon:
                    action = np.random.randint(0,9)
                else:
                    qvalues = model.predict(currentState)[0]
                    action = np.argmax(qvalues)
                
                if action == 0:
                    yDir = 0
                    xDir = 0
                elif action == 1:
                    yDir = 0
                    xDir = -1
                elif action == 2:
                    yDir = 0
                    xDir = 1
                elif action == 3:
                    yDir = 1
                    xDir = -1
                elif action == 4:
                    yDir = 1
                    xDir = 0
                elif action == 5:
                    yDir = 1
                    xDir = 1
                elif action == 6:
                    yDir = -1
                    xDir = -1
                elif action == 7:
                    yDir = -1
                    xDir = 0
                elif action == 8:
                    yDir = -1
                    xDir = 1
                
                frame, reward, gameOver = env.step(xDir, yDir)
                totReward += reward
                frame = prepareFrame(frame, scalingFactor)
                frame = np.reshape(frame, (1, frame.shape[0], frame.shape[1], frame.shape[2]))
                nextState = np.append(nextState, frame, axis = 3)
                for i in range(3):
                    nextState = np.delete(nextState, i, axis = 3)
                
                dqn.remember([currentState, action, reward, nextState], gameOver)
                if iteration % 5 == 0:
                    inputs, targets = dqn.getBatch(model, batchSize)
                    model.train_on_batch(inputs, targets)
                
                currentState = nextState
            
            
            rewards.append(totReward)
            plt.plot(rewards)
            plt.xlabel('Epoch')
            plt.ylabel('Reward')
            plt.show()
            
            if epsilon > minEpsilon:
                epsilon -= epsilonDecay
            if epoch % saveRate == 0 and epoch != 0:
                model.save(filepathToSave)
            
                
                
                    
                
                
                
                
                
                
                
                
                
                
                
                
            
