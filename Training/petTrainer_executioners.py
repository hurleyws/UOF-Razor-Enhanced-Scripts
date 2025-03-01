from System import Int32 as int
from System import Byte
from System.Collections.Generic import List
import time
import random

Spin = Mobiles.FindBySerial(0x0001DDFA)
worldSavePause = False
BandageHeal.Start()


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

def playerPosCheck(operator, value):
    if operator == '<':
        if Player.Position.Z < value:
            goHome()
            Misc.SendMessage("Moved up or down stairs.")
            Misc.Pause(500)
    elif operator == '>':
        if Player.Position.Z > value:
            goHome()
            Misc.SendMessage("Moved up or down stairs.")
            Misc.Pause(500)
    elif operator == '<=':
        if Player.Position.Z <= value:
            goHome()
    elif operator == '>=':
        if Player.Position.Z >= value:
            goHome()
    elif operator == '==':
        if Player.Position.Z == value:
            goHome()
    elif operator == '!=':
        if Player.Position.Z != value:
            goHome()
    else:
        Misc.SendMessage("Invalid operator provided to playerPosCheck", 33)


def detectGreyNames():
    """
    Detects mobiles with notoriety codes 4 or 5 (grey names) and sends a message if any are found.
    Ignores mobs that have "slave" in their property list.
    """
    # Create the filter
    mobFilter = Mobiles.Filter()
    mobFilter.Enabled = True
    mobFilter.IsHuman = True
    mobFilter.Notorieties = List[Byte](bytes([1,2,3,4,5]))  # Notoriety codes 4 (criminals) and 5 (neutral grey names)
    
    # Apply the filter
    greyMobiles = Mobiles.ApplyFilter(mobFilter)
    
    # Check and process the detected mobs
    for mob in greyMobiles:
        mobProps = Mobiles.GetPropStringList(mob)  # Get the property list of the mob
        if mobProps and not any("slave" in prop.lower() for prop in mobProps):
            Player.HeadMessage(34, f"Grey detected: {mob.Name}")  # Show a message above the player's head
            Misc.Pause(500)
            goHome()  # Recall to a safe location
            # Announce the detected grey mobs name
            Player.HeadMessage(34, f"Grey detected: {mob.Name}")  # Show a message above the player's head
            Misc.Pause(500)

            
    if Player.Weight > 330:
        attempt_recall("winter 2")
        Player.HeadMessage(34,"Overweight.")
        Misc.Pause(500)
        Misc.ScriptStop("petTrainer.py")

                
def followMobile(mobile):
    """
    Follows a mobile until the player is within 1 tile of it or the timer times out.
    Dynamically adjusts the target position based on the relative position of the mobile and the player.
    """
    start_time = time.time()  # Record the start time for the timeout

    if Player.DistanceTo(mobile) > 2:
        Spin = Mobiles.FindBySerial(0x0001DDFA)
        if not Spin:
            Misc.SendMessage("Spin not found!")
            return

        mobilePosition = Spin.Position
        playerPosition = Player.Position
        route = PathFinding.Route()
        route.MaxRetry = 5
        route.StopIfStuck = False

        # Determine dynamic adjustments for X and Y based on relative positions
        if mobilePosition.X < playerPosition.X:
            route.X = mobilePosition.X + 1  # Move 1 tile to the right
        elif mobilePosition.X > playerPosition.X:
            route.X = mobilePosition.X - 1  # Move 1 tile to the left
        else:
            route.X = mobilePosition.X  # No adjustment on X axis

        if mobilePosition.Y < playerPosition.Y:
            route.Y = mobilePosition.Y + 1  # Move 1 tile down
        elif mobilePosition.Y > playerPosition.Y:
            route.Y = mobilePosition.Y - 1  # Move 1 tile up
        else:
            route.Y = mobilePosition.Y  # No adjustment on Y axis

        # Execute pathfinding with the dynamically adjusted position
        PathFinding.Go(route)
        Misc.Pause(250)
        Misc.SendMessage(f"Pathfinding to: X={route.X}, Y={route.Y}")
        Misc.Pause(250)
        Misc.SendMessage(f"Current Distance: {Player.DistanceTo(mobile)}")
        Misc.Pause(250)
        deadCheck()


        
