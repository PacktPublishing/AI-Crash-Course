# -*- coding: utf-8 -*-
"""
Created on Sat May  4 17:46:08 2019

@author: janwa
"""

import pygame
import cv2
import numpy as np
from brain import Brain
from environment import Environment

filepathToOpen = 'model.h5'
scalingFactor = 0.2
nLastFrames = 3
nMaxIterations = 400


env = Environment(0, 0, 0, 5)

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

editFromHere = False
while True:
    if env.editEnabled:
        env.edit()
    else:
        
        currentState = initializeState(env)
        brain = Brain(0.001, (currentState.shape[1], currentState.shape[2], currentState.shape[3]), 9)
        model = brain.loadModel(filepathToOpen)
        while not env.editEnabled:
            gameOver = False
            currentState = initializeState(env)
            iteration = 0
            env.reset()
            nextState = currentState
            while not gameOver and  iteration < nMaxIterations:
                iteration += 1
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_e:
                            env.editEnabled = True
                            editFromHere = True
                            env.reset()
                
                if editFromHere:
                    break
                
                action = np.argmax(model.predict(currentState)[0])
                
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
                
                frame, _, gameOver = env.step(xDir, yDir)
                
                frame = prepareFrame(frame, scalingFactor)
                frame = np.reshape(frame, (1, frame.shape[0], frame.shape[1], frame.shape[2]))
                nextState = np.append(nextState, frame, axis = 3)
                for i in range(3):
                    nextState = np.delete(nextState, i, axis = 3)
    
                currentState = nextState
        env.finished = False