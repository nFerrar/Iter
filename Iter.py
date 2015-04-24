import sys

class Person(object):
	def __init__(self, name, inventory):
		self.name = name
		self.inventory = inventory
	
	def addToInventory(self, newItem, quantity):
		for i in self.inventory:
			if(newItem == i):
				self.inventory[i] = self.inventory[i] + quantity
				break
			else:
				self.inventory[newItem] = quantity
				break
			
	def removeFromInventory(self, item, quantity):
		for i in self.inventory:
			if(item == i):
				if(self.inventory[i] > quantity):
					self.inventory[i] = self.inventory[i] - quantity
					break
				else:
					del self.inventory[i]
					break
		
		else:
			print("You're not carrying a %s." % (str(item)))
	
class PC(Person):
	def checkInventory(self):
		print("You take a moment to check what you're carrying.")
		print("You have on you:")
		for i in self.inventory:
			if(self.inventory[i] > 1):
				print(str(self.inventory[i]) + " " + str(i) + "s")
			else:
				print(str(i))

class Zone(object):

	def __init__(self, name, references, description, contents, exits, bLocked, keyItem, blockedText, unlockText, bDestroyKey, keyDestroyText, bEvent, Trigger, Event):
		self.name = name
		self.references = references
		self.description = description
		self.contents = contents
		self.exits = exits
		self.bLocked = bLocked
		self.keyItem = keyItem
		self.blockedText = blockedText
		self.unlockText = unlockText
		self.bDestroyKey = bDestroyKey
		self.keyDestroyText = keyDestroyText
		self.bEvent = bEvent
		self.Trigger = Trigger
		self.Event = Event
		
	def examineRoom(self):
		print("You are in a " + self.description)
		
	def searchRoom(self):
		print("You search the immediate area, and you find:")
		for i in self.contents:
			if(self.contents[i] == 1):
				print(stringToClass(i).name)
			else:
				print(str(self.contents[i])+ " " + i + "s")
		print("And exits to the")
		for x in self.exits:
			print(x)
				
	def addItem(self, item, quantity):
		for i in self.contents:
			if(item == i):
				self.contents[i] = self.contents[i] + quantity
				break		
			else:
				self.contents[item] = quantity
				break
	
	def removeItem(self, item, quantity):
		for i in self.contents:
			if(i == item):
				if(self.contents[i] > quantity):
					self.contents[i] = self.contents[i] - quantity
					break
				else:
					del self.contents[i]
					break
			
class Item(object):
	
	def __init__(self, name, description, bPickUp, bUseable, bUseAlone, useWith, useText, bEvent, Trigger, Event):
		self.name = name
		self.description = description
		self.bPickUp = bPickUp
		self.bUseable = bUseable
		self.bUseAlone = bUseAlone
		self.useWith = useWith
		self.useText = useText
		self.bEvent = bEvent
		self.Trigger = Trigger
		self.Event = Event
		
	def describeItem(self):
		print("It's %s" % (self.description))

class Container(Item):
	
	tempD = {}

	def __init__(self, name, description, bPickUp, openDescription, contents, openText, closeText, bOpen, bUseable, bUseAlone, useWith, useText, bEvent, Trigger, Event):
		self.name = name
		self.description = description
		self.bPickUp = bPickUp
		self.openDescription  = openDescription
		self.contents = contents
		self.openText = openText
		self.closeText = closeText
		self.bOpen = bOpen
		self.bUseable = bUseable
		self.bUseAlone = bUseAlone
		self.useWith = useWith
		self.useText = useText
		self.bEvent = bEvent
		self.Trigger = Trigger
		self.Event = Event
		
	def describeItem(self):
		if(self.bOpen == False):
			print("It's %s" % (self.description))
		else:
			print("It's %s" % (self.openDescription))
	
	def openContainer(self, Location, Character):
		self.bOpen = True
		print(self.openText + " Inside you see")
		for i in self.contents:
			if(self.contents[i] > 1):
				print(str(self.contents[i]) + " " + i)
				Location.addItem(i, self.contents[i])
			else:
				print(i)
				Location.addItem(i, 1)
				
	def closeContainer(self, Location, Character):
		self.bOpen = False
		print(self.closeText)
		for i in self.contents:
			for x in Location.contents:
				if(i == x):
					self.tempD[i] = Location.contents[x]
					Location.removeItem(x, self.contents[i])
					break
		self.contents = self.tempD
		self.tempD = {}

