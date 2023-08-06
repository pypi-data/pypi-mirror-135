"""docstring"""
import sys
from   tkinter              import ttk
import tkinter.filedialog   as     tkFileDialog
import tkinter              as     Tk
from   guiblox              import theme
END = Tk.END

class listWindow:
    """docstring"""
    def __init__(self, master):
        """docstring"""
        self.master = master
        self.frame = Tk.Frame(master)
        self.listWindow = Tk.Text(self.frame,bg=master.clr['txtBg'], fg=master.clr['txtFg'], insertbackground=master.clr['txtFg'])
        self.scrlWindow = ttk.Scrollbar(self.frame, orient=Tk.VERTICAL,command=self.listWindow.yview)  #Create scrollbar
        self.listWindow['yscrollcommand'] = self.scrlWindow.set

        self.listWindow.grid(row=0,column=0,sticky='nsew')
        self.scrlWindow.grid(row=0,column=1,sticky='nsew')
        self.listWindow.config(font='Courier 11 bold')
        self.frame.grid(sticky='nsew')

    def add_Files(self):
        """docstring"""
        self.listWindow.delete(0,END)
        filez = tkFileDialog.askopenfilenames()
        fileList = list(filez)
        for i in fileList:
            self.listWindow.insert(END,i)
        self.listWindow.see(END)

    def clear(self):
        """docstring"""
        self.listWindow.delete(0.0,END)

    def getlist(self):
        """docstring"""
        return self.listWindow.get("1.0",END).split('\n')

    def getstr(self):
        """docstring"""
        return self.listWindow.get("1.0",END)

    def stdOut(self):
        """docstring"""
        sys.stdout = StdoutRedirector(self.listWindow)

    def writeN(self,inStr):
        """docstring"""
        self.listWindow.insert(END,f'{inStr}\n')
        self.listWindow.see(END)
        self.master.update()
        return self

    def writeH(self,inStr):
        """docstring"""
        self.listWindow.insert(END,f'{inStr}\n')
        self.listWindow.see(END)
        indexx = int(self.listWindow.index(Tk.INSERT).split('.')[0]) - 1
        self.listWindow.tag_add("here", f'{indexx}.0', f'{indexx}.80')
        self.listWindow.tag_config("here", background="green2", foreground="black")
        self.master.update()
        return self

class StdoutRedirector(object):
    """docstring"""
    def __init__(self, text_area):
        """docstring"""
        self.text_area = text_area

    def write(self, writeString):
        """redirecting stdout to this Text widget"""
        self.text_area.insert("end", writeString)
        self.text_area.see(END)
        self.text_area.master.update()

    def flush(self):
        """docstring"""
        sys.stdout = sys.__stdout__             #Send Stdout back to terminal

if __name__ == '__main__':
    root = theme().addColor()
    app = listWindow(root)                      #pylint: disable=unused-variable
    app.stdOut()
    app.listWindow.config(width=20, height=7)
    for i in range(2):
        print(2355345)
        app.writeH('asdfasdf')
        app.writeN(1234)
    root.mainloop()
