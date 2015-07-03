import sys
import os
import time
import collections
import re
import random

class Person(object):##this is a generic person, with a name, inventory and basic add/remove item functions
	def __init__(self, name, description, inventory, Mind, Body, Spirit, HP, SP, MP, Attacks):
		self.name = name
		self.description = description
		self.inventory = inventory
		self.Mind = Mind
		self.Body = Body
		self.Spirit = Spirit
		self.HP = HP
		self.SP = SP
		self.MP = MP
		self.Attacks = Attacks
	
	def addToInventory(self, newItem, quantity):
		if(len(self.inventory) > 0):
			for i in self.inventory:
				if(newItem == i):
					self.inventory[i] = self.inventory[i] + quantity
					break
				else:
					self.inventory[newItem] = quantity
					break
		else:
			self.inventory[newItem] = quantity
			
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
	
class PC(Person):##this is the player character class, it adds a checkInventory function to the Person class
	def checkInventory(self):
		print("You take a moment to check what you're carrying.")
		
		if(self.inventory != {}):
			print("You have on you:")
			for i in self.inventory:
				if(self.inventory[i] > 1):
					print(str(self.inventory[i]) + " " + str(i) + "s")
				else:
					print(str(i))
		
		else:
			print("You don't seem to be carrying anything.")

class NPC(Person):##NPCs. Anything other than the player.
	def __init__(self, name, pronouns, inventory, Mind, Body, Spirit, HP, SP, MP, description, bEvent, Trigger, Event, Convo, bAggressive, Attacks):
		self.name = name
		self.pronouns = pronouns
		self.inventory = inventory
		self.Mind = Mind
		self.Body = Body
		self.Spirit = Spirit
		self.HP = HP
		self.SP = SP
		self.MP = MP
		self.description = description
		self.bEvent = bEvent
		self.Trigger = Trigger
		self.Event = Event
		self.Convo = Convo
		self.bAggressive = bAggressive
		self.Attacks = Attacks
		
	def describeNPC(self):
		print("%s is %s" % (self.name, self.description))
		if(self.body >= 100):
			print("%s looks in perfect health." % (self.pronouns["he"]))
		elif(self.body >= 50):
			print("%s looks a little worse for ware." % (self.pronouns["he"]))
		else:
			print("%s looks near death." % (self.pronouns["he"]))

class Zone(object):##this is all rooms and areas the player will be in. It has add/remove item functions and search/examine functions

	def __init__(self, name, references, description, contents, exits, bLocked, keyItem, blockedText, unlockText, bDestroyKey, keyDestroyText, bEvent, Trigger, Event, structures, npcs):
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
		self.structures = structures
		self.npcs = npcs
		
	def examineRoom(self):
		print("You are in a " + self.description)
		
	def searchRoom(self):
		print("You search the immediate area, and you find:")
		
		if(self.contents != {}):
			for i in self.contents:
				if(self.contents[i] == 1):
					print(stringToClass(i).name)
				else:
					print(str(self.contents[i])+ " " + i + "s")
		else:
			print("Nothing.")
		
		if(self.structures != []):
			print("In the %s you also see:" % (self.references[0]))
			for s in self.structures:
				print(stringToClass(s).name)
				
		if(self.exits != {}):
			print("And exits to the")
			for x in self.exits:
				print(x)
			
		if(self.npcs != []):
			for c in self.npcs:
				print("%s is here." % (stringToClass(c).name))
				
	def addItem(self, item, quantity):
		if(len(self.contents) > 0):
			for i in self.contents:
				if(item == i):
					self.contents[i] = self.contents[i] + quantity
					break		
				else:
					self.contents[item] = quantity
					break
		else:
			self.contents[item] = quantity
	
	def removeItem(self, item, quantity):
		for i in self.contents:
			if(i == item):
				if(self.contents[i] > quantity):
					self.contents[i] = self.contents[i] - quantity
					break
				else:
					del self.contents[i]
					break
	
	def addExit(self, direction, zone):
		for x in self.exits:
			if(x == direction):
				print("There is already an exit that way.")
				break
		else:
			self.exits[direction] = zone

	def removeExit(self, direction):
		for x in self.exits:
			if(x == direction):
				del self.exits[x]
				break
	
	def addStructure(self, newStructure):
		for i in self.structures:
			if(newStructure == i):
				break		
		else:
			self.structures.append(newStructure)
							
	def removeStucture(self, Structure):
		for i in self.structures:
			if(i == Structure):
				self.structures.remove(i)
				break
				
	def addNPC(self, NPC):
		for c in self.npcs:
			if(NPC == c):
				break
		else:
			self.npcs.append(NPC)
	
	def removeNPC(self, NPC):
		for c in self.npcs:
			if(c == NPC):
				self.npcs.remove(c)
				break
	
class Item(object):##this is a basic item, it has many many variables that cover its name and description and use, along with attached events
	
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

