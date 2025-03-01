from System import Int32 as int
from System import Byte
from System.Collections.Generic import List
import time
import random
import datetime

farmingEvil = False
farmingFey = True

goldLog = 'C:/Users/Hurley/Documents/GitHub/UOF-Razor-Enhanced-Scripts/Resource Gathering/goldLog.USR'

pchest = [0x0E41,0x09AB,0x0E7C,0x0E40]

rune_ids = {
    0x483B, 0x483E, 0x4841, 0x4844, 0x4847, 0x484A, 0x484D, 0x4850,
    0x4853, 0x4856, 0x4859, 0x485C, 0x485F, 0x4862, 0x4865, 0x4868,
    0x486B, 0x4871, 0x486E, 0x4874, 0x4877, 0x487A, 0x487D, 0x4880, 0x4883
}

creature_statue_ids = {0x2100, 0x25B6, 0x2581}  # IDs for creature statues

rune_destination = 0x417D8A37  # Destination container for runes
statue_destination = 0x42EA55BA  # Destination container for statues

Spin = Mobiles.FindBySerial(0x0001DDFA)
Shuck = Mobiles.FindBySerial(0x0008064C)
Misc.IgnoreObject(Spin)
Misc.Pause(100)
Misc.IgnoreObject(Shuck)
Misc.Pause(100)
worldSavePause = False
BandageHeal.Start()


def log_gold_amount():
    """
    Gets the current gold count in the backpack and appends it to the log file with a timestamp.
    """
    gold_amount = Items.BackpackCount(0x0EED, -1)  # Get gold count (0x0EED is the gold coin ID)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current date and time

    with open(goldLog, 'a') as file:  # 'a' mode appends instead of overwriting
        file.write(f"{timestamp}, {gold_amount}\n")  # Write timestamp and gold amount

    Misc.SendMessage(f"Logged: {timestamp} - Gold: {gold_amount}", 53)

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


#def moveToCorpse(max_retry=5, timeout=5):
#    """
#    Continuously finds and moves to the closest corpse within range.
#    :param max_retry: Maximum retry attempts for each corpse
#    :param timeout: Timeout in seconds for each move attempt
#    """
#    overall_start_time = time.time()  # Overall timer for the entire process
#
#    while True:
#        corpse_list = findCorpses()  # Refresh corpse list dynamically
#
#        if not corpse_list:
#            Misc.SendMessage("No corpses found.", 33)
#            Misc.Pause(500)
#            break  # Exit if no corpses remain
#        
#        # Always get the closest corpse
#        corpse = corpse_list[0]  
#
#        Misc.SendMessage(f"Moving to closest corpse: {corpse.Serial}", 33)
#        Misc.Pause(1000)
#        target_position = corpse.Position
#
#        if Player.DistanceTo(corpse) > 2:
#            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Directions: Down, Up, Right, Left
#            
#            for dx, dy in directions:
#                if time.time() - overall_start_time > 30:  # Overall process timeout (30 seconds)
#                    Misc.SendMessage("Overall timeout exceeded. Exiting function.", 33)
#                    Misc.Pause(500)
#                    return
#
#                target_coords = PathFinding.Route()
#                target_coords.MaxRetry = max_retry
#                target_coords.StopIfStuck = False
#                target_coords.X = target_position.X + dx
#                target_coords.Y = target_position.Y + dy
#
#                success = PathFinding.Go(target_coords)
#                Misc.Pause(500)
#
#                if not success:
#                    Misc.SendMessage(f"Failed to move to position: ({target_coords.X}, {target_coords.Y})", 33)
#                    Misc.Pause(500)
#                    continue
#
#                Misc.Pause(500)
#                deadCheck()
#
#                start_time = time.time()
#                while Player.DistanceTo(corpse) > 2:
#                    if time.time() - start_time > timeout:  # Individual corpse timeout
#                        Misc.SendMessage("Timeout reached for this position. Trying next direction.", 33)
#                        Misc.Pause(500)
#                        break
#
#                    if time.time() - overall_start_time > 30:  # Overall timeout check
#                        Misc.SendMessage("Overall timeout exceeded. Exiting function.", 33)
#                        Misc.Pause(500)
#                        return
#
#                # Check if the player is close enough to the corpse
#                if Player.DistanceTo(corpse) <= 2:
#                    Misc.Pause(1000)
#                    break  # Break out of the direction loop once corpse is reached
#        else:
#            Misc.SendMessage(f"Already close to corpse: {corpse.Serial}", 33)
#            Misc.Pause(500)
#
#        # **Refresh the corpse list dynamically and continue**
#        Misc.Pause(500)
#
#    Misc.SendMessage("Finished processing all corpses.", 33)
#    Misc.Pause(500)