class Event(object):

	bRun = True
	
	def __init__(self, EventActions, bRepeat):
		self.EventActions = EventActions
		self.bRepeat = bRepeat
		
	def triggerEvent(self, Location, Character):
		if(self.bRun == True):
			for e in self.EventActions:
				stingToClassDef(self, e)(Location, Character, self.EventActions[e])
			if(self.bRepeat == True):
				Scene(Location, Character)
			else:
				self.bRun = False
				Scene(Location, Character)
			Scene(Location, Character)
		else:
			Scene(Location, Character)

	def PRINT(self, Location, Character, text):
		print(text)
	
	def ADDTOINVENTORY(self, Location, Character, item):
		Character.addToInventory(item, 1)
		
	def REMOVEFROMINVENTORY(self, Location, Character, item):
		Character.removeFromInventory(item, 1)
		
	def ADDITEM(self, Location, Character, item):
		Location.addItem(item, 1)
		
	def REMOVEITEM(self, Location, Character, item):
		Location.removeItem(item, 1)

class PlayerCommands(object):##These are all the commands the player can perform, they are as dynamic as possible.
	def __init__(self):
		pass
	
	def search(self, Location, Character):##Search the area, makes the Zone print its contents
		Location.searchRoom()
		checkForEvent(Location, Character, Location, "searchZone")
	
	def examine(self, Location, Character):##Examines the area, makes the Zone print its description
		cmd = input("Examine what? >>>")
		
		for i in Location.references:
			if(cmd.lower() == i):
				Location.examineRoom()
				checkForEvent(Location, Character, Location, "examineZone")
				
		else:
			for i in Location.contents:
				if(cmd.lower() == i):
					stringToClass(i).describeItem()
					if(Location.contents[i] > 1):
						print("There are " + str(Location.contents[i]) + " of them.")
					checkForEvent(Location, Character, stringToClass(i), "examineItem")

			else:
				for i in Player.inventory:
					if(cmd.lower() == i):
						stringToClass(i).describeItem()
						if(Player.inventory[i] > 1):
							print("You are carrying " + str(Player.inventory[i]) + " of them.")
						checkForEvent(Location, Character, stringToClass(i), "examineItem")

				else:
					print("You don't see a %s here." % (cmd.lower()))
					Scene(Location, Character)
	
	def inventory(self, Location, Character):##Checks the players Inventory, printing its contents
		Player.checkInventory()
		Scene(Location, Character)
		
	def quit(self, Location, Character):##lets you quit, has a confirmation. NO SAVE BITCHES. YOLO
		cmd = input("Are you sure you want to quit?")
		
		if(cmd.lower() == "y" or cmd.lower() == "yes"):
			print("Shutting Down...")
			exit()
			
		else:
			Scene(Location, Character)
		
	def help(self, Location, Character):##siply prints all the commands, no descriptions for you
		print("Available Commands:")
		for c in Commands:
			print(c)
		Scene(Location, Character)
		
	def open(self, Location, Character):##used to open Container class items. toggles variables
		cmd = input("Open what? >>>")
		
		for i in itemList:
			if(i == cmd.lower()):
				if hasattr(stringToClass(cmd.lower()), "bOpen"):
					if(stringToClass(cmd.lower()).bOpen == False):
						stringToClass(cmd.lower()).openContainer(Location, Character)
						checkForEvent(Location, Character, stringToClass(i), "openContainer")

					else:
						print("It's already open.")
						Scene(Location, Character)
						
				else:
					print("You can't open that.")
					Scene(Location, Character)
		else:
			print("You don't see a %s here." % (cmd.lower()))
			Scene(Location, Character)
		
	def close(self, Location, Character):##used to close open Containers. toggles variables and re-checks contents in case of deletion.
		cmd = input("Close what? >>>")
		
		for i in itemList:
			if(i == cmd.lower()):
				if hasattr(stringToClass(cmd.lower()), "bOpen"):
					if(stringToClass(cmd.lower()).bOpen == True):
						stringToClass(cmd.lower()).closeContainer(Location, Character)
						checkForEvent(Location, Character, stringToClass(i), "closeContainer")

					else:
						print("It's already closed.")
						Scene(Location, Character)
				else:
					print("You can't close that.")
					Scene(Location, Character)
		else:
			print("You don't see a %s here." % (cmd.lower()))
			Scene(Location, Character)

	def take(self, Location, Character):##lets the player pick up Items marked as pickupable.
		cmd = input("What would you like to pick up? >>>")
		
		for l in Location.contents:
			if(l == cmd.lower()):
				if(stringToClass(cmd.lower()).bPickUp == True):
					Character.addToInventory(cmd.lower(), Location.contents[cmd.lower()])
					Location.removeItem(cmd.lower(), Location.contents[cmd.lower()])
					print("You pick up the %s." % (l))
					checkForEvent(Location, Character, stringToClass(l), "pickupItem")

				else:
					print("You can't pick that up.")
					Scene(Location, Character)
		else:
			print("There isn't a %s here." % (cmd.lower()))
			Scene(Location, Character)
			
	def drop(self, Location, Character):##drops an item from the inventory to the zone. will go back into a container it came from
		cmd = input("What do you want to drop? >>>")
		
		for l in Character.inventory:
			if(l == cmd.lower()):
				q = input("Drop how many? >>>")
				
				try:
					if(int(q) <= Character.inventory[cmd.lower()]):
						Character.removeFromInventory(cmd.lower(), int(q))
						Location.addItem(cmd.lower(), int(q))
						print("You drop the %s." % (l))
						checkForEvent(Location, Character, stringToClass(cmd.lower()), "dropItem")

					else:
						print("You don't have that many " + cmd.lower() +"s.")
						Scene(Location, Character)
				except:
					print("That's not a number!")
					Scene(Location, Character)
		else:
			print("You're not carrying a %s." % (cmd.lower()))
			Scene(Location, Character)
			
	def move(self, Location, Character):##moves the character from one location to another.
		cmd = input("Which direction do you want to go? >>>")
		
		for d in Location.exits:
			if(d == cmd.lower()):
				if(stringToClass(Location.exits[d]).bLocked == False):
					ChangeLocation(Location, stringToClass(Location.exits[d]), Character)
					break
				else:
					for k in Character.inventory:
						if(k == stringToClass(Location.exits[d]).keyItem):
							stringToClass(Location.exits[d]).bLocked = False
							print(stringToClass(Location.exits[d]).unlockText)
						
							if(stringToClass(Location.exits[d]).bDestroyKey == False):
								ChangeLocation(Location, stringToClass(Location.exits[d]), Character)
								break
							else:
								print(stringToClass(Location.exits[d]).keyDestroyText)
								Character.removeFromInventory(stringToClass(Location.exits[d]).keyItem, 1)
								ChangeLocation(Location, stringToClass(Location.exits[d]), Character)
								break
					else:
						print(stringToClass(Location.exits[d]).blockedText)
						Scene(Location, Character)
						break
		else:
			print("You cannot go that way.")
			Scene(Location, Character)
	
	def use(self, Location, Character):
		cmd = input("Use what? >>>")
		
		for i in Character.inventory:
			if(cmd.lower() == i):
				if(stringToClass(cmd.lower()).bUseable == True):
					if(stringToClass(cmd.lower()).bUseAlone == True):
						print(stringToClass(cmd.lower()).useText)
						checkForEvent(Location, Character, stringToClass(i), "useItem")

					else:
						u = input("Use with what? >>>")
						for x in Character.inventory:
							if(u.lower() == x):
								if(stringToClass(cmd.lower()).useWith == x):
									print(stringToClass(cmd.lower()).useText)
									checkForEvent(Location, Character, stringToClass(i), "useItem")

								else:
									print("You can't use those together.")
									Scene(Location, Character)
						for x in Location.contents:
							if(u.lower() == x):
								if(stringToClass(cmd.lower()).useWith == x):
									print(stringToClass(cmd.lower()).useText)
									checkForEvent(Location, Character, stringToClass(i), "useItem")

								else:
									print("You can't use those together.")
									Scene(Location, Character)
						else:
							print("There isn't a %s here." % (u.lower()))
							Scene(Location, Character)
				else:
					print("You can't use that.")
					Scene(Location, Character)
					
		for i in Location.contents:
			if(cmd.lower() == i):
				if(stringToClass(cmd.lower()).bUseable == True):
					if(stringToClass(cmd.lower()).bUseAlone == True):
						print(stringToClass(cmd.lower()).useText)
						checkForEvent(Location, Character, stringToClass(i), "useItem")

					else:
						u = input("Use with what? >>>")
						for x in Character.inventory:
							if(u.lower() == x):
								if(stringToClass(cmd.lower()).useWith == x):
									print(stringToClass(cmd.lower()).useText)
									checkForEvent(Location, Character, stringToClass(i), "useItem")

								else:
									print("You can't use those together.")
									Scene(Location, Character)
						for x in Location.contents:
							if(u.lower() == x):
								if(stringToClass(cmd.lower()).useWith == x):
									print(stringToClass(cmd.lower()).useText)
									checkForEvent(Location, Character, stringToClass(i), "useItem")

								else:
									print("You can't use those together.")
									Scene(Location, Character)
						else:
							print("There isn't a %s here." % (u.lower()))
							Scene(Location, Character)
				else:
					print("You can't use that.")
					Scene(Location, Character)
		else:
			print("There isn't a %s here." % (cmd.lower()))
			Scene(Location, Character)

