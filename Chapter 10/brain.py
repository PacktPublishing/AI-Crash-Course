# -*- coding: utf-8 -*-
"""
Created on Sat May  4 17:46:39 2019

@author: janwa
"""

from keras.models import Sequential, load_model
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from keras.optimizers import Adam

class Brain(object):
    
    def __init__(self, lr, inputShape, nO):
        self.model = Sequential()
        self.model.add(Conv2D(32, (3,3), activation = 'relu', input_shape = inputShape))
        self.model.add(MaxPooling2D((2,2)))
        self.model.add(Conv2D(32, (2,2), activation = 'relu'))
        self.model.add(MaxPooling2D((2,2)))
        self.model.add(Flatten())
        self.model.add(Dense(units = 256, activation = 'relu'))
        self.model.add(Dense(units = nO))
        self.model.compile(loss = 'mse', optimizer = Adam(lr = lr))
    
    def loadModel(self, filepath):
        self.model = load_model(filepath)
        return self.model