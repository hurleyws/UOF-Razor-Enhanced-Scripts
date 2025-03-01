from System.Collections.Generic import List
from System import Byte
from System import Int32 as int
import time
import random

# Filter to find NPCs (non-player characters)
npcFilter = Mobiles.Filter()
npcFilter.Notorieties = List[Byte](bytes([6]))  # Notoriety level 6: NPC
npcFilter.RangeMax = 8  # Maximum distance from player (12 tiles)
npcFilter.IsHuman = True  # Filter for humans only (you can adjust this)
npcFilter.CheckLineOfSight = True  # Check line of sight

companyFilter = Mobiles.Filter()
companyFilter.IsHuman = False
companyFilter.Notorieties = List[Byte](bytes([1]))  # Notoriety level 1: blue pets




# Filter to find corpses
corpseFilter = Items.Filter()
corpseFilter.IsCorpse = True  # Only look for corpses
corpseFilter.OnGround = True  # Ensure the corpse is on the ground
corpseFilter.Movable = False  # Ensure the corpse is not movable (optional)

def worldSave():
    if Journal.SearchByType('The world is saving, please wait.', 'System' ):
        Misc.SendMessage('Pausing for world save', 33)
        while not Journal.SearchByType('World save complete.', 'System'):
            Misc.Pause(1000)
        Misc.SendMessage('Continuing', 33)
        Journal.Clear()

def killNPCs():
    Player.ChatSay("All guard me")
    Misc.Pause(500)
    Player.ChatSay("All guard me")
    Misc.Pause(500)
    worldSave()

    # Get the start time for the timer
    start_time = time.time()

    while True:
        # Check for any notoriety 1 non-humans (blue pets)
        bluePetList = Mobiles.ApplyFilter(companyFilter)  # Refresh the list of blue pets

        # If any blue pets are found, break out of the function entirely
        if len(bluePetList) > 0:
            Misc.SendMessage("Company detected: Blue pets nearby. Exiting killNPCs.")
            Misc.Pause(500)
            return  # Break out of the function

        # Check elapsed time (in seconds)
        elapsed_time = time.time() - start_time
        if elapsed_time > 120:  # If more than 2 minutes have passed
            Misc.SendMessage("2 minutes passed, restarting function...")
            Misc.Pause(500)
            killNPCs()  # Restart the function
            worldSave()
            return  # Exit the current loop and function

        # Refresh the list of NPCs
        npcList = Mobiles.ApplyFilter(npcFilter)

        # If there are NPCs in the list, attack them
        if len(npcList) > 0:
            # Attack the first NPC in the list
            target_npc = npcList[0]  # Get the first NPC from the list
            Player.Attack(target_npc)  # Attack the NPC
            Misc.Pause(1000)
            worldSave()
            healthCheck()

        else:
            Misc.SendMessage("No more NPCs.")
            Misc.Pause(500)
            worldSave()
            return  # Exit the function if no NPCs are found


def stockRegs():
    root = Items.BackpackCount(0x0F86,-1)
    moss = Items.BackpackCount(0x0F7B,-1)
    pearl = Items.BackpackCount(0x0F7A,-1)
  
    Items.UseItem(0x4043C469)
    Misc.Pause(500)

    

    if root < 50:
        Items.Move(Items.FindByID(0x0F86,-1,0x4043C469),Player.Backpack.Serial,50-root)
        Misc.Pause(1000)
    elif root > 50:
        Items.Move(Items.FindByID(0x0F86,-1,Player.Backpack.Serial),0x4043C469,root-50)
        Misc.Pause(1000)
    else:
        Misc.Pause(200)
    
    if moss < 50:
        Items.Move(Items.FindByID(0x0F7B,-1,0x4043C469),Player.Backpack.Serial,50-moss)
        Misc.Pause(1000)
    elif moss > 50:
        Items.Move(Items.FindByID(0x0F7B,-1,Player.Backpack.Serial),0x4043C469,moss-50)
        Misc.Pause(1000)
    else:
        Misc.Pause(200)
        
    if pearl < 50:
        Items.Move(Items.FindByID(0x0F7A,-1,0x4043C469),Player.Backpack.Serial,50-pearl)
        Misc.Pause(1000)
    elif pearl > 50:
        Items.Move(Items.FindByID(0x0F7A,-1,Player.Backpack.Serial),0x4043C469,pearl-50)
        Misc.Pause(1000)
    else:
        Misc.Pause(200)
               


