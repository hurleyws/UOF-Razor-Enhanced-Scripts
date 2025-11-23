from System import Int32 as int
from System import Byte
from System.Collections.Generic import List
import time
import random
import datetime

# Global heal flag
needs_heal = False

worldSavePause = False

primaryPet = 0x00136CD2 #drago 0x00136CD2
secondaryPet = 0x00000A14 #steed 0x00000A14

goldLog = 'C:/Users/Hurley/Documents/GitHub/UOF-Razor-Enhanced-Scripts/Resource Gathering/goldLog.USR'

gem_ids = [0x0F21,0x0F16,0x0F19,0x0F13,0x0F10,0x0F25,0x0F2D,0x0F15,0x0F26,0x0F21] 

pchest = [0x0E41,0x09AB,0x0E7C,0x0E40]

rune_ids = {
    0x483B, 0x483E, 0x4841, 0x4844, 0x4847, 0x484A, 0x484D, 0x4850,
    0x4853, 0x4856, 0x4859, 0x485C, 0x485F, 0x4862, 0x4865, 0x4868,
    0x486B, 0x4871, 0x486E, 0x4874, 0x4877, 0x487A, 0x487D, 0x4880, 0x4883
}

creature_statue_ids = {0x2100, 0x25B6, 0x2581, 0x1BF2, 0x14EC,0x25D7,0x20ED}  # IDs for creature statues + ingots 0x1BF2 + tmaps 0x0F7A

rune_destination = 0x417D8A37  # Destination container for runes
statue_destination = 0x42EA55BA  # Destination container for statues
BandageHeal.Start()

def countItemsByID(itemIDs):
    """
    Counts the total number of specified items by their IDs in the players backpack.
    
    Args:
    - itemIDs (list): A list of item IDs to count in the backpack.
    
    Returns:
    - int: The total count of specified items.
    """
    totalCount = 0

    # Iterate over each item ID in the list
    for itemID in itemIDs:
        # Count items in the backpack matching the current item ID
        # Assuming color is not specified (-1) and searching recursively
        count = Items.ContainerCount(Player.Backpack.Serial, itemID, -1, True)
        
        # Add the count for this item ID to the total count
        totalCount += count

    # Return the total count of items
    return totalCount


def sellGems():
    totalGems = countItemsByID(gem_ids)
    if totalGems > 20:
        SellAgent.Enable()
        attempt_recall("Sell Gems")
        Misc.Pause(3000)
        Misc.WaitForContext(0x0026BFC1, 10000)
        Misc.ContextReply(0x0026BFC1, 2)
        Misc.Pause(500)
        Misc.WaitForContext(0x0026CC5D, 10000)
        Misc.ContextReply(0x0026CC5D, 2)
        Misc.Pause(1000)
        Player.ChatSay(26, 'I thank thee.')
        Misc.Pause(500)

def checkSelfHealth():
    global needs_heal
    if Player.Poisoned:
        needs_heal = True
        return

    if Player.Hits < Player.HitsMax and not needs_heal:
        if Player.Hits <= Player.HitsMax - 25:
            needs_heal = True


def tryHealIfSafe():
    global needs_heal
    if needs_heal:
        if Player.Poisoned:
            Spells.CastMagery("Cure")
            Misc.Pause(800)
            Target.WaitForTarget(1000, False)
            Target.Self()
            Misc.Pause(200)
            checkSelfHealth()
        else:
            Spells.CastMagery("Greater Heal")
            Misc.Pause(800)
            Target.WaitForTarget(1000, False)
            Target.TargetExecute(Player.Serial)
            Misc.Pause(200)
        needs_heal = False

def deadCheck():
    if Player.IsGhost:
        Misc.ScriptStop("petTrainer_while.py")
        Misc.Pause(500)
        Misc.ScriptStop("petTrainer.py")
        Misc.Pause(500)
    if pet1 and pet1.Hits <= 5 or pet2 and pet2.Hits <= 5:
        Misc.SendMessage("One or both pets are dead. Heading home.", 33)
        Misc.Pause(500)
        goHome()
        Misc.ScriptStop("petTrainer.py")
        Misc.Pause(500)


def log_gold_amount():
    """
    Gets the current gold count in the backpack and appends it to the log file with a timestamp.
    """
    gold_amount = Items.BackpackCount(0x0EED, -1)  # Get gold count (0x0EED is the gold coin ID)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current date and time

    with open(goldLog, 'a') as file:  # 'a' mode appends instead of overwriting
        file.write(f"{timestamp}, {gold_amount}\n")  # Write timestamp and gold amount

    Misc.SendMessage(f"Logged: {timestamp} - Gold: {gold_amount}", 53)
    Misc.Pause(300)

