# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 21:22:07 2019

@author: janwa
"""

class Bot():
    
    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy
    
    def move(self, speedx, speedy):
        self.posx += speedx
        self.posy += speedy
    
bot = Bot(3, 4)
bot.move(2, -1)
print(bot.posx, bot.posy)
