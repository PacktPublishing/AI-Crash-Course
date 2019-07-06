# -*- coding: utf-8 -*-
"""
Created on Thu May  2 13:22:25 2019

@author: janwa
"""

import pygame
import numpy as np
import time
import pandas as pd
    

class Player(object):
    
    def __init__(self, x, y):
        self.posx = x
        self.posy = y
        self.defaultx = self.posx
        self.defaulty = self.posy
    
class Enemy(object):
    
    def __init__(self,x, y, direction):
        self.posx = x
        self.posy = y
        self.defaultx = self.posx
        self.defaulty = self.posy
        self.direction = direction
        
class Environment(object):
    
    def __init__(self, dr = -0.03, pr = 1, nr = -1, obsDist = 5):
        self.width = 1000
        self.height = 720
        self.nColumns = 25
        self.nRows = 18
        self.enemyRadius = 10
        self.speedPlayer = 2
        self.speedEnemy = 4
        self.slowdown = 0.0 #in seconds
        self.playerScale = 0.8
        self.defReward = dr
        self.negReward = nr
        self.posReward = pr
        self.obsDistance = obsDist
        self.filepathToOpenMap = 'Maps/map1.csv'
        self.filepathToSaveMap = 'Maps/map1.csv'        
        
        self.playerHeight = self.playerScale*(self.height/self.nRows)
        self.playerWidth = self.playerScale*(self.width/self.nColumns)
        self.board = np.zeros((self.nRows, self.nColumns))
        self.AIGatesList = list()
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.cellWidth = self.width / self.nColumns
        self.cellHeight = self.height / self.nRows
        self.enemies = list()
        
        self.resetScreen()
        
        pygame.display.flip()
        print('Press 1 to add spawn point')
        print('Press 2 to add enemy')
        print('Press 3 to add checkpoint space')
        print('Press 4 to add board')
        print('Press 5 to add background')
        print('Press 6 to add reward gates for AI')
        print('Press 7 to set finish line')
        
        self.editEnabled = True
        
        self.drawSpawn = False
        self.drawEnemy = False
        self.drawCheckpoint = False
        self.drawBoard = False
        self.drawBackground = False
        self.addAIGate = False
        self.preciseEditing = False
        self.addFinishLine = False
        
        self.finished = False
        
    def resetScreen(self):
        for i in range(self.nRows):
            for j in range(self.nColumns):
                if self.board[i][j] == 0:
                    pygame.draw.rect(self.screen, (170, 165, 255), (j*self.cellWidth, i*self.cellHeight, self.cellWidth, self.cellHeight))
                    
                elif self.board[i][j] == 1:
                    if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                        pygame.draw.rect(self.screen, (248, 247, 255), (j*self.cellWidth, i*self.cellHeight, self.cellWidth, self.cellHeight))
                    else:
                        pygame.draw.rect(self.screen, (224, 218, 254), (j*self.cellWidth, i*self.cellHeight, self.cellWidth, self.cellHeight))
                        
                elif self.board[i][j] == 2 or self.board[i][j] == 4:
                    pygame.draw.rect(self.screen, (158, 242, 155), (j*self.cellWidth, i*self.cellHeight, self.cellWidth, self.cellHeight))
                elif self.board[i][j] == 3:
                    pygame.draw.rect(self.screen, (30, 189, 255), (j*self.cellWidth, i*self.cellHeight, self.cellWidth, self.cellHeight))
        try:
            pygame.draw.rect(self.screen, (255, 0, 0), (self.player.posx, self.player.posy, self.playerWidth, self.playerHeight))
        except:
            pass
        
        for i in range(len(self.enemies)):
            enemy = self.enemies[i]
            pygame.draw.circle(self.screen, (0, 0, 255), (int(enemy.posx), int(enemy.posy)), self.enemyRadius)
            
    def edit(self):
        x,y = pygame.mouse.get_pos()
        
        self.resetScreen()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.drawSpawn = True
                    self.drawCheckpoint = False
                    self.drawEnemy = False
                    self.drawBoard = False
                    self.addAIGate = False
                    self.drawBackground = False
                    self.addFinishLine = False
                    
                elif event.key == pygame.K_2:
                    self.drawEnemy = True
                    self.drawBoard = False
                    self.drawSpawn = False
                    self.drawCheckpoint = False
                    self.drawBackground = False
                    self.addAIGate = False
                    self.addFinishLine = False
                    
                elif event.key == pygame.K_3:
                    self.drawEnemy = False
                    self.drawBoard = False
                    self.addAIGate = False
                    self.drawSpawn = False
                    self.drawBackground = False
                    self.addFinishLine = False
                    if not self.drawCheckpoint:
                        self.drawCheckpoint = True
                    else:
                        self.drawCheckpoint = False
                        
                elif event.key == pygame.K_4:
                    self.drawEnemy = False
                    self.drawCheckpoint = False
                    self.addAIGate = False
                    self.drawSpawn = False
                    self.drawBackground = False
                    self.addFinishLine = False
                    if not self.drawBoard:
                        self.drawBoard = True
                    else:
                        self.drawBoard = False
                        
                elif event.key == pygame.K_5:
                    self.drawEnemy = False
                    self.drawCheckpoint = False
                    self.drawSpawn = False
                    self.addAIGate = False
                    self.drawBoard = False
                    self.addFinishLine = False
                    if not self.drawBackground:
                        self.drawBackground = True
                    else:
                        self.drawBackground = False
                elif event.key == pygame.K_6:
                    self.drawEnemy = False
                    self.drawCheckpoint = False
                    self.drawSpawn = False
                    self.drawBackground = False
                    self.drawBoard = False
                    self.addFinishLine = False
                    if not self.addAIGate:
                        self.addAIGate = True
                    else:
                        self.addAIGate = False
                elif event.key == pygame.K_7:
                    self.drawEnemy = False
                    self.drawCheckpoint = False
                    self.drawSpawn = False
                    self.drawBackground = False
                    self.drawBoard = False
                    self.addAIGate = False
                    if not self.addFinishLine:
                        self.addFinishLine = True
                    else:
                        self.addFinishLine = False
                        
                elif event.key == pygame.K_s:
                    print('')
                    print('Saving map to ' + self.filepathToSaveMap)
                    self.saveMap(self.filepathToSaveMap)
                    
                elif event.key == pygame.K_l:
                    print('')
                    print('Loading map from ' + self.filepathToOpenMap)
                    self.loadMap(self.filepathToOpenMap)
                elif event.key == pygame.K_RETURN:
                    self.AIGatesList.clear()
                    for i in range(self.nRows):
                        for j in range(self.nColumns):
                            if self.board[i][j] == 3:
                                self.AIGatesList.append((i, j))
                    self.editEnabled = False
                    print('')
                    print('You have entered play mode')
                    if not hasattr(self, 'player'):
                        print('')
                        print('Please add a player by pressing 1')
                        self.editEnabled = True
                        print('You have entered edit mode')
                        
                    finishExists = False
                    for i in range(self.nRows):
                        for j in range(self.nColumns):
                            if self.board[i][j] == 4:
                                finishExists = True
                    if not finishExists:
                        print('')
                        print('Please add a finish line by pressing 7')
                        self.editEnabled = True
                        print('You have entered edit mode')
                    
                
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.preciseEditing = True
                    
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.preciseEditing = False
              
        rowPos = int(y/self.cellHeight)
        columnPos = int(x/self.cellWidth)
                
        
        if self.drawSpawn:
            precisex = int(columnPos*self.cellWidth + (self.cellWidth - self.playerWidth)/2)
            precisey = int(rowPos*self.cellHeight + (self.cellHeight - self.playerHeight)/2)
            if pygame.mouse.get_pressed()[0] == 0:
                if not self.preciseEditing:
                    pygame.draw.rect(self.screen, (255, 0, 0), (x, y, self.playerWidth, self.playerHeight))
                else:
                    pygame.draw.rect(self.screen, (255, 0, 0), (precisex, precisey, self.playerWidth, self.playerHeight))
            else:
                if not self.preciseEditing:
                    self.player = Player(x, y)
                else:
                    self.player = Player(precisex, precisey)
                self.drawSpawn = False
                
        if self.drawEnemy:
            precisex = int(columnPos*self.cellWidth + self.cellWidth/2)
            precisey = int(rowPos*self.cellHeight + self.cellHeight/2)
            if pygame.mouse.get_pressed()[0] == 0:
                if self.preciseEditing:
                    pygame.draw.circle(self.screen, (0, 0, 255), (precisex, precisey), self.enemyRadius)
                else:
                    pygame.draw.circle(self.screen, (0, 0, 255), (x, y), self.enemyRadius)
            else:
                direction = input('Enter direction (0 = up, 1 = down, 2 = right, 3 = left): ')
                print('Direction set to ' + str(direction))
                direction = int(direction)
                if not self.preciseEditing:
                    enemy = Enemy(x, y, direction)
                else:
                    enemy = Enemy(precisex, precisey, direction)
                self.enemies.append(enemy)
                self.drawEnemy = False
                
        if self.drawCheckpoint:
            if pygame.mouse.get_pressed()[0] == 0:
                pygame.draw.rect(self.screen, (158, 242, 155), (columnPos*self.cellWidth, rowPos*self.cellHeight, self.cellWidth, self.cellHeight))
            else:
                self.board[rowPos][columnPos] = 2
        
        if self.drawBoard:
            if pygame.mouse.get_pressed()[0] == 0:
                if (rowPos % 2 == 0 and columnPos % 2 == 0) or (rowPos % 2 == 1 and columnPos % 2 == 1):
                    pygame.draw.rect(self.screen, (248, 247, 255), (columnPos*self.cellWidth, rowPos*self.cellHeight, self.cellWidth, self.cellHeight))
                else:
                    pygame.draw.rect(self.screen, (224, 218, 254), (columnPos*self.cellWidth, rowPos*self.cellHeight, self.cellWidth, self.cellHeight))
            else:
                self.board[rowPos][columnPos] = 1
             
        if self.drawBackground:
            if pygame.mouse.get_pressed()[0] == 0:
                pygame.draw.rect(self.screen, (170, 165, 255), (columnPos*self.cellWidth, rowPos*self.cellHeight, self.cellWidth, self.cellHeight))
            else:
                self.board[rowPos][columnPos] = 0
        
        if self.addAIGate:
            if pygame.mouse.get_pressed()[0] == 0:
                pygame.draw.rect(self.screen, (30, 189, 255), (columnPos*self.cellWidth, rowPos*self.cellHeight, self.cellWidth, self.cellHeight))
            else:
                self.board[rowPos][columnPos] = 3
                
        if self.addFinishLine:
            if pygame.mouse.get_pressed()[0] == 0:
                pygame.draw.rect(self.screen, (158, 242, 155), (columnPos*self.cellWidth, rowPos*self.cellHeight, self.cellWidth, self.cellHeight))
            else:
                self.board[rowPos][columnPos] = 4
            
        pygame.display.flip()
      
    
    def reset(self):
        try:
            self.player.posx = self.player.defaultx
            self.player.posy = self.player.defaulty
        except:
            pass
        
        for i in range(len(self.enemies)):
            enemy = self.enemies[i]
            enemy.posx = enemy.defaultx
            enemy.posy = enemy.defaulty
      
        for i in range(len(self.AIGatesList)):
            self.board[self.AIGatesList[i][0]][self.AIGatesList[i][1]] = 3
    
    def observe(self):
        
        w = self.cellWidth * self.obsDistance
        h = self.cellHeight * self.obsDistance
        if self.player.posx - (self.obsDistance / 2)*self.cellWidth >= 0:
            x = self.player.posx + self.playerWidth/2 - (self.obsDistance / 2) * self.cellWidth
        else:
            x = 0
        if self.player.posy - (self.obsDistance / 2)*self.cellHeight >= 0:
            y = self.player.posy + self.playerHeight/2 - (self.obsDistance / 2) * self.cellHeight
        else:
            y = 0

        if x + w > self.width:
            x = self.width - w
        if y + h > self.height:
            y = self.height - h
        
        roi = pygame.Rect(x, y, w, h)
        sub = self.screen.subsurface(roi)
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, w, h), 2)
        image = pygame.surfarray.array3d(sub)
        image = image.transpose([1, 0, 2])
        return image
    
    def saveMap(self, filepath):
        df = pd.DataFrame([[self.width, self.height, self.nRows, self.nColumns, len(self.enemies)]])
        df = df.append(pd.DataFrame(self.board))
        for enemy in self.enemies:
            df = df.append(pd.DataFrame([[enemy.posx, enemy.posy, enemy.direction]]))
        df = df.append(pd.DataFrame([[self.player.defaultx, self.player.defaulty]]))
        df.to_csv(filepath)
    
    def loadMap(self, filepath):
        df = pd.read_csv(filepath)
        data = np.array(df.iloc[:, 1:].values)
        
        width = int(data[0][0])
        height = int(data[0][1])
        self.nRows = int(data[0][2])
        self.nColumns = int(data[0][3])
        nEnemies = int(data[0][4])

        for i in range(self.nRows):
            for j in range(self.nColumns):
                self.board[i][j] = int(data[i + 1][j])
        
        scaleW = self.width / width
        scaleH = self.height / height
        for i in range(nEnemies):
            x = int(data[self.nRows + 1 + i][0])
            y = int(data[self.nRows + 1 + i][1])
            x *= scaleW
            y *= scaleH
            direction = int(data[self.nRows + 1 + i][2])
            enemy = Enemy(x, y, direction)
            self.enemies.append(enemy)
        
        xp = int(data[self.nRows + nEnemies + 1][0])
        yp = int(data[self.nRows + nEnemies + 1][1])
        xp *= scaleW
        yp *= scaleH
        
        
        self.player = Player(xp, yp)
        self.cellHeight = self.height / self.nRows
        self.cellWidth = self.width / self.nColumns
        
        self.playerHeight = self.playerScale * (self.height/self.nRows)
        self.playerWidth = self.playerScale * (self.width/self.nColumns)
    
    def step(self, xDir, yDir):
        
        
        
        gameOver = False
        reward = self.defReward    
        
        if self.finished:
            reward = 0.
        
        xs = []
        ys = []
        cany = True
        canx = True
        xs.append(self.player.posx)             #x1 = self.player.posx = xs[0]
        ys.append(self.player.posy)             #y1 = self.player.posy = ys[0]
        xs.append(xs[0] + self.playerWidth)     #x2 = x1 + self.playerWidth = xs[1]
        ys.append(ys[0])                        #y2 = y1 = ys[1]
        xs.append(xs[0])                        #x3 = x1 = xs[2]
        ys.append(ys[0] + self.playerHeight)    #y3 = y1 + self.playerHeight = ys[2] 
        xs.append(xs[1])                        #x4 = x2 = xs[3]
        ys.append(ys[2])                        #y4 = y3 = ys[3]
        
        if xDir > 0:
            columnPos2 = int((xs[1] + self.speedPlayer)/self.cellWidth)
            rowPos2 = int(ys[1]/self.cellHeight)
            columnPos4 = int((xs[3] + self.speedPlayer)/self.cellWidth)
            rowPos4 = int(ys[3]/self.cellHeight)
            if columnPos2 < self.nColumns:
                if self.board[rowPos2][columnPos2] == 0 or self.board[rowPos4][columnPos4] == 0:
                    canx = False
                if self.board[rowPos2][columnPos2] == 3:
                    reward = self.posReward
                    self.board[rowPos2][columnPos2] = 1
                elif self.board[rowPos4][columnPos4] == 3:
                    reward = self.posReward
                    self.board[rowPos4][columnPos4] = 1
                if self.board[rowPos2][columnPos2] == 4 or self.board[rowPos4][columnPos4] == 4:
                    if not self.finished:
                        reward = self.posReward
                        self.finished = True

            else:
                canx = False
                
        elif xDir < 0:
            columnPos1 = int((xs[0] - self.speedPlayer)/self.cellWidth)
            rowPos1 = int(ys[0]/self.cellHeight)
            columnPos3 = int((xs[2] - self.speedPlayer)/self.cellWidth)
            rowPos3 = int(ys[2]/self.cellHeight)
            if xs[0] - self.speedPlayer >= 0:
                if self.board[rowPos1][columnPos1] == 0 or self.board[rowPos3][columnPos3] == 0:
                    canx = False
                if self.board[rowPos1][columnPos1] == 3:
                    reward = self.posReward
                    self.board[rowPos1][columnPos1] = 1
                elif self.board[rowPos3][columnPos3] == 3:
                    reward = self.posReward
                    self.board[rowPos3][columnPos3] = 1
                if self.board[rowPos1][columnPos1] == 4 or self.board[rowPos3][columnPos3] == 4:
                    if not self.finished:
                        reward = self.posReward
                        self.finished = True

            else:
                canx = False
                
        if yDir > 0:
            columnPos3 = int(xs[2]/self.cellWidth)
            rowPos3 = int((ys[2] + self.speedPlayer)/self.cellHeight)
            columnPos4 = int(xs[3]/self.cellWidth)
            rowPos4 = int((ys[3] + self.speedPlayer)/self.cellHeight)
            if rowPos3 < self.nRows:
                if self.board[rowPos3][columnPos3] == 0 or self.board[rowPos4][columnPos4] == 0:
                    cany = False
                if self.board[rowPos3][columnPos3] == 3:
                    reward = self.posReward
                    self.board[rowPos3][columnPos3] = 1
                elif self.board[rowPos4][columnPos4] == 3:
                    reward = self.posReward
                    self.board[rowPos4][columnPos4] = 1
                if self.board[rowPos3][columnPos3] == 4 or self.board[rowPos4][columnPos4] == 4:
                    if not self.finished:
                        reward = self.posReward
                        self.finished = True

            else:
                cany = False
                
        elif yDir < 0:
            columnPos1 = int(xs[0]/self.cellWidth)
            rowPos1 = int((ys[0] - self.speedPlayer)/self.cellHeight)
            columnPos2 = int(xs[1]/self.cellWidth)
            rowPos2 = int((ys[1] - self.speedPlayer)/self.cellHeight)
            if ys[1] - self.speedPlayer >= 0:
                if self.board[rowPos1][columnPos1] == 0 or self.board[rowPos2][columnPos2] == 0:
                    cany = False
                if self.board[rowPos1][columnPos1] == 3:
                    reward = self.posReward
                    self.board[rowPos1][columnPos1] = 1
                elif self.board[rowPos2][columnPos2] == 3:
                    reward = self.posReward
                    self.board[rowPos2][columnPos2] = 1
                if self.board[rowPos1][columnPos1] == 4 or self.board[rowPos2][columnPos2] == 4:
                    if not self.finished:
                        reward = self.posReward
                        self.finished = True

            else:
                cany = False
        if cany:
            self.player.posy += yDir*self.speedPlayer
        if canx:
            self.player.posx += xDir*self.speedPlayer
            
        for enemy in self.enemies:
            
            if enemy.direction == 0:
                rowPos = int((enemy.posy - self.speedEnemy - self.enemyRadius)/self.cellHeight)
                columnPos = int(enemy.posx/self.cellWidth)
                if enemy.posy - self.speedEnemy - self.enemyRadius >= 0:
                    if self.board[rowPos][columnPos] != 1 and self.board[rowPos][columnPos] != 3:
                        enemy.direction = 1
                    else:
                        enemy.posy -= self.speedEnemy
                else:
                    enemy.direction = 1
            elif enemy.direction == 1:
                rowPos = int((enemy.posy + self.speedEnemy + self.enemyRadius)/self.cellHeight)
                columnPos = int(enemy.posx/self.cellWidth)
                if rowPos < self.nRows:
                    if self.board[rowPos][columnPos] != 1 and self.board[rowPos][columnPos] != 3:
                        enemy.direction = 0
                    else: 
                        enemy.posy += self.speedEnemy
                else:
                    enemy.direction = 0
            elif enemy.direction == 2:
                rowPos = int(enemy.posy/self.cellHeight)
                columnPos = int((enemy.posx + self.speedEnemy + self.enemyRadius)/self.cellWidth)
                if columnPos < self.nColumns:
                    if self.board[rowPos][columnPos] != 1 and self.board[rowPos][columnPos] != 3:
                        enemy.direction = 3
                    else:
                        enemy.posx += self.speedEnemy
                else:
                    enemy.direction = 3
            elif enemy.direction == 3:
                rowPos = int(enemy.posy/self.cellHeight)
                columnPos = int((enemy.posx - self.speedEnemy - self.enemyRadius)/self.cellWidth)
                if enemy.posx - self.speedEnemy - self.enemyRadius >= 0:
                    if self.board[rowPos][columnPos] != 1 and self.board[rowPos][columnPos] != 3:
                        enemy.direction = 2
                    else:
                        enemy.posx -= self.speedEnemy
                else:
                    enemy.direction = 2
        
            if enemy.posy > ys[1] and enemy.posy < ys[3] and enemy.posx < xs[1] and enemy.posx > xs[0]:
                gameOver = True
            elif enemy.posy > ys[1] and enemy.posy < ys[3] and enemy.posx - self.enemyRadius < xs[1] and enemy.posx > xs[0]:
                gameOver = True
            elif enemy.posy > ys[1] and enemy.posy < ys[3] and enemy.posx + self.enemyRadius > xs[0] and enemy.posx < xs[1]:
                gameOver = True
            elif enemy.posx > xs[0] and enemy.posx < xs[1] and enemy.posy + self.enemyRadius > ys[1] and enemy.posy < ys[3]:
                gameOver = True
            elif enemy.posx > xs[0] and enemy.posx < xs[1]and enemy.posy - self.enemyRadius < ys[3] and enemy.posy > ys[1]:
                gameOver = True
            
            
            for i in range(4):
                xDiff = abs(xs[i] - enemy.posx)
                yDiff = abs(ys[i] - enemy.posy)
                d = pow(pow(xDiff,2) + pow(yDiff,2), 0.5)
                distance = d - self.enemyRadius
                if distance < 0:
                    gameOver = True
                    
                
        if gameOver:
            self.reset()
            reward = self.negReward
            
            
            
        self.resetScreen()
        time.sleep(self.slowdown)
        state = self.observe()
        pygame.display.flip()
        
        return state, reward, gameOver
    
env = Environment(1,1,1, 5)
up = False
down = False
right = False
left = False
while True:
    if env.editEnabled:
        
        env.edit()
    else:
        
        xDir = 0
        yDir = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    down = False
                    up = True
                if event.key == pygame.K_DOWN:
                    up = False
                    down = True
                if event.key == pygame.K_RIGHT:
                    right = True
                    left = False
                if event.key == pygame.K_LEFT:
                    right = False
                    left = True
                if event.key == pygame.K_e:
                    env.editEnabled = True
                    print('')
                    print('You have entered edit mode')
                    env.reset()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    up = False
                if event.key == pygame.K_DOWN:
                    down = False
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_LEFT:
                    left = False
        if up:
            yDir = -1
        elif down:
            yDir = 1
        if right:
            xDir = 1
        elif left:
            xDir = -1
        env.step(xDir, yDir)