class Container(Item):##this is much like an item, except it has an inventory of its own, along with functionality to be opened and closed.
	
	tempD = {}

	def __init__(self, name, description, bPickUp, openDescription, contents, openText, closeText, bOpen, bUseable, bUseAlone, useWith, useText, bEvent, Trigger, Event, bLocked, keyItem, lockedText, unlockText, lockedDesc, bDestroyKey, keyDestroyText):
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
		self.bLocked = bLocked
		self.keyItem = keyItem
		self.lockedText = lockedText
		self.unlockText = unlockText
		self.lockedDesc = lockedDesc
		self.bDestroyKey = bDestroyKey
		self.keyDestroyText = keyDestroyText
		
	def describeItem(self):
		if(self.bOpen == False):
			if(self.bLocked == False):
				print("It's %s" % (self.description))
			else:
				print("It's %s" % (self.lockedDesc))
		else:
			print("It's %s" % (self.openDescription))
	
	def openContainer(self, Location, Character):
		if(self.bLocked == False):
			self.bOpen = True
			print(self.openText + " Inside you see")
			for i in self.contents:
				if(self.contents[i] > 1):
					print(str(self.contents[i]) + " " + i)
					Location.addItem(i, self.contents[i])
				else:
					print(i)
					Location.addItem(i, 1)
		else:
			for i in Character.inventory:
				if(i == self.keyItem):
					print(self.unlockText)
					self.bLocked = False
					if(self.bDestroyKey == True):
						print(self.keyDestroyText)
					self.bOpen = True
					print(self.openText + " Inside you see")
					for i in self.contents:
						if(self.contents[i] > 1):
							print(str(self.contents[i]) + " " + i)
							Location.addItem(i, self.contents[i])
						else:
							print(i)
							Location.addItem(i, 1)
					if(self.bDestroyKey == True):
						Character.removeFromInventory(self.keyItem, 1)
					break
			else:
				print(self.lockedText)
				
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

class Structure(object):##Base class for things like doors, walls and pillars of interest. Cannot be picked up.

	def __init__(self, name, description, bUseable, bUseAlone, otherItem, useEvent, bExamineEvent, examineEvent):
		self.name = name
		self.description = description
		self.bUseable = bUseable
		self.bUseAlone = bUseAlone
		self.otherItem = otherItem
		self.useEvent = useEvent
		self.bExamineEvent = bExamineEvent
		self.examineEvent = examineEvent
		
	def examineStructure(self, Location, Character):
		print("It's %s" % (self.description))
		
		if(self.bExamineEvent == True):
			self.examineEvent.triggerEvent(Location, Character)
	
	def useStructure(self, Location, Character):
		if(self.bUseable == True):
			if(self.bUseAlone == True):
				self.useEvent.triggerEvent(Location, Character)
			else:
				cmd = input("What do you want use on it? >>>")
				
				if(cmd.lower() == self.otherItem):
					for i in Character.inventory:
						if(cmd.lower == i):
							self.useEvent.triggerEvent(Location, Character)
							break
					else:
						print("You don't have a %s." % (cmd.lower()))
						Scene(Location, Character)
				else:
					for i in Character.inventory:
						if(cmd.lower == i):
							print("That doesn't seem to work.")
							Scene(Location, Character)
							break
					else:
						print("You don't have a %s." % (cmd.lower()))
						Scene(Location, Character)
		else:
			print("You don't see a way to use that.")
			Scene(Location, Character)
						
class Event(object):##these are events, where the majority of the Engines power comes from, events can print, add/remove items to the room and player, and teleport the player to a new location without informing them. Each command can only be used once it seems.
	
	activeNPC = "none"
	
	def __init__(self, Location, Character, EventActions, EventOrder, Repeat, bToConversation, NPC):
		self.Location = Location
		self.Character = Character
		self.EventActions = EventActions
		self.EventOrder = EventOrder
		self.Repeat = Repeat
		self.bToConversation = bToConversation
		self.NPC = NPC
		
	def triggerEvent(self, activeLocation, activeCharacter):##this runs through all the event items
	
		self.Location = activeLocation
		self.Character = activeCharacter
		
		if(self.Repeat >= 0):
			for e in self.EventOrder:
				if(e != "EVENT"):
					if(e != "RANDOMEVENT"):
						stringToClassDef(self, e)(self.EventActions[e])
						time.sleep(0.1)
					else:
						self.Repeat -= 1
						stringToClassDef(self, e)(self.EventActions[e])
				else:
					self.Repeat -= 1
					stringToClassDef(stringToClass(self.EventActions[e]), "triggerEvent")(self.Location, self.Character)
			self.Repeat -= 1
			if(self.bToConversation == False):
				Scene(self.Location, self.Character)
			else:
				Conversation(self.Location, self.Character, stringToClass(self.NPC), stringToClass(self.NPC).Convo["intro"], stringToClass(self.NPC).Convo["intro"])
		if(self.Repeat <= -1):
			for e in self.EventOrder:
				if(e != "EVENT"):
					if(e != "RANDOMEVENT"):
						stringToClassDef(self, e)(self.EventActions[e])
						time.sleep(0.1)
					else:
						self.Repeat -= 1
						stringToClassDef(self, e)(self.EventActions[e])
				else:
					stringToClassDef(stringToClass(self.EventActions[e]), "triggerEvent")(self.Location, self.Character)
			if(self.bToConversation == False):
				Scene(self.Location, self.Character)
			else:
				Conversation(self.Location, self.Character, stringToClass(self.NPC), stringToClass(self.NPC).Convo["intro"], stringToClass(self.NPC).Convo["intro"])
			
		else:
			if(self.bToConversation == False):
				Scene(self.Location, self.Character)
			else:
				Conversation(self.Location, self.Character, stringToClass(self.NPC), stringToClass(self.NPC).Convo["intro"], stringToClass(self.NPC).Convo["intro"])

	def PRINT(self, text):##Call to print something to screen.
		print(text)
	
	def ADDTOINVENTORY(self, item):##Call to add an item to the player character
		self.Character.addToInventory(item[0], item[1])
		
	def REMOVEFROMINVENTORY(self, item):##Call to remove an item from the player character
		self.Character.removeFromInventory(item[0], item[1])
		
	def ADDITEM(self, item):##Call to add an item to the surround area
		self.Location.addItem(item[0], item[1])
		
	def REMOVEITEM(self, item):##Call to remove an item from the surrounding area
		self.Location.removeItem(item[0], item[1])
		
	def TELEPORT(self, newLocation):##Call to teleport the player to a different room without telling them. Good for making a room 'change'
		self.Location = stringToClass(newLocation)

	def ADDEXIT(self, newExit):##This adds exits to the Location
		for x in newExit:
			self.Location.addExit(x, newExit[x])
			
	def REMOVEEXIT(self, delExit):##This removes and exit from the Location
		self.Location.removeExit(delExit)
	
	def WAIT(self, waitText):##Prints waitText and waits for input, does not save input. Use this for walls of text/page turning etc. I dont like the current functionality, but its the only way to actually make it reliable.
		os.system("echo %s" % (waitText))
		os.system("pause")
	
	def ADDSTRUCTURE(self, structure):##Adds a structure to the room
		self.Location.addStructure(structure)
	
	def REMOVESTRUCTURE(self, structure):## Removes a structure from the room.
		self.Location.removeStucture(structure)
	
	def ADDNPC(self, NPC):##Adds NPC to zone
		self.Location.addNPC(NPC)
		
	def REMOVENPC(self, NPC):##Removes an NPC from the zone
		self.Location.removeNPC(NPC)
	
	def ADDTONPCINVENTORY(self, item):##Adds item to the active NPCs inventory
		stringToClass(item[0]).addToInventory(item[1], item[2])
	
	def REMOVEFROMNPCINVENTORY(self, item):##Removes item from active NPC inventory.
		stringToClass(item[0]).removeFromInventory(item[1], item[2])

	def RANDOMEVENT(self, eventList):##Rolls through a list of events and picks one at random.
		stringToClassDef(stringToClass(eventList[random.randint(0, len(eventList)-1)]), "triggerEvent")(self.Location, self.Character)
	
	def MODIFYPCHP(self, mod):
		Character.HP += mod
	
	def MODIFYPCSP(self, mod):
		Character.SP += mod
	
	def MODIFYPCMP(self, mod):
		Character.MP += mod
		
	def MODIFYPCMIND(self, mod):
		Character.Mind += mod
		
	def MODIFYPCBODY(self, mod):
		Character.Body += mod
		
	def MODIFYPCSPIRIT(self, mod):
		Character.Spirit += mod
		
	def SETPCHP(self, mod):
		Character.HP = mod
	
	def SETPCSP(self, mod):
		Character.SP = mod
	
	def SETPCMP(self, mod):
		Character.MP = mod
		
	def SETPCMIND(self, mod):
		Character.Mind = mod
		
	def SETPCBODY(self, mod):
		Character.Body = mod
		
	def SETPCSPIRIT(self, mod):
		Character.Spirit = mod
			