def moveToCorpse(max_retry=5, overall_timeout=30, individual_timeout=5):
    """
    Continuously finds and moves to the closest corpse within range using directional movement.
    
    :param max_retry: Maximum retry attempts for each corpse.
    :param overall_timeout: Maximum time in seconds for the entire function execution.
    :param individual_timeout: Timeout in seconds for reaching each individual corpse.
    """
    overall_start_time = time.time()  # Start overall timeout timer

    while True:
        corpse_list = findCorpses()  # Refresh corpse list dynamically
        if not corpse_list:
            Misc.SendMessage("No corpses found.", 33)
            Misc.Pause(500)
            break  # Exit if no corpses remain

        corpse = corpse_list[0]  # Always get the closest corpse
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
                Misc.SendMessage("Timeout reached for this corpse. Moving to next.", 33)
                Misc.Pause(500)
                break  # Stop trying to reach this corpse and move to the next one

            # Determine the best direction to move towards the corpse
            direction = calculateDirectionToRun(corpse)
            if direction:
                Player.Walk(direction)
                Misc.Pause(300)  # Prevent excessive movement requests
            
            deadCheck()  # Ensure safe movement
        
        Misc.SendMessage(f"Reached corpse: {corpse.Serial}", 33)
        Misc.Pause(500)  # Short delay before processing next corpse

    Misc.SendMessage("Finished processing all corpses.", 33)
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
        else:
            Misc.SendMessage('Pausing for world save.', 33)
        
        # Loop until a resume condition occurs
        while True:
            Misc.Pause(1000)

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



def detectGreyNames():
    """
    Detects mobiles with notoriety codes 4 or 5 (grey names) and sends a message if any are found.
    Ignores mobs that have "slave" in their property list.
    """
    # Create the filter
    mobFilter = Mobiles.Filter()
    mobFilter.Enabled = True
    mobFilter.IsHuman = True
    mobFilter.Notorieties = List[Byte](bytes([1,3,6]))  # Notoriety codes 4 (criminals) and 5 (neutral grey names)
    
    # Apply the filter
    greyMobiles = Mobiles.ApplyFilter(mobFilter)
    
    # Check and process the detected mobs
    for mob in greyMobiles:
        if mob.Name == "Teddy Ruxpin":
            Misc.SendMessage("Known grey detected, continuing...",33)
            Misc.Pause(500)
            Misc.IgnoreObject(mob)
            Misc.Pause(500)
            return
        mobProps = Mobiles.GetPropStringList(mob)  # Get the property list of the mob
        if mobProps and not any("slave" in prop.lower() for prop in mobProps):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current date/time
            log_entry = f"{timestamp}, {mob.Name}\n"  # Format log entry

            # Append to greyLog file
            with open(goldLog, 'a') as file:
                file.write(log_entry)
            goHome()  # Recall to a safe location
            Misc.ScriptStop("petTrainer.py")
            Misc.Pause(500)
            # Announce the detected grey mobs name


            
    if Player.Weight > 330:
        Player.HeadMessage(34,"Overweight.")
        Misc.Pause(500)
        log_gold_amount()
        goHome()
        Misc.ScriptStop("petTrainer.py")
        Misc.Pause(500)

                
