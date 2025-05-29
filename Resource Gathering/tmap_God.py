from Scripts.glossary.spells import spells
from Scripts.glossary.items.spellScrolls import spellScrolls
from Scripts.utilities.items import MoveItem
import re
from System import Int32 as int
from System import Byte
from System.Collections.Generic import List
import time
import random

book1_16 = 0x402B008A
book17_32 = 0x402B06DE
book33_48 = 0x402B0AC6
book49_64 = 0x402B0D08
book65_80 = 0x402B0E9B
book81_96 = 0x402B10CD
book97_112 = 0x402B123F
book113_128 = 0x402B1419
book129_144 = 0x402B18F0
book145_160 = 0x402B1BB0
book161_176 = 0x402B5185
book177_192 = 0x402B4D18
book193_200 = 0x402B4905


# Loot toggle settings
loot_scrolls = False  # Set to False to move scrolls to a corpse instead
loot_arms = False  # Set to False to move arms to a corpse instead

# Item ID lists
spellScrollIDs = [spellScrolls[scroll].itemID for scroll in spellScrolls]
regs = {0x0F7A, 0x0F7B, 0x0F86, 0x0F8C, 0x0F84, 0x0F88, 0x0F85, 0x0F8D, 0x2260}
gem_ids = [0x0F21, 0x0F16, 0x0F19, 0x0F13, 0x0F10, 0x0F25, 0x0F2D, 0x0F15, 0x0F26, 0x0F21]  # Includes RDA frag 0x0F21
arms_ids = [
    0x0DF2, 0x0F49, 0x0F4D, 0x140E, 0x0F47, 0x0DF0, 0x13B2, 0x0F5E, 0x1B72, 0x1B73, 0x13F6, 
    0x13BB, 0x13BE, 0x13BF, 0x0EC3, 0x1408, 0x13B4, 0x0F50, 0x1441, 0x0F52, 0x0F4B, 0x0F45, 
    0x13F8, 0x143E, 0x143D, 0x0F43, 0x1B76, 0x13FD, 0x140A, 0x13FF, 0x1B74, 0x1B79, 0x1401, 
    0x13FB, 0x1C06, 0x1C0A, 0x1DB9, 0x13C6, 0x13C7, 0x13CB, 0x1C00, 0x1C08, 0x13CD, 0x13CC, 
    0x0F62, 0x0F61, 0x0F5C, 0x143B, 0x1B7B, 0x140C, 0x0E86, 0x0E87, 0x1C04, 0x1412, 0x1415, 
    0x1410, 0x1414, 0x1413, 0x1411, 0x0E89, 0x13EB, 0x13F0, 0x13EE, 0x13EC, 0x13B6, 0x0E81, 
    0x1403, 0x1C02, 0x1C0C, 0x13D5, 0x13D6, 0x13DA, 0x13DC, 0x13DB, 0x1443, 0x13B9, 0x13B0, 
    0x1405, 0x1439, 0x1407, 0x1B7A, 0x1C04, 0x0F52
]

# Special items to always loot
special_items = {0x2AA2, 0x14EC, 0x0F21}  # Relic, TMap, RDA Frag

from System import Byte
from System.Collections.Generic import List