class PlayerCommands(object):##These are all the commands the player can perform, they are as dynamic as possible.
	def __init__(self):
		pass
	
	def search(self, Location, Character, Command):##Search the area, makes the Zone print its contents
		Location.searchRoom()
		checkForEvent(Location, Character, Location, "searchZone")
	
	def examine(self, Location, Character, Command):##Examines the area, makes the Zone print its description
			
		if(len(Command) > 7):
			for i in Location.references:
				if(stringContains(i, Command) == True):
					Location.examineRoom()
					checkForEvent(Location, Character, Location, "examineZone")
					break
					
			for i in Location.contents:
				if(stringContains(i, Command) == True):
					stringToClass(i).describeItem()
					if(Location.contents[i] > 1):
						print("There are " + str(Location.contents[i]) + " of them.")
					checkForEvent(Location, Character, stringToClass(i), "examineItem")
					break
					
			for c in Location.npcs:
				if(stringContains(c, Command) == True):
					stringToClass(c).describeNPC()
					checkForEvent(Location, Character, stringToClass(c), "examineNPC")
					break
					
			for i in Player.inventory:
				if(stringContains(i, Command) == True):
					stringToClass(i).describeItem()
					if(Player.inventory[i] > 1):
						print("You are carrying " + str(Player.inventory[i]) + " of them.")
					checkForEvent(Location, Character, stringToClass(i), "examineItem")
					break
						
			for s in Location.structures:
				if(stringContains(s, Command) == True):
					stringToClass(s).examineStructure(Location, Character)
					break
			
		else:
			cmd = input("Examine what? >>>")
			
			for i in Location.references:
				if(cmd.lower() == i):
					Location.examineRoom()
					checkForEvent(Location, Character, Location, "examineZone")
					break
					
			for i in Location.contents:
				if(cmd.lower() == i):
					stringToClass(i).describeItem()
					if(Location.contents[i] > 1):
						print("There are " + str(Location.contents[i]) + " of them.")
					checkForEvent(Location, Character, stringToClass(i), "examineItem")
					break

			for c in Location.npcs:
				if(cmd.lower() == c):
					stringToClass(c).describeNPC()
					checkForEvent(Location, Character, stringToClass(c), "examineNPC")
					break
					
			for i in Player.inventory:
				if(cmd.lower() == i):
					stringToClass(i).describeItem()
					if(Player.inventory[i] > 1):
						print("You are carrying " + str(Player.inventory[i]) + " of them.")
					checkForEvent(Location, Character, stringToClass(i), "examineItem")
					break
			
			for s in Location.structures:
				if(cmd.lower() == s):
					stringToClass(s).examineStructure(Location, Character)
					break
				
			else:
				if(cmd.lower() == "self"):
					print("You are " + Character.name + ", a " + Character.description)
					print("----------")
					print("HP: %s" % (str(Character.HP)))
					print("SP: %s" % (str(Character.SP)))
					print("MP: %s" % (str(Character.MP)))
					print("----------")
					print("Body: %s" % (str(Character.Body)))
					print("Spirit: %s" % (str(Character.Spirit)))
					print("Mind: %s" % (str(Character.Mind)))
					print("----------")
					Scene(Location, Character)
				else:
					print("You don't see a %s here." % (cmd.lower()))
					Scene(Location, Character)
						
	def inventory(self, Location, Character, Command):##Checks the players Inventory, printing its contents
		Player.checkInventory()
		Scene(Location, Character)
		
	def quit(self, Location, Character, Command):##lets you quit, has a confirmation. NO SAVE BITCHES. YOLO
		cmd = input("Are you sure you want to quit?")
		
		if(cmd.lower() == "y" or cmd.lower() == "yes"):
			print("Shutting Down...")
			exit()
			
		else:
			Scene(Location, Character)
		
	def help(self, Location, Character, Command):##simply prints all the commands, no descriptions for you GLHF
		print("Available Commands:")
		for c in Commands:
			print(c)
		Scene(Location, Character)
		
	def open(self, Location, Character, Command):##used to open Container class items. toggles variables
			
		if(len(Command) > 4):
			for i in Location.contents:
				if(stringContains(i, Command) == True):
					if hasattr(stringToClass(i), "bOpen"):
						if(stringToClass(i).bOpen == False):
							stringToClass(i).openContainer(Location, Character)
							checkForEvent(Location, Character, stringToClass(i), "openContainer")

						else:
							print("It's already open.")
							Scene(Location, Character)
							
					else:
						print("You can't open that.")
						Scene(Location, Character)
			
		else:
			cmd = input("Open what? >>>")
			
			for i in Location.contents:
				if(i == cmd.lower()):
					if hasattr(stringToClass(i), "bOpen"):
						if(stringToClass(i).bOpen == False):
							stringToClass(i).openContainer(Location, Character)
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
		
	def close(self, Location, Character, Command):##used to close open Containers. toggles variables and re-checks contents in case of deletion.
			
		if(len(Command) > 5):
			for i in Location.contents:
				if(stringContains(i, Command) == True):
					if hasattr(stringToClass(i), "bOpen"):
						if(stringToClass(i).bOpen == True):
							stringToClass(i).closeContainer(Location, Character)
							checkForEvent(Location, Character, stringToClass(i), "closeContainer")

						else:
							print("It's already closed.")
							Scene(Location, Character)
					else:
						print("You can't close that.")
						Scene(Location, Character)
			
		else:
			cmd = input("Close what? >>>")
			
			for i in Location.contents:
				if(i == cmd.lower()):
					if hasattr(stringToClass(i), "bOpen"):
						if(stringToClass(i).bOpen == True):
							stringToClass(i).closeContainer(Location, Character)
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

	def take(self, Location, Character, Command):##lets the player pick up Items marked as pickupable.
			
		if(len(Command) > 4):
			for l in Location.contents:
				if(stringContains(l, Command) == True):
					if(stringToClass(l).bPickUp == True):
						Character.addToInventory(l, Location.contents[l])
						Location.removeItem(l, Location.contents[l])
						print("You pick up the %s." % (l))
						checkForEvent(Location, Character, stringToClass(l), "pickupItem")

					else:
						print("You can't pick that up.")
						Scene(Location, Character)
			
		else:
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
			
	def drop(self, Location, Character, Command):##drops an item from the inventory to the zone. will go back into a container it came from
		
		if(len(Command) > 4):
			for l in Character.inventory:
				if(stringContains(l, Command) == True):
					q = input("Drop how many? >>>")
						
					try:
						if(int(q) <= Character.inventory[l]):
							Character.removeFromInventory(l, int(q))
							Location.addItem(l, int(q))
							print("You drop the %s." % (l))
							checkForEvent(Location, Character, stringToClass(l), "dropItem")

						else:
							print("You don't have that many " + l +"s.")
							Scene(Location, Character)
					except:
						print("That's not a number!")
						Scene(Location, Character)
					
		else:
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
			
	def move(self, Location, Character, Command):##moves the character from one location to another.
		
		if(len(Command) > 4):
			for d in Location.exits:
				if(stringContains(d, Command) == True):
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
		
		else:
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
	
	def use(self, Location, Character, Command):##Uses items, duh ISSUE HERE WITH THE SECOND USE WITH WHAT COMMAND NOT INTELLIGENT
		
		if(len(Command) > 3):
			for i in Character.inventory:
				if(stringContains(i, Command) == True):
					if(stringToClass(i).bUseable == True):
							if(stringToClass(i).bUseAlone == True):
								print(stringToClass(i).useText)
								checkForEvent(Location, Character, stringToClass(i), "useItem")
								break

							else:
								u = input("Use with what? >>>")
								for x in Character.inventory:
									if(stringContains(x, u) == True):
										if(stringToClass(i).useWith == x):
											print(stringToClass(i).useText)
											checkForEvent(Location, Character, stringToClass(i), "useItem")
											break

										else:
											print("You can't use those together.")
											Scene(Location, Character)
								for x in Location.contents:
									if(stringContains(x, u) == True):
										if(stringToClass(i).useWith == x):
											print(stringToClass(i).useText)
											checkForEvent(Location, Character, stringToClass(i), "useItem")
											break

										else:
											print("You can't use those together.")
											Scene(Location, Character)
											break
								else:
									print("There isn't a %s here." % (u.lower()))
									Scene(Location, Character)
									break
					else:
						print("You can't use that.")
						Scene(Location, Character)
						break

			for i in Location.contents:
				if(stringContains(i, Command) == True):
					if(stringToClass(i).bUseable == True):
						if(stringToClass(i).bUseAlone == True):
							print(stringToClass(i).useText)
							checkForEvent(Location, Character, stringToClass(i), "useItem")
							break

						else:
							u = input("Use with what? >>>")
							for x in Character.inventory:
								if(stringContains(x, u) == True):
									if(stringToClass(i).useWith == x):
										print(stringToClass(i).useText)
										checkForEvent(Location, Character, stringToClass(i), "useItem")
										break

									else:
										print("You can't use those together.")
										Scene(Location, Character)
										break
							for x in Location.contents:
								if(stringContains(x, u) == True):
									if(stringToClass(i).useWith == x):
										print(stringToClass(i).useText)
										checkForEvent(Location, Character, stringToClass(i), "useItem")
										break

									else:
										print("You can't use those together.")
										Scene(Location, Character)
										break
							else:
								print("There isn't a %s here." % (u.lower()))
								Scene(Location, Character)
								break
					else:
						print("You can't use that.")
						Scene(Location, Character)
						break

			for s in Location.structures:
				if(stringContains(s, Command) == True):
					stringToClass(s).useStructure(Location, Character)
					break
			
			
		else:
			cmd = input("Use what? >>>")
			
			for i in Character.inventory:
				if(cmd.lower() == i):
					if(stringToClass(cmd.lower()).bUseable == True):
						if(stringToClass(cmd.lower()).bUseAlone == True):
							print(stringToClass(cmd.lower()).useText)
							checkForEvent(Location, Character, stringToClass(i), "useItem")
							break

						else:
							u = input("Use with what? >>>")
							for x in Character.inventory:
								if(u.lower() == x):
									if(stringToClass(cmd.lower()).useWith == x):
										print(stringToClass(cmd.lower()).useText)
										checkForEvent(Location, Character, stringToClass(i), "useItem")
										break

									else:
										print("You can't use those together.")
										Scene(Location, Character)
							for x in Location.contents:
								if(u.lower() == x):
									if(stringToClass(cmd.lower()).useWith == x):
										print(stringToClass(cmd.lower()).useText)
										checkForEvent(Location, Character, stringToClass(i), "useItem")
										break

									else:
										print("You can't use those together.")
										Scene(Location, Character)
										break
							else:
								print("There isn't a %s here." % (u.lower()))
								Scene(Location, Character)
								break
					else:
						print("You can't use that.")
						Scene(Location, Character)
						break
			
			for i in Location.contents:
				if(cmd.lower() == i):
					if(stringToClass(cmd.lower()).bUseable == True):
						if(stringToClass(cmd.lower()).bUseAlone == True):
							print(stringToClass(cmd.lower()).useText)
							checkForEvent(Location, Character, stringToClass(i), "useItem")
							break

						else:
							u = input("Use with what? >>>")
							for x in Character.inventory:
								if(u.lower() == x):
									if(stringToClass(cmd.lower()).useWith == x):
										print(stringToClass(cmd.lower()).useText)
										checkForEvent(Location, Character, stringToClass(i), "useItem")
										break

									else:
										print("You can't use those together.")
										Scene(Location, Character)
										break
							for x in Location.contents:
								if(u.lower() == x):
									if(stringToClass(cmd.lower()).useWith == x):
										print(stringToClass(cmd.lower()).useText)
										checkForEvent(Location, Character, stringToClass(i), "useItem")
										break

									else:
										print("You can't use those together.")
										Scene(Location, Character)
										break
							else:
								print("There isn't a %s here." % (u.lower()))
								Scene(Location, Character)
								break
					else:
						print("You can't use that.")
						Scene(Location, Character)
						break
			
			for s in Location.structures:
				if(cmd.lower() == s):
					stringToClass(s).useStructure(Location, Character)
					break
			
			else:
				print("There isn't a %s here." % (cmd.lower()))
				Scene(Location, Character)

	def talk(self, Location, Character, Command):##talk to NPCs and hear the shit they have to say
		
		if(len(Command) > 4):
			for c in Location.npcs:
				if(stringContains(c, Command) == True):
					print("<<" + stringToClass(c).name + "<<" + stringToClass(c).Convo["intro"]["introtext"])
					Conversation(Location, Character, stringToClass(c), stringToClass(c).Convo["intro"], stringToClass(c).Convo["intro"])
					break
		else:
			cmd = input("Who do you want to talk to? >>>")
			
			for c in Location.npcs:
				if(cmd.lower() == c):
					print(stringToClass(c).Convo["intro"]["introtext"])
					Conversation(Location, Character, stringToClass(c), stringToClass(c).Convo["intro"], stringToClass(c).Convo["intro"])
					break
			else:
				print("You don't see anyone called %s here." % (cmd))
				Scene(Location, Character)
	
	def attack(self, Location, Character, Command):##Use this to attack people, you monster
	
		if(len(Command) > 6):
			for c in Location.npcs:
				if(stringContains(c, Command) == True):
					print("You make a move towards %s, and they turn to face you, seeing your intent. You've a fight on your hands." % stringToClass(c).name)
					stringToClass(c).bAggressive = True
					Scene(Location, Character)
					break
		else:
			cmd = input("Who do you want to attack? >>>")
			
			for c in Location.npcs:
				if(stringContains(c, cmd) == True):
					print("You make a move towards %s, and they turn to face you, seeing your intent. You've a fight on your hands." % (stringToClass(c).name))
					stringToClass(c).bAggressive = True
					Scene(Location, Character)
					break
					
			else:
				print("You don't see %s here." % (cmd))
				Scene(Location, Character)
			
	def self(self, Location, Character, Command):
		print("You are " + Character.name + ", a " + Character.description)
		print("----------")
		print("HP: %s" % (str(Character.HP)))
		print("SP: %s" % (str(Character.SP)))
		print("MP: %s" % (str(Character.MP)))
		print("----------")
		print("Body:   %s" % (str(Character.Body)))
		print("Spirit: %s" % (str(Character.Spirit)))
		print("Mind:   %s" % (str(Character.Mind)))
		Scene(Location, Character)
	
