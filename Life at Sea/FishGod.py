from Scripts import config
from Scripts.glossary.colors import colors
from Scripts.glossary.items.containers import FindHatch
from Scripts.glossary.items.tools import tools
from Scripts.utilities.items import FindItem, MoveItem
from System.Collections.Generic import List
from System import Byte
from System import Int32 as int
import threading

dragdelay = 1000
corpse_ID = 0x2006
hide_ID = 0x26B4
gold_ID = 0x0EED
net_ID = 0x0DCA
sos_ID = 0x099F
rope_ID = 0x14F8
ingot_ID = 0x1BF2
horned_ID = 0x1081
tmap_ID = 0x14EC
recipe_ID = 0x2831
meat_ID = 0x09F1
pearl_ID = 0x0F7A

loot_list  = [pearl_ID,hide_ID,gold_ID, net_ID, sos_ID, rope_ID, ingot_ID,horned_ID,recipe_ID]
fishIDs = [ 0x09CF, 0x09CE, 0x09CC, 0x09CD ]
fishingPole = Items.FindByID(0x0DBF,-1,Player.Backpack.Serial)
# True will move the boat with the foward and backword commands
# False will move the boat with the left and right commands
moveForwardBackward = True

def worldSave():
    if (Journal.SearchByType('The world will save in 1 minute.', 'System') or Journal.SearchByType('pause', 'Regular')):
        Misc.Pause(700)
        Misc.SendMessage('Pausing for world save or player-called break.', 33)
        while (not Journal.SearchByType('World save complete.', 'System') and not Journal.SearchByType('play', 'Regular')):
            Misc.Pause(1000)
        Misc.Pause(2500)
        Misc.SendMessage('Continuing run', 33)
        Misc.Pause(700)
    Journal.Clear() 
    
def pkRadar():
    # Check if either of the scripts is already running
    if not Misc.ScriptStatus("PK Radar Crowsnest.py") and not Misc.ScriptStatus("PK Radar Crowsnest_Boats Near.py"):

        Player.ChatSay(64, "Lets see... any deserted boats in the area?")

        # Wait a moment for the player to respond
        Misc.Pause(5000)  # Adjust the time as needed

        # Check the players response in the journal
        if Journal.SearchByName("yes", "Salty McFishface"):
            # Run the script for boats nearby
            Misc.ScriptRun("PK Radar Crowsnest_Boats Near.py")
            Misc.Pause(1000)
            Player.ChatSay("Ill keep a careful eye on the horizon...")
            

        elif Journal.SearchByName("no", "Salty McFishface"):
            # Run the standard radar script
            Misc.ScriptRun("PK Radar Crowsnest.py")
            Misc.Pause(1000)
            Player.ChatSay(64, "Tiller, please keep watch for pirates.")

        else:
            # Handle cases where no valid response was detected
            Player.ChatSay(64, "No valid response detected.")
    else:
        # One of the scripts is already running
        Player.ChatSay(64, "Lookouts are scanning the seas for pirates.")
        

def supplyCheck():
    # Minimum required supplies
    min_arrows = 75
    min_bandages = 35
    min_poles = 2
    drag_delay = 500  # Adjust drag delay if needed
    fish_ids = [0x09CC, 0x09CD, 0x09CF, 0x09CE]  # Example fish IDs, replace with actual IDs if needed

    # Check supplies in the backpack
    arrows = Items.BackpackCount(0x0F3F, -1)  # Arrows
    bandages = Items.BackpackCount(0x0E21, -1)  # Bandages
    poles = Items.BackpackCount(0x0DBF, -1)  # Poles

    # Call supplyRun if any item count is below the minimum
    if arrows < min_arrows or bandages < min_bandages or poles < min_poles:
        supplyRun()

    # Check if Players weight exceeds the limit
    if Player.Weight > 335:
        Misc.Pause(1000)
        # Process fish in the backpack
        for fish_id in fish_ids:
            while True:
                fish = Items.FindByID(fish_id, -1, Player.Backpack.Serial)
                if fish is None:
                    break  # Exit loop if no more fish of this type
                
                # Use knife to cut fish into steaks
                knife = Items.FindByID(0x0F52, -1, Player.Backpack.Serial)
                if knife:
                    Items.UseItem(knife)
                    Misc.Pause(500)
                    Target.TargetExecute(fish)
                    Misc.Pause(drag_delay)
        
        # Ensure all fish are processed before moving to corpse logic
        Misc.Pause(1000)
        
        # Find fish steaks in the backpack
        fish_steaks = Items.FindByID(0x097A, -1, Player.Backpack.Serial)

        if fish_steaks:
            # Apply corpse filter to find nearby corpses
            corpses_filter = Items.Filter()
            corpses_filter.IsCorpse = True
            corpses_filter.RangeMax = 2
            corpses_filter.Graphics = List[int]([0x2006])  # Corpse graphic ID

            # Find the nearest corpse
            corpses = Items.ApplyFilter(corpses_filter)

            if corpses:
                # Move fish steaks to the first found corpse
                for corpse in corpses:
                    Items.Move(fish_steaks, corpse, -1)
                    Misc.Pause(drag_delay)
                    break  # Move to only one corpse
            else:
                Misc.SendMessage("No corpse found to move fish steaks.", 33)
                Misc.Pause(500)
        else:
            Misc.SendMessage("No fish steaks found in the backpack.", 33)
            Misc.Pause(500)

        # Run supplyRun if still overweight
        if Player.Weight > 335:
            supplyRun()
    else:
        Misc.Pause(100)



        