def checkPetHealth():
    # Find pets by their serial
    Shuck = Mobiles.FindBySerial(0x0008064C)  # Replace with actual serial
    Spin = Mobiles.FindBySerial(0x0001DDFA)  # Replace with actual serial

    healing_active = False  # Track if healing is in progress
    healing_pet = None  # Track which pet is being healed


    pets = [Shuck, Spin]

    # Check players health and act accordingly
    if Player.Hits < 25:
        Misc.SendMessage("Health critically low, returning home!", 35)
        Misc.Pause(500)
        goHome()
        Misc.ScriptStop("petTrainer.py")
        return  # Exit function to prevent further execution

    elif Player.Hits < 61:
        Spells.CastMagery("Greater Heal")
        Target.WaitForTarget(10000, False)
        Target.TargetExecute(Player.Serial)
        Misc.Pause(500)

    # Check health of both pets
    for pet in pets:
        if pet and pet.Hits < 9:  # If any pet is critically low, go home
            Misc.SendMessage(f"{pet.Name} is critically low! Returning home!", 35)
            Misc.Pause(500)
            goHome()
            Misc.ScriptStop("petTrainer.py")
            return

        if pet and pet.Hits < 13:  # If pet is injured but not critical
            if not healing_active or healing_pet != pet:  # Start healing if not already active
                Misc.SendMessage(f"{pet.Name} is injured! Starting BandageHeal...", 55)
                Misc.Pause(500)
                BandageHeal.Start()
                Player.ChatSay(64, f"{pet.Name} follow me")
                Misc.Pause(500)

                # Tell the other pet to guard you
                for other_pet in pets:
                    if other_pet and other_pet != pet:
                        Player.ChatSay(64, f"{other_pet.Name} guard me")
                        Misc.Pause(500)


                healing_active = True
                healing_pet = pet

            # Continue checking both pets while healing the injured one
            while healing_active and pet.Hits < 22:
                Misc.Pause(2000)  # Wait before checking health again
                Player.ChatSay(64, f"{pet.Name} follow me")
                Misc.Pause(500)
                for other_pet in pets:  
                    if other_pet and other_pet != pet and other_pet.Hits < 10:
                        Misc.SendMessage(f"{other_pet.Name} is also injured! Switching healing...", 55)
                        Misc.Pause(500)
                        Player.ChatSay(64, f"{other_pet.Name} follow me")
                        Misc.Pause(500)
                        healing_pet = other_pet

            # Once healed, stop bandage healing
            Misc.SendMessage(f"{pet.Name} has recovered! Stopping BandageHeal...", 55)
            Misc.Pause(500)
            BandageHeal.Stop()
            healing_active = False
            healing_pet = None

def get_nearby_mobiles(range_max=10, notorieties=[3,4]):
    """
    Finds and returns a sorted list of mobiles within a given range based on distance.
    
    Args:
        range_max (int): Maximum range to search for mobiles.
        notorieties (list): List of notorieties to filter.

    Returns:
        list: Sorted list of mobiles (nearest first).
    """
    mobiles_filter = Mobiles.Filter()
    mobiles_filter.RangeMax = range_max
    mobiles_filter.Notorieties = List[Byte](bytes(notorieties))
    mobiles_filter.CheckIgnoreObject = True
    mobiles_filter.CheckLineOfSight = True
    mobiles_filter.IsHuman = False

    nearby_mobiles = Mobiles.ApplyFilter(mobiles_filter)
    
    # Sort the list by distance (closest first)
    return sorted(nearby_mobiles, key=lambda mob: Player.DistanceTo(mob))

def attack_nearest_mobile():
    """
    Finds the nearest valid mobile (excluding 'Alyer Base'), attacks it, and continuously checks if its still alive.
    Moves on to the next target once the current one is dead.
    """
    while True:  # Keep looking for targets
        nearby_mobiles = get_nearby_mobiles()

        # Filter out "Alyer Base"
        valid_mobiles = [mob for mob in nearby_mobiles if mob.Name != "Alyer Base"]

        if not valid_mobiles:
            Misc.SendMessage("No valid targets found.", 33)
            break

        # Select the nearest valid mobile
        target = valid_mobiles[0]
        Misc.SendMessage(f"Attacking {target.Name} (ID: {target.Serial})", 55)
        Player.Attack(target)

        # Keep checking if the target still exists
        while Mobiles.FindBySerial(target.Serial):
            Misc.Pause(500)  # Adjust as needed
            checkPetHealth

        Misc.SendMessage(f"{target.Name} is dead. Searching for next target...", 55)






# Find nearest corpse within 2 tiles
def find_nearest_corpse():
    corpses_filter = Items.Filter()
    corpses_filter.IsCorpse = True
    corpses_filter.OnGround = True
    corpses_filter.RangeMax = 2
    corpses_filter.Graphics = List[int]([0x2006])

    corpses = Items.ApplyFilter(corpses_filter)
    return corpses[0].Serial if corpses else None