def followMobile(mobile):
    """
    Follows a mobile until the player is within 1 tile of it or the timer times out.
    Dynamically adjusts the target position based on the relative position of the mobile and the player.
    """
    if mobile is None:
        Misc.SendMessage("Error: Mobile is None!", 33)
        Misc.Pause(500)
        return

    if mobile.Position is None:
        Misc.SendMessage("Error: Mobile position is None!", 33)
        Misc.Pause(500)
        return

    start_time = time.time()  # Record the start time for the timeout

    # Check initial distance
    distance = Player.DistanceTo(mobile)
    Misc.Pause(100)

    if distance > 5:
        Spin = Mobiles.FindBySerial(0x0001DDFA)
        if not Spin or Spin.Position is None:
            Misc.SendMessage("Spin not found or has no position!", 33)
            Misc.Pause(500)
            return

        route = PathFinding.Route()
        route.MaxRetry = 5
        route.StopIfStuck = False

        # Determine dynamic adjustments for X and Y based on relative positions
        route.X = Spin.Position.X + (3 if Spin.Position.X < Player.Position.X else -3)
        route.Y = Spin.Position.Y + (3 if Spin.Position.Y < Player.Position.Y else -3)

        # Execute pathfinding with the dynamically adjusted position
        if mobile:
            Misc.Pause(500)
            PathFinding.Go(route)
            Misc.Pause(500)
            
            Misc.SendMessage(f"Pathfinding to: X={route.X}, Y={route.Y}", 66)
            Misc.Pause(500)
            
            # Check distance again after moving
            new_distance = Player.DistanceTo(mobile)
            Misc.Pause(500)

            deadCheck()



        
def deadCheck():
    if Player.IsGhost:
        Misc.ScriptStopAll(True)

        
def attackEvil():
    Spin = Mobiles.FindBySerial(0x0001DDFA)
    Shuck = Mobiles.FindBySerial(0x0008064C)
    """
    Continuously applies the filter to find mobiles with notoriety 6,
    attacks them until the list is empty, and then keeps checking for new targets.
    Ensures that the two mobs targeted for provocation have the same Z value as the player.
    """
    while True:
        Misc.IgnoreObject(Spin)
        Misc.Pause(100)
        Misc.IgnoreObject(Shuck)
        Misc.Pause(100)
        
        # Apply the filter
        mobFilter = Mobiles.Filter()
        mobFilter.Notorieties = List[Byte](bytes([3,4]))
        mobFilter.CheckLineOfSight = True
        mobFilter.RangeMax = 11
        mobFilter.CheckIgnoreObject = True
        mobList = sorted(Mobiles.ApplyFilter(mobFilter), key=lambda mob: Player.DistanceTo(mob))  # Sort by greatest distance
        
        if not mobList:
            Misc.Pause(500)
            break  # Restart loop if no mobs found
        
        mob = mobList[0]  # Always start with the closest mob
            
        # Proceed with attacking
        Player.ChatSay("All guard me")
        Misc.Pause(600)
        Player.Attack(mob)
        Misc.Pause(500)
        Misc.Pause(2000) #positioning delay

        start_time = time.time()  # Start the timer
        while Mobiles.FindBySerial(mob.Serial):  # Wait until the mob is dead
            if time.time() - start_time > 38:  # If more than 40 seconds passed, move to the next mob
                Misc.SendMessage(f"Timeout reached, moving to next target.", 33)
                Misc.Pause(200)
                break
            Misc.Pause(500)  # Pause to prevent spamming
            checkPetHealth()
            #######EXPERIMENT ZONE##############
