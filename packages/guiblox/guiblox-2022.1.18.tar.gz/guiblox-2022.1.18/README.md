# Object oriented TKINTER WIDGETS 
[![Travis Status](https://travis-ci.org/mclim9/guiBlox.svg?branch=master)](https://pypi.org/project/guiblox/) 
[![PyPi version](https://badge.fury.io/py/guiblox.svg)](https://badge.fury.io/py/guiblox) 
[![Coverage Status](https://coveralls.io/repos/github/mclim9/guiBlox/badge.svg?branch=master)](https://coveralls.io/github/mclim9/guiBlox?branch=master)
![Github Actions](https://github.com/mclim9/guiBlox/workflows/Python%20package/badge.svg)

## Project goals

Object oriented GUI library.  Programatically generate common gui items.

## Installation

```python
from guiblox                    import buttonRow, entryCol, theme, listWindow
```
## Getting Started

```python
from guiblox.__main__ import main

main()
```

# Documentation

## Entry Column 
<p align="center"><img src="https://github.com/mclim9/guiBlox/blob/master/pix/entryCol.jpg" alt="img" width="152" height="177"></p>

```python
from guiblox import entryCol

entryDict = {}                                      # Dict for entry column object
entryDict['Entry1']     = 'Data1'                   # Define Label & Default Val
entryDict['Entry2']     = 'Data2'                   # Define Label & Default Val
entryDict['Entry3']     = 'Data3'                   # Define Label & Default Val

root = theme().addColor()                           # Create GUI object w/ colors
root.entryCol = entryCol(root, entryDict)           # Create column of entry fields

### Assign Functions/Behavior
root.entryCol.frame.config(width=100)               # Chg frame width
root.entryCol.chg2Enum('entry2', ['Opt1','Opt2'])   # Chg entry2 to pull down
root.entryCol.entry2_enum.set('Opt1')               # entry2 default value
```

## Button Row
<p align="center"><img src="https://github.com/mclim9/guiBlox/blob/master/pix/buttonRow.jpg"></p>


```python
from guiblox import buttonRow

root = theme().addColor()                           # Create GUI object w/ colors defined.
root.title('GUI Example')

### Create GUI Elements
root.buttnRow = buttonRow(root, 3)                  # pylint: disable=unused-variable

### Assign Functions/Behavior
root.buttnRow.button0.config(text='foo'  ,command=lambda: buttonfunc1(root))
root.buttnRow.button1.config(text='clear',command=lambda: buttonfunc2(root))
root.buttnRow.button2.config(text='baz'  ,command=lambda: buttonfunc3(root))
```

## Output TextBoxes  
<p align="center"><img src="https://github.com/mclim9/guiBlox/blob/master/pix/listWindow.jpg"></p>

```python
from guiblox import listWindow

root = theme().addColor()                           # Create GUI object w/ colors
root.title('GUI Example')

### Create GUI Elements
root.TextBox = listWindow(root)                     # Create bottom text box
root.TextBox.stdOut()                               # Print --> TextBox

### Assign Functions/Behavior
root.TextBox.listWindow.config(height= 5,width=66)
```

listWindow Method       | Description
------------------------|------------------------------------------
listWindow.add_Files    | Opens GUI to add files
listWindow.clear        | Clears listWindow
listWindow.getlist      | returns contents as list
listWindow.getstr       | returns contents as string
listWindow.stdOut       | Redirects Print statements to listWindow
listWindow.writeN       | Prints text to listWindow
listWindow.writeH       | Prints text to listWindow w/ Highlight
