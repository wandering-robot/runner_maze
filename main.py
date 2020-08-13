"""Main section of code to run all the functions and methods"""

from window import CreateWindow, ShowWindow
from maze import Maze
from grapher import Grapher
from gui import GUI


import pickle       #for loading old mazes
from pathlib import Path
from shutil import rmtree   #to delete a preexisitng file if user wants to name a new maze by an old name
import sys      #to exit if user 

class Main:
    def __init__(self):
        self.height = 750                    #starting sizes just to give the program an idea of how big we want the screen to be
        self.width = 500
        self.mode = None            #should pass all options and do nothing
        self.gui = GUI(self)

        self.make_storage()

        if self.mode == 'n':

            self.cell_row_num = None                #will be made in self.optomize_sizes, col_num passed from GUI
                               
            self.cell_size = self.calc_cell_size()

            self.optomize_sizes()

            # self.maze_name = self.get_maze_name()
            self.maze = Maze(self.cell_col_num,self.cell_row_num,self.cell_size)
            self.maze.make_state_dict()

            self.grapher = Grapher(self.maze_name)

            #creating section
            self.window = CreateWindow(self,self.height,self.width,self.cell_size)
            self.create_maze()
            self.window.start_drawing() #start drawing here, window called to start learning in handler
            
            if self.window.running:     #allow user to quit here if they want
                self.window.save_maze()
                self.window.start_learning(autosave=self.autosave)

                #showing section
                self.window = ShowWindow(self,self.height,self.width,self.cell_size,retain_window=self.window.disp_win,maze_name=self.maze_name)
                self.window.show()

        elif self.mode == 'd':
            self.maze = self.load_maze()
            self.grapher = Grapher(self.maze_name)
            self.grapher.load_data()

            #make main object have similar attributes in both new and old cases for consistency
            self.cell_size = self.maze.cell_size
            self.cell_col_num = self.maze.col_num
            self.cell_row_num = self.maze.row_num

            self.optomize_sizes()

            self.window = ShowWindow(self,self.height,self.width,self.cell_size,maze_name=self.maze_name)
            self.window.show()
        
        elif self.mode == 'r':
            self.maze = self.load_maze()
            self.grapher = Grapher(self.maze_name)

            #make main object have similar attributes in both new and old cases for consistency
            self.cell_size = self.maze.cell_size
            self.cell_col_num = self.maze.col_num
            self.cell_row_num = self.maze.row_num

            self.optomize_sizes()

            #learning section
            self.window = CreateWindow(self,self.height,self.width,self.cell_size)
            self.window.cell_dict = self.maze.state_dict
            self.window.starting_state_coord = self.get_starting_state()
            self.window.start_learning(autosave=self.autosave)

            #showing section
            try:            #allow user to quit while learning
                self.window = ShowWindow(self,self.height,self.width,self.cell_size,retain_window=self.window.disp_win,maze_name=self.maze_name)
                self.window.show()
            except:
                pass

    def get_starting_state(self):
        """iterates throug all states to determine which one is the starting state"""
        for state in self.maze.state_dict.values():
            if state.purpose == 'start':
                return state.coord

    def get_maze_name(self):
        """gets name from user, if already been used, has user delete old file"""
        while True:
            maze_name = input('Please name the maze:\t')
            if Path('storage',maze_name).exists():
                valid = False
                while not valid:
                    delete = input("Maze already exists. Overwrite? y/n:\t").lower()
                    valid = (delete =='y' or delete == 'n')
                    if not valid:
                        print('Error, expecting y or n\n')
                if delete == 'y':
                    rmtree(Path('storage',maze_name), ignore_errors=True)
                    break
            else:
                break
        return maze_name

    def load_maze(self):
        """loads the maze object from name_maze file, saves name as self.maze_name"""
        while True:
            try:
                filename = Path('storage',self.maze_name,f'{self.maze_name}_maze')
                infile = open(filename,'rb')
                maze = pickle.load(infile)
                infile.close()
                break
            except:
                print('File not found, please re-input:\t')
        return maze

    def create_maze(self):
        """This method will be the main one run when in creative mode. Called when new = True"""
        self.maze2window()

    def maze2window(self):
        """Assigns the maze's state_dict variable to the window for purpose changing and blotting. 
        Also enables cell aspects of a state"""
        self.window.cell_dict = self.maze.state_dict
        for state in self.window.cell_dict.values():
            state.add_visuals(self.cell_size)

    def optomize_sizes(self):
        """Use col_num to figure out how closely the contents can fill the screen, determines
        cell_size in the process. Then adjust the screen height and width so it fits snugly"""
        #optomize the width aspects
        if self.width % self.cell_col_num != 0:
            self.width = self.cell_col_num * self.cell_size
        
        #extra step to figure out how many cells could even fit vertically
        self.cell_row_num = self.height // self.cell_size   
        
        #optomize the height aspects
        self.height = self.cell_row_num * self.cell_size


    def calc_cell_size(self):
        """returns how many cells could fit in the screen given the width and col_num"""
        return self.width // self.cell_col_num        

    def make_storage(self):
        if not Path('storage').exists():
            Path('storage').mkdir()

if __name__ == "__main__":
    Main()
    