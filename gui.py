from tkinter import *

class Tinker:
    def __init__(self):
        self.root = Tk()
        self.root.title('Ai_Simulator')
        self.root.geometry('400x350') 

        self.decided = False
        while not self.decided:

            choice = self.main_tinker()
            
            if choice == 1:
                self.new_tinker()
            elif choice == 2:
                self.retrain_tinker()
            elif choice == 3:
                self.display_tinker()

    def main_tinker(self):
        self.frame = LabelFrame(self.root,bg='grey',text="Main Screen",padx=90,pady=90)
        self.frame.pack(padx=10,pady=10)

        lbl = Label(self.frame,text='Choose from the following options',bg='grey')
        lbl.pack()

        self.radio_var = IntVar()
        
        R1 = Radiobutton(self.frame,text='Create New Maze',variable=self.radio_var,value=1,bg='grey')
        R1.pack()
        R2 = Radiobutton(self.frame,text='Display an Old AI',variable=self.radio_var,value=2,bg='grey')
        R2.pack()
        R3 = Radiobutton(self.frame,text='Retrain an Old AI',variable = self.radio_var,value=3,bg='grey')
        R3.pack()

        b = Button(self.frame,text='Next',command=self.main_get_next)
        b.pack()

        self.root.mainloop()

    def main_get_next(self):
        choice = self.radio_var.get()
        if choice == 1 or choice == 2 or choice == 3:
            self.frame.destroy()
        return choice


    def new_tinker(self):
        self.frame = LabelFrame(self.root,bg='grey',text="New Maze",padx=90,pady=90)
        self.frame.pack(padx=10,pady=10)

        lbl = Label(self.frame,text='Choose from the following options',bg='grey')
        lbl.pack()
        self.root.mainloop()




    def retrain_tinker(self):
        lbl = Label(root,text='retrain')
        self.root.mainloop()




    def display_tinker(self):
        lbl = Label(root,text='display')
        self.root.mainloop()




if __name__ == '__main__':
    tink = Tinker()
