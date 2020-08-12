from tkinter import *

class Page(Frame):
    def __init__(self,*args,**kwargs):
        Frame.__init__(self,*args,**kwargs)

    def show(self):
        self.place(x=0, y=0)
        self.lift()

    def hide(self):
        self.place(x=500,y=500)

class MainPage(Page):
    def __init__(self,gui,*args,**kwargs):
        Page.__init__(self,*args,**kwargs)

        self.gui = gui
        main_label1 = Label(self,text='Main Page')
        main_label1.grid(row=0, column=1)

        #make Radio Buttons
        MODES = [
        ("New", "n"),
        ("Retrain", "r"),
        ("Display", "d"),
        ]

        self.var = StringVar()
        self.var.set('n')
        i=1
        for text, mode in MODES:
            b = Radiobutton(self, text=text,variable=self.var, value=mode, command= lambda: self.describe(self.var.get()), justify=LEFT,anchor='nw')
            b.grid(sticky=W, row=i, column=0)
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
        main_label1 = Label(self,text='New Page')
        main_label1.grid(row=0, column=0)

        main_button = Button(self,text='Main',command= lambda: self.gui.show_page('m'))
        main_button.grid(row=1, column=0)

class RetrainPage(Page):
    def __init__(self,gui,*args,**kwargs):
        Page.__init__(self,*args,**kwargs)

        self.gui = gui
        main_label1 = Label(self,text='Retrain Page')
        main_label1.grid(row=0, column=0)

        main_button = Button(self,text='Main',command= lambda: self.gui.show_page('m'))
        main_button.grid(row=1, column=0)


class DisplayPage(Page):
    def __init__(self,gui,*args,**kwargs):
        Page.__init__(self,*args,**kwargs)

        self.gui = gui
        main_label1 = Label(self,text='Display Page')
        main_label1.grid(row=0, column=0)

        main_button = Button(self,text='Main',command= lambda: self.gui.show_page('m'))
        main_button.grid(row=1, column=0)


class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title('Ai_Simulator')
        #self.root.iconbitmap(path to icon)
        self.root.geometry('400x350') 

        self.main = MainPage(self, padx=50, pady=100)
        self.new = NewPage(self, padx=125, pady=125)
        self.retrain = RetrainPage(self, padx=125, pady=125)
        self.display = DisplayPage(self, padx=125, pady=125)

        self.new.place(x=0, y=0)
        self.retrain.place(x=0, y=0)
        self.display.place(x=0, y=0)
        self.main.place(x=0, y=0)

        self.pages = [self.main, self.new, self.retrain, self.display]

        self.hide_pages()
        self.main.show()

        self.root.mainloop()

    def show_page(self,var):
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
        for page in self.pages:
            page.hide()

if __name__ == '__main__':
    gui = GUI()