# Call the function to log gold

def calculateDirectionToRun(mobile):
    # Logic to calculate the direction to walk based on positions
    if mobile.Position.X > Player.Position.X and mobile.Position.Y > Player.Position.Y:
        return 'Down'
    if mobile.Position.X < Player.Position.X and mobile.Position.Y > Player.Position.Y:
        return 'Left'
    if mobile.Position.X > Player.Position.X and mobile.Position.Y < Player.Position.Y:
        return 'Right'
    if mobile.Position.X < Player.Position.X and mobile.Position.Y < Player.Position.Y:
        return 'Up'
    if mobile.Position.X > Player.Position.X and mobile.Position.Y == Player.Position.Y:
        return 'East'
    if mobile.Position.X < Player.Position.X and mobile.Position.Y == Player.Position.Y:
        return 'West'
    if mobile.Position.X == Player.Position.X and mobile.Position.Y > Player.Position.Y:
        return 'South'
    if mobile.Position.X == Player.Position.X and mobile.Position.Y < Player.Position.Y:
        return 'North'
    return ''
    
def findCorpses():
    """
    Find corpses within a specified range.
    :return: List of corpses found within the range
    """
    corpses_filter = Items.Filter()
    corpses_filter.IsCorpse = True
    corpses_filter.OnGround = True
    corpses_filter.RangeMax = 10  # Range for searching corpses
    corpses_filter.Graphics = List[int]([0x2006])  # Corpses only (graphic ID 0x2006)
    corpses_filter.CheckIgnoreObject = True

    # Apply the filter to find corpses
    unsorted_corpse_list = Items.ApplyFilter(corpses_filter)
    corpse_list = sorted(unsorted_corpse_list, key=lambda corpse: Player.DistanceTo(corpse))

    # Return the list of corpses
    return corpse_list


def moveToCorpse(max_loops=10, max_retry=5, overall_timeout=30, individual_timeout=5):
    """
    Continuously finds and moves to the closest corpse within range using directional movement.
    
    :param max_loops: Maximum iterations before breaking out of the loop.
    :param max_retry: Maximum retry attempts for each corpse.
    :param overall_timeout: Maximum time in seconds for the entire function execution.
    :param individual_timeout: Timeout in seconds for reaching each individual corpse.
    """
    overall_start_time = time.time()  # Start overall timeout timer
    loop_count = 0  # Initialize loop counter

    while loop_count < max_loops:
        loop_count += 1  # Increment loop count each iteration

        corpse_list = findCorpses()  # Refresh corpse list dynamically
        if not corpse_list:
            Misc.SendMessage("No corpses found.", 33)
            Misc.Pause(500)
            break  # Exit if no corpses remain

        for corpse in corpse_list:  # Iterate over available corpses
            if not corpse or not Items.FindBySerial(corpse.Serial):
                Misc.SendMessage(f"Corpse {corpse.Serial} no longer exists.", 33)
                Misc.Pause(500)
                continue  # Skip if corpse is gone
                
            attackEvil()
            detectMobiles()
            Misc.SendMessage(f"Moving to closest corpse: {corpse.Serial}", 33)
            Misc.Pause(500)
            

            # Move towards the corpse until within 2 tiles
            start_time = time.time()
            while Player.DistanceTo(corpse) > 2:
                if time.time() - overall_start_time > overall_timeout:
                    Misc.SendMessage("Overall timeout exceeded. Exiting function.", 33)
                    Misc.Pause(500)
                    return
                
                if time.time() - start_time > individual_timeout:
                    Misc.SendMessage(f"Timeout for corpse {corpse.Serial}. Trying next.", 33)
                    Misc.Pause(500)
                    Misc.IgnoreObject(corpse)  # Ignore unreachable corpses
                    Misc.Pause(500)
                    break  

                if not Items.FindBySerial(corpse.Serial):
                    Misc.SendMessage(f"Corpse {corpse.Serial} disappeared. Skipping.", 33)
                    Misc.Pause(500)
                    break
                    
                Misc.Pause(500)

                Player.PathFindTo(corpse.Position.X,corpse.Position.Y,corpse.Position.Z)
                

                deadCheck()  # Ensure safe movement

            if Player.DistanceTo(corpse) <= 2:
                Misc.SendMessage(f"✅ Reached corpse: {corpse.Serial}", 65)
                Misc.Pause(500)  # Short delay before processing next corps
                break  # Stop processing once a corpse is reached
                
            

    Misc.SendMessage("✅ Finished processing all corpses or hit max loops.", 65)
    Misc.Pause(500)




