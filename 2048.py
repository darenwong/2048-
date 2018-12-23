# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 05:29:17 2018

@author: Daren
"""

import pygame
import numpy as np
import copy


class gameboard:
    def __init__(self):
        self.w = 400
        self.h = 400
        self.tile_width = 90
        self.tile_height = 90
        self.grid = 100    
        self.display = pygame.display.set_mode((self.w, self.h))
        self.state = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
    
    def move_left(self):
        for a in self.state:
            num = 0
            while 0 in a: 
                a.remove(0) 
                num += 1    
            for n in range(num):
                a.append(0)           
            
            for n in range(len(a)):
                if n < len(a) - 1:
                    if a[n] == a[n+1]:
                        a[n] *= 2
                        for i in range(len(a) - n - 2):
                            a[n+1+i] = a[n+2+i]
                        a[-1] = 0
        return self.state 
        
        
    def move_up(self):
        self.state = np.array(self.state)
        self.state = np.rot90(self.state, 1)
        self.state = self.state.tolist()
        self.state = self.move_left()
        self.state = np.array(self.state)
        self.state = np.rot90(self.state, 3)
        self.state = self.state.tolist() 
        return self.state
        
    def move_down(self):
        self.state = np.array(self.state)
        self.state = np.rot90(self.state, 3)
        self.state = self.state.tolist()
        self.state = self.move_left()
        self.state = np.array(self.state)
        self.state = np.rot90(self.state, 1)
        self.state = self.state.tolist() 
        return self.state
    
    def move_right(self):
        self.state = np.array(self.state)
        self.state = np.rot90(self.state, 2)
        self.state = self.state.tolist()
        self.state = self.move_left()
        self.state = np.array(self.state)
        self.state = np.rot90(self.state, 2)
        self.state = self.state.tolist() 
        return self.state
    
    def spawn(self):
        zeros = []
        self.state = np.array(self.state)
        for i in range(self.state.shape[1]):
            for j in range(self.state.shape[0]):
                if self.state[i, j] == 0:
                    zeros.append([i,j])
        
        zeros = np.array(zeros)
        np.random.shuffle(zeros)
        if np.random.rand() > 0.75:    
            self.state[zeros[0,0], zeros[0,1]] = 1
        else:
            self.state[zeros[0,0], zeros[0,1]] = 2
        
        self.state = self.state.tolist()
        return self.state

    def check_status(self):
        teststate = copy.deepcopy(self.state)
        testboard = gameboard()
        testboard.state = teststate
        
        if testboard.move_left() == teststate and testboard.move_up() == teststate and testboard.move_down() == teststate and testboard.move_right() == teststate:
            done = 1
        else:
            done = 0    
        
        return done
    
    def check_empty(self):
        self.state = np.array(self.state)
        empty = 0 in self.state  
        self.state = self.state.tolist()
        return empty
    
    def render(self):
        self.display.fill((255, 255, 255))
        self.state = np.array(self.state)
        thickness = 0
            
        for i in range(self.state.shape[1]):
            for j in range(self.state.shape[0]):
                if self.state[j,i] != 0:
                    point = int(np.log2(self.state[j,i]))
            
                    if point < 5:
                        color = (0, 255, 255-point*51)
                    elif 5 <= point < 10:
                        color = ((point)*28, 255, 0)
                    elif point >= 10:
                        color= (255, 255-(point)*15, 0)
                        
                    font = pygame.font.SysFont(None, 50)    
    
                    
                    pygame.draw.rect(self.display, color, (i*self.grid+5, j*self.grid+5, self.tile_width, self.tile_height), thickness)
                    text = font.render(str(self.state[j,i]), True, (255, 255, 255))
                    textsize = text.get_rect()
                    textsize.center = (self.grid*(1/2+i), self.grid*(1/2+j))
                    self.display.blit(text,textsize)
                    
                else:
                    color = (255, 255, 255)
            
        self.state = self.state.tolist()
        pygame.display.update()
        
        
#Start menu screen
def game_loop():
    pygame.init()
    
    done = False
    board = gameboard()
    board.spawn()

    while not done:
  
        done = board.check_status()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True 
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:   
                    teststate = copy.deepcopy(board.state)
                    board.state = board.move_down()

                    if teststate != board.state and board.check_empty():
                        board.spawn()
                        board.render()
                        
                if event.key == pygame.K_UP:   
                    teststate = copy.deepcopy(board.state)
                    board.state = board.move_up()

                    if teststate != board.state and board.check_empty():
                        board.spawn()
                        board.render()

                if event.key == pygame.K_LEFT:   
                    teststate = copy.deepcopy(board.state)
                    board.state = board.move_left()

                    if teststate != board.state and board.check_empty():
                        board.spawn()
                        board.render()

                if event.key == pygame.K_RIGHT:   
                    teststate = copy.deepcopy(board.state)
                    board.state = board.move_right()

                    if teststate != board.state and board.check_empty():
                        board.spawn()
                        board.render()

        board.render()
        
game_loop()
pygame.quit()      
