# ---------- References
# --- https://stackoverflow.com/questions/38153754/can-you-fit-multiple-buttons-in-one-grid-cell-in-tkinter
# --- https://bytes.com/topic/python/answers/935717-tkinter-text-widget-check-if-text-edited
# --- https://cs111.wellesley.edu/archive/cs111_fall14/public_html/labs/lab12/tkintercolor.html
# --- https://web.archive.org/web/20150321101604/http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
# ---------- Imports
# ----- Internal Libs
import math
from os import scandir,mkdir,remove,path
import tkinter as tk
# ---------- TODOS
# TODO: Add controls for font selection and size
# TODO: Add control for selecting an input file other than example.txt
# TODO: As part of the programmatic pre-compiled scripts it'd be REALLY nice to give a "translucent" character
#       to ease headaches in building programmatic code
# TODO: Investigate adding sound?
# TODO: This ux is ugly as hell

# Have to put this here because of blnRunLoop
window = tk.Tk()
window.geometry("391x600")
window.title("Artanoid")
# ---------- Initialize
dirRoot        = path.dirname(path.realpath(__file__))
dirData        = dirRoot+"\\data"
lvlDataRom     = dirData+"\\arkanoidrevengeofdoh\\b08_13.3e"
blnSaving      = False
lstBrickData   = []
strCurrentGame  = tk.StringVar()
strCurrentBlock = tk.StringVar()
GAME_DATA = {
    "arkanoid":{
        "ROWS":17,
        "COLS":13,
        "BLOCKS":{
            "clear"          : {"CODES":{"static":"00"},"COLORS":["#AAA"]},
            "white_flat"     : {"CODES":{"static":"01"},"COLORS":[f'#{242:02x}{242:02x}{242:02x}']},
            "red_flat"       : {"CODES":{"static":"21"},"COLORS":[f'#{242:02x}{0:02x}{0:02x}']},
            "pink_flat"      : {"CODES":{"static":"31"},"COLORS":[f'#{242:02x}{80:02x}{226:02x}']},
            "orange_flat"    : {"CODES":{"static":"09"},"COLORS":[f'#{242:02x}{145:02x}{0:02x}']},
            "yellow_flat"    : {"CODES":{"static":"39"},"COLORS":[f'#{242:02x}{242:02x}{0:02x}']},
            "green_flat"     : {"CODES":{"static":"19"},"COLORS":[f'#{0:02x}{242:02x}{0:02x}']},
            "turqouise_flat" : {"CODES":{"static":"11"},"COLORS":[f'#{0:02x}{242:02x}{242:02x}']},
            "blue_flat"      : {"CODES":{"static":"29"},"COLORS":[f'#{0:02x}{144:02x}{242:02x}']},
            "grey_1ridge"    : {"CODES":{"static":"03"},"COLORS":[f'#{176:02x}{176:02x}{208:02x}',f'#{192:02x}{192:02x}{224:02x}',f'#{112:02x}{112:02x}{144:02x}']}
        },
        "LEVELS":{}
    },
    "arkanoid:revengeofdoh":{
        "ROWS":17,
        "COLS":13,
        "BLOCKS":{
            "clear"          : {"CODES":{"static":"00"},"COLORS":["#AAA"]},
            "white_flat"     : {"CODES":{"static":"01"},"COLORS":[f'#{242:02x}{242:02x}{242:02x}']},
            "red_flat"       : {"CODES":{"static":"21"},"COLORS":[f'#{242:02x}{0:02x}{0:02x}']},
            "pink_flat"      : {"CODES":{"static":"31"},"COLORS":[f'#{242:02x}{80:02x}{226:02x}']},
            "orange_flat"    : {"CODES":{"static":"09"},"COLORS":[f'#{242:02x}{145:02x}{0:02x}']},
            "yellow_flat"    : {"CODES":{"static":"39"},"COLORS":[f'#{242:02x}{242:02x}{0:02x}']},
            "green_flat"     : {"CODES":{"static":"19"},"COLORS":[f'#{0:02x}{242:02x}{0:02x}']},
            "turqouise_flat" : {"CODES":{"static":"11"},"COLORS":[f'#{0:02x}{242:02x}{242:02x}']},
            "blue_flat"      : {"CODES":{"static":"29"},"COLORS":[f'#{0:02x}{144:02x}{242:02x}']},
            "grey_1ridge"    : {"CODES":{"static":"03"},"COLORS":[f'#{176:02x}{176:02x}{208:02x}',f'#{192:02x}{192:02x}{224:02x}',f'#{112:02x}{112:02x}{144:02x}']},
            "gold_1ridge"    : {"CODES":{"static":"83"},"COLORS":[f'#{240:02x}{192:02x}{0:02x}',f'#{240:02x}{224:02x}{0:02x}',f'#{160:02x}{128:02x}{0:02x}']},
            "grey_2ridge"    : {"CODES":{"static":"53"},"COLORS":[f'#{176:02x}{176:02x}{208:02x}',f'#{192:02x}{192:02x}{224:02x}',f'#{112:02x}{112:02x}{144:02x}']}
        },
        "LEVELS":{
            "1":0x593E
        }
    }
}