## START PLAYER COMMANDS## NO TOUCHING ##
Commands = ["search", "examine", "inventory", "quit", "help", "open", "close", "take", "drop", "move", "use", "talk", "attack", "self"]
playerCommand = PlayerCommands()
## END PLAYER COMMANDS## NO TOUCHING ##

###########################
##ASSIGN ALL CLASSES HERE##
###########################

## BEGIN PLAYER CREATION ##
pInv = {}
playerAttacks = {
	"HP": ["You strike out at the enemy,", "With a yell you batter your opponent with a series of blows,"],
	"SP" : ["You yell in an attempt intimidate the enemy,", "You sling a slew of insults at your opponent,"],
	"MP" : ["Summoning your inner reserves, you focus energy at your enemy,", "You thrust forward your arm, letting out a stream of energy,"]
	}
Player = PC("Dickbutt", "short, ugly and kind of intangible being who is the closest thing to a human without actually being one. Weird.", pInv, 10, 10, 10, 100, 100, 100, playerAttacks)
## END PLAYER CREATION ##

## BEGIN EVENT ASSIGNMENTS ##

## END EVENT ASSIGNMENTS ##

## BEGIN ITEM/CONTAINER ASSIGNMENTS ##

## END ITEM/CONTAINER ASSIGNMENTS ##

