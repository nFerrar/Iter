# Iter
A text adventure engine written in Python. Because I can.

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

talk
- lets you talk to NPCs!

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

and they can be limited to running once or a set number of times. Or infintly.

ALL NEW! You can now randomise events! Super grindy gameplay can now be implemented. yay.

A limitation of the events system is that currently each action can only be performed once per event, however this can be cicumvented as events can trigger other events.

Three types of things!

- Items:

Can be used, examined, sometimes pickupable, stack, can activate events.

- Containers:

Can be opened and closed, have an internal inventory, cant be picked up, can activate events.

- Structures:

Can only be examines and used, triggering events.

Now with all new NPCs! These guys have names, stats, descriptions, inventories, and even limited conversational skills!

# Known Bugs

None! How did this happen? Is it a bug?

# To do, in something resembling an order of priority:

Add functionality for NPC inventories and deeper conversation trees that can !trigger events!

Combat System.

Rebuild events to be more smarter when handling quantities.

?Quest System?
