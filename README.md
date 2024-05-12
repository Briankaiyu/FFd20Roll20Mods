# FFd20Roll20Mods
Repo for Roll20 Mods for FFd20 system

# FFd20Spellbook Instructions (Requires Roll20 Pro):
It is recommend to copy your game before installation, in the event something goes wrong.

Planned updates:
*Introduce handling for different capitalization
*Continue investigation on how script can avoid needing to store json within the script itself

Installation:
1. Download FFd20Spellbook.js
2. Open Roll20 and Login
3. Go to your game
4. Under Settings, select Mod (API) Scripts
5. Select "New Script"
6. Open FFd20Spellbook.js in your text editor of choice
7. Copy the contents from FFd20Spellbook.js into roll20's script editor
8. Rename "New Script" to preferred name
9. Save script

To use, in chatbox type "!spell [spell name]" where spell name is the name of the desired spell to look up.
This script matches spell name exactly, so please check your spelling.
Example command: "!spell Summon Monster I"

In the event included spells are out of date, I have provided a python script that will pull the latest state of FFd20 spells and create a json file. This script will also by default create a subfolder in its current location containing html files of every FFd20 spell. The output json file will be located in the same folder as the script by default.
As this is a python script, this will require an installation of Python 3.12.3 or higher

 Update Instructions:
 1. Execute python script
 2. Open json file
 3. Using the same instructions as detailed under Installation, navigate to script
 4. Around line 50, where var FFd20SpellList is declared, replace the contents within the quotes with the contents of the json file.
 5. To ease copy paste, you can click to the right of the first quote, use the side bar to navigate to the end of the script, then hold shift while clicking to the left of the last quote. This should highlight the proper area
 6. Save script
