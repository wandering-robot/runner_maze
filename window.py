"""Window class will host the program and show all visuals.
These visuals pertain to the drawing of the maze as well as the 
showing of the agent's body completing the maze using q-values"""
from handler import CreateHandler
import pygame as py

class Window:
    def __init__(self,height,width,cell_size):
        self.height = height
        self.width = width
        self.cell_size = cell_size          #all cells will be a square with a sidelength of this value

        self.cell_dict = None       #will be linked to maze state_dict when maze2window called in main
        self.avatar = None        #Not None if in showing mode

        #pygame stuff
        py.init()
        self.disp_win = py.display.set_mode((self.width,self.height))
        self.background = py.Surface(self.disp_win.get_size()).convert()
        self.background.fill((255,255,255))

    def update_screen(self):
        self.disp_win.blit(self.background,(0,0))
        for cell in self.cell_dict:
            self.disp_win.blit(cell.cell,self.state2cell(cell.coord))

    @staticmethod
    def state2cell(coord):
        """takes in the states coord and returns the cell's top left coord for blotting"""
        return coord[0] * self.cell_size, coord[1] * self.cell_size

class CreateWindow(Window):
    def __init__(self,height,width,cell_size):
        super().__init__(height,width,cell_size)

        self.handler = CreateHandler(self)
    