"""Each window will have their own event handler. The event's/actions they do/take
depend on if the program is creating or showing"""

class Handler:
    def __init__(self,window):
        self.window = window
        self.cell_size = window.cell_size

        #shutting down the program
    def stop_running(self):
        py.quit()
    
    @staticmethod
    def cell2state(pos):
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

    #create a wall to block the maze runner from the mouse position
    def create_wall(self):
        pos = py.mouse.get_pos()
        try:
            a = 'wall'                   ###ToDo: determine how to change walls
        except:
            pass

    #delete a wall from the mouse position
    def delete_wall(self):
        pos = py.mouse.get_pos()
        try:
            a = None                   ###ToDo: determine how to change walls
        except:
            pass

    #create the starting point for the maze runner from the mouse position
    def make_start(self):
        pos = py.mouse.get_pos()
        try:
            a = 'start'                   ###ToDo: determine how to change walls
            self.made_start = True
        except:
            pass

    #create the finish line for the maze runner from the mouse position
    def make_finish(self):
        pos = py.mouse.get_pos()
        try:
            a = 'finish'                   ###ToDo: determine how to change walls
            self.made_finish = True
        except:
            pass