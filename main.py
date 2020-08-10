"""Main section of code to run all the functions and methods"""

from window import CreateWindow, ShowWindow
from maze import Maze

import pickle       #for loading old mazes
from pathlib import Path
from shutil import rmtree   #to delete a preexisitng file if user wants to name a new maze by an old name
import sys      #to exit if user 

class Main:
    def __init__(self,new=True,autosave=None):
        self.height = 750                    #starting sizes just to give the program an idea of how big we want the screen to be
        self.width = 500
        self.autosave = autosave        #so that can automatically save if i want   

        if new:
            self.cell_col_num = 4                  #number of cells that will span the width of the window
            self.cell_row_num = None                #will be made in self.optomize_sizes
                               
            self.cell_size = self.calc_cell_size()

            self.optomize_sizes()

            self.maze_name = self.get_maze_name()
            self.maze = Maze(self.cell_col_num,self.cell_row_num,self.cell_size)
            self.maze.make_state_dict()

            #creating section
            self.window = CreateWindow(self,self.height,self.width,self.cell_size)
            self.create_maze()
            self.window.start_drawing() #start drawing here, window called to start learning in handler
            self.window.start_learning(autosave=autosave)

            #showing section
            self.window = ShowWindow(self,self.height,self.width,self.cell_size,retain_window=self.window.disp_win,maze_name=self.maze_name)
            self.window.show()
        else:
            self.maze = self.load_maze()
            #make main object have similar attributes in both new and old cases for consistency
            self.cell_size = self.maze.cell_size
            self.cell_col_num = self.maze.col_num
            self.cell_row_num = self.maze.row_num

            self.optomize_sizes()

            self.window = ShowWindow(self,self.height,self.width,self.cell_size,maze_name=self.maze_name)
            self.window.show()

    def get_maze_name(self):
        """gets name from user, if already been used, has user delete old file"""
        while True:
            maze_name = input('Please name the maze:\t')
            if Path(maze_name).exists():
                valid = False
                while not valid:
                    delete = input("Maze already exists. Overwrite? y/n:\t").lower()
                    valid = (delete =='y' or delete == 'n')
                    if not valid:
                        print('Error, expecting y or n\n')
                if delete == 'y':
                    rmtree(Path(maze_name), ignore_errors=True)
                    break
            else:
                break
        return maze_name

    def load_maze(self):
        """loads the maze object from name_maze file"""
        while True:
            self.maze_name = input('Please name the maze:\t')  
            try:
                filename = Path(self.maze_name,f'{self.maze_name}_maze')
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
        if self.height % self.cell_row_num != 0:
            self.height = self.cell_row_num * self.cell_size


    def calc_cell_size(self):
        """returns how many cells could fit in the screen given the width and col_num"""
        return self.width // self.cell_col_num        


if __name__ == "__main__":
    user = input('[N]ew file or [L]oad?\t').lower()
    status = not user == 'l'
    main = Main(new=status,autosave=100)

