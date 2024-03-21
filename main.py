# ---------- References
# --- https://stackoverflow.com/questions/38153754/can-you-fit-multiple-buttons-in-one-grid-cell-in-tkinter
# --- https://bytes.com/topic/python/answers/935717-tkinter-text-widget-check-if-text-edited
# --- https://cs111.wellesley.edu/archive/cs111_fall14/public_html/labs/lab12/tkintercolor.html
# --- https://web.archive.org/web/20150321101604/http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
# ---------- Imports
# ----- Internal Libs
from os import path
from enum import Enum
# ----- External Libs
import tkinter as tk
# ----- User Generated Libs
import blocks
import datahandler
# ---------- TODOS
#TODO: Classes for level data
#TODO: dismantel more of the GAME_DATA object
#TODO: Revenge of DOH has movable blocks. lets add a radio button for those
window = tk.Tk()
window.geometry("391x600")
window.title("Artanoid")

# ---------- Initialize
class ShiftDirection(Enum):
    LEFT  = 0
    RIGHT = 1
    UP    = 2
    DOWN  = 3

lstBrickData    = []
lstSwathData    = []
strCurrentGame  = tk.StringVar()
strCurrentBlock = tk.StringVar()
strCurrentLevel = tk.StringVar()


# ----- Header
frmHeader       = tk.Frame(window,height=30,pady=5)
frmControls     = tk.Frame(window)
frmPaddingLeft  = tk.Frame(window,width=20)
frmPaddingRight = tk.Frame(window,width=20)
frmDisplay      = tk.Frame(window)

# - Canvas
cnvSwathes = tk.Canvas(frmHeader,bg = blocks.Clear().getColor_Base(),width=(blocks.BLOCK_WIDTHS*6),height=(blocks.BLOCK_HEIGHTS*2),highlightthickness=0, relief='sunken')
cnvSwathes.pack()
cnvDisplay = tk.Canvas(frmDisplay,bg = blocks.Clear().getColor_Base(),width=(blocks.BLOCK_WIDTHS*13),height=(blocks.BLOCK_HEIGHTS*18))
cnvDisplay.pack()
# - Label for Header
#lblSwathes = tk.Label(frmHeader,text="Pick a Brick")
#lblSwathes.grid(row=0, column=0)
# - Game Select Control
lblGameSelect = tk.Label(frmControls,text="Game:")
lblGameSelect.grid(row=0, column=0)
txtGameSelect = tk.Spinbox(frmControls,textvariable=strCurrentGame,values=["arkanoid","arkanoidrevengeofdoh"],state='readonly')
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
block_btn_frame = tk.Frame(frmControls)
block_btn_frame.grid(row=1, column=2,columnspan=3,sticky="W")
lblActions = tk.Label(block_btn_frame,text="Actions:")
lblActions.grid(row=0, column=1)
btnClear = tk.Button(block_btn_frame, text='Clear')
btnClear.grid(row=0, column=2)
btnFill = tk.Button(block_btn_frame, text='Fill All')
btnFill.grid(row=0, column=3)
#-- OS Operations
os_btn_frame = tk.Frame(frmControls)
os_btn_frame.grid(row=2, column=0,columnspan=5,sticky="W")
lblOs = tk.Label(os_btn_frame,text="Options:")
lblOs.grid(row=1, column=0)
btnSave = tk.Button(os_btn_frame, text='Save')
btnSave.grid(row=1, column=1)
btnLoad = tk.Button(os_btn_frame, text='Load')
btnLoad.grid(row=1, column=2)
btnExport = tk.Button(os_btn_frame, text='ExportTo Rom')
btnExport.grid(row=1, column=3)

#-- Shifting
shift_btn_frame = tk.Frame(frmControls)
shift_btn_frame.grid(row=3, column=0,columnspan=5,sticky="W")
lblShift = tk.Label(shift_btn_frame,text="Shift:")
lblShift.grid(row=1, column=1)
btnShiftLeft = tk.Button(shift_btn_frame, text='Left')
btnShiftLeft.grid(row=1, column=2)
btnShiftRight = tk.Button(shift_btn_frame, text='Right')
btnShiftRight.grid(row=1, column=3)
btnShiftUp = tk.Button(shift_btn_frame, text='Up')
btnShiftUp.grid(row=1, column=4)
btnShiftDown = tk.Button(shift_btn_frame, text='Down')
btnShiftDown.grid(row=1, column=5)
#-- Instructions
lblInstructions = tk.Label(frmControls,text="-----")
lblInstructions.grid(row=4, column=0,columnspan=4)
lblInstructions = tk.Label(frmControls,text="Left click places block. Right click removes blocks")
lblInstructions.grid(row=5, column=0,columnspan=4)
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

