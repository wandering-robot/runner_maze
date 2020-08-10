"""Window class will host the program and show all visuals.
These visuals pertain to the drawing of the maze as well as the 
showing of the agent's body completing the maze using q-values"""
from handler import CreateHandler, RunningHandler, ShowingHandler
from ai import AI, Knowledge

import pygame as py
import pickle           #to save an AI's knowledge
from pathlib import Path    #to make a file path to save the knowledge to
import os       #same as pathlib

class Window:
    def __init__(self,main,height,width,cell_size,retain_window=None):  #retain window lets code carryover the old window for displaying so that it doesn't close/reopen
        self.running = True     #false if program terminated

        self.main = main
        self.height = height
        self.width = width
        self.cell_size = cell_size          #all cells will be a square with a sidelength of this value

        self.cell_dict = None       #will be linked to maze state_dict when maze2window called in main
        self.avatar = None        #Not None if in showing mode

        #pygame stuff
        py.init()
        if retain_window == None:
            self.disp_win = py.display.set_mode((self.width,self.height))
        else:
            self.disp_win = retain_window
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
    def __init__(self,main,height,width,cell_size):
        super().__init__(main,height,width,cell_size)

        self.handler = CreateHandler(self)

    def start_drawing(self):
        """method to run the drawing aspect of the program."""
        self.drawing = True
        while self.drawing:
            self.update_screen()
            self.handler.handle() 

    def start_learning(self):
        """method that commences with the AI's learning, showing current results on screen"""
        self.ai = AI(self)
        self.handler = RunningHandler(self)

        while self.running:
            steps = self.ai.run_episode()
            ep_num = self.ai.episode_num
            if ep_num % 20 == 0:
                self.progress_screen(ep_num,steps)
            status = self.handler.handle()
            if status == 'finished':
                for q in self.ai.qs.values():
                    q.state.add_visuals()
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
        """creates a knowledge class to be pickeled"""
        ep_num = self.ai.episode_num
        qs = self.ai.qs
        for q in qs.values():
            state = q.state
            state.desurface()
        knowledge = Knowledge(qs,ep_num)

        #save knowledge to file name_knowledge_number
        if not Path(self.main.maze_name).exists():
            Path(self.main.maze_name).mkdir()
        filename = Path(self.main.maze_name)/ f'{self.main.maze_name}_knowledge_{ep_num}'
        outfile = open(filename,'wb')
        pickle.dump(knowledge,outfile)
        outfile.close()

    def save_maze(self):
        #save maze layout
        if not Path(self.main.maze_name,f'{self.main.maze_name}_maze').exists():
            maze_file = Path(self.main.maze_name,f'{self.main.maze_name}_maze')
            outfile = open(maze_file,'wb')
            pickle.dump(self.main.maze,outfile)
            outfile.close()

class ShowWindow(Window):
    def __init__(self,main,height,width,cell_size,retain_window=None,maze_name=None):
        super().__init__(main,height,width,cell_size,retain_window)

        self.handler = ShowingHandler(self)
        #get maze name
        if maze_name == None:
            self.maze_name = self.get_maze_name()
        else:
            self.maze_name = maze_name
        #load maze layout and resurface all the states
        self.maze = self.load_maze()
        for state in self.maze.state_dict.values(): #resurface all the states
            state.add_visuals()
        #load knowledge iterations and sort them in ascending order
        self.knowledge = self.load_knowledge()
        self.sort_knowledge()


    def load_maze(self):
        """loads the maze object from name_maze file"""
        filename = Path(self.maze_name,f'{self.maze_name}_maze')
        infile = open(filename,'rb')
        maze = pickle.load(infile)
        infile.close()
        return maze

    def load_knowledge(self):
        """returns a list of knowledge"""
        iter_files = [f for f in os.listdir(Path(self.maze_name))]
        for i, f in enumerate(iter_files):
            if not f[-1].isnumeric():         #gets rid of the maze layout file
                del iter_files[i]
        iter_knowledge = []
        for f in iter_files:
            infile = open(Path(self.maze_name) / f,'rb')
            iter_knowledge.append(pickle.load(infile))
            infile.close()
        return iter_knowledge


    def sort_knowledge(self):
        self.knowledge.sort(key= lambda i: i.episode)

    def get_maze_name(self):
        """gets maze name from user and ensures that it exists"""
        while True:
            maze_name = input('Input maze_name to load:\t')
            if Path(maze_name).exists(): 
                break
            else:
                print('Maze not found, please re-input')
        return maze_name
