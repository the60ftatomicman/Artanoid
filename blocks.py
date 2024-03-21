from enum import Enum
import math
#---
#
# Utility Functions
#
#---
class BlockType(Enum):
    CLEAR = 0
    FLAT = 1
    ONE_RIDGE = 2
    TWO_RIDGE = 3

def RGB2TkinterColor(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'

def findBlockColRow(pixelX,pixelY):
    blockRow=math.ceil(pixelY / BLOCK_HEIGHTS)-1
    blockCol=math.ceil(pixelX / BLOCK_WIDTHS)-1
    return {"row":blockRow,"col":blockCol}

BLOCK_WIDTHS=26
BLOCK_HEIGHTS=16
BLOCK_PADDING=2
# --
# Represents a block drawn on the screen
# 
# Key -> the code name I use throughout the python program for this "block"
#
# Colors -> this is the color that we expect to draw on the canvas
#   At most I use 3 colors for "ridged" blocks in Revenge of Doh.
#   Original Arkanoid doesn't have cool ridged colors
#   In this array indexes are: 0=Base, 1=Highlight 2=Shadow
#
# Codes -> Represents the hex code that needs to be put into the ROM for this block to appear
#   Always meant to be interpretted as a hexadecimal value.
#   We can have multiple codes for Revenge of Doh has blocks that can move.
#   Indexes are: 0=Static (non moving) 1=Moving
# --
class Block:
    def __init__(self,key,type,codes, colors):
        self.key    = key    # Example: red_flat
        self.type   = type   # Example: Blocktype.FLAT
        self.codes  = codes  # Example: ["00","32"]
        self.colors = colors # Example: [f'#{242:02x}{242:02x}{242:02x}'] or [RGB2TkinterColor(255,0,255),RGB2TkinterColor(0,255,0),RGB2TkinterColor(0,0,0)]
    ##---
    ## Functions for Color Fetching
    ##--
    def getColor_Base(self):
        return self.colors[0]
    
    def getColor_Highlight(self):
        return self.colors[1]

    def getColor_Shadow(self):
        return self.colors[2]

    def draw(self,cnvDisplay,row,col):
            oX=col*BLOCK_WIDTHS
            oY=row*BLOCK_HEIGHTS
            paddedWidth  = BLOCK_WIDTHS-BLOCK_PADDING
            paddedHeight = BLOCK_HEIGHTS-BLOCK_PADDING
            base  = self.getColor_Base()
            if(self.type == BlockType.ONE_RIDGE):
                highlight    = self.getColor_Highlight()
                shadow       = self.getColor_Shadow()
               
                # Draw Black Border
                cnvDisplay.create_rectangle(oX,oY,oX+BLOCK_WIDTHS,oY+BLOCK_HEIGHTS,outline="#000", fill="#000")
                # Draw Base rect
                cnvDisplay.create_rectangle(oX,oY,oX+paddedWidth ,oY+paddedHeight,outline="#000", fill=base)
                # Draw Ridge
                cnvDisplay.create_polygon(oX,oY+1,oX+6,oY+7,oX,oY+paddedHeight-1,outline=highlight, fill=highlight)
                cnvDisplay.create_polygon(oX+23,oY+1,oX+17,oY+7,oX+23,oY+paddedHeight-1,outline=shadow, fill=shadow)

            elif(self.type == BlockType.TWO_RIDGE):
                highlight    = self.getColor_Highlight()
                shadow       = self.getColor_Shadow()
               
                # Draw Black Border
                cnvDisplay.create_rectangle(oX,oY,oX+BLOCK_WIDTHS,oY+BLOCK_HEIGHTS,outline="#000", fill="#000")
                # Draw Base rect
                cnvDisplay.create_rectangle(oX,oY,oX+paddedWidth ,oY+paddedHeight,outline="#000", fill=base)
                # Draw Ridge 1
                min=4
                rng=6
                max=min+rng
                mid=min+(rng/2)
                cnvDisplay.create_polygon(oX+min,oY+max,oX+max,oY+max,oX+mid,oY+mid,
                    outline=highlight, fill=highlight)
                cnvDisplay.create_polygon(oX+max,oY+max,oX+max,oY+min,oX+mid,oY+mid,
                    outline=shadow, fill=shadow)
                # Draw Ridge 2
                offset=(rng+4)
                cnvDisplay.create_polygon(oX+min+offset,oY+max,oX+max+offset,oY+max,oX+mid+offset,oY+mid,
                    outline=highlight, fill=highlight)
                cnvDisplay.create_polygon(oX+max+offset,oY+max,oX+max+offset,oY+min,oX+mid+offset,oY+mid,
                    outline=shadow, fill=shadow)
            elif(self.type == BlockType.FLAT):
                cnvDisplay.create_rectangle(oX,oY,oX+BLOCK_WIDTHS,oY+BLOCK_HEIGHTS,outline="#000", fill="#000")
                cnvDisplay.create_rectangle(oX,oY,oX+paddedWidth,oY+paddedHeight,outline="#000", fill=base)
            else:
                cnvDisplay.create_rectangle(oX,oY,oX+BLOCK_WIDTHS,oY+BLOCK_HEIGHTS,outline="#000", fill=base)

    ##---
    ## Functions for Code Fetching
    ##--
    def getCode_Static(self):
        return bytes.fromhex(self.codes[0])
    
    def getColor_Moving(self):
        return bytes.fromhex(self.codes[1])
#---
#
# Inherited Classes
#
#---
class Clear(Block):
    def __init__(self):
        super().__init__("clear",BlockType.CLEAR,["00"],[RGB2TkinterColor(76,106,78)])
#-- Arkanoid
class White_Flat(Block):
    def __init__(self):
        super().__init__("white_flat",BlockType.FLAT,["01"],[RGB2TkinterColor(255,255,255)])
class Red_Flat(Block):
    def __init__(self):
        super().__init__("red_flat",BlockType.FLAT,["12"],[RGB2TkinterColor(255,0,0)])
class Pink_Flat(Block):
    def __init__(self):
        super().__init__("pink_flat",BlockType.FLAT,["19"],[RGB2TkinterColor(255,0,255)])
class Orange_Flat(Block):
    def __init__(self):
        super().__init__("orange_flat",BlockType.FLAT,["05"],[RGB2TkinterColor(255,143,0)])
class Yellow_Flat(Block):
    def __init__(self):
        super().__init__("yellow_flat",BlockType.FLAT,["1D"],[RGB2TkinterColor(255,255,0)])
class Green_Flat(Block):
    def __init__(self):
        super().__init__("green_flat",BlockType.FLAT,["0E"],[RGB2TkinterColor(0,255,0)])
class Turqouise_Flat(Block):
    def __init__(self):
        super().__init__("turqouise_flat",BlockType.FLAT,["0A"],[RGB2TkinterColor(0,255,255)])
class Blue_Flat(Block):
    def __init__(self):
        super().__init__("blue_flat",BlockType.FLAT,["16"],[RGB2TkinterColor(0,112,255)])
class Grey_Flat(Block):
    def __init__(self):
        super().__init__("grey_flat",BlockType.FLAT,["03"],[RGB2TkinterColor(157,157,157)])
class Gold_Flat(Block):
    def __init__(self):
        super().__init__("gold_flat",BlockType.FLAT,["FF"],[RGB2TkinterColor(188,174,0)])

#-- Arkanoid Revenge of Doh
class White_Flat_AROD(Block):
    def __init__(self):
        super().__init__("white_flat",BlockType.FLAT,["01"],[RGB2TkinterColor(242,242,242)])
class Red_Flat_AROD(Block):
    def __init__(self):
        super().__init__("red_flat",BlockType.FLAT,["21"],[RGB2TkinterColor(242,0,0)])
class Pink_Flat_AROD(Block):
    def __init__(self):
        super().__init__("pink_flat",BlockType.FLAT,["31"],[RGB2TkinterColor(242,80,226)])
class Orange_Flat_AROD(Block):
    def __init__(self):
        super().__init__("orange_flat",BlockType.FLAT,["09"],[RGB2TkinterColor(242,145,0)])
class Yellow_Flat_AROD(Block):
    def __init__(self):
        super().__init__("yellow_flat",BlockType.FLAT,["39"],[RGB2TkinterColor(242,242,0)])
class Green_Flat_AROD(Block):
    def __init__(self):
        super().__init__("green_flat",BlockType.FLAT,["19"],[RGB2TkinterColor(0,242,0)])
class Turqouise_Flat_AROD(Block):
    def __init__(self):
        super().__init__("turqouise_flat",BlockType.FLAT,["11"],[RGB2TkinterColor(0,242,242)])
class Blue_Flat_AROD(Block):
    def __init__(self):
        super().__init__("blue_flat",BlockType.FLAT,["29"],[RGB2TkinterColor(0,144,242)])
class Grey_1Ridge_AROD(Block):
    def __init__(self):
        super().__init__("grey_1ridge",BlockType.ONE_RIDGE,["03"],
        [RGB2TkinterColor(176,176,208),RGB2TkinterColor(192,192,224),RGB2TkinterColor(112,112,144)])
class Grey_2Ridge_AROD(Block):
    def __init__(self):
        super().__init__("grey_2ridge",BlockType.TWO_RIDGE,["53"],
        [RGB2TkinterColor(176,176,208),RGB2TkinterColor(192,192,224),RGB2TkinterColor(112,112,144)])
class Gold_1Ridge_AROD(Block):
    def __init__(self):
        super().__init__("gold_1ridge",BlockType.ONE_RIDGE,["83"],
        [RGB2TkinterColor(240,192,0),RGB2TkinterColor(240,224,0),RGB2TkinterColor(160,128,0)])