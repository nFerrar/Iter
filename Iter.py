import sys
import os
import time
import collections
import re
import random

class Person(object):##this is a generic person, with a name, inventory and basic add/remove item functions
	def __init__(self, name, inventory, mind, body, spirit):
		self.name = name
		self.inventory = inventory
		self.mind = mind
		self.body = body
		self.spirit = spirit
	
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
	
class PC(Person):##this is the player character class, it adds a checkInventory function to the Person class
	def checkInventory(self):
		print("You take a moment to check what you're carrying.")
		print("You have on you:")
		for i in self.inventory:
			if(self.inventory[i] > 1):
				print(str(self.inventory[i]) + " " + str(i) + "s")
			else:
				print(str(i))

class NPC(Person):##NPCs. Anything other than the player.
	def __init__(self, name, pronouns, inventory, mind, body, spirit, description, bEvent, Trigger, Event, Convo):
		self.name = name
		self.pronouns = pronouns
		self.inventory = inventory
		self.mind = mind
		self.body = body
		self.spirit = spirit
		self.description = description
		self.bEvent = bEvent
		self.Trigger = Trigger
		self.Event = Event
		self.Convo = Convo
		
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
		self.Character.addToInventory(item, 1)
		
	def REMOVEFROMINVENTORY(self, item):##Call to remove an item from the player character
		self.Character.removeFromInventory(item, 1)
		
	def ADDITEM(self, item):##Call to add an item to the surround area
		self.Location.addItem(item, 1)
		
	def REMOVEITEM(self, item):##Call to remove an item from the surrounding area
		self.Location.removeItem(item, 1)
		
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
	
	def SETACTIVENPC(self, NPC):##Sets the active NPC, so the NPC can be interacted with specifically.
		activeNPC = NPC
	
	def ADDTONPCINVENTORY(self, item):##Adds item to the active NPCs inventory
		if(activeNPC != "none"):
			stringToClass(activeNPC).addToInventory(item, 1)
		else:
			print("No active NPC set in event.")
	
	def REMOVEFROMACTIVENPCINVENTORY(self, item):##Removes item from active NPC inventory.
		if(activeNPC != "none"):
			stringToClass(activeNPC).removeFromInventory(item, 1)

	def RANDOMEVENT(self, eventList):##Rolls through a list of events and picks one at random.
		stringToClassDef(stringToClass(eventList[random.randint(0, len(eventList)-1)]), "triggerEvent")(self.Location, self.Character)
			
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
				if(stringContains(s, Commands) == True):
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
		
	def help(self, Location, Character, Command):##siply prints all the commands, no descriptions for you
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
	
###########################
##ASSIGN ALL CLASSES HERE##
###########################

## START PLAYER COMMANDS##
Commands = ["search", "examine", "inventory", "quit", "help", "open", "close", "take", "drop", "move", "use", "talk"]
playerCommand = PlayerCommands()
## END PLAYER COMMANDS##

## BEGIN PLAYER CREATION ##
pInv = {
		"clothing" : 1,
		"wallet" : 1,
		"shin" : 30,
		}
Player = PC("Dickbutt", pInv, 100, 100, 100)
## END PLAYER CREATION ##

## BEGIN EVENT ASSIGNMENTS ##
testEventActions = {
	"PRINT" : "It seems you won't be able to go any further for now, have some clothes and a wallet.",
	"ADDTOINVENTORY" : "clothing",
	"ADDITEM" : "wallet",
	}
testEventOrder = ["PRINT", "ADDTOINVENTORY", "ADDITEM"]
testEvent = Event("none", "none", testEventActions, testEventOrder, -1, False, "none")

boxEventActions = {
	"PRINT" : "You somehow manage to pinch your fingers as you close it, man it would be stupid if you did that every time you closed this box...",
	"EVENT" : "secondEvent",
	}
boxEventOrder = ["PRINT", "EVENT"]
boxEvent = Event("none", "none", boxEventActions, boxEventOrder,  2, False, "none")

secondEventAction = {
	"PRINT" : "Turns out you can trigger events from events. This is good news.",
	"WAIT" : "And you are restricted to a single instance of each operation per event. So long, complicated events will have to be split up between multiple events. This is a pain."
	}
secondEventOrder = ["PRINT", "WAIT"]
secondEvent = Event("none", "none", secondEventAction, secondEventOrder, 1, False, "none")

bulbEventActions = {
	"ADDTOINVENTORY" : "lightbulb",
	"TELEPORT" : "DarkTestRoom",
	"PRINT" : "Once you remove the lightbulb the room and you are both plunged into inky blackness, now you can't see!",
	"WAIT" : "However, in the dark, you notice a strange, thin line of light coming off the wall. If you could see you might be able to go and investigate.",
	}
bulbEventOrder = ["ADDTOINVENTORY", "TELEPORT", "PRINT", "WAIT"]
bulbEvent = Event("none", "none", bulbEventActions, bulbEventOrder, -1, False, "none")

