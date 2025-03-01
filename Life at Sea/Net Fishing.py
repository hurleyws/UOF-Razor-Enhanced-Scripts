# Importing required modules and libraries
from Scripts import config
from Scripts.glossary.colors import colors
from Scripts.glossary.items.containers import FindHatch
from Scripts.glossary.items.tools import tools
from Scripts.utilities.items import FindItem, MoveItem
from System.Collections.Generic import List
from System import Byte
from System import Int32 as int

#SET NET TYPE
net_container = 0x42C396E3 #regular
#net_container = 0x400B331C #fabled

# Consolidated configuration for items and containers
min_arrows = 750
min_bandages = 150
min_poles = 8
min_pearl = 15
min_moss = 15
min_root = 15
min_ash = 15
min_cure = 10
min_heal = 10
cure_id = 0x0F07 #cure pots
heal_id = 0x0F0C #heal pots
net_id = 0x0DCA
mib_id = 0x099F
mib_container = 0x405A1E11
fish_id = 0x097A
fish_container = 0x4641DD1D
supply_container = 0x4043C469  # Replace with the actual Serial of the supply container
pole_container = 0x43DE1F06
pole_pouch = 0x40680829
gold_ID = 0x0EED
corpse_ID = 0x2006
scale_ID = 0x26B4
gold_ID = 0x0EED
net_ID = 0x0DCA
sos_ID = 0x099F
rope_ID = 0x14F8
ingot_ID = 0x1BF2
horned_ID = 0x1081
tmap_ID = 0x14EC
recipe_ID = 0x2831
meat_ID = 0x09F1
rope_ID = 0x14F8
dragdelay = 1000
corpse_ID = 0x2006
scale_ID = 0x26B4
gold_ID = 0x0EED
net_ID = 0x0DCA
sos_ID = 0x099F
rope_ID = 0x14F8
ingot_ID = 0x1BF2
horned_ID = 0x1081
peal_ID = 0x0F7A
tmap_ID = 0x14EC
recipe_ID = 0x2831
meat_ID = 0x09F1
rune_ids = [0x483B,0x483E,0x4841,0x4844,0x4847,0x484A,0x484D,0x4850,0x4853,0x4856,0x4859,0x485C,0x485F,0x4862,0x4865,0x4868,0x486B,0x4871,0x486E,0x4874,0x4877,0x487A,0x487D,0x4880,0x4883]
loot = [peal_ID, scale_ID,gold_ID, net_ID, sos_ID, rope_ID, ingot_ID,horned_ID,recipe_ID]
loot_list  = loot + rune_ids

# Delay configurations and other settings
dragdelay = 1000  # Delay for dragging items or actions

# HELPER FUNCTIONS
def adjustStock(itemID, threshold, containerID, targetCount, isRods=False):
    """Helper function to move items to/from the backpack based on count."""
    currentCount = Items.BackpackCount(itemID, -1)
    
    if currentCount < threshold:
        if isRods:
            # Move individual rods one at a time
            for x in range(0, threshold - currentCount):
                Items.Move(Items.FindByID(itemID, -1, containerID), Player.Backpack.Serial, 1)
                Misc.Pause(1000)
        else:
            Items.Move(Items.FindByID(itemID, -1, containerID), Player.Backpack.Serial, threshold - currentCount)
            Misc.Pause(1000)
    elif currentCount > threshold:
        if isRods:
            # Move individual rods one at a time
            for x in range(0, currentCount - threshold):
                Items.Move(Items.FindByID(itemID, -1, Player.Backpack.Serial), containerID, 1)
                Misc.Pause(1000)
        else:
            Items.Move(Items.FindByID(itemID, -1, Player.Backpack.Serial), containerID, currentCount - threshold)
            Misc.Pause(1000)
    else:
        Misc.Pause(200)

def checkAndRestock(itemID, min_count, supply_container):
    count = Items.BackpackCount(itemID, -1)
    if count < min_count:
        item_to_move = Items.FindByID(itemID, -1, supply_container)
        if item_to_move:
            move_count = min_count - count
            Items.Move(item_to_move, Player.Backpack.Serial, move_count)
            Misc.Pause(1000)  # Adjust delay as needed