def goHome():
    worldSave()
    attempt_recall("Winter Lodge")
    Player.PathFindTo(6783, 3899, 17)
    Misc.Pause(1500)
    door = Items.FindBySerial(0x42F89EBD)
    if door.ItemID == 0x06A7:
        Items.UseItem(door)
        Misc.Pause(500)
    Player.PathFindTo(6783, 3898, 17)
    Misc.Pause(1500)
    Player.PathFindTo(6782, 3897, 17)
    Misc.Pause(1500)
    Player.PathFindTo(6780, 3893, 17)
    Misc.Pause(4000)
    if Player.Hits < 80:
        Spells.Cast("Greater Heal")
        Misc.Pause(1500)
        Target.Self()
    stockRegs()

            
def attempt_recall(location):
    while True:
        Misc.Pause(500)
        Player.ChatSay("All follow me")
        Misc.Pause(500)  
        Player.ChatSay("All follow me")
        Misc.Pause(500) 
        crabCheck()
        worldSave()
        Player.ChatSay(f"[recall {location}")
        Misc.Pause(2500)  # Wait for the spell to cast

        # Check if the spell was disturbed
        if Journal.SearchByType("Your concentration is disturbed, thus ruining thy spell.", "System"):
            Misc.SendMessage("Spell was disturbed. Recasting...")
            Journal.Clear()
            Misc.Pause(500)
            continue  # Skip the rest of the loop and start over
            
        elif Journal.SearchByType("Insufficient mana for this spell.","System"):
            while Player.Mana < 11:
                Misc.Pause(1000)
            Misc.Pause(1000)
            Journal.Clear()
            continue
            
        elif Journal.SearchByType("Insufficient mana for this spell.","System"):
            while Player.Mana < 11:
                Misc.Pause(1000)
            Misc.Pause(1000)
            Journal.Clear()
            continue
            
        elif Journal.SearchByType("This book needs time to recharge.","System"):
            Misc.Pause(500)
            Misc.Pause(1500)
            Journal.Clear()
            Misc.Pause(500)
            continue            
            
        else:
            break  # Exit the loop if no disturbance is detected

def healthCheck():
    if Player.Hits < 30:
        Misc.Beep()
        goHome()
        Misc.ScriptStopAll(False)

def crabCheck():
    crab = Mobiles.FindBySerial(0x0008064C)
    
    # Start the timer
    start_time = time.time()

    while Player.DistanceTo(crab) > 1:
        # Check if the 15-second timer has expired
        elapsed_time = time.time() - start_time
        if elapsed_time > 16:  # If more than 15 seconds have passed
            Misc.SendMessage("15 seconds passed, stopping all scripts...")
            Misc.ScriptStopAll(False)  # Stop all scripts
            return  # Exit the function

        Player.ChatSay("All follow me")
        Misc.Pause(2000)        
            
        
# List of possible locations
locations = ["Seat of Knowledge", "The Learned Mage", "Windy Inn", "Magical Supplies", "Mage's Things", "Windy Clothes", "Seeker's Inn", "Seeker's Inn 2", "Wind Alchemy", "Wind Alchemy 2"]
# Shuffle the list of locations to create a randomized order
random.shuffle(locations)

while True:
    for location in locations:
        attempt_recall(location)
        Misc.Pause(2500)
        killNPCs()
        
    goHome()
    Misc.Pause(300000)
