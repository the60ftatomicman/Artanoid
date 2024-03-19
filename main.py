# ---------- References
# --- https://stackoverflow.com/questions/38153754/can-you-fit-multiple-buttons-in-one-grid-cell-in-tkinter
# --- https://bytes.com/topic/python/answers/935717-tkinter-text-widget-check-if-text-edited
# --- https://cs111.wellesley.edu/archive/cs111_fall14/public_html/labs/lab12/tkintercolor.html
# --- https://web.archive.org/web/20150321101604/http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
# ---------- Imports
# ----- Internal Libs
import math
from os import path
# ----- External Libs
import tkinter as tk
# ----- User Generated Libs
import blocks
import datahandler
# ---------- TODOS
#TODO: Classes and making this less...rigid.
#TODO: Revenge of DOH has movable blocks. lets add a radio button for those
#TODO: A click menu instead of a drop down (think like paint!)
window = tk.Tk()
window.geometry("391x600")
window.title("Artanoid")
# ---------- Initialize
blnSaving      = False
lstBrickData   = []
strCurrentGame  = tk.StringVar()
strCurrentBlock = tk.StringVar()
strCurrentLevel = tk.StringVar()


# ----- Header
frmHeader       = tk.Frame(window,height=20)
frmControls     = tk.Frame(window)
frmPaddingLeft  = tk.Frame(window,width=20)
frmPaddingRight = tk.Frame(window,width=20)
frmDisplay      = tk.Frame(window)

# - Canvas
cnvDisplay = tk.Canvas(frmDisplay,bg = "#aaa",width=(blocks.BLOCK_WIDTHS*13),height=(blocks.BLOCK_HEIGHTS*18))
cnvDisplay.pack()
# - Game Select Control
lblGameSelect = tk.Label(frmControls,text="Game:")
lblGameSelect.grid(row=0, column=0)

def refreshKeys():
    global txtBlockSelect,txtLevelSelect
    tempList = list(datahandler.GAME_DATA[strCurrentGame.get()]["LEVELS"].keys())
    txtLevelSelect.config(values=tempList)
    tempList = list(datahandler.GAME_DATA[strCurrentGame.get()]["DATAHANDLER"].blockset.keys())
    tempList.remove("clear")
    txtBlockSelect.config(values=tempList)
    initBrickData()
    drawBricks()

txtGameSelect = tk.Spinbox(frmControls,textvariable=strCurrentGame,values=["arkanoidrevengeofdoh","arkanoid"],state='readonly',command=refreshKeys)
txtGameSelect.grid(row=0, column=1)
# -- Level Select
lblLevelSelect = tk.Label(frmControls,text="Level:")
lblLevelSelect.grid(row=0, column=2)
tempList = list(datahandler.GAME_DATA[strCurrentGame.get()]["LEVELS"].keys())
txtLevelSelect = tk.Spinbox(frmControls,textvariable=strCurrentLevel,values=tempList,state='readonly')
txtLevelSelect.grid(row=0, column=3)
# - Block Select Control
lblBlockSelect = tk.Label(frmControls,text="Block:")
lblBlockSelect.grid(row=1, column=0)
tempList = list(datahandler.GAME_DATA[strCurrentGame.get()]["DATAHANDLER"].blockset.keys())
tempList.remove("clear")
txtBlockSelect = tk.Spinbox(frmControls,textvariable=strCurrentBlock,values=tempList,state='readonly')
txtBlockSelect.grid(row=1, column=1)
# - Save Button
btnSave = tk.Button(frmControls, text='Save')
btnSave.grid(row=1, column=2,columnspan=2)
#-- Instructions
lblInstructions = tk.Label(frmControls,text="Left click places block. Right click removes blocks")
lblInstructions.grid(row=3, column=0,columnspan=4)
# -- build it all together
frmHeader.grid(row=0,column=0,columnspan=3)
frmPaddingLeft.grid(row=1,column=0)
frmDisplay.grid(row=1,column=1)
frmPaddingRight.grid(row=1,column=2)
frmControls.grid(row=2,column=1)
# ---------- Event Handling
def leftMouseEvent(event):
    coords= blocks.findBlockColRow(event.x,event.y)
    print("clicked Row: " +str(coords["row"])+" Col: "+str(coords["col"]))
    setBrickData(coords["row"],coords["col"],strCurrentBlock.get())
# --
def rightMouseEvent(event):
    coords= blocks.findBlockColRow(event.x,event.y)
    print("erased Row: " +str(coords["row"])+" Col: "+str(coords["col"]))
    setBrickData(coords["row"],coords["col"],"clear")
# ---------- Methods
def saveData():
    lvlStart =  datahandler.GAME_DATA[strCurrentGame.get()]["LEVELS"][strCurrentLevel.get()]
    rows     =  datahandler.GAME_DATA[strCurrentGame.get()]["ROWS"]
    cols     =  datahandler.GAME_DATA[strCurrentGame.get()]["COLS"]
    datahandler.GAME_DATA[strCurrentGame.get()]["DATAHANDLER"].save(lvlStart,rows,cols,lstBrickData)
        
def setBrickData(row,col,color):
    global lstBrickData
    lstBrickData[(row*datahandler.GAME_DATA[strCurrentGame.get()]["COLS"])+col] = color
    drawBricks()

def initBrickData():
    global lstBrickData
    if len(lstBrickData) > 0:
        lstBrickData=[]
    for row in range(datahandler.GAME_DATA[strCurrentGame.get()]["ROWS"]):
        for col in range(datahandler.GAME_DATA[strCurrentGame.get()]["COLS"]):
            lstBrickData.append("clear")

def drawBricks():
    global lstBrickData,cnvDisplay
    #TODO -- constants
    for row in range(datahandler.GAME_DATA[strCurrentGame.get()]["ROWS"]):
        for col in range(datahandler.GAME_DATA[strCurrentGame.get()]["COLS"]):
            colorIdx = lstBrickData[(row*datahandler.GAME_DATA[strCurrentGame.get()]["COLS"])+col]
            datahandler.GAME_DATA[strCurrentGame.get()]["DATAHANDLER"].blockset[colorIdx].draw(cnvDisplay,row,col)

# ---------- Main
if __name__ == '__main__':
    # have to set these AFTER we initalize
    cnvDisplay.bind("<ButtonPress 1>", leftMouseEvent)
    cnvDisplay.bind("<ButtonPress 3>", rightMouseEvent)

    initBrickData()
    drawBricks()
    btnSave.configure(command=saveData)

    #
    window.update()
    window.mainloop()