## BEGIN ITEM/CONTAINER LIST ##
itemList = []
## END ITEM/CONTAINER LIST ##

## BEGIN STRUCTURE ASSIGNMENTS ##

## END STRUCTURE ASSIGNMENTS ##

## BEGIN STRUCTURE LIST ##
structureList = []
## END STRUCTURE LIST ##

## BEGIN ZONE ASSGNMENTS ##
TestRoomReferences = ["room", "area", "surroundings", "zone",]
TestRoomDescription = "a small and uninteresting room. You don't remember how you got here, or even what this place is but you know it's the beginning of something much larger than you."
TestRoomContents = {}
TestRoomExits = {}
TestRoomStructures = []
TestRoomNPCs = []
TestRoom = Zone("Test Room", TestRoomReferences, TestRoomDescription, TestRoomContents, TestRoomExits, False, "none", "Not Locked, this is an error.", "Wasn't locked, this is an error.", False, "No key item, this is an error.", False, "none", "none", TestRoomStructures, TestRoomNPCs)
## END ZONE ASSIGNMENTS ##

## BEGIN NPC CREATION ##

## END NPC CREATION ##

def stringContains(word, phrase):##this guy finds a word in a phrase, and can be asked in a manner consistent with the rest of python.
	if(findWord(word)(phrase)):
		return True
	else:
		return False