def selectSwathEvent(event):
    global lstSwathData
    coords   = blocks.findBlockColRow(event.x,event.y)
    swathIdx = (coords["row"] * 6) + coords["col"]
    swath    = lstSwathData[swathIdx]
    print("clicked SWATH ["+str(swathIdx)+","+swath+"] at Row: " +str(coords["row"])+" Col: "+str(coords["col"]))
    if swath != "clear":
        strCurrentBlock.set(swath)

def refreshKeys():
    global txtBlockSelect,txtLevelSelect
    tempList = list(datahandler.GAME_DATA[strCurrentGame.get()]["LEVELS"].keys())
    txtLevelSelect.config(values=tempList)
    tempList = list(datahandler.GAME_DATA[strCurrentGame.get()]["DATAHANDLER"].blockset.keys())
    tempList.remove("clear")
    txtBlockSelect.config(values=tempList)
    lstBrickData = []
    initBrickData()
    drawBricks()
    initSwathData()
    drawSwathes()

def shiftKeys(dir):
    global lstBrickData
    if lstBrickData is not None and len(lstBrickData) > 0:
        if dir == ShiftDirection.LEFT:
            print("Shift LEFT")
            firstElm = lstBrickData[0]
            lstBrickData.pop(0)
            lstBrickData.append(firstElm)
            drawBricks()
        elif dir == ShiftDirection.RIGHT:
            print("Shift RIGHT")
            lastElm = lstBrickData[len(lstBrickData) - 1]
            lstBrickData = lstBrickData[:len(lstBrickData) - 1]
            lstBrickData.insert(0,lastElm)
            drawBricks()
        elif dir == ShiftDirection.UP:
            print("Shift UP")
            firstElms = lstBrickData[:datahandler.GAME_DATA[strCurrentGame.get()]["COLS"]]
            lstBrickData = lstBrickData[datahandler.GAME_DATA[strCurrentGame.get()]["COLS"]:]
            for elm in firstElms:
                lstBrickData.append(elm)
            drawBricks()
        elif dir == ShiftDirection.DOWN:
            print("Shift DOWN")
            lastIdx = len(lstBrickData) - 1
            colCount = datahandler.GAME_DATA[strCurrentGame.get()]["COLS"]
            lastElms = lstBrickData[(lastIdx - colCount + 1):]
            lstBrickData = lstBrickData[:(lastIdx - colCount + 1)]
            for elmIdx in range(len(lastElms)):
                elm = lastElms[(len(lastElms)-1)-elmIdx]
                lstBrickData.insert(0,elm)
            drawBricks()
        else: 
            print("Shift Direction skip")

def shiftLeft():
    shiftKeys(ShiftDirection.LEFT)
def shiftRight():
    shiftKeys(ShiftDirection.RIGHT)
def shiftUp():
    shiftKeys(ShiftDirection.UP)
def shiftDown():
    shiftKeys(ShiftDirection.DOWN)

def exportData():
    lvlStart =  datahandler.GAME_DATA[strCurrentGame.get()]["LEVELS"][strCurrentLevel.get()]
    rows     =  datahandler.GAME_DATA[strCurrentGame.get()]["ROWS"]
    cols     =  datahandler.GAME_DATA[strCurrentGame.get()]["COLS"]
    datahandler.GAME_DATA[strCurrentGame.get()]["DATAHANDLER"].export(lvlStart,rows,cols,lstBrickData)
# ---------- Methods
def saveData():
    global lstBrickData
    datahandler.GAME_DATA[strCurrentGame.get()]["DATAHANDLER"].save(lstBrickData)
def loadData():
    global lstBrickData
    lstBrickData = datahandler.GAME_DATA[strCurrentGame.get()]["DATAHANDLER"].load()
    drawBricks()

def clearBoard():
    initBrickData()
    drawBricks()

def setBrickData(row,col,color):
    global lstBrickData
    lstBrickData[(row*datahandler.GAME_DATA[strCurrentGame.get()]["COLS"])+col] = color
    drawBricks()

