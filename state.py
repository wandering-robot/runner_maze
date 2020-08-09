"""States and cells are interchangeable, makes sense to think of them as a bunch of 1x1 squares of a
checkerboard. They will be rescaled as necessary by the window"""
import pygame as py

class State:
    def __init__(self,row,col):
        self.col = col
        self.row = row
        self.coord = (row,col)              #state coord is row,col 

        self.purpose = None
        self.reward = None


    def add_visuals(self,size):
        """Method run to add the cell aspects to each state. Mostly to tell them what size they are"""
        py.init()           #check to see if I still need this later
        self.size = size
        self.cell = py.Surface((self.size,self.size)).convert()


    def asssign_purpose(self,role):
        """given a user-inputted role (just another word for purpose) update the state's
        purpose. This will update the state's reward as well."""
        self.purpose = role
        if role == 'wall':
            self.reward = -5
            self.colour = (0,0,0)
        elif role == 'end':
            self.reward = 5
            self.colour = (255,0,0)
        else:
            self.reward = -1
            self.colour = (0,0,100)