def deadCheck():
    if Player.IsGhost:
        Misc.ScriptStopAll(True)

def continuousAttack():
    """
    Continuously applies the filter to find mobiles with notoriety 6,
    attacks them until the list is empty, and then keeps checking for new targets.
    Ensures that the two mobs targeted for provocation have the same Z value as the player.
    """
    # Apply the filter
    mobFilter = Mobiles.Filter()
    mobFilter.Notorieties = List[Byte](bytes([6]))
    mobFilter.CheckLineOfSight = True
    mobFilter.RangeMax = 12
    mobList = Mobiles.ApplyFilter(mobFilter)

    # Filter mobs with the same Z value as the player
    playerZ = Player.Position.Z
    mobList = [mob for mob in mobList if mob.Position.Z == playerZ]
    
    # Create the filter
    slaveFilter = Mobiles.Filter()
    slaveFilter.Enabled = True
    slaveFilter.IsHuman = True
    slaveFilter.RangeMax = 12
    slaveFilter.CheckLineOfSight = True
    slaveFilter.Notorieties = List[Byte](bytes([1, 2, 3, 4, 5]))  # Notoriety codes for grey names
    slaveList = Mobiles.ApplyFilter(slaveFilter)
    
    detectGreyNames()
    
    # Ensure there are at least two mobs with the same Z value
    if len(mobList) > 1:
        # Use Provocation on the first two mobs
        Player.UseSkill("Provocation")
        Misc.Pause(500)
        
        # Target the first mob
        Target.TargetExecute(mobList[0])
        Misc.Pause(500)
        
        # Target the second mob
        Target.TargetExecute(mobList[1])
        Misc.Pause(500)


    if mobList:  # If there are mobs in the list
        for mob in mobList:
            if mob:  # Ensure the mob is valid
                Player.ChatSay("Shuck follow me!")
                Misc.Pause(166)
                Player.ChatSay("Shuck follow me!")
                Misc.Pause(166)
                Player.ChatSay("Shuck follow me!")
                Misc.Pause(166)
                Player.ChatSay("Spin guard me!")
                Misc.Pause(500)
                Player.Attack(mob)
                Misc.Pause(1000)
                Player.ChatSay("Shuck guard me!")
                Misc.Pause(500)
                Player.ChatSay("All guard me!")
                Misc.Pause(500)
                Misc.SendMessage(f"Attacking {mob.Name}")
                Misc.Pause(500)
                Player.Attack(mob)
                while Mobiles.FindBySerial(mob.Serial):  # Wait until the mob is dead
                    Misc.Pause(500)  # Pause to prevent spamming
                    checkPetHealth()
                    followMobile(Spin)
                Misc.Pause(1000)
                followMobile(Spin)
                detectGreyNames()

    elif slaveList:
        for mob in slaveList:
            mobProps = Mobiles.GetPropStringList(mob) 
            if mob and mob.Position.Z > 15 and mobProps and any("slave" in prop.lower() for prop in mobProps):  # Ensure the mob is valid
                Player.ChatSay("Spin guard me!")
                Misc.Pause(500)
                Player.Attack(mob)
                Misc.Pause(500)
                Player.ChatSay("Shuck guard me!")
                Misc.Pause(500)
                Player.ChatSay("All guard me!")
                Misc.Pause(500)
                Misc.SendMessage(f"Attacking {mob.Name}")
                Misc.Pause(500)
                Player.Attack(mob)
                while Mobiles.FindBySerial(mob.Serial):  # Wait until the mob is dead
                    Misc.Pause(500)  # Pause to prevent spamming
                    checkPetHealth()
                    detectGreyNames()
                    followMobile(Spin)
                Misc.Pause(1000)
                followMobile(Spin)
                    