def supplyRun():
    # Define minimum counts
    min_arrows = 250
    min_bandages = 150
    min_poles = 8
    min_pearl = 15
    min_moss = 15
    min_root = 15
    min_ash = 15
    net_id = 0x0DCA
    net_container = 0x42C396E3
    mib_id = 0x099F
    mib_container = 0x405A1E11
    fish_id = 0x097A
    fish_container = 0x4641DD1D
    supply_container = 0x4043C469  # Replace with the actual Serial of the supply container
    pole_container = 0x41A07467 #hanging backpack
    pole_pouch = 0x42040183 #exceptional rod pouch
    gold_ID = 0x0EED

    # Recall and move to the supply location
    Player.ChatSay("[recall Winter Lodge")
    Misc.Pause(2500)
    Player.PathFindTo(6783, 3899, 17)
    Misc.Pause(2000)
    Player.PathFindTo(6779, 3893, 17)
    Misc.Pause(4000)
    for fishID in fishIDs:
        fish = Items.FindByID( fishID, -1, Player.Backpack.Serial )
        if fish != None:
            Items.UseItemByID( 0x0F52 )
            Target.WaitForTarget( 2000, True )
            Target.TargetExecute( fish )
            Misc.Pause( 1000 )

    # Open supply containers
    Items.UseItem(supply_container)
    Misc.Pause(500)
    Items.UseItem(pole_container)
    Misc.Pause(500)
    Items.UseItem(pole_pouch)
    Misc.Pause(500)
    polecount = Items.BackpackCount(0x0DBF,-1)
    
    for x in range(0,min_poles-polecount):
        checkAndRestock(0x0DBF, min_poles, pole_pouch)
        Misc.Pause(200)


    # Check and restock items
    checkAndRestock(0x0F3F, min_arrows, supply_container)  # Arrows
    checkAndRestock(0x0E21, min_bandages, supply_container)  # Bandages
    checkAndRestock(0x0F7A, min_pearl, supply_container)  # Pearl
    checkAndRestock(0x0F7B, min_moss, supply_container)  # Moss
    checkAndRestock(0x0F86, min_root, supply_container)  # Root
    checkAndRestock(0x0F8C, min_ash, supply_container)  # Ash
    
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

        for fishID in fishIDs:
            fish = Items.FindByID( fishID, -1, Player.Backpack.Serial )
            if fish != None:
                Items.UseItemByID( 0x0F52 )
                Target.WaitForTarget( 2000, True )
                Target.TargetExecute( fish )
                Misc.Pause( 1000 )


        # Move items to their respective containers
        while True:
            if Items.FindByID(net_id, -1, Player.Backpack.Serial):
                Items.Move(Items.FindByID(net_id,-1, Player.Backpack.Serial), net_container, 1)
                Misc.Pause(1000)
            elif Items.FindByID(mib_id, -1, Player.Backpack.Serial):
                Items.UseItemByID(mib_id,-1)
                Misc.Pause(1000)
            elif Items.FindByID(0x14EE,-1,Player.Backpack.Serial):
                Items.Move(Items.FindByID(0x14EE,-1,Player.Backpack.Serial),mib_container,1)
                Misc.Pause(1000)
            elif Items.FindByID(fish_id, -1, Player.Backpack.Serial):
                Items.Move(Items.FindByID(fish_id,-1, Player.Backpack.Serial), fish_container, -1)
                Misc.Pause(1000)
            elif Items.FindByID(gold_ID, -1, Player.Backpack.Serial):
                Items.Move(Items.FindByID(gold_ID,-1, Player.Backpack.Serial), fish_container, -1)
                Misc.Pause(1000)
            elif Items.FindByID(hide_ID, -1, Player.Backpack.Serial):
                Items.Move(Items.FindByID(hide_ID,-1, Player.Backpack.Serial), fish_container, -1)
                Misc.Pause(1000)
            elif Items.FindByID(horned_ID, -1, Player.Backpack.Serial):
                Items.Move(Items.FindByID(horned_ID,-1, Player.Backpack.Serial), fish_container, -1)
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
        else:
            Player.ChatSay("No ship rune found.")
                