def worldSave():
    manualPause = False
    
    # Check for world save or manual pause
    if Journal.SearchByType('The world will save in 1 minute.', 'System') or Journal.SearchByType('pause', 'Regular'):
        Misc.Pause(700)
        
        # If "pause" is typed, set manualPause flag
        if Journal.SearchByType('pause', 'Regular'):
            manualPause = True
            Misc.SendMessage('Manual pause initiated.', 33)
            Misc.Pause(300)
        else:
            Misc.SendMessage('Pausing for world save.', 33)
            Misc.Pause(300)
        
        # Loop until a resume condition occurs
        while True:
            Misc.Pause(1000)
            attackEvil()

            # If world save finishes and were NOT in manual pause, resume
            if not manualPause and Journal.SearchByType('World save complete.', 'System'):
                break

            # If "play" is typed during manual pause, resume
            if manualPause and Journal.SearchByType('play', 'Regular'):
                break

        Misc.Pause(2500)
        Misc.SendMessage('Continuing run.', 33)
        Misc.Pause(700)

    Journal.Clear()



def detectMobiles():
    # Create the filter
    mobFilter = Mobiles.Filter()
    mobFilter.Enabled = True
    mobFilter.IsHuman = True
    mobFilter.CheckLineOfSight = True
    mobFilter.CheckIgnoreObject = True

    # Apply the filter
    mobilesList = Mobiles.ApplyFilter(mobFilter)

    # Filter out "a restless soul"
    filteredMobiles = [mob for mob in mobilesList if mob.Name.lower() != "a restless soul"]

    if not filteredMobiles:
        Misc.SendMessage("No valid mobiles detected", 76)
        Misc.Pause(500)
        return

    mob = filteredMobiles[0]  # Take the first valid mob
    Misc.SendMessage("Mobile detected: {}".format(mob.Name), 33)
    Misc.Pause(500)

    mobProps = Mobiles.GetPropStringList(mob)
    if mobProps:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp}, {mob.Name}\n"

        with open(goldLog, 'a') as file:
            file.write(log_entry)

        goHome()
        Misc.ScriptStop("petTrainer.py")
        Misc.Pause(500)
                
def followMobile(mobile):
    """
    Follows a mobile until the player is within 1 tile or a timeout occurs.
    Dynamically adjusts target position and keeps trying offsets until movement occurs.
    """
    if not mobile or not mobile.Position:
        Misc.SendMessage("Error: Invalid mobile or position!", 33)
        Misc.Pause(300)
        return

    start_time = time.time()
    timeout = 20  # seconds
    pet1 = Mobiles.FindBySerial(primaryPet)

    if not pet1 or not pet1.Position:
        Misc.SendMessage("pet1 not found or has no position!", 33)
        Misc.Pause(300)
        return

    # Retry movement with different offsets until we succeed or time runs out
    offsets = [(-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1), (-1, 1), (1, -1)]
    while time.time() - start_time < timeout:
        current_pos = Player.Position

        for dx, dy in offsets:
            target_x = pet1.Position.X + dx
            target_y = pet1.Position.Y + dy
            target_z = pet1.Position.Z

            Player.PathFindTo(target_x, target_y, target_z)
            Misc.Pause(100)

            # Estimate time to travel based on distance
            distance = max(abs(Player.Position.X - target_x), abs(Player.Position.Y - target_y))
            travel_pause = int(distance * 500)  # Adjust 500ms as needed
            Misc.Pause(travel_pause)


            if Player.Position != current_pos:
                Misc.SendMessage(f"Moved to offset ({dx}, {dy})", 66)
                Misc.Pause(300)
                return  # Movement succeeded

    Misc.SendMessage("Failed to move to pet after all retries.", 33)
    Misc.Pause(300)


def stayCloseToPet(pet, max_distance=6):
    if not pet or not pet.Position:
        return

    if Player.DistanceTo(pet) > max_distance:
        Misc.SendMessage("Pet is too far — moving closer.", 33)

        offsets = [(-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1), (-1, 1), (1, -1)]

        for dx, dy in offsets:
            target_x = pet.Position.X + dx
            target_y = pet.Position.Y + dy
            target_z = pet.Position.Z

            path = PathFinding.GetPath(target_x, target_y, True)
            if path:
                PathFinding.RunPath(path, 3000)
                Misc.Pause(1000)
                return  # Move once and exit
    
    