socketEventActions = {
	"REMOVEFROMINVENTORY" : "lightbulb",
	"TELEPORT" : "TestRoom",
	"PRINT" : "You can see again! That's better. Now, about that suspicious wall.",
	"ADDSTRUCTURE" : "wall",
	} 
socketEventOrder = ["REMOVEFROMINVENTORY", "TELEPORT", "PRINT", "ADDSTRUCTURE"]
socketEvent = Event("none", "none", socketEventActions, socketEventOrder, -1, False, "none")

dropClothesEventActions = {
	"PRINT" : "You feel a little cold without your clothes on, and you doubt you'll be able to engage in decent society if you don't remedy the situation.",
	}
dropEventOrder = ["PRINT",]
dropClothesEvent = Event("none", "none", dropClothesEventActions, dropEventOrder, -1, False, "none")

pickupKeyEventActions = {
	"PRINT" : "As you hold the key in your hand, you get a sense of great...contextual importance."
	}
pickupKeyEventOrder = ["PRINT",]
pickupKeyEvent = Event("none", "none", pickupKeyEventActions, pickupKeyEventOrder, -1, False, "none")

hiddenDoorEventActions = {
	"PRINT" : "As you apply some pressure to the wall, there is a creak, thunk, and rattle as the section of wall shifts back and rises up into the ceiling in a shower of dust, revealing a small exit to the east.",
	"ADDEXIT" : {"east" : "TestSecretRoom"},
	"REMOVESTRUCTURE" : "wall",
	}
hiddenDoorEventOrder = ["PRINT", "ADDEXIT", "REMOVESTRUCTURE"]
hiddenDoorEvent = Event("none", "none", hiddenDoorEventActions, hiddenDoorEventOrder, 1, False, "none")

bobFuckEventActions = {
	"PRINT" : "<<Bob<<'Why you gotta be so rude?'",
	}
bobFuckEventOrder = ["PRINT"]
bobFuckEvent = Event("none", "none", bobFuckEventActions, bobFuckEventOrder, -1, True, "bob")

bobMeEventActons = {
	"PRINT" : "<<Bob<<'You know, these kind of things wouldn't happen in a modern RPG.'",
	}
bobMeEventOrder = ["PRINT"]
bobMeEvent = Event("none", "none", bobMeEventActons, bobMeEventOrder, -1, True, "bob")

bobHowEventActions = {
	"PRINT" : "Bob seems to sigh deeply and stares at you with his dead little eyes. It's incredibly awkward.",
	"WAIT" : "He just keeps staring.....",
	}
bobHowEventOrder = ["PRINT", "WAIT"]
bobHowEvent = Event("none", "none", bobHowEventActions, bobFuckEventOrder, -1, True, "bob")

bobLightsEventActions = {
	"PRINT" : "<<Bob<<'Turn the fucking light back on you fuckwit.'",
	"WAIT" : "His voice carries the implication of violence.",
	}
bobLighsEventOrder = ["PRINT", "WAIT"]
bobLightsEvent = Event("none", "none", bobLightsEventActions, bobLighsEventOrder, -1, False, "none")

randEvent1Actions = {
	"PRINT" : "Random Event 1",
	}
randEvent1Order = ["PRINT"]
randEvent1 = Event("none", "none", randEvent1Actions, randEvent1Order, -1, False, "none")

randEvent2Actions = {
	"PRINT" : "Random Event 2",
	}
randEvent2Order = ["PRINT"]
randEvent2 = Event("none", "none", randEvent2Actions, randEvent2Order, -1, False, "none")

randEvent3Actions = {
	"PRINT" : "Random Event 3",
	}
randEvent3Order = ["PRINT"]
randEvent3 = Event("none", "none", randEvent3Actions, randEvent3Order, -1, False, "none")

rollEventActions = {
	"PRINT" : "Rolling random Event...",
	"RANDOMEVENT" : ["randEvent1", "randEvent2", "randEvent3",],
	}
rollEventOrder = ["PRINT", "RANDOMEVENT",]
rollEvent = Event("none", "none", rollEventActions, rollEventOrder, 1, False, "none")
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

## BEGIN STRUCTURE ASSIGNMENTS ##
wall = Structure("a suspicious wall", "a wall that seems a little off. With a closer inspection, it almost sounds hollow.", False, False, "none", "none", True, hiddenDoorEvent)
## END STRUCTURE ASSIGNMENTS ##

## BEGIN STRUCTURE LIST ##
structureList = ["wall",]
## END STRUCTURE LIST ##

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
TestRoomStructures = []
TestRoomNPCs = ["bob"]
TestRoom = Zone("Test Room", TestRoomReferences, TestRoomDescription, TestRoomContents, TestRoomExits, False, "none", "Not Locked, this is an error.", "Wasn't locked, this is an error.", False, "No key item, this is an error.", True, "enterZone", rollEvent, TestRoomStructures, TestRoomNPCs)