###########################
##ASSIGN ALL CLASSES HERE##
###########################

## START PLAYER COMMANDS##
Commands = ["search", "examine", "inventory", "quit", "help", "open", "close", "take", "drop", "move", "use",]
playerCommand = PlayerCommands()
## END PLAYER COMMANDS##

## BEGIN EVENT ASSIGNMENTS ##
testEventActions = {
	"PRINT" : "It seems you won't be able to go any further for now.",
	"ADDTOINVENTORY" : "clothing",
	"ADDITEM" : "wallet",
	}
testEvent = Event(testEventActions, True)

boxEventActions = {
	"PRINT" : "You somehow manage to pinch your fingers as you close it, man it would be stupid if you did that every time you closed this box...",
	}
boxEvent = Event(boxEventActions, False)

bulbEventActions = {
	"ADDTOINVENTORY" : "lightbulb",
	"REMOVEITEM" : "light",
	"ADDITEM" : "socket"
	}
bulbEvent = Event(bulbEventActions, True)

socketEventActions = {
	"REMOVEFROMINVENTORY" : "lightbulb",
	"REMOVEITEM" : "socket",
	"ADDITEM" : "light"
	}
socketEvent = Event(socketEventActions, True)

dropClothesEventActions = {
	"PRINT" : "You feel a little cold without your clothes on, and you doubt you'll be able to engage in decent society if you don't remedy the situation.",
	}
