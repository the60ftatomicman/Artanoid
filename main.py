# ---------- References
# --- https://stackoverflow.com/questions/38153754/can-you-fit-multiple-buttons-in-one-grid-cell-in-tkinter
# --- https://bytes.com/topic/python/answers/935717-tkinter-text-widget-check-if-text-edited
# --- https://cs111.wellesley.edu/archive/cs111_fall14/public_html/labs/lab12/tkintercolor.html
# --- https://web.archive.org/web/20150321101604/http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
# ---------- Imports
# ----- Internal Libs
import math
from os import path
import tkinter as tk
# ---------- TODOS
#TODO: Classes and making this less...rigid.
#TODO: Revenge of DOH has movable blocks. lets add a radio button for those


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
strCurrentLevel = tk.StringVar()
GAME_DATA = {
    "arkanoid":{
        "ROWS":18,
        "COLS":13,
        "ROM":"",
        "CHECKSUM":{"location":0x0A99,"override":b'\xAF'},
        "BLOCKS":{
            "clear"          : {"CODES":{"static":"00"},"COLORS":["#AAA"]},
            "white_flat"     : {"CODES":{"static":"01"},"COLORS":[f'#{255:02x}{255:02x}{255:02x}']},
            "red_flat"       : {"CODES":{"static":"21"},"COLORS":[f'#{255:02x}{0:02x}{0:02x}']},
            "pink_flat"      : {"CODES":{"static":"31"},"COLORS":[f'#{255:02x}{0:02x}{255:02x}']},
            "orange_flat"    : {"CODES":{"static":"09"},"COLORS":[f'#{255:02x}{143:02x}{0:02x}']},
            "yellow_flat"    : {"CODES":{"static":"39"},"COLORS":[f'#{255:02x}{255:02x}{0:02x}']},
            "green_flat"     : {"CODES":{"static":"19"},"COLORS":[f'#{0:02x}{255:02x}{0:02x}']},
            "turqouise_flat" : {"CODES":{"static":"11"},"COLORS":[f'#{0:02x}{255:02x}{255:02x}']},
            "blue_flat"      : {"CODES":{"static":"29"},"COLORS":[f'#{0:02x}{112:02x}{255:02x}']},
            "grey_flat"      : {"CODES":{"static":"03"},"COLORS":[f'#{157:02x}{157:02x}{157:02x}']},
            "gold_flat"      : {"CODES":{"static":"03"},"COLORS":[f'#{188:02x}{174:02x}{0:02x}']}
        },
        "LEVELS":{
            "1":0xBF15,"2":0x0138,"3":0xBE2B,"4":0x04CB,"5":0x0FE0,
            "6":0x14D8,"7":0x16C1,"8":0x1F46,"9":0x22CE,"10":0x2980,
            "11":0x0A08,"12":0x3460,"13":0x40F6,"14":0x41E0,"15":0x4DEC,
            "16":0x502E,"17":0x547A,"18":0x5BAF,"19":0x5CB1,"20":0x5D9B,
            "21":0x64E8,"22":0x6698,"23":0x6829,"24":0x73F3,"25":0x74DD,
            "26":0x75C8,"27":0x7D9E,"28":0x7F88,"29":0x870E,"30":0x8FAE,
            "31":0x9098,"32":0x9CF0
        }
    },
    "arkanoidrevengeofdoh":{
        "ROWS":18,
        "COLS":13,
        "ROM":"b08_13.3e",
        "CHECKSUM":{"location":0x0A99,"override":b'\xAF'},
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
            "1":0x593E,"2R":0x6676,"2L":0x68AA,"3R":0x5C8C,"3L":0x5DA6,
            "4R":0x620E,"4L":0x9D8A,"5R":0x93A0,"5L":0x6328,"6R":0x9C70,"6L":0x6E2C,
            "7R":0x7060,"7L":0x5EC0,"8R":0x5A58,"8L":0x6328,"9R":0x6F46,"9L":0x6CD2,
            "10R":0x60F4,"10L":0x5FDA,"11R":0x7EB2,"11L":0x8782,"12R":0x7816,"12L":0x96EE,
            "13R":0x8200,"13L":0x9922,"14R":0x9286,"14L":0x8434,"15R":0x94BA,"15L":0x7930,
            "16R":0x69C4,"16L":0x6ADE,"18R":0x7C7E,"18L":0x7B64,"19R":0x89B6,"19L":0x8668,
            "20R":0x7294,"20L":0x831A,"21R":0x6D12,"21L":0x8D04,"22R":0x8F38,"22L":0x6442,
            "23R":0x7FCC,"23L":0x5B72,"24R":0x73AE,"24L":0x889C,"25R":0x9B56,"25L":0x76FC,
            "26R":0x95D4,"26L":0x655C,"27R":0x8E1E,"27L":0x7D98,"28R":0x8AD0,"28L":0x75E2,
            "29R":0x74C8,"29L":0x916C,"30R":0x854E,"30L":0x9A3C,"31R":0x80E6,"31L":0x9052,
            "32R":0x9808,"32L":0x8BEA,"33R":0x717A,"33L":0x6790
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
cnvDisplay = tk.Canvas(frmDisplay,bg = "#aaa",width=(26*13),height=(18*16))
cnvDisplay.pack()
# - Game Select Control
lblGameSelect = tk.Label(frmControls,text="Game:")
lblGameSelect.grid(row=0, column=0)

def refreshKeys():
    global txtBlockSelect,txtLevelSelect
    tempList = list(GAME_DATA[strCurrentGame.get()]["LEVELS"].keys())
    txtLevelSelect.config(values=tempList)
    tempList = list(GAME_DATA[strCurrentGame.get()]["BLOCKS"].keys())
    tempList.remove("clear")
    txtBlockSelect.config(values=tempList)
    initBrickData()
    drawBricks()

txtGameSelect = tk.Spinbox(frmControls,textvariable=strCurrentGame,values=["arkanoidrevengeofdoh","arkanoid"],state='readonly',command=refreshKeys)
txtGameSelect.grid(row=0, column=1)
# -- Level Select
lblLevelSelect = tk.Label(frmControls,text="Level:")
lblLevelSelect.grid(row=0, column=2)
tempList = list(GAME_DATA[strCurrentGame.get()]["LEVELS"].keys())
txtLevelSelect = tk.Spinbox(frmControls,textvariable=strCurrentLevel,values=tempList,state='readonly')
txtLevelSelect.grid(row=0, column=3)
# - Block Select Control
lblBlockSelect = tk.Label(frmControls,text="Block:")
lblBlockSelect.grid(row=1, column=0)
tempList = list(GAME_DATA[strCurrentGame.get()]["BLOCKS"].keys())
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
    global GAME_DATA,strCurrentGame,strCurrentLevel,lstBrickData
    content = []
    lvlDataRom = dirData+"\\"+strCurrentGame.get()+"\\"+GAME_DATA[strCurrentGame.get()]["ROM"]
    if path.exists(lvlDataRom+".new"):
        lvlDataRom = lvlDataRom+".new"
    with open(lvlDataRom, "rb") as fr:
        data = fr.read(1)
        content=data
        idx=0
        lvlStart=int(GAME_DATA[strCurrentGame.get()]["LEVELS"][strCurrentLevel.get()])-1
        while data:
            data = fr.read(1)
            if idx == int(GAME_DATA[strCurrentGame.get()]["CHECKSUM"]["location"])-1:
                content+=GAME_DATA[strCurrentGame.get()]["CHECKSUM"]["override"]
            elif idx >= lvlStart and idx < lvlStart+(GAME_DATA[strCurrentGame.get()]["COLS"] * GAME_DATA[strCurrentGame.get()]["ROWS"]):
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
    if ".new" not in lvlDataRom: 
        with open(lvlDataRom+".new", "wb") as fw:
            fw.write(content)
    else:
        with open(lvlDataRom, "wb") as fw:
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