def findWord(w):##This guy finds if a word is in a phrase, intelligently
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

def bDeeper(dictValue):##This checks if there i a deeper level of conversation
	try:
		x = len(dictValue.keys())
		return True
	except:
		return False
	
def Conversation(Location, Character, NPC, stage, previousStage):##conversation 'scene'. KISS STRIKES AGAIN, WAIT EVENT NOT WORKING
	
	cmd = input(">>Say>>")
	
	if(cmd.lower() == "back" or cmd.lower() == "nevermind"):
		print("<<" + NPC.name + "<<" + previousStage["introtext"])
		Conversation(Location, Character, NPC, previousStage, NPC.Convo["intro"])
		
	if("bye" in cmd.lower() or stringContains("leave", cmd) == True or "farewell" in cmd.lower()):
		print("<<" + NPC.name + "<<" + NPC.Convo["intro"]["goodbye"])
		Scene(Location, Character)

	for i in stage:
		if(stringContains(i, cmd.lower()) == True):
			if(bDeeper(stage[i]) == True):
				print("<<" + NPC.name + "<<" + stage[i]["introtext"])
				if(NPC.bEvent == False):
					Conversation(Location, Character, NPC, stage[i], stage)
					break
				else:
					for e in NPC.Event.keys():
						if(i in e):
							stringToClass(NPC.Event[e]).triggerEvent(Location, Character)
							break
					else:
						Conversation(Location, Character, NPC, stage[i], stage)
						break
					
			else:
				if(NPC.bEvent == False):
					print("<<" + NPC.name + "<<" + stage[i])
					Conversation(Location, Character, NPC, stage, previousStage)
					break
				else:
					print("<<" + NPC.name + "<<" + stage[i])
					for e in NPC.Event:
						if(i in e):##+++++++++++++++++++++++++++++++++++++++++++CLOSER
							stringToClass(NPC.Event[e]).triggerEvent(Location, Character)
							break
					else:
						Conversation(Location, Character, NPC, stage, previousStage)
						break
	else:
		print("%s looks confused." % (NPC.name))
		print("<<" + NPC.name + "<<" + NPC.Convo["intro"]["none"])
		Conversation(Location, Character, NPC, stage, previousStage)
				