dropClothesEvent = Event(dropClothesEventActions, True)

pickupKeyEventActions = {
	"PRINT" : "As you hold the key in your hand, you get a sense of great...contextual importance."
	}
pickupKeyEvent = Event(pickupKeyEventActions, True)
## END EVENT ASSIGNMENTS ##

## BEGIN ITEM ASSIGNMENTS ##
boxContents = {
	"key" : 1,
	"cloth" : 5,
	}
box = Container("a box", "a wooden crate, covered in dust. It looks old, and has hinges on the back edge.", False, "an open wooden box, emanating a musty small from it's dark interior.", boxContents, "As you slowly open the box it's hinges give a protesting groan and despite your gentle motions you are surrounded by a plume of dust which slowly settles to the floor.", "You close the box with a creak.", False, False, False, "None, error", "none, error", True, "closeContainer", boxEvent)
cloth = Item("a piece of cloth", "a small piece of dirty, off white cloth, smelling slightly of alcohol. Maybe, beer?", True, True, False, "light", "Protecting your hand with the cloth, you manage to gently remove the lightbulb from its fitting.", True, "useItem", bulbEvent)
clothing = Item("simple clothing", "a simple outfit of various materials. It is far from fancy, or comfortable, but it is sufficient.", True, False, False, "none error", "none error", True, "dropItem", dropClothesEvent)
wallet = Item("a small leather wallet", "a small and worn wallet made of leather, or maybe fake leather. It smells of dust.", True, False, False, "none error", "none error", False, "none, error", "none, error")
shin = Item("a shin", "a shiny stick of metal and plastic, with an intricate patterns carved up the side. These are what is used as currency when barter will not suffice.", True, False, False, "none error", "none error", False, "none, error", "none, error")
key = Item("a small key", "a small tarnished key of silver. it looks as though it hasn't been touched in  very long time.", True, False, False, "none error", "none error", True, "pickupItem", pickupKeyEvent)
light = Item("a light", "a small, dull light bulb hanging from the ceiling by a thin cord.", False, True, True, "none, error", "You burn your hand as you try to touch the light. That wasn't very clever.", False, "none, error", "none, error")
lightbulb = Item("a lightbulb", "a small lightbulb of murky brown glass. It appears to be in working order", True, True, False, "socket", "You gently screw the bulb into place, and are briefly blinded by its surprisingly bright light as it turns on again.", True, "useItem", socketEvent)
socket = Item("an empty light socket", "an empty electrical socket hanging by a ting cord from the ceiling. It looks like it should have a lightbulb in it.", False, True, False, "lightbulb", "You gently screw the bulb into place, and are briefly blinded by its surprisingly bright light as it turns on again.", True, "useItem", socketEvent)
## END ITEM ASSIGNMENTS ##