#            followMobile(mob)
            if mob and Player.DistanceTo(Spin) > 6:
                for x in range (3):
                    Player.Walk(calculateDirectionToRun(Spin))
                    Misc.Pause(300)
            if mob and Player.DistanceTo(Shuck) > 6:
                for x in range (3):
                    Player.Walk(calculateDirectionToRun(Shuck))
                    Misc.Pause(300)
            if mob and Player.DistanceTo(Shuck) <=1 or Player.DistanceTo(Spin) <= 1:
                Player.Attack(mob)
                Misc.Pause(500)
                
            # Keep trying to move away inside loop, but never ignore
            checkAndMoveAway(mob, can_ignore=False)
        Misc.Pause(1000)
        Spin = Mobiles.FindBySerial(0x0001DDFA)
        Shuck = Mobiles.FindBySerial(0x0008064C)
        if Shuck.Hits < 18 or Spin.Hits < 18:
            Player.ChatSay(64, "all follow me")
            Misc.Pause(500)
            BandageHeal.Start()
            while Spin.Hits < 22 or Shuck.Hits < 22:
                Misc.Pause(1000)
                Spin = Mobiles.FindBySerial(0x0001DDFA)
                Shuck = Mobiles.FindBySerial(0x0008064C)
            BandageHeal.Stop()

        

        gatherPets()
        worldSave()
        detectGreyNames() 
    
def gatherPets():
    timeout = time.time() + 10  # Set 10-second timeout
    Spin = Mobiles.FindBySerial(0x0001DDFA)
    Shuck = Mobiles.FindBySerial(0x0008064C)  
    while Player.DistanceTo(Shuck) > 1 or Player.DistanceTo(Spin) > 1:
        if time.time() > timeout:  # If 10 seconds have passed, call followMobile()
            Player.ChatSay("All follow me")
            Misc.Pause(3000)
            if Player.DistanceTo(Spin) > 1:
                for x in range (5):
                    Player.Run(calculateDirectionToRun(Spin))
                    Misc.Pause(500)
            if Player.DistanceTo(Shuck) >1:
                for x in range (5):
                    Player.Run(calculateDirectionToRun(Shuck))
                    Misc.Pause(500)
            
        Misc.Pause(100)
        Misc.SendMessage("Waiting for pets to heal.", 33)
        Misc.Pause(500)

     
        
        # Refresh pet references in case of position updates
        Spin = Mobiles.FindBySerial(0x0001DDFA)
        Shuck = Mobiles.FindBySerial(0x0008064C)    

def attackFey():
    Spin = Mobiles.FindBySerial(0x0001DDFA)
    Shuck = Mobiles.FindBySerial(0x0008064C)
    """
    Continuously applies the filter to find mobiles with notoriety 6,
    attacks them until the list is empty, and then keeps checking for new targets.
    Ensures that the two mobs targeted for provocation have the same Z value as the player.
    """
    while True:
        Misc.IgnoreObject(Spin)
        Misc.Pause(100)
        Misc.IgnoreObject(Shuck)
        Misc.Pause(100)
        
        # Apply the filter
        mobFilter = Mobiles.Filter()
        mobFilter.Notorieties = List[Byte](bytes([3,4]))
        mobFilter.CheckLineOfSight = True
        mobFilter.RangeMax = 11
        mobFilter.CheckIgnoreObject = True
        mobList = sorted(Mobiles.ApplyFilter(mobFilter), key=lambda mob: Player.DistanceTo(mob), reverse = True)  # Sort by greatest distance
        
        if not mobList:
            Misc.Pause(500)
            break  # Restart loop if no mobs found
        
        mob = mobList[0]  # Always start with the closest mob
        
        if mob.Name == "a serpentine dragon" or Player.DistanceTo(mob) < 3:
            reason = "Too Close" if Player.DistanceTo(mob) < 3 else "too dangerous"
            Misc.SendMessage(f"Ignoring {mob.Name} - {reason}", 33)  # 33 is red
            Misc.Pause(600)
            Misc.IgnoreObject(mob)
            Misc.Pause(500)
            continue
            
            
        # Proceed with attacking
        Player.ChatSay("All kill")
        Misc.Pause(500)
        if Target.HasTarget():
            Target.TargetExecute(mob)
        else:
            Spells.CastMagery("Greater Heal")
            Misc.Pause(1500)
            Target.Self()
        Player.ChatSay("All kill")
        Misc.Pause(500)
        if Target.HasTarget():
            Target.TargetExecute(mob)
        else:
            Spells.CastMagery("Greater Heal")
            Misc.Pause(1500)
            Target.Self()
        Misc.Pause(2500) #positioning delay

        start_time = time.time()  # Start the timer
        while Mobiles.FindBySerial(mob.Serial):  # Wait until the mob is dead
            if time.time() - start_time > 38:  # If more than 40 seconds passed, move to the next mob
                Misc.SendMessage(f"Timeout reached, moving to next target.", 33)
                Misc.Pause(200)
                break
            Misc.Pause(500)  # Pause to prevent spamming
            checkPetHealth()
            #######EXPERIMENT ZONE##############
