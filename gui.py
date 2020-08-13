from tkinter import *
from pathlib import Path
import os

class Page(Frame):
    def __init__(self,*args,**kwargs):
        Frame.__init__(self,*args,**kwargs)

    def show(self):
        """makes visible"""
        self.place(x=0, y=0)
        self.lift()

    def hide(self):
        """makes invisible"""
        self.place(x=500,y=500)

class MainPage(Page):
    def __init__(self,gui,*args,**kwargs):
        Page.__init__(self,*args,**kwargs)

        self.gui = gui
        main_label1 = Label(self,text='Please select program mode')
        main_label1.grid(row=0, column=1, sticky=W, columnspan=2)

        #make Radio Buttons
        MODES = [
        ("New", "n"),
        ("Re-train", "r"),
        ("Display", "d"),
        ]

        self.var = StringVar()
        self.var.set('n')
        i=1
        for text, mode in MODES:
            b = Radiobutton(self, text=text,variable=self.var, value=mode, command= lambda: self.describe(self.var.get()), justify=LEFT,anchor='nw')
            b.grid(sticky=W, row=i, column=0,padx=20)
            i += 1

        #make initial text block
        self.describe(self.var.get())

        #make continue Button
        cont = Button(self, text='Continue', command= lambda:self.gui.show_page(self.var.get()))
        cont.grid(row=4, column=2)

    def describe(self,mode):
        if mode == 'n':
            func_text = 'Create a new maze, and train a new AI to solve  it.'
        elif mode == 'r':
            func_text = 'Load an old maze from memory, and train a new AI to solve it.'
        elif mode == 'd':
            func_text = 'Load an old maze from memory, and display the old AI\'s solution to it.'
        textbox = Text(self, height=6, width=25, wrap=WORD)
        textbox.insert('1.0',func_text)
        textbox.grid(sticky=W, row=1, column=2,rowspan=3)

class NewPage(Page):
    def __init__(self,gui,*args,**kwargs):
        Page.__init__(self,*args,**kwargs)

        self.gui = gui
        self.checked_name = False       #make sure can't go without a name

        #lable next to name entry
        new_label2 = Label(self,text='Maze Name:')      #had label1 but deleted it
        new_label2.grid(row=1,column=0)
        #button to check name availability
        name_button = Button(self, text='Check Name', command=self.display_availability)
        name_button.grid(row=1, column=2)
        #name entry
        name = StringVar()
        name.set('')
        self.display_availability(name.get())
        self.new_name_entry = Entry(self, width=25, textvariable=name)
        self.new_name_entry.grid(row=1, column=1)
        #button to return to main screen
        main_button = Button(self,text='Back',command= lambda: self.gui.show_page('m'))
        main_button.grid(row=8, column=0)
        #label next to resolution slider
        new_label3 = Label(self, text='Maze Resolution')
        new_label3.grid(row=5,column=0)
        #label under resolution slider
        new_label4 = Label(self, text='*High Resolution = Long Solving Time*', justify=CENTER)
        new_label4.grid(row=6,column=1)
        #extra space label
        new_label5 = Label(self, text=' ', justify=CENTER)
        new_label5.grid(row=7,column=1)

        #resolution slider
        self.slider = Scale(self, orient=HORIZONTAL, from_=3, to=12, length=125)            #set col num from 3 to 12
        self.slider.grid(row=5, column=1)
        #start button
        start_button = Button(self,text='Start!',command=self.start_new_simulation)
        start_button.grid(row=8,column=2)

    def display_availability(self,name=None):
        """called when name button pressed to inform user if name has been used already"""
        if name == None:
            name = self.new_name_entry.get()        #so that can be called at beginning to space things out
        if not name == '':
            self.checked_name = True
            if Path('storage',name).exists():
                avail_label = Label(self, text=f'     Name {name} is taken.     ', justify=CENTER)
                avail_label2 = Label(self, text=f'This will overwrite old file.', justify=CENTER)
            else:
                avail_label = Label(self, text=f'Name {name} is available', justify=CENTER)
                avail_label2 = Label(self, text=f'                                              ')
        else:
            avail_label = Label(self, text=f'')
            avail_label2 = Label(self, text=f'')

        avail_label.grid(row=2, column=1)
        avail_label2.grid(row=3, column=1)
        avail_label3 = Label(self, text=f'')
        avail_label3.grid(row=4, column=1)

    def start_new_simulation(self):
        "start a new simlation"
        self.name = self.new_name_entry.get()
        self.col_num = self.slider.get()

        if self.name != '' and self.checked_name:
            print(f'start {self.name} with col num {self.col_num}')
        else:
            label6 = Label(self, text='Enter and Check Name', justify=CENTER)
            label6.grid(row=9, column=1)