def checkPetHealth():
    """
    Checks the health of Shuck and Spin. If their hits fall below 8,
    the player will say "all follow me" three times with 500 ms pauses and then goHome().
    """
    # Find pets by their serial
    Shuck = Mobiles.FindBySerial(0x0008064C)
    Spin = Mobiles.FindBySerial(0x0001DDFA)

    Misc.Pause(500)

    # Check health of both pets
    if Shuck and Shuck.Hits < 8 or Spin and Spin.Hits < 8 or Player.Hits < 50:
        # Command "all follow me" three times
        for _ in range(3):
            Player.ChatSay(64, "all follow me")
            Misc.Pause(500)  # Pause for 500 milliseconds
        
        # Go home if either pet is in critical condition
        goHome()
        Misc.SendMessage("Health too low, returned home.",35)
        Misc.Pause(500)
    else:
        # Concatenate strings and integer values properly
        Misc.SendMessage(
            "Player health: " + str(Player.Hits) +
            ", Spin health: " + str(Spin.Hits if Spin else "N/A") +
            ", Shuck health: " + str(Shuck.Hits if Shuck else "N/A")
        )
        Misc.Pause(500)
    
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
        Misc.Pause(500)
        Player.ChatSay("All guard me")
        Misc.Pause(500)
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
    lootList = [0x1BD1,0x09F1,0x0EED]
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
    Misc.ScriptStop("petTrainer.py")
    Misc.Pause(500)
    

def stockRegs():
    root = Items.BackpackCount(0x0F86,-1)
    moss = Items.BackpackCount(0x0F7B,-1)
    pearl = Items.BackpackCount(0x0F7A,-1)
    bandages = Items.BackpackCount(0x0E21,-1)
    shade = Items.BackpackCount(0x0F88,-1)
    garlic = Items.BackpackCount(0x0F84,-1)
    ginseng = Items.BackpackCount(0x0F85,-1)
    ash = Items.BackpackCount(0x0F8C,-1)
    silk = Items.BackpackCount(0x0F8D,-1)
    gold = Items.FindByID(0x0EED,-1,Player.Backpack.Serial)
  
    Items.UseItem(0x42E88440)
    Misc.Pause(500)
    Items.UseItem(0x42E87E92)
    Misc.Pause(500)
    

    if root < 15:
        Items.Move(Items.FindByID(0x0F86,-1,0x42E88440),Player.Backpack.Serial,15-root)
        Misc.Pause(1000)
    elif root > 15:
        Items.Move(Items.FindByID(0x0F86,-1,Player.Backpack.Serial),0x42E88440,root-15)
        Misc.Pause(1000)
    else:
        Misc.Pause(200)
    
    if moss < 15:
        Items.Move(Items.FindByID(0x0F7B,-1,0x42E88440),Player.Backpack.Serial,15-moss)
        Misc.Pause(1000)
    elif moss > 15:
        Items.Move(Items.FindByID(0x0F7B,-1,Player.Backpack.Serial),0x42E88440,moss-15)
        Misc.Pause(1000)
    else:
        Misc.Pause(200)
        
    if pearl < 15:
        Items.Move(Items.FindByID(0x0F7A,-1,0x42E88440),Player.Backpack.Serial,15-pearl)
        Misc.Pause(1000)
    elif pearl > 15:
        Items.Move(Items.FindByID(0x0F7A,-1,Player.Backpack.Serial),0x42E88440,pearl-15)
        Misc.Pause(1000)
    else:
        Misc.Pause(200)
        
    if bandages < 200:
        Items.Move(Items.FindByID(0x0E21,-1,0x42E87E92),Player.Backpack.Serial,200-bandages)
        Misc.Pause(1000)        
    if silk < 15:
        Items.Move(Items.FindByID(0x0F8D,-1,0x42E88440),Player.Backpack.Serial,15-silk)
        Misc.Pause(1000)
    if ash < 15:
        Items.Move(Items.FindByID(0x0F8C,-1,0x42E88440),Player.Backpack.Serial,15-ash)
        Misc.Pause(1000)
    if ginseng < 15:
        Items.Move(Items.FindByID(0x0F85,-1,0x42E88440),Player.Backpack.Serial,15-ginseng)
        Misc.Pause(1000)
    if garlic < 15:
        Items.Move(Items.FindByID(0x0F84,-1,0x42E88440),Player.Backpack.Serial,15-garlic)
        Misc.Pause(1000)
    if shade < 15:
        Items.Move(Items.FindByID(0x0F88,-1,0x42E88440),Player.Backpack.Serial,15-shade)
        Misc.Pause(1000)
    if gold:
        Items.Move(gold,0x42E87E92,-1,148, 84)
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