def detectTargets():
    paragon_hue = 0x0485

    mobFilter = Mobiles.Filter()
    mobFilter.Notorieties = List[Byte](bytes([3,4,5,6]))  # Enemies
    mobFilter.CheckLineOfSight = True
    mobFilter.CheckIgnoreObject = True
    mobFilter.RangeMax = 12

    mobs = Mobiles.ApplyFilter(mobFilter)

    # Sort: Paragons (True=0, False=1), then by distance
    return sorted(
        mobs,
        key=lambda mob: (
            mob.Hue != paragon_hue,           # Paragons first
            Player.DistanceTo(mob)            # Then closest
        )
    )

    
def pathfindAndWait(x, y, z):
    start_pos = Player.Position
    start_time = time.time()

    # Create and configure pathfinding route
    route = PathFinding.Route()
    route.X = x
    route.Y = y
    route.MaxRetry = 5
    route.StopIfStuck = False

    PathFinding.Go(route)  # Initiate movement

    # Wait until player arrives or timeout
    while Player.Position.X != x or Player.Position.Y != y:
        Misc.Pause(200)
        if time.time() - start_time > 30:  # Optional: 30-second timeout
            Misc.SendMessage("Pathfinding timed out", 33)
            Misc.Pause(300)
            break

    # Final pause to ensure arrival
    travel_duration = time.time() - start_time
    Misc.SendMessage(f"Travel completed in {round(travel_duration, 2)} seconds.", 65)
    Misc.Pause(int(travel_duration * 1000))  # Pause in milliseconds
        
def refresh_pets():
    global pet1, pet2
    pet1 = Mobiles.FindBySerial(primaryPet)
    pet2 = Mobiles.FindBySerial(secondaryPet)


def no_targets_behavior():
    Player.HeadMessage(55, "No targets detected.")
    Misc.Pause(500)
    return


def engage_target(target_list):
    target = target_list[0]
    start_time = time.time()
    max_guard_duration = 3

    checkAndMoveAway(target, can_ignore=False)

    while Player.DistanceTo(pet1) < 2 and time.time() - start_time < max_guard_duration:
        if pet1 and not pet1.WarMode:
            Player.ChatSay("All guard me")
            Misc.Pause(300)
        Player.Attack(target)
        Misc.Pause(250)

    combat_with_target(target)



def combat_with_target(target):
    start_time = time.time()
    retry_count = 0
    max_retries = 3

    while Mobiles.FindBySerial(target.Serial):
        avoidNearbyThreats()
        current_targets = detectTargets()
        stayCloseToPet(pet1)

        if pet1 and not pet1.WarMode:
            Player.ChatSay("All guard me")
            Misc.Pause(500)
            retry_count += 1

            if retry_count >= max_retries:
                Misc.SendMessage("Pet didnt enter WarMode. Breaking out after 3 attempts.", 33)
                Misc.Pause(500)
                break  # Exit the function
        else:
            retry_count = 0  # reset counter if pet successfully engaged


def engage_with_pet(target):
    start_time = time.time()
    while target and Player.DistanceTo(pet2) < 2 and time.time() - start_time < 5:
        Player.ChatSay(f"{pet2.Name} kill")
        Misc.Pause(500)
        Target.TargetExecute(target)
        Misc.Pause(200)
        Mobiles.Message(target, 66, "attacking")
        Misc.Pause(200)


def maintain_combat_position(pet, target):
    if pet and Player.DistanceTo(pet) > 6:
        followMobile(pet)