def checkAndRestock(itemID, min_count, supply_container):
    count = Items.BackpackCount(itemID, -1)
    if count < min_count:
        item_to_move = Items.FindByID(itemID, -1, supply_container)
        if item_to_move:
            move_count = min_count - count
            Items.Move(item_to_move, Player.Backpack.Serial, move_count)
            Misc.Pause(1000)  # Adjust delay as needed


def checkAndRestock(itemID, min_count, supply_container):
    count = Items.BackpackCount(itemID, -1)
    if count < min_count:
        item_to_move = Items.FindByID(itemID, -1, supply_container)
        if item_to_move:
            move_count = min_count - count
            Items.Move(item_to_move, Player.Backpack.Serial, move_count)
            Misc.Pause(1000)  # Adjust delay as needed
    

def goHome():
    while True:
        Player.ChatSay("[recall Winter Lodge")
        Misc.Pause(2500)  # Wait for the spell to cast

        # Check if the spell was disturbed
        if Journal.SearchByType("Your concentration is disturbed, thus ruining thy spell.", "System"):
            Misc.SendMessage("Spell was disturbed. Recasting...")
            Misc.Pause(4000)
            Journal.Clear()
            continue  # Skip the rest of the loop and start over
        elif Journal.SearchByType("Insufficient mana for this spell.","System"):
            Misc.Pause(10000)
            Journal.Clear()
            continue
        else:
            break  # Exit the loop if no disturbance is detected

def FightEnemy():
    serpFilter = Mobiles.Filter()
    serpFilter.Enabled = True
    serpFilter.Notorieties = List[Byte](bytes([3,4,6]))
    
    while True:
        serpList = Mobiles.ApplyFilter(serpFilter)
        serpListbyDistance = sorted(serpList, key=lambda mob: Player.DistanceTo(mob))
        if len(serpList) > 0:
            serpSelection = serpListbyDistance[0]
            Player.ChatSay(64,"Serpent on the horizon!")
            Misc.Pause(500)
            if not Player.CheckLayer("LeftHand"):
                #find and equip bow
                bow = Items.FindByID(0x26C2, -1, Player.Backpack.Serial)
                if bow:
                    Player.EquipItem(bow)
                    Misc.Pause(500)
                else:
                    # Check again with a slight delay
                    Player.ChatSay("No bow? Second try.")
                    Misc.Pause(500)
                    bow = Items.FindByID(0x26C2, -1, Player.Backpack.Serial)
                    if bow:
                        Player.EquipItem(bow)
                        Misc.Pause(500)


            Player.Attack(serpSelection)
            Misc.Pause(500)
            #eat buff fish, if I have any
            if Items.FindByID(0x0DD6,-1,Player.Backpack.Serial):
                Items.UseItemByID(0x0DD6,-1)
                Misc.Pause(500)
            while Mobiles.FindBySerial(serpSelection.Serial):
                Misc.Pause(500)
        else:
            break
            
    corpses_filter = Items.Filter()
    corpses_filter.IsCorpse = True 
    corpses_filter.OnGround = True 
    corpses_filter.RangeMin = 0 
    corpses_filter.RangeMax = 10
    corpses_filter.Graphics = List[int]([0x2006]) 
    corpses_filter.CheckIgnoreObject = True

    corpse_list = Items.ApplyFilter(corpses_filter)
    
    for corpse in corpse_list:
        FindCorpse(corpse)  
            
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
        
def getpositionx():
   return Player.Position.X
def getpositiony():
   return Player.Position.Y

def returnToOriginalPosition(originalPosition, directionToReturn):
    while Player.Position != originalPosition:
        Player.ChatSay(directionToReturn)
        Misc.Pause(500)
        directionToReturn = calculateDirectionToSail(originalPosition, Player.Position)
        
def FindCorpse(corpse):
    originalPosition = Player.Position
    directionToCorpse = calculateDirectionToSail(corpse.Position, Player.Position)

    # Move to the corpse
    while Player.DistanceTo(corpse) > 2:     
        # Adjust the distance as needed
        Player.ChatSay(directionToCorpse)
        Misc.Pause(500)
        directionToCorpse = calculateDirectionToSail(corpse.Position, Player.Position)
    
    Misc.Pause(500)

    autoLoot()

    # Calculate direction to return
    directionToReturn = calculateDirectionToSail(originalPosition, Player.Position)
    returnToOriginalPosition(originalPosition, directionToReturn)

    
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
   
