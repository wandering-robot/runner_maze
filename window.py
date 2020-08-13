"""Window class will host the program and show all visuals.
These visuals pertain to the drawing of the maze as well as the 
showing of the agent's body completing the maze using q-values"""
from handler import CreateHandler, RunningHandler, ShowingHandler
from ai import AI, Knowledge, Runner

import pygame as py
import pickle           #to save an AI's knowledge
from pathlib import Path    #to make a file path to save the knowledge to
import os       #same as pathlib
from time import sleep #to slow down the showing window   


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

    def update_screen(self):
        """blits all the cells and the ai' avatar onto disp_win"""
        #blit the background
        self.disp_win.blit(self.background,(0,0))
        #blit all the cells
        for cell in self.cell_dict.values():
            pixel = self.state2cell(cell.coord) #top left pixel
            self.disp_win.blit(cell.cell,pixel)
        #blit the AI's avatar (if there is one, won't be in drawing mode)
        if self.avatar != None:                                                 
            pixel = self.state2cell(self.avatar.pos)
            self.disp_win.blit(self.avatar.body,pixel)
        py.display.flip()

    def state2cell(self,coord):
        """takes in the states coord and returns the cell's top left coord for blotting"""
        return coord[1] * self.cell_size, coord[0] * self.cell_size

    #starting state set in this method
    def resurface_states(self,state_dict):
        """resurfaces all the states in a dictionary, also ascribes starting state to self"""
        for state in state_dict:
            state.add_visuals()
            if state.purpose == 'start':
                self.starting_state = state
                self.starting_state_coord = state.coord

class CreateWindow(Window):
    def __init__(self,main,height,width,cell_size):
        super().__init__(main,height,width,cell_size)
        py.font.init()
        self.myfont = py.font.SysFont('Comic Sans MS',30)
        self.small_font = py.font.SysFont('Comic Sans MS',15)
        self.handler = CreateHandler(self)

    def start_drawing(self):
        """method to run the drawing aspect of the program."""
        self.running = True
        while self.running:
            try:
                self.update_screen()
                self.handler.handle() 
            except Exception as error:
                print(error)

    def start_learning(self,autosave=None):
        """method that commences with the AI's learning, showing current results on screen"""
        self.ai = AI(self)
        self.handler = RunningHandler(self)
        self.delete_old_knowledge()             #clear out old pickeld knowledge 
        while self.running:
            steps = self.ai.run_episode()
            ep_num = self.ai.episode_num
            self.main.grapher.add_data_point((ep_num,steps))     #save data to graph later
            if ep_num % 20 == 0:
                self.progress_screen(ep_num,steps)
            status = self.handler.handle()
            if autosave != None:
                if ep_num % autosave == 0:
                    self.save_knowledge()
            if status == 'finished':
                for q in self.ai.qs.values():
                    q.state.add_visuals()
                break

    def delete_old_knowledge(self):
        """called by start_learning to empty knowledge memory if any exists"""
        iter_files = [f for f in os.listdir(Path('storage',self.main.maze_name))]
        to_delete = []
        for f in iter_files:
            if f[-1].isnumeric():         #gets rid of knowledge files
                to_delete.append(f)
        for f in to_delete:
            os.remove(Path('storage',self.main.maze_name,f))

    def progress_screen(self,ep_num,steps):
        """displays the AI's learning progress"""
        self.disp_win.blit(self.background,(0,0))
        title1 = f'Episode #{ep_num}'
        title2 = f'took {steps} steps'
        title3 = '(press enter when you want to stop learning)'
        text1_surface = self.myfont.render(title1,False,(0,0,0))
        text2_surface = self.myfont.render(title2,False,(0,0,0))
        text3_surface = self.small_font.render(title3,False,(0,0,0))

        self.disp_win.blit(text1_surface,(self.width/4,self.height/3))
        self.disp_win.blit(text2_surface,(self.width/4,self.height/3 + 30))
        self.disp_win.blit(text3_surface,(self.width/6,2*self.height/3 + 30))

        py.display.flip()

    def save_knowledge(self):
        """creates a knowledge class to be pickeled"""
        ep_num = self.ai.episode_num
        qs = self.ai.qs

        knowledge = Knowledge(qs,ep_num)

        #save knowledge to file name_knowledge_number
        if not Path('storage',self.main.maze_name).exists():
            Path('storage',self.main.maze_name).mkdir()
        filename = Path('storage',self.main.maze_name)/ f'{self.main.maze_name}_knowledge_{ep_num}'
        outfile = open(filename,'wb')
        pickle.dump(knowledge,outfile)
        outfile.close()

    def save_maze(self):
        """save maze layout"""
        #make file if haven't yet
        if not Path('storage',self.main.maze_name).exists():
            Path('storage',self.main.maze_name).mkdir()
        #desurface all cells for 'storage'
        for state in self.cell_dict.values():
            state.desurface()
        #save maze object
        if not Path('storage',self.main.maze_name,f'{self.main.maze_name}_maze').exists():
            maze_file = Path('storage',self.main.maze_name,f'{self.main.maze_name}_maze')
            outfile = open(maze_file,'wb')
            pickle.dump(self.main.maze,outfile)
            outfile.close()