class RetrainPage(Page):
    def __init__(self,gui,*args,**kwargs):
        Page.__init__(self,*args,**kwargs)

        self.gui = gui
        #top label
        train_label1 = Label(self,text='Available Mazes',anchor='s')
        train_label1.grid(row=2, column=1)
        #label next to selector
        train_label2 = Label(self,text='Choose a Map')
        train_label2.grid(row = 3, column=0,padx=50)
        #maze_selector
        scroller = Scrollbar(self)
        self.selector = Listbox(self, height=5, selectmode=SINGLE, yscrollcommand=scroller)
        self.selector.grid(row=3, column=1)
        self.get_options(self.selector)
        #start button
        start_button = Button(self,text='Start!',command=self.start_retrain_simulation,)
        start_button.grid(row=5,column=2,pady=50)
        #warning label
        self.warning()
        #autosave number getter
        autosave1_label = Label(self,text='Record progress every').grid(row=0,column=0)
        autosave2_lable = Label(self,text='episodes').grid(row=0, column=2)
        self.spinner = Spinbox(self,from_=100,to=10000,textvariable=150)
        self.spinner.grid(row=0,column=1,pady=20)

        #return to main button
        main_button = Button(self,text='Back',command= lambda: self.gui.show_page('m'))
        main_button.grid(row=5, column=0)

    def get_options(self,selector):
        """fill the selector with all the saved mazes available"""
        i=1
        for root, dirs, files in os.walk('storage'):
            for name in dirs:
                selector.insert(i,name)

    def warning(self,warn=False):
        """make the label that tells user they need to select a name"""
        if not warn:
            warn_label = Label(self,text='                   ')
        else:
            warn_label = Label(self,text='Must Select a Maze')
        warn_label.grid(row=4,column=1)

    def start_retrain_simulation(self):
        """tries to start the simulation"""
        try:
            self.name = self.selector.get(self.selector.curselection())
            self.save_freq = self.spinner.get()
            print(self.name,self.save_freq)
        except:
            self.warning(warn=True)

class DisplayPage(Page):
    def __init__(self,gui,*args,**kwargs):
        Page.__init__(self,*args,**kwargs)

        self.gui = gui
        #top label
        train_label1 = Label(self,text='Available Mazes',anchor='s')
        train_label1.grid(row=2, column=1)
        #label next to selector
        train_label2 = Label(self,text='Choose a Map')
        train_label2.grid(row = 3, column=0,padx=50)
        #maze_selector
        scroller = Scrollbar(self)
        self.selector = Listbox(self, height=5, selectmode=SINGLE, yscrollcommand=scroller)
        self.selector.grid(row=3, column=1)
        self.get_options(self.selector)
        #start button
        start_button = Button(self,text='Start!',command=self.start_retrain_simulation,)
        start_button.grid(row=5,column=2,pady=50)
        #warning label
        self.warning()

        #return to main button
        main_button = Button(self,text='Back',command= lambda: self.gui.show_page('m'))
        main_button.grid(row=5, column=0)

    def get_options(self,selector):
        """fill the selector with all the saved mazes available"""
        i=1
        for root, dirs, files in os.walk('storage'):
            for name in dirs:
                selector.insert(i,name)

    def warning(self,warn=False):
        """make the label that tells user they need to select a name"""
        if not warn:
            warn_label = Label(self,text='                   ')
        else:
            warn_label = Label(self,text='Must Select a Maze')
        warn_label.grid(row=4,column=1)

    def start_retrain_simulation(self):
        """tries to start the simulation"""
        try:
            self.name = self.selector.get(self.selector.curselection())
            print(self.name)
        except:
            self.warning(warn=True)


class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title('Ai_Simulator')
        #self.root.iconbitmap(path to icon)
        self.root.geometry('400x350') 
        self.root.resizable(False,False)

        self.main = MainPage(self, padx=35, pady=100)
        self.new = NewPage(self, padx=10, pady=75)
        self.retrain = RetrainPage(self, padx=5, pady=50)
        self.display = DisplayPage(self, padx=5, pady=75)

        self.new.place(x=0, y=0)
        self.retrain.place(x=0, y=0)
        self.display.place(x=0, y=0)
        self.main.place(x=0, y=0)

        self.pages = [self.main, self.new, self.retrain, self.display]

        self.hide_pages()
        self.main.show()

        self.root.mainloop()

    def show_page(self,var):
        """moves all the pages out of view, then unhides the one we want"""
        self.hide_pages()
        if var == 'n':
            self.new.show()
        elif var == 'm':
            self.main.show()
        elif var == 'r':
            self.retrain.show()
        elif var == 'd':
            self.display.show()

    def hide_pages(self):
        """moves all the pages out of view"""
        for page in self.pages:
            page.hide()

if __name__ == '__main__':
    gui = GUI()