#            followMobile(mob)
            if mob and Player.DistanceTo(Spin) > 6:
                for x in range (3):
                    Player.Walk(calculateDirectionToRun(Spin))
                    Misc.Pause(300)
            if mob and Player.DistanceTo(Shuck) > 6:
                for x in range (3):
                    Player.Walk(calculateDirectionToRun(Shuck))
                    Misc.Pause(300)
            if mob and Player.DistanceTo(Shuck) <=1 or Player.DistanceTo(Spin) <= 1:
                Player.ChatSay("All kill")
                if Target.HasTarget():
                    Target.TargetExecute(mob)
                else:
                    Spells.CastMagery("Greater Heal")
                    Misc.Pause(1500)
                    Target.Self()
                Misc.Pause(500)
                
            # Keep trying to move away inside loop, but never ignore
            checkAndMoveAway(mob, can_ignore=False)
        Misc.Pause(1000)
        Spin = Mobiles.FindBySerial(0x0001DDFA)
        Shuck = Mobiles.FindBySerial(0x0008064C)
        if Shuck.Hits < 18 or Spin.Hits < 18:
            Player.ChatSay(64, "all follow me")
            Misc.Pause(500)
            BandageHeal.Start()
            while Spin.Hits < 22 or Shuck.Hits < 22:
                Misc.Pause(1000)
                Spin = Mobiles.FindBySerial(0x0001DDFA)
                Shuck = Mobiles.FindBySerial(0x0008064C)
            BandageHeal.Stop()

        timeout = time.time() + 10  # Set 10-second timeout

        while Player.DistanceTo(Shuck) > 1 or Player.DistanceTo(Spin) > 1:
            if time.time() > timeout:  # If 10 seconds have passed, call followMobile()
                Player.ChatSay("All follow me")
                Misc.Pause(3000)
                if Player.DistanceTo(Spin) > 1:
                    for x in range (5):
                        Player.Run(calculateDirectionToRun(Spin))
                        Misc.Pause(500)
                if Player.DistanceTo(Shuck) >1:
                    for x in range (5):
                        Player.Run(calculateDirectionToRun(Shuck))
                        Misc.Pause(500)
                
            Misc.Pause(100)
            Misc.SendMessage("Waiting for pets to heal.", 33)
            Misc.Pause(500)

         
            
            # Refresh pet references in case of position updates
            Spin = Mobiles.FindBySerial(0x0001DDFA)
            Shuck = Mobiles.FindBySerial(0x0008064C)

            
        worldSave()
        detectGreyNames()     



                   