worldSave()    
attempt_recall("Executioners")
continuousAttack()
playerPosCheck("<", 20)

# First stop: x=379
if Player.Position.X < 371:
    destination = (371, 915)
    pause_time = calculate_pause(Player.Position.X, Player.Position.Y, *destination)
    Player.PathFindTo(*destination, 20)
    Misc.Pause(pause_time)

continuousAttack()
playerPosCheck("<", 20)
worldSave()

# Second stop: Between x=379 and x=387 (intermediate point, e.g., x=383)
if Player.Position.X < 378:
    destination = (378, 915)
    pause_time = calculate_pause(Player.Position.X, Player.Position.Y, *destination)
    Player.PathFindTo(*destination, 20)
    Misc.Pause(pause_time)

continuousAttack()
continuousAttack()
continuousAttack()
playerPosCheck("<", 20)
worldSave()

# Third stop: x=387
if Player.Position.X < 383:
    destination = (383, 915)
    pause_time = calculate_pause(Player.Position.X, Player.Position.Y, *destination)
    Player.PathFindTo(*destination, 20)
    Misc.Pause(pause_time)

continuousAttack()
continuousAttack()
continuousAttack()
playerPosCheck("<", 20)
worldSave()

# Fourth stop: y=898
if Player.Position.Y > 911:
    destination = (387, 911)
    pause_time = calculate_pause(Player.Position.X, Player.Position.Y, *destination)
    Player.PathFindTo(*destination, 20)
    Misc.Pause(pause_time)

continuousAttack()
continuousAttack()
continuousAttack()
playerPosCheck("<", 20)
worldSave()

# Fifth stop: Between y=898 and y=892 (intermediate point, e.g., y=895)
if Player.Position.Y > 904:
    destination = (387, 904)
    pause_time = calculate_pause(Player.Position.X, Player.Position.Y, *destination)
    Player.PathFindTo(*destination, 20)
    Misc.Pause(pause_time)

continuousAttack()
continuousAttack()
continuousAttack()
playerPosCheck("<", 20)
worldSave()

# Sixth stop: y=892
if Player.Position.Y > 899:
    destination = (387, 899)
    pause_time = calculate_pause(Player.Position.X, Player.Position.Y, *destination)
    Player.PathFindTo(*destination, 20)
    Misc.Pause(pause_time)

continuousAttack()
continuousAttack()
continuousAttack()
playerPosCheck("<", 20)
worldSave()

# Sixth stop: y=895
if Player.Position.Y > 895:
    destination = (387, 895)
    pause_time = calculate_pause(Player.Position.X, Player.Position.Y, *destination)
    Player.PathFindTo(*destination, 20)
    Misc.Pause(pause_time)

continuousAttack()
continuousAttack()
continuousAttack()
playerPosCheck("<", 20)
worldSave()

# Apply the filter
mobFilter = Mobiles.Filter()
mobFilter.Notorieties = List[Byte](bytes([6]))
mobFilter.CheckLineOfSight = True
mobFilter.RangeMax = 12
mobList = Mobiles.ApplyFilter(mobFilter)

if len(mobList) > 0:
    attempt_recall("Executioners 2")
    continuousAttack()
    continuousAttack()
    continuousAttack()
    playerPosCheck(">", 0)
    worldSave()

    attempt_recall("Executioners 3")
    continuousAttack()
    continuousAttack()
    continuousAttack()
    playerPosCheck(">", 0)
    worldSave()


# Return home
goHome()
Misc.SendMessage("Executioner run complete.",70)


    