def checkForEvent(Location, Character, caller, situation):##Call this to check if an event should be run.

	if(caller.bEvent == True):

		if(caller.Trigger == situation):
			caller.Event.triggerEvent(Location, Character)
		else:
			Scene(Location, Character)
	else:
		Scene(Location, Character)

def ChangeLocation(oldLocation, newLocation, Character):##This moves the player from oldLocation to newLocation. Moves the character class to maintain inventory and stats.
	print("You step out of the " + oldLocation.name + " and into " + newLocation.name + ", " + newLocation.description)
	if(newLocation.npcs != []):
		for c in newLocation.npcs:
			print("%s is here." % (stringToClass(c).name))
	checkForEvent(newLocation, Character, newLocation, "enterZone")

def Scene(Location, Character):##====This is the current scene. All commands and events should come back to this.
	for c in Location.npcs:
		if stringToClass(c).bAggressive == True:
			print("Battle because %s wants to fight." % (stringToClass(c).name))
			print("----------")
			Battle(Character, stringToClass(c), Location)
			break
	else:
		print("----------")##clock could go here.
		cmd = input(">>>")
		
		for i in Commands:
			if(stringContains(i, cmd) == True):
				stringToClassDef(playerCommand, i)(Location, Character, cmd)## This is where all player input is passed to the relevant command
				
		else:
			print("Command not recognised.")
			Scene(Location, Character)

def stringToClass(str):##This is meant to turn strings into class names.
	return getattr(sys.modules[__name__], str)

def stringToClassDef(className, defName):##This takes strings and makes them a def name within a class. className.defName is the result. can be handed arguments
	return getattr(className, defName)
	
def enemyAttack(player, enemy, location, bDefend):
	atk = random.randint(0, 2)
	
	if(bDefend == False):
		if atk == 0:
			if(player.Body + random.randint(1, 20) < enemy.Body + random.randint(1, 20)):
				Edmg = int(random.randint(0, enemy.HP) / 2)
				print(enemy.Attacks["HP"][random.randint(0, len(enemy.Attacks["HP"])-1)])
				print("You receive " + str(Edmg) + " HP damage.")
				player.HP -= Edmg
				print("----------")
				if player.HP <= 0:
					enemy.bAggressive = False
					BattleComplete("playerHP_Lose", player, enemy, location)
				else:
					Battle(player, enemy, location)

			else:
				print(enemy.Attacks["HP"][random.randint(0, len(enemy.Attacks["HP"])-1)])
				print("You manage to avoid taking damage.")
				print("----------")
				Battle(player, enemy, location)
				
		if atk == 1:
			if(player.Spirit + random.randint(1, 20) < enemy.Spirit + random.randint(1, 20)):
				Edmg = int(random.randint(0, enemy.SP) / 2)
				print(enemy.Attacks["SP"][random.randint(0, len(enemy.Attacks["SP"])-1)])
				print("You receive " + str(Edmg) + " SP damage.")
				player.SP -= Edmg
				print("----------")
				if player.SP <= 0:
					enemy.bAggressive = False
					BattleComplete("playerSP_Lose", player, enemy, location)
				else:
					Battle(player, enemy, location)
			else:
				print(enemy.Attacks["SP"][random.randint(0, len(enemy.Attacks["SP"])-1)])
				print("You manage to avoid taking damage.")
				print("----------")
				Battle(player, enemy, location)
				
		if atk == 2:
			if(player.Mind + random.randint(1, 20) < enemy.Mind + random.randint(1, 20)):
				Edmg = int(random.randint(0, enemy.MP) / 2)
				print(enemy.Attacks["MP"][random.randint(0, len(enemy.Attacks["MP"])-1)])
				print("You receive " + str(Edmg) + " MP damage.")
				player.MP -= Edmg
				print("----------")
				if player.MP <= 0:
					enemy.bAggressive = False
					BattleComplete("playerMP_Lose", player, enemy, location)
				else:
					Battle(player, enemy, location)
			else:
				print(enemy.Attacks["MP"][random.randint(0, len(enemy.Attacks["MP"])-1)])
				print("You manage to avoid taking damage.")
				print("----------")
				Battle(player, enemy, location)
				
	else:
		if atk == 0:
			if(player.Body + random.randint(10, 30) < enemy.Body + random.randint(1, 20)):
				Edmg = int(random.randint(0, enemy.HP) / 2)
				print(enemy.Attacks["HP"][random.randint(0, len(enemy.Attacks["HP"])-1)])
				print("You receive " + str(Edmg) + " HP damage.")
				player.HP -= Edmg
				print("----------")
				if player.HP <= 0:
					enemy.bAggressive = False
					BattleComplete("playerHP_Lose", player, enemy, location)
				else:
					Battle(player, enemy, location)
			else:
				print(enemy.Attacks["HP"][random.randint(0, len(enemy.Attacks["HP"])-1)])
				print("You manage to avoid taking damage.")
				print("----------")
				Battle(player, enemy, location)
				
		if atk == 1:
			if(player.Spirit + random.randint(10, 30) < enemy.Spirit + random.randint(1, 20)):
				Edmg = int(random.randint(0, enemy.SP) / 2)
				print(enemy.Attacks["SP"][random.randint(0, len(enemy.Attacks["SP"])-1)])
				print("You receive " + str(Edmg) + " SP damage.")
				player.SP -= Edmg
				print("----------")
				if player.SP <= 0:
					enemy.bAggressive = False
					BattleComplete("playerSP_Lose", player, enemy, location)
				else:
					Battle(player, enemy, location)
			else:
				print(enemy.Attacks["SP"][random.randint(0, len(enemy.Attacks["SP"])-1)])
				print("You manage to avoid taking damage.")
				print("----------")
				Battle(player, enemy, location)
				
		if atk == 2:
			if(player.Mind + random.randint(10, 30) < enemy.Mind + random.randint(1, 20)):
				Edmg = int(random.randint(0, enemy.MP) / 2)
				print(enemy.Attacks["MP"][random.randint(0, len(enemy.Attacks["MP"])-1)])
				print("You receive " + str(Edmg) + " MP damage.")
				player.MP -= Edmg
				print("----------")
				if player.MP <= 0:
					enemy.bAggressive = False
					BattleComplete("playerMP_Lose", player, enemy, location)
				else:
					Battle(player, enemy, location)
			else:
				print(enemy.Attacks["MP"][random.randint(0, len(enemy.Attacks["MP"])-1)])
				print("You manage to avoid taking damage.")
				print("----------")
				Battle(player, enemy, location)		

