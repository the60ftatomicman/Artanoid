# Artanoid
Arkanoid and Arkanoid Revenge of Doh Editor
![Screenshot from editing](./imgs/readme/v1.0.0.png)

# What does this do
If provided the proper ROM file, this tool will generate new ROM files to overwrite the existing ROMS for either of these games.
Block data will be applied AS WELL AS the necessary hacks to jump past ROM checks which are necessary to play any modifications to these games in MAME or on a real machine.
In short, you draw with the tool. The tool writes all the annoying hex values where they need to go for the block data AND rom checks.
Note: I am testing against the ROMSTAR Arkanoid and WORLD copy of Revenge of Doh

# Requirements (as of 3/14/2024)
* Runs on **Python 3.10.11***
  * Uses **tkinter** library as the UI ```pip install tk```
* You'll need a ROM copy of Arkanoid and Arkanoid: Revenge of Doh (World Edition)
  * Both are not needed! Just the ones necessary for the game you want to edit.
----
# Setup (as of 3/14/2024)
## Preparing your MAME folder
1) Start by **backing up** then **unzip** the arkanoid roms into the ROM directory for your MAME emulator
2) **Rename the backup ZIP roms**, otherwise you will not be saving changes!

## Preparing this python application
1) In the root of this project, create a folder called **data**
2) From the roms folder you copied in "Preparing your MAME folder", copy the following ROM files into the newly created **data** folder on your root:
**Arkanoid Revenge of Doh:** -> copy *b08_13.3e* under a directory called "arkanoidrevengeofdoh"
**Arkanoid:** -> copy *a75-18.ic16* and copy *a75-19.ic17* under a directory called "arkanoid"
It should look like
Root
 |- arkanoid 
 |    |-> a75-18.ic16
 |    |-> a75-19.ic17
 |- arkanoidrevengeofdoh
         |-> b08_13.3e


## Running the application
1) Start with whatever flavor of tool you want to use to start a python app. I use **VSCode** since im also developing it
2) Select the game you want to generate a level for
3) Select the block type you want to place
4) **Left click adds** the block, **Right click removes** the block
5) Click Save
6) Goto the data folder, you'll see a file with **.new** at the end. this is our output!

## Running in Mame
1) Copy the **.new** file to the ROM folder in your MAME setup
2) Rename the old file (ex:**b08_13.3e.old**), replace it with the new file (so just remove the .new)
3) run the rom **from the command line!**
   I've only been able to get this to run on an older version of mame...heads up!
----
# Features Working
* Revenge of Doh you can edit any level (17 and 34 are bosses so they are uneditable) with basic blocks.
* Arkanoid you can edit any level (except the final as its a boss) with basic blocks.

# TODOS
* OG Arkanoids lvls 8,9,10 leads to no coin insert bug.
* OG Arkanoids lvl 11 leads to ball through roof bug.
* ~~OG Arkanoid's piracy protection is if you overwrite a75-19.ic17; it allows you to skip all levels. Need to fix!~~ (3/25/2024)
* Refactor and make a class or two. Eeesh right?
* ~~Add better instructions in application~~ (3/13/2024)
* ~~Add level select (currently just modifies level 1)~~ (3/13/2024)
* ~~Finish mapping and Add locations for Arkanoid 1~~ (3/13/2024)
* ~~Finish and add instructions filewise for Arkanoid 1~~ (3/14/2024)
* ~~Add "Useful Lua Scripts" folder so anyone who wants to help in this effort has the tools to make this NOT a grinding task for fetching all the necessary memory locations~~ (3/14/2024)
* ~~Add a cool block picker like in paint~~ (3/18/2024)
* Add flags for moveable blocks (Revenge of Doh only)
* Add load from ROM
* ~~Add Save/Load to String -- for sharing!~~ (3/21/2024)
* Research how backgrounds work for both games, can they change?
* Add MAME launcher in python project? Might be nice....

# Some shortcuts
* For windows users, I have a bat script I use to do my copy and pasting from the repo to my MAME roms. I also launch my game this way. IT WILL SAVE TIME.
 * ```xcopy "/path/to/data/in/this/repo" "/path/to/mame/rom/folder/nowfilenamehere.extension"```
 * ```./mame64 arkanoid2``` run without debug mode
 * ```./mame64 arkanoid2 --debug``` run WITH debug mode if you want to use the memory assembler to see your changes

# Resources
* [Memory Mapping for Arkanoid Revenge of Doh](http://www.arcaderestoration.com/memorymap/365/Arkanoid+-+Revenge+of+DOH.aspx)
* [Initial thread I created to track my progress on this tool](https://www.romhacking.net/forum/index.php?topic=38737.0)