def heal_pets_if_needed():
    if (pet2 and pet2.Hits < 18) or (pet1 and pet1.Hits < 18):
        Player.ChatSay(64, "all follow me")
        Target.Cancel()
        Misc.Pause(500)
        Player.ChatSay(64, "all follow me")
        Misc.Pause(500)

        BandageHeal.Start()
        Misc.Pause(2000)


        while (pet1 and pet1.Hits < 22) or (pet2 and pet2.Hits < 22):
            refresh_pets()
            Misc.Pause(500)

            # If pets are still taking damage after 30s, give up


            # Check for threats during healing
            active_targets = detectTargets()
            if active_targets:
                target = active_targets[0]  # First detected enemy

                # Re-engage pets if they’re idle and in range
                if pet1 and not pet1.WarMode and Player.DistanceTo(pet1) < 8:
                    Player.ChatSay(f"{pet1.Name} kill")
                    Misc.Pause(300)
                    Target.TargetExecute(target)
                    Misc.Pause(200)

                if pet2 and not pet2.WarMode and Player.DistanceTo(pet2) < 8:
                    Player.ChatSay(f"{pet2.Name} kill")
                    Misc.Pause(300)
                    Target.TargetExecute(target)
                    Misc.Pause(200)

                # Stop healing temporarily to let pets re-engage
                BandageHeal.Stop()
                Misc.Pause(1500)  # Let pets stabilize
                BandageHeal.Start()
                healing_timer = time.time()  # Reset healing timer after restart

            Misc.Pause(500)

        BandageHeal.Stop()

        
        


def attempt_remount():
    if not pet2:
        return

    while Player.DistanceTo(pet2) > 2:
        Player.ChatSay(pet2.Name + " follow me")
        Misc.Pause(500)

    Journal.Clear()
    attempt_start = time.time()
    timeout = 10

    while not Player.Mount and time.time() - attempt_start < timeout:
        Mobiles.UseMobile(pet2)
        Misc.Pause(500)

        if Journal.SearchByType("Your mount refuses to let you ride here!", "System"):
            Misc.SendMessage("❌ Mount refused to be ridden here.", 33)
            Misc.Pause(200)
            break

        elif Journal.SearchByType("This mount is too ill to ride.", "System"):
            Spells.CastMagery("Cure")
            Target.WaitForTarget(10000, False)
            Misc.Pause(500)
            Target.TargetExecute(pet2)
            Misc.Pause(500)
            
def avoidNearbyThreats():
    checkSelfHealth()  # 🩸 check for damage

    threats = detectTargets()
    for mob in threats:
        if Player.DistanceTo(mob) <= 1:
            checkAndMoveAway(mob, can_ignore=False)
            break


def attackEvil():
    refresh_pets()
    Misc.Pause(200)

    # NEW: Check immediately after entering area
    checkAndMoveAway(detectClosestHostile(), can_ignore=False)

    while True:
        target_list = detectTargets()
        if not target_list:
            Player.HeadMessage(55, "No targets detected.")
            Misc.Pause(500)
            break

        engage_target(target_list)
        Misc.Pause(1000)
        deadCheck()
        checkPetHealth()
        refresh_pets()
        heal_pets_if_needed()

        if len(detectTargets()) == 0:
            gatherPets()

        worldSave()
        attempt_remount()



def gatherPets():
    timeout = time.time() + 10  # Set 10-second timeout
    pet1 = Mobiles.FindBySerial(primaryPet)
    pet2 = Mobiles.FindBySerial(secondaryPet)

    # Only check distances for pets that exist
    def petTooFar(pet):
        return pet and Player.DistanceTo(pet) > 1

    while petTooFar(pet1) or petTooFar(pet2):
        if time.time() > timeout:
            Player.ChatSay("All follow me")
            Misc.Pause(3000)

            if petTooFar(pet1):
                for _ in range(5):
                    Player.Walk(calculateDirectionToRun(pet1))
                    Misc.Pause(500)
            
        Misc.Pause(100)
        Misc.SendMessage("Waiting for pets to heal.", 33)
        Misc.Pause(1500)
        Player.ChatSay("All guard me")
        Misc.Pause(500)
       

     
        
        # Refresh pet references in case of position updates
        pet1 = Mobiles.FindBySerial(primaryPet)
        pet2 = Mobiles.FindBySerial(secondaryPet)    


def checkPetHealth():
    pet2 = Mobiles.FindBySerial(primaryPet)
    pet1 = Mobiles.FindBySerial(secondaryPet)

    pets = [pet1, pet2]

    # Abort if either pet is dead
    if any(pet and pet.Hits < 16 for pet in pets):  
        BandageHeal.Start()
        Misc.Pause(200)
        Player.ChatSay("All follow me")
        Misc.Pause(500)
        Player.ChatSay("All follow me")
        Misc.Pause(500)
        Player.ChatSay("All follow me")
        Misc.Pause(1500)

        timeout = 10  # seconds to wait for pets to come close
        wait_start = time.time()

        while time.time() - wait_start < timeout:
            all_close = True
            for pet in pets:
                if pet and Player.DistanceTo(pet) > 1:
                    all_close = False
                    break
            if all_close:
                break
            Misc.Pause(500)

        # Extra short delay to allow pets to fully stop before switching mode
        Misc.Pause(500)
        Player.ChatSay("All guard me")
        Misc.Pause(500)

        # Optional: Resume attacking if a valid target still exists
        targetList = detectTargets()
        if targetList:
            Player.Attack(targetList[0])
            Misc.Pause(500)
    
    