def supplyRun():
    # Recall and move to the supply location
    Player.ChatSay("[recall Winter Lodge")
    Misc.Pause(2500)
    Player.PathFindTo(6783, 3899, 17) #auto open door
    Misc.Pause(2000)
    door = Items.FindBySerial(0x42F89EBD)
    if door.ItemID == 0x06A7:
        Items.UseItem(door)
        Misc.Pause(500)
    Player.PathFindTo(6783, 3897, 17) #stand by gold cabinet
    Misc.Pause(2000)
    gold = Items.FindByID(0x0EED,-1,Player.Backpack.Serial)
    if gold:
        Items.Move(gold,0x408E8DA8,-1)
        Misc.Pause(1000)
    Player.PathFindTo(6779, 3893, 17)
    Misc.Pause(4500)

    # Open supply containers
    Items.UseItem(supply_container)
    Misc.Pause(500)
    Items.UseItem(pole_container)
    Misc.Pause(500)
    Items.UseItem(pole_pouch)
    Misc.Pause(500)


    # Check and restock items
    adjustStock(0x0F86, 15, 0x4043C469, 15)  # Root
    adjustStock(0x0F7B, 15, 0x4043C469, 15)  # Moss
    adjustStock(0x0F7A, 15, 0x4043C469, 15)  # Pearl
    adjustStock(0x0F8C, 15, 0x4043C469, 15)  # Ash
    
    # Bandages, Arrows, Cure, and Heal with different thresholds
    adjustStock(0x0E21, 150, 0x4043C469, 150)  # Bandages
    adjustStock(0x0F3F, 750, 0x4043C469, 750)  # Arrows
    adjustStock(0x0F07, 10, 0x4043C469, 10)  # Cure
    adjustStock(0x0F0C, 10, 0x4043C469, 10)  # Heal
    adjustStock(0x0F0E, 0, 0x4043C469, 0)  # Bottles
    
    if Items.FindByID(net_id, -1, Player.Backpack.Serial) or \
       Items.FindByID(mib_id, -1, Player.Backpack.Serial) or \
       Items.FindByID(gold_ID, -1, Player.Backpack.Serial) or \
       Items.FindByID(fish_id, -1, Player.Backpack.Serial):

        # Execute pathfinding and pausing sequences
        Player.PathFindTo(6785, 3885, 17)
        Misc.Pause(4000)
        Player.PathFindTo(6789, 3880, 17)
        Misc.Pause(3500)
        Player.PathFindTo(6803, 3882, 17)
        Misc.Pause(8000)
        
        # Open each container
        Items.UseItem(net_container)
        Misc.Pause(500)  # Adjust pause as necessary
        Items.UseItem(mib_container)
        Misc.Pause(500)  # Adjust pause as necessary
        Items.UseItem(fish_container)
        Misc.Pause(500)  # Adjust pause as necessary

        nets = Items.BackpackCount(0x0DCA,-1)
        min_nets = 12

        
        for x in range(0,min_nets-nets):
            checkAndRestock(0x0DCA, min_nets, net_container)
            Misc.Pause(200)
            
        # Move items to their respective containers
        while True:
            if Items.FindByID(mib_id, -1, Player.Backpack.Serial):
                Items.UseItem(Items.FindByID(mib_id, -1, Player.Backpack.Serial))
                Misc.Pause(500)
                Items.Move(Items.FindByID(0x14EE,-1, Player.Backpack.Serial), mib_container, 1)
                Misc.Pause(1000)
            elif Items.FindByID(fish_id, -1, Player.Backpack.Serial):
                Items.Move(Items.FindByID(fish_id,-1, Player.Backpack.Serial), fish_container, -1)
                Misc.Pause(1000)
            elif Items.FindByID(gold_ID, -1, Player.Backpack.Serial):
                Items.Move(Items.FindByID(gold_ID,-1, Player.Backpack.Serial), fish_container, -1)
                Misc.Pause(1000)
            elif Items.FindByID(scale_ID, -1, Player.Backpack.Serial):
                Items.Move(Items.FindByID(scale_ID,-1, Player.Backpack.Serial), fish_container, -1)
                Misc.Pause(1000)
            elif Items.FindByID(horned_ID, -1, Player.Backpack.Serial):
                Items.Move(Items.FindByID(horned_ID,-1, Player.Backpack.Serial), fish_container, -1)
                Misc.Pause(1000)
            elif Items.FindByID(rope_ID, -1, Player.Backpack.Serial):
                Items.Move(Items.FindByID(rope_ID,-1, Player.Backpack.Serial), fish_container, -1)
                Misc.Pause(1000)
            else:
                break
                
        rune = Items.FindByID(0x1F14,0x003d,Player.Backpack.Serial)
        Misc.Pause(200)
        if rune:
            Spells.Cast("Recall")
            Misc.Pause(2500)
            Target.TargetExecute(rune)
            Misc.Pause(2500)
            Player.PathFindTo(Player.Position.X,Player.Position.Y+1,Player.Position.Z)
            Misc.Pause(500)
            equipBow()
        else:
            Player.ChatSay("No ship rune found.")

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