def setAllBrickData():
    global lstBrickData
    for idx in range(len(lstBrickData)):
        lstBrickData[idx] = strCurrentBlock.get()
    drawBricks()

def initBrickData():
    global lstBrickData,cnvDisplay
    cnvDisplay.destroy()
    cnvDisplay = tk.Canvas(frmDisplay,bg = blocks.Clear().getColor_Base(),width=(blocks.BLOCK_WIDTHS*13),height=(blocks.BLOCK_HEIGHTS*18))
    cnvDisplay.pack()
    cnvDisplay.bind("<ButtonPress 1>", leftMouseEvent)
    cnvDisplay.bind("<ButtonPress 3>", rightMouseEvent)
    if len(lstBrickData) > 0:
        lstBrickData=[]
    for row in range(datahandler.GAME_DATA[strCurrentGame.get()]["ROWS"]):
        for col in range(datahandler.GAME_DATA[strCurrentGame.get()]["COLS"]):
            lstBrickData.append("clear")

def drawBricks():
    # the reinitlize canvas is a hack for performance -_- tkinter is VERY slow and creates
    # children with each shape (MY BAD!)
    # ill fix it another time. maybe we can make the children more dynamic a'la the blocks!
    global lstBrickData,cnvDisplay
    cnvDisplay.destroy()
    cnvDisplay = tk.Canvas(frmDisplay,bg = blocks.Clear().getColor_Base(),width=(blocks.BLOCK_WIDTHS*13),height=(blocks.BLOCK_HEIGHTS*18))
    cnvDisplay.pack()
    cnvDisplay.bind("<ButtonPress 1>", leftMouseEvent)
    cnvDisplay.bind("<ButtonPress 3>", rightMouseEvent)
    for row in range(datahandler.GAME_DATA[strCurrentGame.get()]["ROWS"]):
        for col in range(datahandler.GAME_DATA[strCurrentGame.get()]["COLS"]):
            colorIdx = lstBrickData[(row*datahandler.GAME_DATA[strCurrentGame.get()]["COLS"])+col]
            datahandler.GAME_DATA[strCurrentGame.get()]["DATAHANDLER"].blockset[colorIdx].draw(cnvDisplay,row,col)

def initSwathData():
    global lstSwathData,cnvSwathes
    cnvSwathes.destroy()
    cnvSwathes = tk.Canvas(frmHeader,bg = blocks.Clear().getColor_Base(),width=(blocks.BLOCK_WIDTHS*6),height=(blocks.BLOCK_HEIGHTS*2),highlightthickness=0, relief='sunken')
    cnvSwathes.pack()
    cnvSwathes.bind("<ButtonPress 1>", selectSwathEvent)
    for swath in range(12):
        lstSwathData.append("clear")

def drawSwathes():
    global lstSwathData,cnvSwathes
    cnvSwathes.destroy()
    cnvSwathes = tk.Canvas(frmHeader,bg =blocks.Clear().getColor_Base(),width=(blocks.BLOCK_WIDTHS*6),height=(blocks.BLOCK_HEIGHTS*2),highlightthickness=0, relief='sunken')
    cnvSwathes.pack()
    cnvSwathes.bind("<ButtonPress 1>", selectSwathEvent)
    swathIdx = -1
    for swath in datahandler.GAME_DATA[strCurrentGame.get()]["DATAHANDLER"].blockset:
        if swath != "clear":
            swathIdx += 1
            lstSwathData[swathIdx] = swath
            row = 0
            if swathIdx > 5:
                row = 1
            col = (swathIdx % 6)
            datahandler.GAME_DATA[strCurrentGame.get()]["DATAHANDLER"].blockset[swath].draw(cnvSwathes,row,col)
            
# ---------- Main
if __name__ == '__main__':
    # have to set these AFTER we initalize
    txtGameSelect.configure(command=refreshKeys)
    btnExport.configure(command=exportData)
    btnSave.configure(command=saveData)
    btnLoad.configure(command=loadData)
    btnClear.configure(command=clearBoard)
    btnFill.configure(command=setAllBrickData)
    btnShiftLeft.configure(command=shiftLeft)
    btnShiftRight.configure(command=shiftRight)
    btnShiftUp.configure(command=shiftUp)
    btnShiftDown.configure(command=shiftDown)
    initBrickData()
    drawBricks()

    initSwathData()
    drawSwathes()
    #
    window.update()
    window.mainloop()




