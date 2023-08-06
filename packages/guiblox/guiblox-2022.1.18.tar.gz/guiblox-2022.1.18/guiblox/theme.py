"""docstring"""
import tkinter as tk

class theme():
    """docstring"""
    def __init__(self):
        """docstring"""
        # self = tk.Tk()                                        #pylint: disable=W0642
        self.btn = {}
        self.btn['width']   = 10
        self.btn['height']  = 10

    def addColor(self):
        """docstring"""
        self = tk.Tk()                                          #pylint: disable=W0642
        self.clr = {}
        self.clr['txtFg']    = "green2"
        self.clr['txtBg']    = "black"
        self.clr['appFg']    = 'white'
        self.clr['appBg']    = "grey30"
        self.config(bg=self.clr['appBg'])
        return self

if __name__ == '__main__':
    app = theme().addColor()
    app.mainloop()