# ----- Header
frmHeader= tk.Frame(window,height=20)
frmControls  = tk.Frame(window)
frmPaddingLeft= tk.Frame(window,width=20)
frmPaddingRight= tk.Frame(window,width=20)
frmDisplay   = tk.Frame(window)

# - Canvas
cnvDisplay = tk.Canvas(frmDisplay,bg = "#aaa",width=(26*13),height=(17*16))
cnvDisplay.pack()
# - Game Select Control
lblGameSelect = tk.Label(frmControls,text="GAME:")
lblGameSelect.grid(row=0, column=0)
def refreshKeys():
    global txtBlockSelect
    tempList = list(GAME_DATA[strCurrentGame.get()]["BLOCKS"].keys())
    tempList.remove("clear")
    txtBlockSelect.config(values=tempList)
    initBrickData()
    drawBricks()
strCurrentGame.set("arkanoid:revengeofdoh")
txtGameSelect = tk.Spinbox(frmControls,textvariable=strCurrentGame,values=["arkanoid","arkanoid:revengeofdoh"],state='readonly',command=refreshKeys)
txtGameSelect.grid(row=0, column=1)
# - Block Select Control
lblBlockSelect = tk.Label(frmControls,text="Block:")
lblBlockSelect.grid(row=1, column=0)
tempList = list(GAME_DATA[strCurrentGame.get()]["BLOCKS"].keys())
tempList.remove("clear")
txtBlockSelect = tk.Spinbox(frmControls,textvariable=strCurrentBlock,values=tempList,state='readonly')
txtBlockSelect.grid(row=1, column=1)
# - Save Button
btnSave = tk.Button(frmControls, text='Save')
btnSave.grid(row=2, column=1,columnspan=3)
# -- build it all together
frmHeader.grid(row=0,column=0,columnspan=3)
frmPaddingLeft.grid(row=1,column=0)
frmDisplay.grid(row=1,column=1)
frmPaddingRight.grid(row=1,column=2)
frmControls.grid(row=2,column=1)
# ---------- Event Handling
def leftMouseEvent(event):
    #TODO -- add in constants based on game
    blockRow=math.ceil(event.y / 16)-1
    blockCol=math.ceil(event.x / 26)-1
    print("clicked Row: " +str(blockRow)+" Col: "+str(blockCol))
    setBrickData(blockRow,blockCol,strCurrentBlock.get())
cnvDisplay.bind("<ButtonPress 1>", leftMouseEvent)
# --
def rightMouseEvent(event):
    #TODO -- add in constants based on game
    blockRow=math.ceil(event.y / 16)-1
    blockCol=math.ceil(event.x / 26)-1
    print("erased Row: " +str(blockRow)+" Col: "+str(blockCol))
    setBrickData(blockRow,blockCol,"clear")
cnvDisplay.bind("<ButtonPress 3>", rightMouseEvent)
# ---------- Methods
def saveData():
    global GAME_DATA,strCurrentGame,lstBrickData
    content = []
    with open(lvlDataRom, "rb") as fr:
        data = fr.read(1)
        content=data
        idx=0
        lvlStart=int(0x593E)-1
        while data:
            data = fr.read(1)
            if idx == int(0x0A99)-1:
                content+=b'\xAF'
            elif idx >= lvlStart and idx < lvlStart+(GAME_DATA[strCurrentGame.get()]["COLS"] * GAME_DATA[strCurrentGame.get()]["ROWS"]):
                #QuickHotfix
                #if idx != lvlStart+13:
                offset=(idx-lvlStart)
                maxCols=GAME_DATA[strCurrentGame.get()]["COLS"]
                cellRow=math.ceil(offset/maxCols)-1
                if cellRow < 0:
                    cellRow = 0
                cellCol=math.ceil(offset%maxCols)
                cellIdx=(cellRow*maxCols)+(maxCols-cellCol)-1
                #try:
                code = GAME_DATA[strCurrentGame.get()]["BLOCKS"][lstBrickData[cellIdx]]["CODES"]["static"]
                romCode=bytes.fromhex(code)
                content+=romCode
                #except:
                #    print("Col: %d Row %d generated Index: %d" % (cellCol,cellRow,cellIdx))
                #    content+=data
            else:
                content+=data
            idx+=1
    print("done reading")
    with open(lvlDataRom+".new", "wb") as fw:
        fw.write(content)
    print("done writing")
   