def BattleComplete(cause, PC, NPC, location):##called when the battle is complete.
	if(len(NPC.inventory) > 0):
		print("The %s is defeated, dropping:" % NPC.name)
		for i in NPC.inventory:
			location.addItem(i, NPC.inventory[i])
			if NPC.inventory[i] > 1:
				print(str(NPC.inventory[i]) + " " + i + "s")
			else:
				print("a %s" % i)
	else:
		print("The %s is defeated, dropping no items." % NPC.name)
	print("----------")
	stringToClass(NPC.Event[cause]).triggerEvent(location, PC)
			
def Battle(player, enemy, location):

	print("You are battling a " + enemy.name + ", " + enemy.description)
	
	if enemy.HP >= (enemy.Body * 10 / 2):
		print("It looks in perfect health.")
	if enemy.HP <= (enemy.Body * 10 / 4):
		print("It looks a little shaky on its feet.")
	if enemy.HP <= (enemy.Body):
		print("It looks near death.")

	print("----------")
	print("HP: %s" % (str(player.HP)))
	print("SP: %s" % (str(player.SP)))
	print("MP: %s" % (str(player.MP)))
	print("----------")
	cmd = input(">>Attack>>")
	print("----------")
	
	if cmd.lower() == "help":
		print("Available Battle Commands:")
		print("'Body'   -   A basic attack.")
		print("'Spirit' -   Perform a spiritual attack on your enemy.")
		print("'Mind'   -   Attack your enemy's mind.")
		print("'Defend' -   Ready yourself for any enemy attack.")
		print("----------")
		Battle(player, enemy, location)
	
	if cmd.lower() == "body":
		if(player.Body + random.randint(1, 20) > enemy.Body + random.randint(1, 20)):
			dmg = int(random.randint(0, player.HP) / 2)
			print(player.Attacks["HP"][random.randint(0, len(player.Attacks["HP"]) -1)] + " causing " + str(dmg) + " HP damage.")
			enemy.HP -= dmg
			print("----------")
			
			if enemy.HP <= 0:
				enemy.bAggressive = False
				BattleComplete("playerHP_Victory", player, enemy, location)
			
			else:		
				enemyAttack(player, enemy, location, False)
		else:
			print(player.Attacks["HP"][random.randint(0, len(player.Attacks["HP"]) -1)] + " but your attack misses.")
			print("----------")
			enemyAttack(player, enemy, location, False)
				
	if cmd.lower() == "spirit":
		if(player.Spirit + random.randint(1, 20) > enemy.Spirit + random.randint(1, 20)):
			dmg = int(random.randint(0, player.SP) / 2)
			print(player.Attacks["SP"][random.randint(0, len(player.Attacks["SP"]) -1)] + " causing " + str(dmg) + " SP damage.")
			enemy.SP -= dmg
			print("----------")
			
			if enemy.SP <= 0:
				enemy.bAggressive = False
				BattleComplete("playerSP_Victory", player, enemy, location)
			
			else:		
				enemyAttack(player, enemy, location, False)
		else:
			print(player.Attacks["SP"][random.randint(0, len(player.Attacks["SP"]) -1)] + " but your attack fails.")
			print("----------")
			enemyAttack(player, enemy, location, False)
				
	if cmd.lower() == "mind":
		if(player.Mind + random.randint(1, 20) > enemy.Mind + random.randint(1, 20)):
			dmg = int(random.randint(0, player.MP) / 2)
			print(player.Attacks["MP"][random.randint(0, len(player.Attacks["MP"]) -1)] + " causing " + str(dmg) + " MP damage.")
			enemy.MP -= dmg
			print("----------")
			
			if enemy.MP <= 0:
				enemy.bAggressive = False
				BattleComplete("playerMP_Victory", player, enemy, location)
			
			else:		
				enemyAttack(player, enemy, location, False)
		else:
			print(player.Attacks["MP"][random.randint(0, len(player.Attacks["MP"]) -1)] + " but your attack fails.")
			print("----------")
			enemyAttack(player, enemy, location, False)

	if cmd.lower() == "defend":
		print("You ready yourself for any attacks that may come.")
		print("----------")
		enemyAttack(player, enemy, location, True)
			
	else:
		print("Command not recognized")
		print("----------")
		Battle(player, enemy, location)
		
def boot():##=========================Just the boot screen
	print("ITER: The Journey.")
	print("Coming Soon.")
	print("----------")
	print("Type your name to enter the test room.")
	cmd = input(">>>")
	Player.name = cmd
	print("Welcome %s." % (Player.name))
	print("----------")
	ChangeLocation(TestRoom, TestRoom, Player)

boot()##====================the only base level command if at all possible.