def checkPetHealth():
    # Find pets by their serial
    Shuck = Mobiles.FindBySerial(0x0008064C)
    Spin = Mobiles.FindBySerial(0x0001DDFA)

    Misc.Pause(500)

    # Check players health and act accordingly
    if Player.Hits < 25:
        Misc.SendMessage("Health critically low, returning home!", 35)  
        Misc.Pause(500)
        goHome()
        Misc.ScriptStop("petTrainer.py")
        Misc.Pause(500)
        return  # Exit function to prevent further execution
    elif Player.Hits < 61:
        Spells.CastMagery("Greater Heal")
        Target.WaitForTarget(10000, False)
        Target.TargetExecute(Player.Serial)
        Misc.Pause(500)
    
    # Check health of both pets
    if (Shuck and Shuck.Hits < 8) or (Spin and Spin.Hits < 8):
        # Command "all follow me" three times
        for _ in range(3):
            Player.ChatSay(64, "all follow me")
            Misc.Pause(500)  # Pause for 500 milliseconds
        
        # Go home if a pet is critically low
        goHome()
        Misc.SendMessage("A pets health is too low, returning home!", 35)
        Misc.ScriptStop("petTrainer.py")
        Misc.Pause(500)
        return  # Exit function
    
    
    # Notify if either pet is missing
    if not Shuck or not Spin:
        missing_pets = []
        if not Shuck:
            missing_pets.append("Shuck")
        if not Spin:
            missing_pets.append("Spin")
        Misc.SendMessage(f"The following pet(s) are not found: {', '.join(missing_pets)}")
        Misc.Pause(500)



def attempt_recall(location):
    while True:
        Player.ChatSay("All guard me")
        Misc.Pause(250)
        Player.ChatSay("All guard me")
        Misc.Pause(250)
        gatherPets()
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
    attempt_recall("Winter 2")
    deadCheck()
    Player.PathFindTo(6802, 3901, 12)
    Misc.Pause(1500)
    door = Items.FindBySerial(0x42F89EDC)
    if door.ItemID == 0x0677:
        Items.UseItem(door)
        Misc.Pause(500)
    Player.PathFindTo(6803, 3897, 17)
    Misc.Pause(2500)
    Items.UseItem(0x42E87E92)
    Misc.Pause(500)
    Items.UseItem(0x435ED948)
    Misc.Pause(500)
    lootList = [0x1BD1,0x09F1,0x0EED,0x1BF2]
    for i in Player.Backpack.Contains:
        if i.ItemID == 0x0F95 or i.ItemID == 0x1081 or i.ItemID == 0x0F7E: #bolt, leather, bones
            Items.Move(i,0x435ED948,-1)
            Misc.Pause(1000)
    for i in Player.Backpack.Contains:
        if i.ItemID in lootList: #feather, meat, or gold
            Items.Move(i,0x42E87E92,-1)
            Misc.Pause(1000)
    bandages = Items.BackpackCount(0x0E21,-1)
    bolts = Items.ContainerCount(0x435ED948,0x0F95,-1)
    bolts = Items.FindByID(0x0F95,-1,0x435ED948)
    if bandages < 100:
        bandages = Items.FindByID(0x0E21,-1,0x42E87E92)
        Misc.Pause(500)
        Items.Move(bandages,Player.Backpack.Serial,50)
        Misc.Pause(1000)
    Misc.Pause(500)
    Items.UseItem(0x42E88440)
    Misc.Pause(500)
    stockRegs()
    Player.PathFindTo(6800, 3898, 17)
    Misc.Pause(2500)
    for item in Player.Backpack.Contains:
        if item.ItemID in rune_ids:
            Items.Move(item, rune_destination, 1)
            Misc.Pause(1000)
        elif item.ItemID in creature_statue_ids:
            Items.Move(item, statue_destination, 1)
            Misc.Pause(1000)
        elif item.ItemID in pchest:
            Items.Move(item, statue_destination, 1)
            Misc.Pause(1000)
        elif item.ItemID == 0x2260: #skill scroll ID
            Items.Move(item, 0x422E5A11, 1)
            Misc.Pause(1000)

