from tkinter import *
import tkinter as tk

class Page(Frame):
    def __init__(self,*args,**kwargs):
        Frame.__init__(self,*args,**kwargs)

    def show(self):
        self.lift()

class MainPage(Page):
    def __init__(self,gui,*args,**kwargs):
        Page.__init__(self,*args,**kwargs)

        self.gui = gui
        main_label1 = Label(self,text='Main Page')
        main_label1.grid(row=0, column=1)

        new_button = Button(self,text='New',command= lambda: self.gui.show_page('n'))
        new_button.grid(row=1, column=0)

        new_button = Button(self,text='Retrain',command= lambda: self.gui.show_page('r'))
        new_button.grid(row=1, column=1)

        new_button = Button(self,text='Display',command= lambda: self.gui.show_page('d'))
        new_button.grid(row=1, column=2)

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

        self.main = MainPage(self, padx=125, pady=125)
        self.new = NewPage(self, padx=125, pady=125)
        self.retrain = RetrainPage(self, padx=125, pady=125)
        self.display = DisplayPage(self, padx=125, pady=125)

        self.new.place(x=0, y=0)
        self.retrain.place(x=0, y=0)
        self.display.place(x=0, y=0)
        self.main.place(x=0, y=0)


        self.main.show()

        self.root.mainloop()

    def show_page(self,var):
        if var == 'n':
            self.new.show()
        elif var == 'm':
            self.main.show()
        elif var == 'r':
            self.retrain.show()
        elif var == 'd':
            self.display.show()

if __name__ == '__main__':
    gui = GUI()