def FollowMobile( mobile, maxDistanceToMobile = 4):
    
    mobilePosition = mobile.Position
    playerPosition = Player.Position
    directionToWalk = ''
    if mobilePosition.X > playerPosition.X and mobilePosition.Y > playerPosition.Y:
        directionToWalk = 'back one'
    if mobilePosition.X < playerPosition.X and mobilePosition.Y > playerPosition.Y:
        directionToWalk = 'left one'
    if mobilePosition.X > playerPosition.X and mobilePosition.Y < playerPosition.Y:
        directionToWalk = 'right one'
    if mobilePosition.X < playerPosition.X and mobilePosition.Y < playerPosition.Y:
        directionToWalk = 'forward one'
    if mobilePosition.X > playerPosition.X and mobilePosition.Y == playerPosition.Y:
        directionToWalk = 'right one'
    if mobilePosition.X < playerPosition.X and mobilePosition.Y == playerPosition.Y:
        directionToWalk = 'left one'
    if mobilePosition.X == playerPosition.X and mobilePosition.Y > playerPosition.Y:
        directionToWalk = 'back one'
    if mobilePosition.X == playerPosition.X and mobilePosition.Y < playerPosition.Y:
        directionToWalk = 'forward one'

    playerPosition = Player.Position
    Misc.Pause(200)
    Player.ChatSay( directionToWalk )

def poisonCheck():
    cure = Items.FindByID(0x0F07,-1,Player.Backpack.Serial)
    heal = Items.FindByID(0x0F0C,-1,Player.Backpack.Serial)
    if cure:
        if Player.Poisoned:
            Items.UseItem(cure)
            Misc.Pause(500)
    if heal:
        if Player.Hits < 50:
            Player.ChatSay("Back")
            Misc.Pause(500)
            Misc.Beep()
            Misc.Pause(500)
            Items.UseItem(heal)
            Misc.Pause(5000)
            Player.ChatSay("Stop")
            Misc.Pause(5000)

def returnToOriginalPosition(originalPosition, directionToReturn):
    while Player.Position != originalPosition:
        Player.ChatSay(directionToReturn)
        Misc.Pause(500)
        directionToReturn = calculateDirectionToSail(originalPosition, Player.Position)            
            
def calculateDirectionToSail(mobilePosition, playerPosition):
    # Logic to calculate the direction to walk based on positions
    if mobilePosition.X > playerPosition.X and mobilePosition.Y > playerPosition.Y:
        return 'back one'
    if mobilePosition.X < playerPosition.X and mobilePosition.Y > playerPosition.Y:
        return 'left one'
    if mobilePosition.X > playerPosition.X and mobilePosition.Y < playerPosition.Y:
        return 'right one'
    if mobilePosition.X < playerPosition.X and mobilePosition.Y < playerPosition.Y:
        return 'forward one'
    if mobilePosition.X > playerPosition.X and mobilePosition.Y == playerPosition.Y:
        return 'right one'
    if mobilePosition.X < playerPosition.X and mobilePosition.Y == playerPosition.Y:
        return 'left one'
    if mobilePosition.X == playerPosition.X and mobilePosition.Y > playerPosition.Y:
        return 'back one'
    if mobilePosition.X == playerPosition.X and mobilePosition.Y < playerPosition.Y:
        return 'forward one'
    return ''   