def attempt_recall(location):
    while True:
        Player.ChatSay("All guard me")
        Misc.Pause(250)
        Player.ChatSay("All guard me")
        Misc.Pause(250)
        gatherPets()
        Player.ChatSay(f"[recall {location}")
        Misc.Pause(1800)  # Wait for the spell to cast

        # Check if the spell was disturbed
        if Journal.SearchByType("Your concentration is disturbed, thus ruining thy spell.", "System"):
            Misc.SendMessage("Spell was disturbed. Recasting...")
            Journal.Clear()
            Misc.Pause(500)
            continue  # Skip the rest of the loop and start over
            
        elif Journal.SearchByType("Insufficient mana for this spell.","System"):
            while Player.Mana < 11:
                Misc.Pause(1000)
            Journal.Clear()
            continue
            
        elif Journal.SearchByType("Insufficient mana for this spell.","System"):
            while Player.Mana < 11:
                Misc.Pause(1000)
            Journal.Clear()
            continue
            
        elif Journal.SearchByType("This book needs time to recharge.","System"):
            Misc.Pause(500)
            Journal.Clear()
            Misc.Pause(500)
            continue            
            
        else:
            break  # Exit the loop if no disturbance is detected

            
def goHome():
    # Container definitions
    trash_container = 0x409C3212
    keep_container = 0x42E87E92
    other_container = 0x435ED948
    reg_container = 0x42E88440
    secondary_bolt_container = 0x422E5A11

    # Item classification sets
    specific_items = {0x0F95, 0x1081, 0x0F7E}  # bolts, leather, bones
    loot_list = {0x09B7, 0x0EED, 0x1BF2, 0xBB7C, 0x1F4C}
    trash_list = {0x141B, 0x0FC7}
    excluded_hued_items = {0x22C5, 0x0E79, 0x3679, 0x108A, 0x1EA7}
    special_move = {0x0E86, 0x14FC}  # pickaxe or lockpick
    other_move = {0x2260, 0x0F95}  # leather and bolts

    # Travel and setup
    
    attempt_recall("Winter 2")
    deadCheck()
    Player.PathFindTo(6802, 3901, 12)
    Misc.Pause(1000)

    door = Items.FindBySerial(0x42F89EDC)
    if door and door.ItemID == 0x0677:
        Items.UseItem(door)
        Misc.Pause(500)

    Player.PathFindTo(6803, 3898, 17)
    Misc.Pause(2000)

    for container in [keep_container, other_container]:
        Items.UseItem(container)
        Misc.Pause(500)

    # Phase 1: Main sorting
    backpack_items = Player.Backpack.Contains
    for item in backpack_items:
        if item.ItemID == 0x14EC:  # Treasure map
            props = Items.GetPropStringList(item)
            if any("plainly drawn" in prop.lower() for prop in props):
                Items.Move(item, trash_container, -1)
                Misc.Pause(1000)
            else:
                while not Journal.SearchByName("The treasure is marked by the red pin.", ""):
                    Items.UseItem(item)
                    Misc.Pause(800)
                Misc.SendMessage("Map decoded")
                Misc.Pause(300)
                Journal.Clear()

        elif item.ItemID == 0x0E86:  # Pickaxe
            if "<BASEFONT COLOR=#FFFF00> orcish pickaxe<BASEFONT COLOR=#FFFFFF>" in item.Name:
                Player.ChatSay("Ah, an Orcish Pickaxe!")
                Misc.Pause(300)
            else:
                Items.Move(item, trash_container, -1)
                Misc.Pause(1000)

        elif item.ItemID in specific_items:
            Items.Move(item, other_container, -1)
        elif item.ItemID in loot_list:
            Items.Move(item, keep_container, -1)
        elif item.ItemID in pchest:
            Items.Move(item, reg_container, 1)
        elif item.ItemID in trash_list:
            Items.Move(item, trash_container, 1)
        elif item.ItemID == 0x1081:
            Items.Move(item, other_container, -1)

        Misc.Pause(1000)

    # Phase 2: Restock bandages
    bandage_count = Items.BackpackCount(0x0E21, -1)
    if bandage_count < 100:
        bandages = Items.FindByID(0x0E21, -1, keep_container)
        if bandages:
            Items.Move(bandages, Player.Backpack.Serial, 50)
            Misc.Pause(1000)

    # Phase 3: Reagents
    Items.UseItem(reg_container)
    Misc.Pause(400)
    stockRegs()

    # Phase 4: Final sort (hued junk, runes, statues)
    Player.PathFindTo(6800, 3898, 17)
    Misc.Pause(600)

    backpack_items = Player.Backpack.Contains
    for item in backpack_items:
        if item.ItemID in rune_ids:
            Items.Move(item, rune_destination, 1)
        elif item.ItemID in creature_statue_ids:
            Items.Move(item, statue_destination, -1)
        elif item.ItemID in special_move:
            Items.Move(item, statue_destination, -1)
        elif item.ItemID in other_move:
            Items.Move(item, secondary_bolt_container, 1)
        elif item.Hue != 0x0000 and item.ItemID not in excluded_hued_items:
            Items.Move(item, statue_destination, -1)

        Misc.Pause(1000)


