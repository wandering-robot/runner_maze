"""Each window will have their own event handler. The event's/actions they do/take
depend on if the program is creating or showing"""

import pygame as py

class Handler:
    def __init__(self,window):
        self.window = window
        self.cell_size = window.cell_size

        #shutting down the program
    def stop_running(self):
        self.window.running = False
        py.quit()
    
    def cell2state(self,pos):
        """Converts the mouse pos to the appropriate state"""
        return pos[0]//self.cell_size, pos[1]//self.cell_size

class CreateHandler(Handler):
    def __init__(self,window):
        super().__init__(window)
        #so that can move mouse around and continously draw, not constantly clicking
        self.wall_maker_mode = False
        self.wall_delete_mode = False

        #used to check that a start and finish have been drawn
        self.made_start = False
        self.made_finish = False

    def handle(self):
        for event in py.event.get():    
            if event.type == py.QUIT:
                if self.made_start and self.made_finish:    #ensure start and finish are made
                    self.stop_running()
                else:
                    print("Error: Must have a start and finish")
            elif event.type == py.MOUSEBUTTONDOWN:
                print(self.cell2state(py.mouse.get_pos()))
                if event.button == 1:
                    self.wall_maker_mode = True
                elif event.button == 3:
                    self.wall_delete_mode = True
            elif event.type == py.MOUSEBUTTONUP:
                if event.button == 1:
                    self.wall_maker_mode = False
                elif event.button == 3:
                    self.wall_delete_mode = False
            elif event.type == py.KEYDOWN:
                if event.key == py.K_s:
                    self.make_start()
                elif event.key == py.K_f:
                    self.make_finish()
        if self.wall_maker_mode:
            self.create_wall()
        elif self.wall_delete_mode:
            self.delete_wall()

    def change_cell(self,pos,purpose):
        """main method to change a cell's purpose"""
        coord = self.cell2state(pos)
        try:
            self.window.cell_dict[coord].assign_purpose(purpose)                
        except:
            pass

    def create_wall(self):
        """create a wall to block the maze runner from the mouse position"""
        pos = py.mouse.get_pos()
        self.change_cell(pos,'wall')

    def delete_wall(self):
        """delete a wall from the mouse position"""
        pos = py.mouse.get_pos()
        self.change_cell(pos,None)

    def make_start(self):
        """create the starting point for the maze runner from the mouse position"""
        pos = py.mouse.get_pos()
        self.change_cell(pos,'start')

    def make_finish(self):
        """create the finish line for the maze runner from the mouse position"""
        pos = py.mouse.get_pos()
        self.change_cell(pos,'finish')