# Move items with fallback to nearest corpse
def move_item(item, destination):
    if destination:
        Items.Move(item, destination, 1)
        Misc.Pause(1000)
        attack_nearest_mobile()
    else:
        Misc.SendMessage("No valid destination found.", 33)

# Handle world save interruptions
def worldSave():
    if Journal.SearchByType('The world will save in 1 minute.', 'System') or Journal.SearchByType('pause', 'Regular'):
        Misc.Pause(700)
        Misc.SendMessage('Pausing for world save or player-called break.', 33)
        while not (Journal.SearchByType('World save complete.', 'System') or Journal.SearchByType('play', 'Regular')):
            Misc.Pause(1000)
        Misc.Pause(2500)
        Misc.SendMessage('Continuing run', 33)
        Misc.Pause(1000)
    Journal.Clear()

# Find treasure chest
Player.ChatSay("All guard me")
Misc.Pause(500)
tChest = Items.FindByID(0x0E40, -1, -1, 2)

if tChest:
    Misc.SendMessage("Starting")
    Misc.Pause(500)
    Items.UseItem(tChest)
    Misc.Pause(500)

    # Get a nearby corpse for trash disposal
    corpse = find_nearest_corpse()

    # Loot special items first
    worldSave()
    for i in tChest.Contains:
        if i.ItemID in special_items:
            Items.Move(i, Player.Backpack.Serial, 1)
            Misc.Pause(1000)
            attack_nearest_mobile()

    # Sort arms
    worldSave()
    for i in tChest.Contains:
        if i.ItemID in arms_ids:
            move_item(i, Player.Backpack.Serial if loot_arms else corpse)
            

    # Sort regs
    worldSave()
    for i in tChest.Contains:
        if i.ItemID in regs:
            Items.Move(i, Player.Backpack.Serial, -1)
            Misc.Pause(1000)
            attack_nearest_mobile()

    # Get gold/tmaps
    worldSave()
    for i in tChest.Contains:
        if i.ItemID in [0x0EED, 0x14EC]:
            Items.Move(i, Player.Backpack.Serial, -1)
            Misc.Pause(1000)
            attack_nearest_mobile()

    # Find ID wands
    worldSave()
    for i in tChest.Contains:
        iprops = Items.GetPropStringList(i)
        if "Identification" in str(iprops):
            Player.ChatSay("ID wand!")
            Misc.Pause(500)
            Items.Move(i, Player.Backpack.Serial, 1)
            Misc.Pause(1000)
            attack_nearest_mobile()

    # Sort gems/RDAs
    worldSave()

    for i in tChest.Contains:
        if i.ItemID in gem_ids:
            Items.Move(i, Player.Backpack.Serial, 1)
            Misc.Pause(1000)
            attack_nearest_mobile()

    # Sort scrolls
    worldSave()
    for i in tChest.Contains:
        if i.ItemID in spellScrollIDs:
            move_item(i, Player.Backpack.Serial if loot_scrolls else corpse)
            attack_nearest_mobile()

    # **Final cleanup: Move remaining trash to the corpse**
    worldSave()
    if corpse:  # Only attempt if a corpse was found
    
        map = Items.FindByID(0x14EC, -1, Player.Backpack.Serial)
        if map:
            props = Items.GetPropStringList(map)
            Misc.Pause(100)
            if any("Completed by Alyer Base" in prop for prop in props):
                Items.Move(map, corpse, 1)
                Misc.Pause(1000)
                
        for i in tChest.Contains:
            Items.Move(i, corpse, 1)
            Misc.Pause(1000)
            

        map = Items.FindByID(0x14EC, -1, Player.Backpack.Serial)
        if map:
            Misc.Pause(100)
            Items.Move(map, corpse, 1)
            Misc.Pause(1000)
            
        Misc.SendMessage("Trash moved to nearby corpse.", 55)
    else:
        Misc.SendMessage("No nearby corpse found for trash.", 33)
        
    
        

    Misc.SendMessage("Looting complete.", 55)

else:
    Misc.SendMessage("No Chest")
