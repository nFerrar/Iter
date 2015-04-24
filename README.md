# Iter
A text adventure written in Python. Because I can.

Conceptually, the idea of this little engine is flexibility through simplicity. Ideally anyone could grab this base engine and write their own little story driven adventure, or make a world to explore, even without Python experience.

Some commenting has been done, and current build supports the following commands and mechanics

# Player Commands
move 
- moves the player to another room in a compass direction, however can navigate by any term. Room inventories are persistent

examine 
- describes items and rooms.

search 
- searches the current area, displaying all items currently visible.

open 
- opens container items, adding their contents to the room and updating descriptions

close 
- closes container items, either removing their contents from the room or removing them from themselves if the item has been picked up/moved

take 
- takes an item from the room, adding it to the players inventory

drop 
- drops the specified item from the player inventory into the room contents

inventory 
- displays the players current inventory

quit 
- quits from the game, no save function yet/ever. yolo

help 
- lists the available commands, without description. GLHF

# Features:
Zones can be marked as locked and require a specific item to be accessed, with the option of destroying the item upon entry, complete with flavour text.

Events System! Items and zones can have Evens tagged to them, which can be triggered by actions such as:
- Searching
- examining
- useing
- picking up
- dropping
and they can be limited to running once or infinitly. Numbered running still to come.

# Known Bugs

Possible shenanigans with containers and their contents spilling into the zone.

# To do, in something resembling an order of priority:
still some quantity issues

Add numerical Event control

Add "teleport" function, that will move the player to a new location without telling them. This will allow for scearios that have a room with the lights out or is on fire or is older. the player can be told the room ages arond them, when really they are secretly teleported to a new room with different descriptions.
  
Add other characters who can be talked to/have items given/taken (fetch quests, away!)

?Quest System?
