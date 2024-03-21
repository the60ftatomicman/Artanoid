

# ---------- Imports
# ----- Internal Libs
from enum import Enum
from math import floor
from os import path
import csv
# ----- External Libs
# ----- User Generated Libs
import blocks

dirRoot    = path.dirname(path.realpath(__file__))
dirData    = dirRoot+"\\data"

class BlockWriteDirection(Enum):
    LEFT_TO_RIGHT = 0
    RIGHT_TO_LEFT = 1
# --
# Class for doing our write out to our Roms
# 
# Game -> which game we want to save for.
# Roms -> name of all the ROM files we'll modify
# MemOffsets -> the offsets which correlate as the starting location with each ROM file
# Checksums -> any overrides we need to provide for the game to run
# --
class ROMWriter:
    def __init__(self,game,roms,memoffsets,checksums,direction,blockset):
        self.game       = game
        self.roms       = roms
        self.memoffsets = memoffsets
        self.checksums  = checksums
        self.direction  = direction
        self.blockset   = blockset
    ##---
    ## Functions Saving
    ##--
    def getROMFilePath(self,levelStartingLocation):
        romIdx = -1
        for offset in self.memoffsets:
            if int(levelStartingLocation) > int(offset):
                romIdx+=1
        romFilePath = dirData+"\\"+self.game+"\\"+self.roms[romIdx]
        if path.exists(romFilePath+".new"):
            romFilePath = romFilePath+".new"
        return romFilePath
    
    def adjustROMAddressForLvlStart(self,writeMemoryLocation):
        offsetIdx = -1
        for offset in self.memoffsets:
            if int(writeMemoryLocation) > int(offset):
                offsetIdx+=1
        return writeMemoryLocation - self.memoffsets[offsetIdx]

    def checkIfChecksum(self,writeMemoryLocation,currentData):
        if len(self.checksums.keys()) > 0:
            if writeMemoryLocation in self.checksums.keys():
                return self.checksums[writeMemoryLocation]
        return currentData

    def export(self,lvlStart,rows,cols,lstBrickData):
        content     = []
        romFilePath = self.getROMFilePath(lvlStart)
        #now adjust lvlStart!
        lvlStart    = self.adjustROMAddressForLvlStart(lvlStart)
        lvlStart    = int(lvlStart)
        lvlEnd      = lvlStart+(cols * rows)

        print("Reading Rom: %s" % romFilePath)
        with open(romFilePath, "rb") as fr:
            data = fr.read(1)
            content=data
            idx=0
            while data:
                data = fr.read(1)
                idx+=1
                checksumData = self.checkIfChecksum(idx,data)
                if checksumData != data:
                    content+=checksumData
                # TODO -- this is shifted in the dumbest way and I cannot figure it out.
                elif idx >= lvlStart and idx < lvlEnd:
                    offset  = (idx-lvlStart)
                    cellRow = floor(offset/cols)
                    cellCol = floor(offset%cols)
                    cellIdx = (cellRow*cols)+(cellCol)
                    if self.direction == BlockWriteDirection.RIGHT_TO_LEFT:
                        cellIdx = (cellRow*cols)+(cols-cellCol)-1 # Because taito wanted to throw off hackers?
                    #print("Mem Idx: %d Cell Idx: %d, Row: %d Col: %d" % (offset,cellIdx,cellRow,cellCol))
                    #try:
                    romCode  = self.blockset[lstBrickData[cellIdx]].getCode_Static()
                    content += romCode
                    #except:
                    #    print("ERROR!"")
                    #    content+=data
                else:
                    content+=data

        print("Done Reading Rom")
        print("Writing Rom: %s" % romFilePath)
        if ".new" not in romFilePath: 
            with open(romFilePath+".new", "wb") as fw:
                fw.write(content)
        else:
            with open(romFilePath, "wb") as fw:
                fw.write(content)
        print("Done Writing Rom")

    def save(self,lstBrickData):
        content = ""
        for brick in lstBrickData:
            content += brick+","+str(self.blockset[brick].getCode_Static())+"\r\n"
        with open(dirData+"\\"+self.game+"\\save.csv", "w") as fw:
                fw.write(content)

    def load(self):
        content = []
        with open(dirData+"\\"+self.game+"\\save.csv", "r") as fr:
            reader = csv.reader(fr)
            for row in reader:
                #TODO -- this is an issue where save double spaces its saves. this overwrites it
                if len(row) == 2:
                    content.append(row[0])
        return content
#---
#
# Inherited Classes
#
#---
class ROMWriter_Arkanoid(ROMWriter):
    def __init__(self):
        super().__init__("arkanoid",
        ["a75-19.ic17","a75-18.ic16"],
        [0x0000,0x8000],{},
        BlockWriteDirection.LEFT_TO_RIGHT,
        {
            "clear"          : blocks.Clear(),
            "white_flat"     : blocks.White_Flat(),
            "red_flat"       : blocks.Red_Flat(),
            "pink_flat"      : blocks.Pink_Flat(),
            "orange_flat"    : blocks.Orange_Flat(),
            "yellow_flat"    : blocks.Yellow_Flat(),
            "green_flat"     : blocks.Green_Flat(),
            "turqouise_flat" : blocks.Turqouise_Flat(),
            "blue_flat"      : blocks.Blue_Flat(),
            "grey_flat"      : blocks.Grey_Flat(),
            "gold_flat"      : blocks.Gold_Flat(),
        }
    )

class ROMWriter_ArkanoidRevengeOfDoh(ROMWriter):
    def __init__(self):
        super().__init__(
        "arkanoidrevengeofdoh",
        ["b08_13.3e"],[0x0000],{int(0x0A99):b'\xAF'},
        BlockWriteDirection.RIGHT_TO_LEFT,
        {
            "clear"          : blocks.Clear(),
            "white_flat"     : blocks.White_Flat_AROD(),
            "red_flat"       : blocks.Red_Flat_AROD(),
            "pink_flat"      : blocks.Pink_Flat_AROD(),
            "orange_flat"    : blocks.Orange_Flat_AROD(),
            "yellow_flat"    : blocks.Yellow_Flat_AROD(),
            "green_flat"     : blocks.Green_Flat_AROD(),
            "turqouise_flat" : blocks.Turqouise_Flat_AROD(),
            "blue_flat"      : blocks.Blue_Flat_AROD(),
            "grey_1ridge"    : blocks.Grey_1Ridge_AROD(),
            "gold_1ridge"    : blocks.Gold_1Ridge_AROD(),
            "grey_2ridge"    : blocks.Grey_2Ridge_AROD()
        }
    )
#---
#
# The big config
#
#---
GAME_DATA = {
    "arkanoid":{
        "ROWS":17,
        "COLS":13,
        "DATAHANDLER": ROMWriter_Arkanoid(),
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
        "DATAHANDLER": ROMWriter_ArkanoidRevengeOfDoh(),
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
