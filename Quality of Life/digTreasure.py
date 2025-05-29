from Scripts.glossary.spells import spells
from Scripts.glossary.items.spellScrolls import spellScrolls
from Scripts.utilities.items import MoveItem
import re
from System import Int32 as int
from System import Byte
from System.Collections.Generic import List
import time
import random

tmap = Items.FindByID(0x14EC,-1,Player.Backpack.Serial)
mount = Mobiles.FindBySerial(0x0008064C)

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

        # Exclude "Alyer Base", then sort to put 0x0485 hue mobs last
        valid_mobiles = sorted(
            [mob for mob in nearby_mobiles if mob.Name != "Alyer Base"],
            key=lambda m: m.Hue == 0x0485
        )

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
            

        Misc.SendMessage(f"{target.Name} is dead. Searching for next target...", 55)
        
Misc.WaitForContext(tmap.Serial, 10000)
Misc.ContextReply(tmap.Serial, 2)
while True:
    nearby_mobiles = get_nearby_mobiles()
    if len(nearby_mobiles) == 0:
        Misc.Pause(500)
    else:
        break
Mobiles.UseMobile(mount)
Misc.Pause(2000)
nearby_mobiles = get_nearby_mobiles()
# Filter out "Alyer Base"
valid_mobiles = [mob for mob in nearby_mobiles if mob.Name != "Alyer Base"]

while len(valid_mobiles) > 0:
    attack_nearest_mobile()
    nearby_mobiles = get_nearby_mobiles()
    # Filter out "Alyer Base"
    valid_mobiles = [mob for mob in nearby_mobiles if mob.Name != "Alyer Base"]
        

