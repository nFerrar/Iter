# Iter
A text adventure written in Python. Because I can.

Ideally this game will be very very easy to modify. I want to write the solid engine first and them from there make a game.

I'll note some structure later, along with actually commenting my code.
Some commenting has been done, and current build supports the following commands and mechanics

# Player Commands
move - moves the player to another room in a compass direction, however can navigate by any term. Room inventories are persistent

examine - describes items and rooms.

search - searches the current area, displaying all items currently visible.

open - opens container items, adding their contents to the room and updating descriptions

close - closes container items, either removing their contents from the room or removing them from themselves if the item has been picked up/moved

take - takes an item from the room, adding it to the players inventory

drop - drops the specified item from the player inventory into the room contents

inventory - displays the players current inventory

quit - quits from the game, no save function yet/ever. yolo

help - lists the available commands, without description. GLHF

# Features:
Zones can be marked as locked and require a specific item to be accessed, with the option of destroying the item upon entry, complete with flavour text.

# Known Bugs

Currently any picking up or putting down disregards item quantity

Not all input has had lower() and as such capitalisation can ruin everything.

# To do, in something resembling an order of priority:
Fix item quantity isues

Use command, this will be difficult to keep flexible/simple.

Add events to rooms, triggers to include:

- entry and exit
  
- inventory changes
  
- more?
  
Add other characters who can be talked to/have items given/taken (fetch quests, away!)

?Quest System?
