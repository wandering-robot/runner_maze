"""the dictionary of cells/states that, depending on their purpose, will be coloured differently.
because cells and states are interchangealbe, they will also contain the reward value for
moving onto a cell/state of that type"""

from state import State

class Maze:
    def __init__(self,col_num,row_num,cell_size):
        self.col_num = col_num
        self.row_num = row_num
        self.cell_size = cell_size

        self.state_dict = None

    def make_state_dict(self):
        """create empty state dictionary to allow all states to be accessed by their coord tup"""
        self.state_dict = {}
        for row in range(self.row_num):
            for col in range(self.col_num):
                s = State(row,col)
                self.state_dict[(row,col)] = s
                s.assign_purpose(None)

        