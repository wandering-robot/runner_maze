"""Main section of code to run all the functions and methods"""

from window import CreateWindow
from maze import Maze

class Main:
    def __init__(self,new=True):
        if new:
            self.cell_col_num = 5                  #number of cells that will span the width of the window
            self.cell_row_num = None                #will be made in self.optomize_sizes
            
            self.height = 750                    #starting sizes just to give the program an idea of how big we want the screen to be
            self.width = 500                      
            self.cell_size = self.calc_cell_size()

            self.optomize_sizes()

            self.maze = Maze(self.cell_col_num,self.cell_row_num)
            self.maze.make_state_dict()

            self.window = CreateWindow(self.height,self.width,self.cell_size)

            self.create_maze()
        else:
            #ToDo: Need to load a pre-exisiting maze with sizes
            raise Exception('Not capable of loading pre-built mazes yet')

        #run the program
        self.window.run()

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
    main = Main()