def FindLootReturn(corpse):
    # Coordinates to ignore
    ignored_position = (Player.Position.X - 1, Player.Position.Y - 4, Player.Position.Z - 3)
    
    # Check if the corpse is at the ignored position
    if (corpse.Position.X, corpse.Position.Y, corpse.Position.Z) == ignored_position:
        Misc.SendMessage("Ignoring this corpse at the specified position.")
        Misc.Pause(500)
        return  # Exit the function if the position matches

    directionToCorpse = calculateDirectionToSail(corpse.Position, Player.Position)

    # Move to the corpse
    while Player.DistanceTo(corpse) > 2:     
        # Adjust the distance as needed
        Player.ChatSay(directionToCorpse)
        Misc.Pause(500)
        directionToCorpse = calculateDirectionToSail(corpse.Position, Player.Position)
    
    Misc.Pause(500)

    autoLoot()

def autoLoot():
    corpses_filter = Items.Filter()
    corpses_filter.IsCorpse = True 
    corpses_filter.OnGround = True 
    corpses_filter.RangeMin = 0 
    corpses_filter.RangeMax = 2
    corpses_filter.Graphics = List[int]([0x2006]) 
    corpses_filter.CheckIgnoreObject = True

    corpse_list = Items.ApplyFilter(corpses_filter)
    
    for corpse in corpse_list:
        Items.Message(corpse, 170, "loot this")
        Misc.Pause(200)
        # Slice it up
        if Items.FindByID(0x0EC4, 0x0494, Player.Backpack.Serial):
            Items.UseItemByID(0x0EC4, -1)
        else:
            Items.UseItemByID(0x0F52, -1)
            
        Misc.Pause(200)
        Target.WaitForTarget(2000)
        Target.TargetExecute(corpse)
        Misc.Pause(200)
        Items.UseItem(corpse)
        Misc.Pause(750)
        # Loot corpse
        for item in corpse.Contains:
            if item.ItemID in loot_list:
                Items.Move(item, Player.Backpack.Serial, -1)
                Misc.Pause(1000)
        Misc.IgnoreObject(corpse)
        supplyCheck() 

# MAIN FUNCTIONS
def radarCheck():
    # Check if neither of the radar scripts is running
    if not Misc.ScriptStatus("PK Radar Crowsnest.py") and not Misc.ScriptStatus("PK Radar Crowsnest_Boats Near.py"):
        Misc.SendMessage("No radar scripts are running. Stopping the current script.", 33)
        Misc.Pause(500)
        Misc.ScriptStopAll(False)  # Stops all running scripts except itself

def supplyCheck():
    min_nets = 2
    min_bandages = 35
    min_arrows = 50

    nets = Items.BackpackCount(0x0DCA, -1)  # Count of arrows in the backpack
    bandages = Items.BackpackCount(0x0E21, -1)  # Count of bandages in the backpack
    arrows = Items.BackpackCount(0x0F3F,-1)

    # Check if any item count is below the minimum required
    if nets < min_nets or bandages < min_bandages or arrows < min_arrows or Player.Weight > 330:
        Misc.SendMessage("Supply check is triggering a supply run.")
        Misc.Pause(500)
        supplyRun()  # Call the supplyRun function
    else:
        Misc.Pause(100)

def equipBow():
    if not Player.CheckLayer("LeftHand"):
        bow = Items.FindByID(0x26C2, -1, Player.Backpack.Serial)
        if bow:
            Player.EquipItem(bow)
            Misc.Pause(1000)
        else:
            Player.ChatSay("No bow found in backpack.")
            Misc.Pause(500)
            Misc.ScriptStop("Net Fishing.py")