def setBrickData(row,col,color):
    global lstBrickData
    lstBrickData[(row*GAME_DATA[strCurrentGame.get()]["COLS"])+col] = color
    drawBricks()

def initBrickData():
    global lstBrickData
    if len(lstBrickData) > 0:
        lstBrickData=[]
    for row in range(GAME_DATA[strCurrentGame.get()]["ROWS"]):
        for col in range(GAME_DATA[strCurrentGame.get()]["COLS"]):  
            lstBrickData.append("clear")

def drawBricks():
    global lstBrickData
    #TODO -- constants
    for row in range(GAME_DATA[strCurrentGame.get()]["ROWS"]):
        for col in range(GAME_DATA[strCurrentGame.get()]["COLS"]):
            oX=col*26
            oY=row*16
            color = lstBrickData[(row*GAME_DATA[strCurrentGame.get()]["COLS"])+col]
            base  = GAME_DATA[strCurrentGame.get()]["BLOCKS"][color]["COLORS"][0]
            if("1ridge" in color):
                highlight =GAME_DATA[strCurrentGame.get()]["BLOCKS"][color]["COLORS"][1]
                shadow    =GAME_DATA[strCurrentGame.get()]["BLOCKS"][color]["COLORS"][2]
                cnvDisplay.create_rectangle(oX,oY,oX+26,oY+16,outline="#000", fill="#000")
                cnvDisplay.create_rectangle(oX,oY,oX+24,oY+14,outline="#000", fill=base)
                cnvDisplay.create_polygon(oX,oY,oX+6,oY+7,oX,oY+14,
                    outline=highlight, fill=highlight)
                cnvDisplay.create_polygon(oX+23,oY,oX+17,oY+7,oX+23,oY+13,
                    outline=shadow, fill=shadow)
            elif("2ridge" in color):
                highlight =GAME_DATA[strCurrentGame.get()]["BLOCKS"][color]["COLORS"][1]
                shadow    =GAME_DATA[strCurrentGame.get()]["BLOCKS"][color]["COLORS"][2]
                cnvDisplay.create_rectangle(oX,oY,oX+26,oY+16,outline="#000", fill="#000")
                cnvDisplay.create_rectangle(oX,oY,oX+24,oY+14,outline="#000", fill=base)
                min=4
                rng=6
                max=min+rng
                mid=min+(rng/2)
                cnvDisplay.create_polygon(oX+min,oY+max,oX+max,oY+max,oX+mid,oY+mid,
                    outline=highlight, fill=highlight)
                cnvDisplay.create_polygon(oX+max,oY+max,oX+max,oY+min,oX+mid,oY+mid,
                    outline=shadow, fill=shadow)
                offset=(rng+4)
                cnvDisplay.create_polygon(oX+min+offset,oY+max,oX+max+offset,oY+max,oX+mid+offset,oY+mid,
                    outline=highlight, fill=highlight)
                cnvDisplay.create_polygon(oX+max+offset,oY+max,oX+max+offset,oY+min,oX+mid+offset,oY+mid,
                    outline=shadow, fill=shadow)
            elif("flat" in color):
                cnvDisplay.create_rectangle(oX,oY,oX+26,oY+16,outline="#000", fill="#000")
                cnvDisplay.create_rectangle(oX,oY,oX+24,oY+14,outline="#000", fill=base)
            else:
                cnvDisplay.create_rectangle(oX,oY,oX+26,oY+16,outline="#000", fill=base)

# ---------- Main
if __name__ == '__main__':
    # have to set these AFTER we initalize
    initBrickData()
    drawBricks()
    btnSave.configure(command=saveData)

    #
    window.update()
    #window.after(0, updateLoop)
    window.mainloop()