## BEGIN ITEM LIST ##
itemList = ["light", "box", "cloth", "clothing", "wallet", "shin", "key", "lightbulb", "socket",]
## END ITEM LIST ##

## BEGIN ZONE ASSGNMENTS ##
TestRoomReferences = ["room", "area", "surroundings", "zone",]
TestRoomDescription = "a small and uninteresting room. You don't remember how you got here, or even what this place is but you know it's the beginning of something much larger than you."
TestRoomContents = {
	"light" : 1,
	"box" : 1,
	"cloth" : 3,
	}
TestRoomExits = {
	"south" : "TestHall",
	}
TestRoom = Zone("Test Room", TestRoomReferences, TestRoomDescription, TestRoomContents, TestRoomExits, False, "none", "Not Locked, this is an error.", "Wasn't locked, this is an error.", False, "No key item, this is an error.", False, "none, error", "none")

TestHallReferences = ["room", "hall", "corridor", "area", "zone", "surroundings",]
TestHallDescription = "a long, seemingly endless hallway. No matter how far you walk down it's length the door you came in through is always right behind you."
TestHallContents = {
	"cloth" : 1,
	}
TestHallExits = {
	"north" : "TestRoom",
	}
TestHall = Zone("Test Hall", TestHallReferences, TestHallDescription, TestHallContents, TestHallExits, True, "key", "A heavy wooden door bars your way. A small tarnished keyhole stares at you defiantly.", "With a dry click the key turns in the lock and the door swings open with an eerie creak.", True, "As you attempt the retrieve the key from the lock it surrenders to the ravages of time, snapping off with a gentle clang. You won't be getting that back.", True, "enterZone", testEvent)
## END ZONE ASSIGNMENTS ##

## BEGIN PLAYER CREATION ##
pInv = {
		"clothing" : 1,
		"wallet" : 1,
		"shin" : 30,
		}
Player = PC("Dickbutt", pInv)
## END PLAYER CREATION ##

## BEGIN NPC CREATION ##
## END NPC CREATION ##

def checkForEvent(Location, Character, caller, situation):
	
	if(caller.bEvent == True):
		if(caller.Trigger == situation):
			caller.Event.triggerEvent(Location, Character)
		else:
			Scene(Location, Character)
	else:
		Scene(Location, Character)

def ChangeLocation(oldLocation, newLocation, Character):##This moves the player from oldLocation to newLocation. Moves the character class to maintain inventory and stats.
	print("You step out of the " + oldLocation.name + " and into " + newLocation.name + ", " + newLocation.description)
	checkForEvent(newLocation, Character, newLocation, "enterZone")

def Scene(Location, Character):##====This is the current scene. All commands and events should come back to this.
	cmd = input(">>>")
	
	for i in Commands:
		if(cmd.lower() == i):
			stingToClassDef(playerCommand, cmd.lower())(Location, Character)## This is where all player input is passed to the relevent command
			
	else:
		print("Command not recognised.")
		Scene(Location, Character)
			
def boot():##=========================Just the boot screen
	print("ITER: The Journey.")
	print("Coming Soon.")
	print("Type your name to enter the test room.")
	cmd = input(">>>")
	Player.name = cmd
	print("Welcome %s." % (Player.name))
	ChangeLocation(TestRoom, TestRoom, Player)

def stringToClass(str):##This is meant to turn strings into class names.
	return getattr(sys.modules[__name__], str)

def stingToClassDef(className, defName):##This takes strings and makes them a def name within a class. className.defName is the result. can be handed arguments
	return getattr(className, defName)
	
boot()##====================the only base level command if at all possible.
