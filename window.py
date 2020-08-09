"""Window class will host the program and show all visuals.
These visuals pertain to the drawing of the maze as well as the 
showing of the agent's body completing the maze using q-values"""
from handler import CreateHandler, RunningHandler
import pygame as py
from ai import AI

class Window:
    def __init__(self,height,width,cell_size):
        self.running = True     #false if program terminated

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
        py.font.init()
        self.myfont = py.font.SysFont('Comic Sans MS',30)

    def update_screen(self):
        """blits all the cells and the ai' avatar onto disp_win"""
        #blit the background
        self.disp_win.blit(self.background,(0,0))
        #blit all the cells
        for cell in self.cell_dict.values():
            pixel = self.state2cell(cell.coord) #top left pixel
            self.disp_win.blit(cell.cell,pixel)
        #blit the AI's avatar (if there is one, won't be in drawing mode)
        if self.avatar != None:                                                 #ToDo: Create avatar that follows these specs
            pixel = self.state2cell(self.avatar.coord)
            self.disp_win.blit(avatar.body,pixel)
        py.display.flip()

    def state2cell(self,coord):
        """takes in the states coord and returns the cell's top left coord for blotting"""
        return coord[0] * self.cell_size, coord[1] * self.cell_size

class CreateWindow(Window):
    def __init__(self,height,width,cell_size):
        super().__init__(height,width,cell_size)

        self.handler = CreateHandler(self)

    def start_drawing(self):
        """method to run the drawing aspect of the program."""
        while self.running:
            self.update_screen()
            self.handler.handle()

    def start_learning(self):
        """method that commences with the AI's learning, showing current results on screen"""
        ai = AI(self)
        self.handler = RunningHandler(self)

        i = 0
        while self.running:
            steps = ai.run_episode()
            i += 1
            if i % 20 == 0:
                self.progress_screen(i,steps)
            status = self.handler.handle()
            if status == 'finished':
                break

    def progress_screen(self,ep_num,steps):
        """displays the AI's learning progress"""
        self.disp_win.blit(self.background,(0,0))
        title1 = f'Episode #{ep_num}'
        title2 = f'took {steps} steps'
        text1_surface = self.myfont.render(title1,False,(0,0,0))
        text2_surface = self.myfont.render(title2,False,(0,0,0))
        self.disp_win.blit(text1_surface,(self.width/4,self.height/3))
        self.disp_win.blit(text2_surface,(self.width/4,self.height/3 + 30))
        py.display.flip()

    def save_knowledge(self):
        pass