def stockRegs():
    # Define items with their respective IDs and target storage
    reg_items = {
        "root": (0x0F86, 35),
        "moss": (0x0F7B, 35),
        "pearl": (0x0F7A, 50),
        "shade": (0x0F88, 35),
        "garlic": (0x0F84, 35),
        "ginseng": (0x0F85, 35),
        "ash": (0x0F8C, 35),
        "silk": (0x0F8D, 35)
    }

    # Define storage containers
    reg_container = 0x42E88440
    bandage_container = 0x42E87E92

    # Open storage containers
    Items.UseItem(reg_container)
    Misc.Pause(500)
    Items.UseItem(bandage_container)
    Misc.Pause(500)

    # Loop through reg items and adjust amounts
    for name, (item_id, target_amount) in reg_items.items():
        current_amount = Items.BackpackCount(item_id, -1)
        if current_amount < target_amount:
            Items.Move(Items.FindByID(item_id, -1, reg_container), Player.Backpack.Serial, target_amount - current_amount)
            Misc.Pause(1000)
        elif current_amount > target_amount:
            Items.Move(Items.FindByID(item_id, -1, Player.Backpack.Serial), reg_container, current_amount - target_amount)
            Misc.Pause(1000)
        Misc.Pause(1000)

    # Handle bandages separately
    bandage_count = Items.BackpackCount(0x0E21, -1)
    if bandage_count < 200:
        Items.Move(Items.FindByID(0x0E21, -1, bandage_container), Player.Backpack.Serial, 200 - bandage_count)
        Misc.Pause(1000)

    # Handle other loot
    item_ids = [0x0EED, 0x0EF3, 0x0F3F]  # Gold, Scroll, Arrow
    for item_id in item_ids:
        item = Items.FindByID(item_id, -1, Player.Backpack.Serial)
        if item:
            Items.Move(item, bandage_container, -1)
            Misc.Pause(1000)

def run_away_from(mob):
    start_x = Player.Position.X
    start_y = Player.Position.Y

    dx = Player.Position.X - mob.Position.X
    dy = Player.Position.Y - mob.Position.Y

    escape_directions = [
        (dx * 3 if dx != 0 else 3, dy * 3 if dy != 0 else 3),  # go 3 tiles in opposite direction
        (3, 0), (-3, 0), (0, 3), (0, -3),  # cardinal directions
        (3, 3), (-3, -3), (-3, 3), (3, -3)  # diagonals
    ]
    
    for offset_x, offset_y in escape_directions:
        target_x = start_x + offset_x
        target_y = start_y + offset_y

        path = PathFinding.GetPath(target_x, target_y, True)
        if path:
            PathFinding.RunPath(path, 3000)  # Run to safety
            Misc.Pause(2000)
            return True  # success

    Player.HeadMessage(33, "All paths blocked!")
    Misc.Pause(500)
    return False  # failure
            
def checkAndMoveAway(mob, can_ignore=False):
    if not mob:
        return

    distance = Player.DistanceTo(mob)
    if distance <= 1:
            
        run_away_from(mob)
        checkSelfHealth()  # 🩸 Immediately check and flag for healing

        if can_ignore:
            Misc.IgnoreObject(mob)