TestHallReferences = ["room", "hall", "corridor", "area", "zone", "surroundings",]
TestHallDescription = "a long, seemingly endless hallway. No matter how far you walk down it's length the door you came in through is always right behind you."
TestHallContents = {
	"cloth" : 1,
	}
TestHallExits = {
	"north" : "TestRoom",
	}
TestHallStructures = []
TestHallNPCs = []
TestHall = Zone("Test Hall", TestHallReferences, TestHallDescription, TestHallContents, TestHallExits, True, "key", "A heavy wooden door bars your way. A small tarnished keyhole stares at you defiantly.", "With a dry click the key turns in the lock and the door swings open with an eerie creak.", True, "As you attempt the retrieve the key from the lock it surrenders to the ravages of time, snapping off with a gentle clang. You won't be getting that back.", True, "enterZone", testEvent, TestHallStructures, TestHallNPCs)

DarkTestRoomReferences = ["room", "area", "surroundings", "zone",]
DarkTestRoomDescription = "a pitch black room. You can hardly see a thing, and all you can feel is an empty light socket bumping against your MASSIVE head."
DarkTestRoomContents = {
	"socket" : 1,
	}
DarkTestRoomExits = {}
DarkTestRoomStructures = []
DarkTestRoomNPCs = []
DarkTestRoom = Zone("Test Room", DarkTestRoomReferences, DarkTestRoomDescription, DarkTestRoomContents, DarkTestRoomExits, False, "none", "none", "none", False, "none", True, "searchZone", bobLightsEvent, DarkTestRoomStructures, DarkTestRoomNPCs)

TestSecretRoomReferences = ["room", "zone", "area", "surroundings",]
TestSecretRoomDescrption = "a tiny room, with more in common with a closet than an actual room."
TestSecretRoomContents = {}
TestSecretRoomExits = {
	"west" : "TestRoom",
	}
TestSecretRoomStructures = []
TestSecretRoomNPCs = ["bob"]
TestSecretRoom = Zone("Secret Room", TestRoomReferences, TestSecretRoomDescrption, TestSecretRoomContents, TestSecretRoomExits, False, "none", "none", "none", False, "none", False, "none", "none", TestSecretRoomStructures, TestSecretRoomNPCs)
## END ZONE ASSIGNMENTS ##

## BEGIN NPC CREATION ##
bobInv = {
	"clothing" : 1,
	"wallet" : 1,
	"shin" : 50,
	}
bobPronouns = {
	"he" : "He",
	"his" : "His",
	"him" : "Him",
	}
bobConvo = {
	"intro" : {
		"introtext" : "'What can I help you with?'",
		"none" : "'I'm sorry. My responses are limited, you must ask the right questions.'",
		"who" : {
			"introtext" : "Who do you want to know about?",
			"me" : "'You? I don't know. If you can't remember then that's something you may want to look into.'",
			"i" : "'You? I don't know. If you can't remember then that's something you may want to look into.'",
			"you" : {
				"introtext" : "What do you want to know about me?",
				"who" : "'I'm Bob, the two dimensional test character who has even less programming behind him than a box. Give me time and I may become a bit more complicated. Until then fuck you and your organic privilege.",
				"where" : "'I'm from nowhere in particular, which is a lovely place this time of year.'",
				"why" : "'I'm only here because Nic needed a way to test NPCs quickly.'",
				"how" : "'I got here through the magic of code. I'm also in the wall.'"
				},
			},
		"here" : "'This is only a small test area. There are three different locations you can visit...well four technically, but as far as your concerned there are only three. Don't expect much from any of them though.'",
		"fuck" : "'Watch your profamity.'",
		"where" : "'This place is just a construct. A framework. Someday it may be a wondrous place of adventure, but right now it is the worldly equivalent of scaffolding held up by google and machete-like practises.'",
		"goodbye" : "'Get the fuck out.'",
		},
	}
bobEvent = {
	"fuck" : "bobFuckEvent",
	"me" : "bobMeEvent",
	"how" : "bobHowEvent",
	}
bob = NPC("Bob", bobPronouns, bobInv, 100, 100, 100, "a short, uninteresting fellow with strange, oddly arranged facial features that you'd think make him easy to remember, but somehow have the opposite effect.", True, "none", bobEvent, bobConvo)
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
	cmd = input(">>>")
	
	for i in Commands:
		if(stringContains(i, cmd) == True):
			stringToClassDef(playerCommand, i)(Location, Character, cmd)## This is where all player input is passed to the relevant command
			
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

def stringToClassDef(className, defName):##This takes strings and makes them a def name within a class. className.defName is the result. can be handed arguments
	return getattr(className, defName)
	
boot()##====================the only base level command if at all possible.