def castNkill():
    
    while True:
        supplyCheck()
        Misc.Pause(500)
        Items.UseItemByID( 0x0DCA )
        Misc.Pause(1000)
        Target.WaitForTarget( 2000, True )
        x = Player.Position.X - 3
        y = Player.Position.Y - 3
        statics = Statics.GetStaticsTileInfo( Player.Position.X+3, Player.Position.Y+3, 0 )
        if len( statics ) > 0:
            water = statics[ 0 ]
            Target.TargetExecute( x, y, water.StaticZ, water.StaticID )
            Misc.Pause(500)
            if Journal.SearchByType("You can only use this in deep water!","System"):
                Player.ChatSay(64,"We must go to deeper waters")
            Journal.Clear()
        else:
            Target.TargetExecute( x, y, -5, 0x0000 )
            Misc.Pause(500)
            if Journal.SearchByType("You can only use this in deep water!","System"):
                Player.ChatSay(64,"We must go to deeper waters")
                Journal.Clear()
            Journal.Clear()

        Misc.Pause(17500)
        
        originalPosition = Player.Position
        #SPAWN -- prioritize the easy kills first#
        filterWaters= Mobiles.Filter()
        filterWaters.Enabled = True
        filterWaters.Notorieties = List[Byte](bytes([3,4,6]))
        filterWaters.Name = "a water elemental"
        filterWatersList = Mobiles.ApplyFilter(filterWaters)

            
        for i in filterWatersList:
            CUO.PlayMacro('Volley')
            Misc.Pause(500)
            Target.TargetExecute(i)
            while Mobiles.FindBySerial(i.Serial):
                Player.Attack(i)
                Misc.Pause(500)
                poisonCheck()
                if Player.DistanceTo(i) > 4:   
                    FollowMobile(i,4)
        
        #Next, prioritize the heavy casters#
        filterDeeps = Mobiles.Filter()
        filterDeeps.Enabled = True
        filterDeeps.Notorieties = List[Byte](bytes([3,4,6]))
        filterDeeps.Name = "a deep water elemental"
        filterDeepsList = Mobiles.ApplyFilter(filterDeeps)
        
            
        for i in filterDeepsList:
            CUO.PlayMacro('Concuss')
            Misc.Pause(500)
            Target.TargetExecute(i)
            while Mobiles.FindBySerial(i.Serial):
                Player.Attack(i)
                Misc.Pause(500)
                poisonCheck()
                if Player.DistanceTo(i) > 4:   
                    FollowMobile(i,4)
                    
        #Next, prioritize the serps#
        filterSerps = Mobiles.Filter()
        filterSerps.Enabled = True
        filterSerps.Notorieties = List[Byte](bytes([3,4,6]))
        filterSerps.Name = "a sea serpent"
        filterSerpsList = Mobiles.ApplyFilter(filterSerps)
        
            
        for i in filterSerpsList:
            CUO.PlayMacro('Concuss')
            Misc.Pause(500)
            Target.TargetExecute(i)
            while Mobiles.FindBySerial(i.Serial):
                Player.Attack(i)
                Misc.Pause(500)
                if Player.DistanceTo(i) > 4:   
                    FollowMobile(i,4)
                    
        #Next, prioritize the Ddeep serps#
        filterDeepSerps = Mobiles.Filter()
        filterDeepSerps.Enabled = True
        filterDeepSerps.Notorieties = List[Byte](bytes([3,4,6]))
        filterDeepSerps.Name = "a deep sea serpent"
        filterDeepSerpsList = Mobiles.ApplyFilter(filterDeepSerps)
        
            
        for i in filterDeepSerpsList:
            CUO.PlayMacro('Concuss')
            Misc.Pause(500)
            Target.TargetExecute(i)
            while Mobiles.FindBySerial(i.Serial):
                Player.Attack(i)
                Misc.Pause(500)
                if Player.DistanceTo(i) > 4:   
                    FollowMobile(i,4)
                    
        #Now finish everything else off#
        filterMobs = Mobiles.Filter()
        filterMobs.Enabled = True
        filterMobs.Notorieties = List[Byte](bytes([3,4,6]))
        filterMobssList = Mobiles.ApplyFilter(filterMobs)
        
            
        for i in filterMobssList:
            CUO.PlayMacro('Concuss')
            Misc.Pause(500)
            Target.TargetExecute(i)
            while Mobiles.FindBySerial(i.Serial):
                Player.Attack(i)
                Misc.Pause(500)
                if Player.DistanceTo(i) > 4:   
                    FollowMobile(i,4)
        
        #Build corpse list - first in case you have to chase a kraken far
        corpses_filter = Items.Filter()
        corpses_filter.IsCorpse = True 
        corpses_filter.OnGround = True 
        corpses_filter.RangeMin = 0 
        corpses_filter.RangeMax = 10
        corpses_filter.Graphics = List[int]([0x2006]) 
        corpses_filter.CheckIgnoreObject = True

        corpse_list = Items.ApplyFilter(corpses_filter)
        
        for corpse in corpse_list:
            FindLootReturn(corpse)  
   
            # Calculate direction to return
        directionToReturn = calculateDirectionToSail(originalPosition, Player.Position)
        returnToOriginalPosition(originalPosition, directionToReturn)        
        supplyCheck()

radarCheck()
BandageHeal.Start()
Journal.Clear() 
supplyCheck()
equipBow()
castNkill()