def detectClosestHostile():
    targets = detectTargets()
    return targets[0] if targets else None
    
    
def calculateDirectionToEscape(mobile):
    # If the mob is exactly on top of the player, pick a random escape direction
    if mobile.Position.X == Player.Position.X and mobile.Position.Y == Player.Position.Y:
        directions = ["North", "Northeast", "East", "Southeast", 
                      "South", "Southwest", "West", "Northwest"]
        return random.choice(directions)

    # Reverse the logic to move away instead of towards the mob
    if mobile.Position.X > Player.Position.X and mobile.Position.Y > Player.Position.Y:
        return 'Up'  # Move opposite of 'Down'
    if mobile.Position.X < Player.Position.X and mobile.Position.Y > Player.Position.Y:
        return 'Right'  # Move opposite of 'Left'
    if mobile.Position.X > Player.Position.X and mobile.Position.Y < Player.Position.Y:
        return 'Left'  # Move opposite of 'Right'
    if mobile.Position.X < Player.Position.X and mobile.Position.Y < Player.Position.Y:
        return 'Down'  # Move opposite of 'Up'
    if mobile.Position.X > Player.Position.X and mobile.Position.Y == Player.Position.Y:
        return 'West'  # Move opposite of 'East'
    if mobile.Position.X < Player.Position.X and mobile.Position.Y == Player.Position.Y:
        return 'East'  # Move opposite of 'West'
    if mobile.Position.X == Player.Position.X and mobile.Position.Y > Player.Position.Y:
        return 'North'  # Move opposite of 'South'
    if mobile.Position.X == Player.Position.X and mobile.Position.Y < Player.Position.Y:
        return 'South'  # Move opposite of 'North'

    return ''
    
def karmaRaise():
    npc = 0x00176F43
    gold = Items.BackpackCount(0x0EED, -1)

    difference = 200 - gold  # Calculate the difference if gold is less than 200

    if gold >= 200:
        for _ in range(20):
            coin = Items.FindByID(0x0EED, -1, Player.Backpack.Serial)
            if coin:
                Items.Move(coin, npc, 1)
                Misc.Pause(1000)
    
    
    
# Movement speed in points per second
movement_speed = 4

# Function to calculate pause based on distance
def calculate_pause(current_x, current_y, dest_x, dest_y):
    # Calculate distance using Pythagorean theorem
    distance = ((dest_x - current_x) ** 2 + (dest_y - current_y) ** 2) ** 0.5
    # Calculate time in seconds and convert to milliseconds
    pause_time = (distance / movement_speed) * 1000
    return int(pause_time)

if worldSavePause:
    Journal.Clear()
    # Randomly select a wait time between 90 and 120 seconds
    wait_time = random.randint(75, 300)
    # Inform the player about the wait time
    Player.ChatSay(64, f"Making a run in {wait_time} seconds.")
    Misc.Pause(wait_time)


pet1 = Mobiles.FindBySerial(primaryPet)
pet2 = Mobiles.FindBySerial(secondaryPet)

if (pet1 and pet1.Hits <= 5) or (pet2 and pet2.Hits <= 5):
    Misc.SendMessage("One or both pets are dead. Stopping script.", 33)
    Misc.Pause(500)
    Misc.ScriptStatus("petTrainer.py")
    Misc.Pause(500)

Journal.Clear()    
worldSave()  
#SellAgent.Enable()
#Misc.Pause(500)
#BuyAgent.Enable()
#Misc.Pause(500)
if not Misc.ScriptStatus("Auto-Loot.py"):
    Misc.ScriptRun("Auto-Loot.py")
#if not Misc.ScriptStatus("petWatcher.py"):
#    Misc.ScriptRun("petWatcher.py")
#
    
#Misc.ClearIgnore()
#Misc.Pause(500)

if not Player.Mount:
    Mobiles.UseMobile(pet2)
    Misc.Pause(500)
    
def farm_cycle():
    locations = [
        "Airs",
        "Airs 2",
        "Despise Titans", 
        "Earths",
        "Earths 2",
        "Deep Earth",
        "Snow Ele",
        "Snow Harpy",
        "Snow Harpy 2",
        "Snow Lady",
        "Overseers"
    ]

    for loc in locations:
        chosen = random.choice(loc) if isinstance(loc, list) else loc
        attempt_recall(chosen)
        detectMobiles()
        attackEvil()
        detectMobiles()
        moveToCorpse()
        worldSave()
        
    sellGems()
    goHome()
    
farm_cycle()
