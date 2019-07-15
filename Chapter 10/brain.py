#AI for Snake using Deep Q-Learning and Convolutional Neural Networks: Snake's brain


import keras
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten
from keras.optimizers import Adam


class Brain():
    
    def __init__(self, iS = (100,100,3), lr = 0.0005):
        self.learningRate = lr
        self.inputShape = iS
        self.numOutputs = 4
        self.model = Sequential() 
        
        self.model.add(Conv2D(32, (3,3), activation = 'relu', input_shape = self.inputShape))
        
        self.model.add(MaxPooling2D((2,2)))
        
        self.model.add(Conv2D(64, (2,2), activation = 'relu'))
        
        self.model.add(Flatten())
        
        self.model.add(Dense(units = 256, activation = 'relu'))
        
        self.model.add(Dense(units = self.numOutputs))
        
        self.model.compile(loss = 'mean_squared_error', optimizer = Adam(lr = self.learningRate))
        

    def loadModel(self, filepath):
        self.model = load_model(filepath)
        return self.model 
