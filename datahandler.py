from os import path
from enum import Enum
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
    def __init__(self,game,roms,memoffsets,checksums):
        self.game       = game
        self.roms       = roms
        self.memoffsets = memoffsets
        self.checksums  = checksums
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

#---
#
# Inherited Classes
#
#---
class ROMWriter_Arkanoid(ROMWriter):
    def __init__(self):
        super().__init__("arkanoid",
        ["a75-18.ic16","a75-19.ic17"],[0x0000,0x8000],{})

class ROMWriter_ArkanoidRevengeOfDoh(ROMWriter):
    def __init__(self):
        super().__init__("arkanoidrevengeofdoh",
        ["b08_13.3e"],[0x0000],{int(0x0A99):b'\xAF'})