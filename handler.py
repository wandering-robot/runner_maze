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
        """clicking the mouse allows you to draw or delete blocks, pressing s or f create start
        and finishing blocks respectively, and pressing enter makes the program stop drawing and 
        start learning"""
        for event in py.event.get():    
            if event.type == py.QUIT:
                self.stop_running()
            elif event.type == py.MOUSEBUTTONDOWN:
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
                elif event.key == py.K_RETURN:      #STOP DRAWING AND START LEARNING
                    if self.made_start and self.made_finish:    #ensure start and finish are made
                        # self.window.start_learning()
                        self.window.drawing = False

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
        self.made_start = True
        self.window.starting_state_coord = self.cell2state(pos)

    def make_finish(self):
        """create the finish line for the maze runner from the mouse position"""
        pos = py.mouse.get_pos()
        self.change_cell(pos,'finish')
        self.made_finish = True

class RunningHandler(Handler):
    """handler for the learning portion of the program."""
    def __init__(self,window):
        super().__init__(window)

    def handle(self):
        """S saves the knowledge, return stops learning. Will return 'finished' if user decideds that it is smart enough"""
        for event in py.event.get():    
            if event.type == py.QUIT:
                self.window.running = False
                py.quit()
                break
            elif event.type == py.KEYDOWN:
                if event.key == py.K_s:
                    self.window.save_knowledge()
                if event.key == py.K_RETURN:
                    return 'finished'