class ShowWindow(Window):
    def __init__(self,main,height,width,cell_size,retain_window=None,maze_name=None):
        super().__init__(main,height,width,cell_size,retain_window)

        #run the graph alongside the episode display
        self.main.grapher.save_data()
        self.main.grapher.display_data()

        py.font.init()
        self.myfont = py.font.SysFont('Comic Sans MS',20)

        #get maze and name
        if maze_name == None:
            self.maze_name = self.get_maze_name()
            self.maze = self.load_maze()
        else:
            self.maze_name = maze_name
            self.maze = self.main.maze

        self.cell_dict = self.maze.state_dict
        self.starting_state = None
        self.resurface_states(self.maze.state_dict.values())

        #load knowledge iterations and sort them in ascending order
        self.knowledge = self.load_knowledge()

        self.handler = ShowingHandler(self)
        self.avatar = Runner(self)

    def show(self):
        self.wait_time = 0.25
        while self.running:
            try:
                self.update_screen()
                self.blit_episode_num()
                self.avatar.move()
                self.handler.handle()       #so that doesn't error out if completed
            except:
                pass
            sleep(self.wait_time)

    def blit_episode_num(self):
        """method to add the episode number on the top right corner of screen"""
        text = f'Episode #{self.avatar.knowledge.episode}'
        text_surface = self.myfont.render(text,False,(0,0,0),(255,255,255))
        self.disp_win.blit(text_surface,(4*self.width/5 - 45,15))
        py.display.flip()

    def load_maze(self):
        """loads the maze object from name_maze file"""
        filename = Path('storage',self.maze_name,f'{self.maze_name}_maze')
        infile = open(filename,'rb')
        maze = pickle.load(infile)
        infile.close()
        return maze

    def load_knowledge(self):
        """returns a list of knowledge"""
        iter_files = [f for f in os.listdir(Path('storage',self.maze_name))]
        to_delete = []
        for f in iter_files:
            if not f[-1].isnumeric():         #gets rid of non-knowledge files
                to_delete.append(f)
        for f in to_delete:
            iter_files.remove(f)
        iter_knowledge = []
        for f in iter_files:
            infile = open(Path('storage',self.maze_name) / f,'rb')
            iter_knowledge.append(pickle.load(infile))
            infile.close()
        iter_knowledge.sort(key= lambda i: i.episode)
 
        return iter_knowledge

    def get_maze_name(self):
        """gets maze name from user and ensures that it exists"""
        while True:
            maze_name = input('Input maze_name to load:\t')
            if Path('storage',maze_name).exists(): 
                break
            else:
                print('Maze not found, please re-input')
        return maze_name


