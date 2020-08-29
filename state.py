"""States and cells are interchangeable, makes sense to think of them as a bunch of 1x1 squares of a
checkerboard. They will be rescaled as necessary by the window"""
import pygame as py
from math import log,exp

class State:
    def __init__(self,row,col):
        self.col = col
        self.row = row
        self.coord = (row,col)              

        self.purpose = None
        self.reward = None
        self.value = None

    def __repr__(self):
        return f'SC@{self.coord}'

    def add_visuals(self,size=None):
        """Method run to add the cell aspects to each state. Mostly to tell them what size they are"""
        py.init()           #check to see if I still need this later
        if size != None:    #needed because I use this function to also resurface the cells
            self.size = size
        self.cell = py.Surface((self.size,self.size)).convert()
        self.cell.fill(self.colour)

    def desurface(self):
        """remove Surface from cell/state so that it can be pickled and saved"""
        self.cell = None

    def assign_purpose(self,role):
        """given a user-inputted role (just another word for purpose) update the state's
        purpose. This will update the state's reward as well."""
        self.purpose = role
        if role == 'wall':
            self.reward = -5
            self.colour = (0,0,0)
        elif role == 'finish':
            self.reward = 100
            self.colour = (0,0,255)
        elif role == 'start':
            self.reward = -1
            self.colour = (255,255,0)
        else:
            self.reward = -1
            self.colour = (0,100,0)
        try:        #because this will run once before add visuals is called
            self.cell.fill(self.colour)
        except:
            pass


    def re_green(self,max,min):
        #rescale so no negatives
        max = max - min + 1
        self.value = self.value - min + 1
        min = 1

        rb = 100*(log(max) - log(self.value))/(log(max) - log(min))
        self.cell.fill((rb,100,rb))

class Q:
    def __init__(self,state,action):
        self.state = state
        self.action = action
        self.elig = 0

        self.value = 0

    def __repr__(self):
        if self.action[0] == 1:
            ud = 'u'
        elif self.action[0] == -1:
            ud = 'd'
        else:
            ud = '0'
        if self.action[1] == 1:
            lr = 'r'
        elif self.action[1] == -1:
            lr = 'l'
        else:
            lr = '0'
        return f'{ud}-{lr}:{self.state}'