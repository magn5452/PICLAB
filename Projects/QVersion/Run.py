import tkinter as tk
import tkinter.font as tkFont

class App:
    def __init__(self, root):
        self.root = root
        #setting title
        root.title("undefined")
        #setting window size
        width=200
        height=140
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GButton_96=tk.Button(root)
        GButton_96["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_96["font"] = ft
        GButton_96["fg"] = "#000000"
        GButton_96["justify"] = "center"
        GButton_96["text"] = "Sweep"
        GButton_96.place(x=50,y=50,width=100,height=30)
        GButton_96["command"] = self.GButton_96_command

        GButton_218=tk.Button(root)
        GButton_218["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_218["font"] = ft
        GButton_218["fg"] = "#000000"
        GButton_218["justify"] = "center"
        GButton_218["text"] = "Align"
        GButton_218.place(x=50,y=10,width=100,height=30)
        GButton_218["command"] = self.GButton_218_command

        GButton_444=tk.Button(root)
        GButton_444["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_444["font"] = ft
        GButton_444["fg"] = "#000000"
        GButton_444["justify"] = "center"
        GButton_444["text"] = "Quit"
        GButton_444.place(x=50,y=100,width=100,height=25)
        GButton_444["command"] = self.GButton_444_command

    def GButton_96_command(self):
        print("command")

    def GButton_218_command(self):
        print("command")


    def GButton_444_command(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