def sailtoCorpse():
    corpses_filter = Items.Filter()
    corpses_filter.IsCorpse = True 
    corpses_filter.OnGround = True 
    corpses_filter.RangeMin = 0 
    corpses_filter.RangeMax = 10 
    corpses_filter.Graphics = List[int]([0x2006]) 
    corpses_filter.CheckIgnoreObject = True

    corpse_list = Items.ApplyFilter(corpses_filter)
   
    if corpse in corpse_list:
        FindCorpse(corpse)


def Fish( fishingPole, x, y ):
    
    #Casts the fishing pole and returns True while the fish are biting
    
    global fishIDs

    Journal.Clear()
    Items.UseItemByID( 0x0DBF )
    
    Target.WaitForTarget( 2000, True )
    
    statics = Statics.GetStaticsTileInfo( x, y, 0 )
    if len( statics ) > 0:
        water = statics[ 0 ]
        Target.TargetExecute( x, y, water.StaticZ, water.StaticID )
    else:
        Target.TargetExecute( x, y, -5, 0x0000 )
        
    
    Misc.Pause( 1000 )
    Target.Cancel()

    Timer.Create( 'timeout', 10000 )
    while not ( Journal.SearchByType( 'You pull', 'System' ) or
    Journal.SearchByType( 'You fish a while, but fail to catch anything.', 'System' ) or
            Journal.SearchByType( 'The fish don\'t seem to be biting here', 'System' ) or
            Journal.SearchByType( 'Your fishing pole bends as you pull a big fish from the depths!', 'System' ) or
            Journal.SearchByType( 'Uh oh! That doesn''t look like a fish!', 'System' ) ):
        if not Timer.Check( 'timeout' ):
            return False
        Misc.Pause( 50 )

    if Journal.SearchByType( 'The fish don\'t seem to be biting here', 'System' ):
        return False
    
#    if Player.Weight >= Player.MaxWeight-55:
#        for fishID in fishIDs:
#            fish = Items.FindByID( fishID, -1, Player.Backpack.Serial )
#            if fish != None:
#                Items.UseItemByID( 0x0F52 )
#                Target.WaitForTarget( 2000, True )
#                Target.TargetExecute( fish )
#                Misc.Pause( dragdelay )
#                
    supplyCheck()
                
                               
    return True
    
def UseFishing():
    global moveForwardBackward
    BandageHeal.Start()

    fishingPoleTool = tools[ 'fishing pole' ]
    fishingPole = FindItem( fishingPoleTool.itemID, Player.Backpack )

    moveBoatInThisDirection = None
    if moveForwardBackward:
        moveBoatInThisDirection = 'forward'
    else:
        moveBoatInThisDirection = 'right'

    while True:
        # Start fishing to the East
        if not Player.Direction == 'North':
            Player.Walk( 'North' )
        x = Player.Position.X - 3
        y = Player.Position.Y - 3
        while Fish( fishingPole, x, y ):
            FightEnemy()
            worldSave()
            
        Player.Walk( 'East' )
        supplyCheck()
        x = Player.Position.X + 3
        y = Player.Position.Y - 3
        while Fish( fishingPole, x, y ):
            FightEnemy()
            worldSave()

        Player.Walk( 'South' )
        supplyCheck()
        x = Player.Position.X + 3
        y = Player.Position.Y + 3
        while Fish( fishingPole, x, y ):
            FightEnemy()
            worldSave()
            
        Player.Walk( 'West' )
        supplyCheck()
        x = Player.Position.X - 3
        y = Player.Position.Y + 3
        while Fish( fishingPole, x, y ):
            FightEnemy()
            worldSave()
                

        Misc.Pause( 320 )
        for i in range( 0, 11 ):
            Player.ChatSay( ( '%s one' % moveBoatInThisDirection ) )
            Misc.Pause( 320 )
        Misc.Pause( 320 )

        Misc.Pause( config.journalEntryDelayMilliseconds )
        if Journal.Search( 'Ar, we\'ve stopped sir.' ):
            if moveForwardBackward:
                if moveBoatInThisDirection == 'forward':
                    moveBoatInThisDirection = 'backward'
                else:
                    moveBoatInThisDirection = 'forward'
            else:
                if moveBoatInThisDirection == 'right':
                    moveBoatInThisDirection = 'left'
                else:
                    moveBoatInThisDirection = 'right'

            Misc.Pause( 320 )
            for i in range( 0, 11 ):
                Player.ChatSay( ( '%s one' % moveBoatInThisDirection ) )
                Misc.Pause( 320 )
            Misc.Pause( 320 )
            
Journal.Clear()
pkRadar()
UseFishing()  