def stockRegs():
    # Define items with their respective IDs and target storage
    reg_items = {
        "root": (0x0F86, 35),
        "moss": (0x0F7B, 35),
        "pearl": (0x0F7A, 35),
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

def checkAndMoveAway(mob, can_ignore=False):
    if mob is None or mob.Position is None:
        return True  # No valid mob, treat as success

    if Player.DistanceTo(mob) < 2:
        Misc.SendMessage("Too close for comfort", 53)
        Misc.Pause(500)

        # Get the correct direction to run away
        direction = calculateDirectionToEscape(mob)

        # If a valid direction is found, run away
        if direction:
            for _ in range(3):  # Run three steps away
                Player.Run(direction)
                Misc.Pause(300)  # Small delay between each step

        Misc.Pause(1500)  # Allow time to move

        if Player.DistanceTo(mob) >= 2:
            return True  # Successfully moved away

        if can_ignore:
            Misc.SendMessage(f"Couldn't create distance from {mob.Name}, ignoring.", 33)
            Misc.Pause(500)
            Misc.IgnoreObject(mob)
            Misc.Pause(250)
            return False  # Ignored the mob

    return True  # Already at a safe distance


def calculateDirectionToEscape(mobile):
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

feylocations = ["serpentine", "serpentine 2", "serpentine 3", "serpentine 4", "serpentine 5", "serpentine 6","Despise", "serpentine 7", "serpentine 8", "serpentine 9"]
evil_locations = ["overseers", "orcs", "orcs too"]
    
    
worldSave()  
Misc.Beep()  
Misc.Pause(500)
SellAgent.Enable()
Misc.Pause(500)
BuyAgent.Enable()
Misc.Pause(500)
BandageHeal.Stop()
Misc.Pause(500)
Misc.ScriptRun("Auto-Loot.py")
Misc.Pause(500)
Misc.ClearIgnore()
Misc.Pause(500)

if farmingFey:
    for location in feylocations:
        Misc.SendMessage(f"Recalling to: {location}", 33)
        Misc.Pause(500)
        attempt_recall(location)
        attackFey()
        corpse_list = findCorpses()
        if corpse_list:
            moveToCorpse(max_retry=5, overall_timeout=30, individual_timeout=5)
        else:
            Misc.SendMessage(f"No corpses found at {location}.", 33)
        Misc.Pause(1000)  # Pause for a moment before moving to the next location
        worldSave()
        attackFey()
        corpse_list = findCorpses()
        if corpse_list:
            moveToCorpse(max_retry=5, overall_timeout=30, individual_timeout=5)
        else:
            Misc.SendMessage(f"No corpses found at {location}.", 33)
        Misc.Pause(1000)  # Pause for a moment before moving to the next location


    attempt_recall("karma")
    karmaRaise()
    worldSave()   
    attempt_recall("Sell Gems")
    Misc.WaitForContext(0x0026BFC1, 10000)
    Misc.ContextReply(0x0026BFC1, 2)
    Misc.Pause(500)
    Misc.WaitForContext(0x0026CC5D, 10000)
    Misc.ContextReply(0x0026CC5D, 2)
    Misc.Pause(500)
    worldSave()   
    attempt_recall("Buy Regs")
    Misc.WaitForContext(0x0026D40E, 10000)
    Misc.ContextReply(0x0026D40E, 1)
    Misc.Pause(500)
    log_gold_amount()       
    # Return home
    worldSave()   
    goHome()

if farmingEvil:
    for location in evil_locations:
        Misc.SendMessage(f"Recalling to: {location}", 33)
        Misc.Pause(500)
        attempt_recall(location)
        attackEvil()
        corpse_list = findCorpses()
        if corpse_list:
            moveToCorpse(max_retry=5, overall_timeout=30, individual_timeout=5)
        else:
            Misc.SendMessage(f"No corpses found at {location}.", 33)
        Misc.Pause(1000)  # Pause for a moment before moving to the next location
        worldSave()
        attackEvil()
        corpse_list = findCorpses()
        if corpse_list:
            moveToCorpse(max_retry=5, overall_timeout=30, individual_timeout=5)
        else:
            Misc.SendMessage(f"No corpses found at {location}.", 33)
        Misc.Pause(1000)  # Pause for a moment before moving to the next location
        
    worldSave()   
    log_gold_amount()       
    # Return home
    worldSave()   
    goHome()
    



    