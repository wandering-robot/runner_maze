import matplotlib.pyplot as plt
from pathlib import Path
from multiprocessing import Process
import pickle

class Grapher:
    """graphing object that is tied to the parent class window"""
    def __init__(self,main):
        self.main = main
        self.maze_name = self.main.maze_name
        self.info_str = f'{self.maze_name}_A{str(self.main.alpha)[2:]}_G{str(self.main.gamma)[2:]}_E{str(self.main.epsilon)[2:]}_L{str(self.main.lamda)[2:]}_Eq{self.main.E_eq}'

        self.domain = []
        self.range = []

    def add_data_point(self,data_tup):
        """adds a data point (in tuple form) to dataset"""
        self.domain.append(data_tup[0])
        self.range.append(data_tup[1])

    def save_data(self):
        path = Path('storage',self.maze_name) / f'{self.info_str}_graph'

        plt.title(self.info_str)
        plt.plot(self.domain,self.range)
        plt.ylabel('Steps taken')
        plt.xlabel('Episode Number')
        plt.savefig(path)

        if not Path('storage',self.maze_name).exists():
            Path('storage',self.maze_name).mkdir()
        filename = Path('storage',self.maze_name)/ f'{self.maze_name}_raw_data'
        outfile = open(filename,'wb')
        data = (self.domain,self.range)
        pickle.dump(data,outfile)
        outfile.close()

    def load_data(self):
        filename = Path('storage',self.maze_name)/ f'{self.maze_name}_raw_data'
        infile = open(filename,'rb')
        data = pickle.load(infile)
        self.domain, self.range = data
        infile.close()

    def _display_data(self):
        plt.plot(self.domain,self.range)
        plt.ylabel('Steps taken')
        plt.xlabel('Episode Number')
        plt.suptitle(f'Maze: {self.maze_name}')
        plt.show()

    def display_data(self):
        pass
        # self.x = Process(target=self._display_data,daemon=True)
        # self.x.start()

    def data_terminate(self):
        pass
        # self.x.join()