
from System import Int32 as int
from System import Byte
from System.Collections.Generic import List
import time
import random

#Mark false if you want to run cemetaries only
#Mark saveDelay false if you want to skip the 90 second wait
farmRun = True
saveDelay = True
#Set to True if checking the loop box for troubleshooting
looping = False

corpse_ID = 0x2006
hide_ID = 0x1081
gold_ID = 0x0EED
feathers_ID = 0x1BD1
wood_ID = 0x1BDD
arrow_ID = 0x0F3F
wool_ID = 0x0DF8
pile_ID = 0x1079
meat_ID = 0x09F1
cloth_ID = 0x1767
wolfStatue_ID = 0x25CF
chickenStatue_ID = 0x20D1
grizzlyStatue_ID = 0x211E
eagleStatue_ID = 0x211D
birdStatue_ID = 0x20EE
deerStatue_ID = 0x20D4
lizardStatue_ID = 0x20DE
skill_scroll_id = 0x2260
relic_ID = 0x2AA2
skeleStatue_ID = 0x20E7
zombieStatue_ID = 0x20EC
crystal_ID = 0x2244

loot_list  = [
    grizzlyStatue_ID, eagleStatue_ID, birdStatue_ID, deerStatue_ID, hide_ID, gold_ID,
    feathers_ID, wood_ID, arrow_ID, wool_ID, pile_ID, meat_ID, cloth_ID,
    chickenStatue_ID, lizardStatue_ID, skill_scroll_id, wolfStatue_ID, relic_ID, skeleStatue_ID, zombieStatue_ID
]

# New bones list
bones = [
    0x1B17, 0x1B18, 0x1B09, 0x1B0F, 0x1B0A, 0x1B0B, 0x1B0C, 0x1B0D,
    0x1B0E, 0x1B0F, 0x1B10, 0x1B15, 0x1B16, 0x1451, 0x1450, 0x144E,
    0x1452, 0x144F
]

# Extend the loot list with the bones list
loot_list.extend(bones)


fragIDs = [0x2244,0x2243,0x2242,0x2241,0x223D,0x223C]

def combineFrags():
    # Step 1: Search the players backpack for a fragment
    originalFrag = None
    for item in Player.Backpack.Contains:
        if item.ItemID in fragIDs:
            originalFrag = item
            break
    
    if not originalFrag:
        Player.HeadMessage(33, "No fragments found in the backpack.")
        return
    
    fragHue = originalFrag.Hue
    
    # Step 2: Search the container for matching fragments
    matchingFrag = None
    for fragID in fragIDs:
        matchingFrag = Items.FindByID(fragID, fragHue, 0x42EA55BA, -1, False)
        if matchingFrag:
            break
    
    if not matchingFrag:
        Player.HeadMessage(33, "No matching fragments found in the container.")
        Items.Move(originalFrag,0x42EA55BA,-1)
        Misc.Pause(1000)
        return
    
    # Step 3: Move the matching fragment to the players backpack
    Items.Move(matchingFrag, Player.Backpack.Serial, 1)
    Misc.Pause(600)  # Adjust the pause as needed for the move to complete
    
    # Step 4: Use the fragment that was moved and target the original fragment
    Items.UseItem(matchingFrag)
    Misc.Pause(500)
    Target.TargetExecute(originalFrag)
    Misc.Pause(500)
    
    # Step 5: Move the combined fragment back to the container
    combinedFrag = None
    for fragID in fragIDs:
        combinedFrag = Items.FindByID(fragID, fragHue, Player.Backpack.Serial, -1, False)
        if combinedFrag:
            break
    
    if combinedFrag:
        Items.Move(combinedFrag, 0x42EA55BA, 1)
        Misc.Pause(600)
    else:
        Player.HeadMessage(33, "No combined fragment found in the backpack.")
            
            
            
            
def storeValuables():
    for i in Player.Backpack.Contains:
        if i.ItemID == relic_ID:
            Items.Move(i,0x42EA55BA,1)
            Misc.Pause(1000)
        if i.ItemID == skill_scroll_id:
            Items.Move(i,0x422E5A11,1)
            Misc.Pause(1000)
    
def repairCheck():
    staff = Items.FindByID(0x0E89, -1, Player.Backpack.Serial)
    if staff is not None:
        prop_list = Items.GetPropStringByIndex(staff, 8) #7 if non-slayer
        if prop_list:
            prop_list_split = prop_list.split()
            if len(prop_list_split) >= 4:  # Making sure the list has enough items to avoid IndexError
                items = int(prop_list_split[1])
                durability = int(prop_list_split[3])

                if items < 20:
                    Items.Move(staff, 0x41547DA9, 1)
                    Misc.Pause(1500)
                    getStaff()
    else:
        # Handle the case where no staff was found
        Misc.SendMessage("No staff found")

    

def manaCheck():
    if Journal.SearchByType("Insufficient mana for this spell.","System"):
        Misc.Pause(8000)
        killGame()
        Misc.Pause(8000)
        Journal.Clear()
    
def findCorpses():
    corpses_filter = Items.Filter()
    corpses_filter.IsCorpse = True # optional
    corpses_filter.OnGround = True # Questionably optional
    corpses_filter.RangeMin = 0 # optional
    corpses_filter.RangeMax = 2 # optoinal
    corpses_filter.Graphics = List[int]([0x2006,0x2006]) # kraken, deep water
    corpses_filter.CheckIgnoreObject = True # optioinal, if you use Misc.IgnoreObject(item) the fitler will ignore if true.

    corpse_list = Items.ApplyFilter(corpses_filter) # returns list of items, manipulate list after this as you wish

    return corpse_list

def lootCorpse(corpse):
    for item_to_loot in corpse.Contains:
        Misc.SendMessage("found a {} with ID {}".format(item_to_loot.Name, item_to_loot.ItemID),130)
        Misc.Pause(10)
        shouldLoot = False
        if checkItemByID(item_to_loot, loot_list):
            shouldLoot = True
                
        if shouldLoot:
            Items.Move(item_to_loot,Player.Backpack,-1 ) # -1 -> all, for stackable items
            Misc.Pause(750)
        
            
def checkItemByID(item_to_check, valid_ids):
    if item_to_check.ItemID in loot_list:
        return True
    return False

def lootGame(): # define the function
    
    crps_list = findCorpses()

    for current_corpse in crps_list:
        Items.UseItem(current_corpse)
        Misc.Pause(500)
        if Items.FindByID(0x0EC4,0x0494,Player.Backpack.Serial):
            Items.UseItemByID(0x0EC4,-1)
        else:
            Items.UseItemByID(0x0F52,-1)
        Misc.Pause(500)
        Target.TargetExecute(current_corpse)
        Misc.Pause(500)
        lootCorpse(current_corpse)
        Misc.Pause(500)
        pile = Items.FindByID(0x1079,-1,Player.Backpack.Serial)
        if pile:
            Items.UseItemByID(0x0F9F,-1)
            Misc.Pause(500)
            Target.TargetExecute(pile)
            Misc.Pause(500)
        Misc.IgnoreObject(current_corpse)
        if Player.Weight > 340:
            break
    
def healthCheck():
    if Player.Hits < 35:
        Player.HeadMessage(64,"This is getting a little hairy...  "+str(Player.Hits)+" health.")
        Misc.Pause(500)
        goHome()
        Misc.ScriptStop("FarmGod.py")
        

def attempt_recall(location):
    while True:
        Player.ChatSay(f"[recall {location}")
        Misc.Pause(2500)  # Wait for the spell to cast

        # Check if the spell was disturbed
        if Journal.SearchByType("Your concentration is disturbed, thus ruining thy spell.", "System"):
            Misc.SendMessage("Spell was disturbed. Recasting...")
            Journal.Clear()
            Misc.Pause(500)
            killGame()
            Misc.Pause(500)
            continue  # Skip the rest of the loop and start over
            
        elif Journal.SearchByType("Insufficient mana for this spell.","System"):
            while Player.Mana < 11:
                Misc.Pause(1000)
            Misc.Pause(1000)
            killGame()
            Journal.Clear()
            continue
            
        elif Journal.SearchByType("Insufficient mana for this spell.","System"):
            while Player.Mana < 11:
                Misc.Pause(1000)
            Misc.Pause(1000)
            killGame()
            Journal.Clear()
            continue
            
        elif Journal.SearchByType("This book needs time to recharge.","System"):
            Misc.Pause(500)
            killGame()
            Misc.Pause(1500)
            Journal.Clear()
            Misc.Pause(500)
            continue            
            
        else:
            break  # Exit the loop if no disturbance is detected

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

def stockRegs():
    root = Items.BackpackCount(0x0F86,-1)
    moss = Items.BackpackCount(0x0F7B,-1)
    pearl = Items.BackpackCount(0x0F7A,-1)
    
    Misc.Pause(200)
    
    if root < 15:
        Items.Move(Items.FindByID(0x0F86,-1,0x42E88440),Player.Backpack.Serial,15-root)
        Misc.Pause(1000)
    
    if moss < 15:
        Items.Move(Items.FindByID(0x0F7B,-1,0x42E88440),Player.Backpack.Serial,15-moss)
        Misc.Pause(1000)
        
    if pearl < 15:
        Items.Move(Items.FindByID(0x0F7A,-1,0x42E88440),Player.Backpack.Serial,15-pearl)
        Misc.Pause(1000)
        
    else:
        Player.HeadMessage(64,"Regs look good")
        Misc.Pause(500)
    
    

def deadCheck():
    if Player.IsGhost:
        Player.ChatSay("Im dead")
        Misc.Pause(500)
        Player.ChatSay("I seek forgiveness")
        Misc.Pause(2000)
        Player.PathFindTo(1474, 1609, 20)
        Misc.Pause(2000)
        Items.UseItem(0x472869ED)
        Misc.Pause(500)
        Gumps.WaitForGump(2957810225, 10000)
        Gumps.SendAction(2957810225, 1)
        Misc.Pause(500)
        Dress.DressFStart()
        Misc.Pause(7000)
        while Player.Mana < 11:
            Misc.Pause(1000)
        BuyAgent.Enable()
        Misc.Pause(200)
        Misc.WaitForContext(0x004F6C2C, 10000)
        Misc.ContextReply(0x004F6C2C, 1)
        Misc.Pause(500)
        goHome()
    
def spinBolts():   
    rawmats = [0x0DF9, 0x1A9C, 0x1A9D, 0x0DF8]

    for item_id in rawmats:
        for item in Player.Backpack.Contains:
            if item.ItemID == item_id:
                while item.Amount > 0:  # Continue processing the stack until depleted
                    worldSave()
                    Items.UseItem(item)
                    Misc.Pause(500)
                    Target.TargetExecute(0x42E7B2C6)
                    Misc.Pause(4000)
                    updated_item = Items.FindByID(item_id,-1,Player.Backpack.Serial)  # Update the item reference to get the current state
                    if updated_item is not None:
                        item = updated_item
                    else:
                        break

    for item in Player.Backpack.Contains:
        if item.ItemID == 0x0FA0 or item.ItemID == 0x0E1D:
            while item.Amount > 0:
                worldSave()
                Items.UseItem(item)
                Misc.Pause(500)
                Target.TargetExecute(0x42E7A998)
                Misc.Pause(500)
                updated_item = Items.FindByID(item.ItemID,-1,Player.Backpack.Serial)
                if updated_item is not None:
                    item = updated_item
                else:
                    break
def goHome():
    attempt_recall("Winter Lodge")
    deadCheck()
    while True:
        kindling = Items.FindByID(0x0DE1, -1, Player.Backpack.Serial)
        if kindling:
            Items.UseItem(kindling)
            Misc.Pause(500)
        else:
            break  # Exit the loop if no kindling is found
    Player.PathFindTo(6802, 3901, 12)
    Misc.Pause(1500)
    Player.PathFindTo(6803, 3897, 17)
    Misc.Pause(2500)
    spinBolts()
    Items.UseItem(0x42E87E92)
    Misc.Pause(500)
    Items.UseItem(0x435ED948)
    Misc.Pause(500)
    cutBones()
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
    bandages = Items.BackpackCount(0x0E21,-1)
    bolts = Items.FindByID(0x0F95,-1,0x435ED948)
    if bandages < 100:
        Misc.Pause(500)
        Items.Move(bolts,Player.Backpack.Serial,2)
        Misc.Pause(1000)
        Items.UseItemByID(0x0F9F,-1)
        Misc.Pause(500)
        packbolts = Items.FindByID(0x0F95,-1,Player.Backpack.Serial)
        Target.TargetExecute(packbolts)
        Misc.Pause(500)
        packcloth = Items.FindByID(0x1766,-1,Player.Backpack.Serial)
        Items.UseItemByID(0x0F9F,-1)
        Misc.Pause(500)
        Target.TargetExecute(packcloth)
        Misc.Pause(500)  
    Misc.Pause(500)
    Items.UseItem(0x42E88440)
    Misc.Pause(500)
    stockRegs()
    Player.PathFindTo(6800, 3898, 17)
    Misc.Pause(2500)
    Items.UseItem(0x42EA55BA)
    Misc.Pause(500)
    storeValuables()
    combineFrags()
    repairCheck()
    getStaff()

    
def armSelf():
    equipAttempts = 0
    while equipAttempts < 3:  # Limit the number of attempts to 3
        if Player.CheckLayer("LeftHand"):
            # Weapon is already in hand, no need to continue.
            break
        else:
            staff = Items.FindByID(0x0E89, -1, Player.Backpack.Serial)
            if staff:
                Player.EquipItem(staff)
                Misc.Pause(500)
                if Player.CheckLayer("LeftHand"):
                    # Staff successfully equipped.
                    break
                else:
                    # Equip attempt failed, increment the counter.
                    equipAttempts += 1
                    Player.HeadMessage(64, "Attempt to equip staff failed.")
            else:
                # Staff not found in the backpack.
                Player.HeadMessage(64, "Staff not found, looking again.")
                equipAttempts += 1
                Misc.Pause(750)

    if equipAttempts >= 3:
        # Failed to equip the staff after 3 attempts or staff not found.
        Player.HeadMessage(64, "Failed to equip staff or not found. Going home.")
        goHome()
        Misc.ScriptStop("FarmGod.py")
        
    
        
def killChickens():
    armSelf()
    Misc.Pause(500)
    while True:
        chickenFilter = Mobiles.Filter()
        chickenFilter.Enabled = True
        chickenFilter.Notorieties = List[Byte](bytes([3,4,6])) # optional, numbers = notoritety codes
        chickenFilter.RangeMax = 2
        chickenList = Mobiles.ApplyFilter(chickenFilter)
        
        if len(chickenList) == 0:
            break

        for chicken in chickenList:
            Player.Attack(chicken)
            Misc.Pause(500)
            turn_opposite_to_mobile(chicken)
            while Player.DistanceTo(chicken) > 1:
                Misc.Pause(250)
                Player.DistanceTo(chicken)
            while Mobiles.FindBySerial(chicken.Serial):
                Misc.Pause(500)
                if Player.DistanceTo( chicken ) > 1:
                    break
                deadCheck()
            Misc.Pause(500)
        lootGame()
            

                    
def killGame():
    def calculate_distance(item):
        # Function to calculate distance from the player to an item
        return Player.DistanceTo(item)

    def restart_function():
        Misc.SendMessage("Time limit exceeded, restarting killGame function.")
        killGame()

    armSelf()
    overall_start_time = time.time()
    overall_time_limit = 3 * 60 + 30  # 3 minutes and 30 seconds in seconds

    while True:
        # Check if the overall time limit has been exceeded
        if time.time() - overall_start_time > overall_time_limit:
            restart_function()
            return  # Exit the current function to restart it

        gameFilter = Mobiles.Filter()
        gameFilter.Enabled = True
        gameFilter.Notorieties = List[Byte](bytes([3, 4, 6]))
        gameFilter.RangeMax = 9
        gameFilter.CheckIgnoreObject = True
        gameFilter.CheckLineOfSight = True
        gameList = Mobiles.ApplyFilter(gameFilter)
        gameList = sorted(gameList, key=calculate_distance)

        if len(gameList) == 0:
            Misc.SendMessage("No more in-range targets.")
            Misc.Pause(500)
            break

        for game in gameList:
            engagement_start_time = time.time()
            if Player.Weight > 340:
                Misc.SendMessage("Overweight, stopping.")
                Misc.Pause(500)
                break

            if game.Name == "a corpser":
                Misc.SendMessage("Corpser, ignoring.")
                Misc.Pause(500)
                Misc.IgnoreObject(game)
                continue

            if game.Hits < 5:
                Misc.SendMessage("Low health, ignoring.")
                Misc.Pause(500)
                Misc.IgnoreObject(game)
                continue

            Misc.SendMessage("Engaging " + str(game.Name))
            Player.Attack(game)
            Misc.Pause(500)            

            

            # Wait for prey to approach
            while Player.DistanceTo(game) > 1:
                # Check overall timer
                if time.time() - overall_start_time > overall_time_limit:
                    restart_function()
                    return  # Exit the current function to restart it

                # Check engagement timer
                if time.time() - engagement_start_time > 10:
                    Misc.SendMessage("Combat timeout, disengaging.")
                    break


                if game.Hits < 13:
                    Misc.SendMessage("Target low health, disengaging.")
                    break

                Misc.Pause(250)
                
            turn_opposite_to_mobile(game)
            if Mobiles.FindBySerial(game.Serial) and Player.DistanceTo(game)< 2:
                CUO.PlayMacro('Scream')
                Misc.Pause(500)
            while Mobiles.FindBySerial(game.Serial):
                # Check overall timer
                if time.time() - overall_start_time > overall_time_limit:
                    restart_function()
                    return  # Exit the current function to restart it

                # Check engagement timer
                if time.time() - engagement_start_time > 10:
                    Misc.SendMessage("Combat timeout, disengaging.")
                    break

                Misc.Pause(500)
                healthCheck()
                armSelf()

                if Player.DistanceTo(game) > 1:
                    Misc.SendMessage("Too far, disengaging.")
                    Misc.Pause(200)
                    break

                deadCheck()

            deadCheck()
            break
        
            
        
    
    Misc.ClearIgnore()
    checkWeight()
    
def calculate_distance(item):
    # Function to calculate distance from the player to an item
    return Player.DistanceTo(item)   
    
def checkWeight():
    if Player.Weight > 370:
        goHome()
        Misc.ScriptStop("FarmGod.py")
        
def reapField():
    def calculate_distance(item):
        # Function to calculate distance from the player to an item
        return Player.DistanceTo(item)
        
    while True:    
        flaxFilter = Items.Filter()
        flaxFilter.Enabled = True
        flaxFilter.Name = "flax"
        flaxFilter.OnGround = True
        flaxFilter.RangeMax = 12
        flaxList = Items.ApplyFilter(flaxFilter)
        flaxList = sorted(flaxList, key=calculate_distance)
        
        if len(flaxList) == 0:
            Misc.SendMessage("No more flax to reap.")
            Misc.Pause(500)
            
        flaxList = sorted(flaxList, key=calculate_distance)
        
        if not flaxList:
            break
            
        flax = flaxList[0]
        if flax in flaxList:
            flaxPosition = flax.Position
            flaxCoords = PathFinding.Route()
            flaxCoords.MaxRetry = 5
            flaxCoords.StopIfStuck = False
            flaxCoords.X = flaxPosition.X
            flaxCoords.Y = flaxPosition.Y
            PathFinding.Go( flaxCoords )
            
            while Player.DistanceTo(flax) > 1:  # Adjust the threshold as needed
                Misc.Pause(500)
             
            if flax:    
                Items.UseItem(flax)
                Misc.Pause(500)
                deadCheck()
def cutBones():
    for i in Player.Backpack.Contains:
        if i.ItemID in bones:
            Items.UseItemByID(0x0F9F,-1)
            Misc.Pause(500)
            Target.TargetExecute(i)
            Misc.Pause(500)
        
def reapTrash():
    def calculate_distance(item):
        # Function to calculate distance from the player to an item
        return Player.DistanceTo(item)

    breedList = [0x0CBB,0x0C58,0x0CA5,0x0C57,0x0C55,0x0C56]
    bundleList = [0x1EBD,0x3184,0x030c]

    while True:
        trashFilter = Items.Filter()
        trashFilter.Enabled = True
        trashFilter.OnGround = True
        trashFilter.RangeMax = 6
        trashFilter.Graphics = List[int]([0x0CBB,0x0C58,0x0CA5,0x0C57,0x0C55,0x0C56])
        trashList = Items.ApplyFilter(trashFilter)

        if len(trashList) == 0:
            Misc.SendMessage("No more weeds to pull.")
            Misc.Pause(500)


        trashList = sorted(trashList, key=calculate_distance)

        # If there are no more items, break the loop
        if not trashList:
            break

        # Process the first item in the sorted list
        trash = trashList[0]
        if trash.ItemID in breedList and trash:
            trashPosition = trash.Position
            trashCoords = PathFinding.Route()
            trashCoords.MaxRetry = 5
            trashCoords.StopIfStuck = False
            trashCoords.X = trashPosition.X
            trashCoords.Y = trashPosition.Y
            PathFinding.Go(trashCoords)
                
        while Player.DistanceTo(trash) > 1:
            Misc.Pause(500)

        if trash:
            Items.UseItem(trash)
            Misc.Pause(500)
            deadCheck()
            

    # Process the bundle list
    for t in Player.Backpack.Contains:
        if t.ItemID in bundleList:
            Misc.Pause(200)
            Items.MoveOnGround(t, -1, Player.Position.X - 1, Player.Position.Y, Player.Position.Z)
            Misc.Pause(1000)

    Misc.Pause(1000)  # Wait a bit before starting the next cycle

def getStaff():
    staff = Items.FindByID(0x0E89, -1, Player.Backpack.Serial)
    if staff:
        Misc.SendMessage("Staff found in backpack")
        Misc.Pause(500)
        return

    equippedStaff = Player.GetItemOnLayer("LeftHand")
    if equippedStaff and equippedStaff.ItemID == 0x0E89:
        Misc.SendMessage("Staff equipped.")
        Misc.Pause(500)
        return

    storageBagSerial = 0x42EA55BA
    storageStaff = Items.FindByID(0x0E89, -1, storageBagSerial)
    if storageStaff:
        Misc.SendMessage("Staff found in storage bag, moving to backpack")
        Misc.Pause(500)
        Items.Move(storageStaff, Player.Backpack.Serial, 1)
        Misc.Pause(1000)
    else:
        Misc.SendMessage("No staff found in storage bag, terminating script")
        Misc.Pause(500)
        Misc.ScriptStop("FarmGod.py")
            
        
# Define a function to get the opposite direction
def get_opposite_direction(direction):
    opposite_directions = {
        "North": "South",
        "South": "North",
        "East": "West",
        "West": "East",
        "Up": "Down",
        "Down": "Up",
        "Left": "Right",
        "Right": "Left"
    }
    return opposite_directions[direction]

# Define a function to turn the character in the opposite direction of the mobile
def turn_opposite_to_mobile(mobile):
    # Add a random pause between 100 and 800 milliseconds
    pause_time = random.randint(100, 1500)
    Misc.Pause(pause_time)
    
    # Get the direction the mobile is facing
    mobile_direction = mobile.Direction

    # Calculate the opposite direction
    opposite_direction = get_opposite_direction(mobile_direction)

    # Get the current direction of the character
    current_direction = Player.Direction
    
    
    # Turn the character to the opposite direction if not already facing it
    if current_direction != opposite_direction:
        
        
        Player.Walk(opposite_direction)
        Misc.Pause(250)
        


def invasionCheck():    
    if Journal.SearchByType("Defenders are needed ","System"):
        Player.ChatSay("Sounds like danger afoot in the towns")
        Misc.Pause(500)
        Items.UseItem(0x42EA55BA)
        Misc.Pause(500)
        getStaff()
        if saveDelay:
            Player.ChatSay(64,"Making a harvest run in 90 seconds.")
            Misc.Pause(90000)
        worldSave()
        # List of possible locations
        locations = ["Jhelom Cemetary", "Britain Cemetary", "Yew Cemetary","Moonglow Cemetary","Deceit","Mummies"]
        # Shuffle the list of locations to create a randomized order
        random.shuffle(locations)

        for location in locations:
            attempt_recall(location)
            Misc.Pause(2500)
            killGame()
            checkWeight()
            worldSave()
            killGame()
            lootGame()
            
        goHome()
        Misc.ClearIgnore()    
        Misc.ScriptStop("FarmGod.py")
        Misc.Pause(2000)
    else:
        Journal.Clear()
        Misc.ClearIgnore()
        BandageHeal.Start()
        deadCheck()
        if saveDelay:
            Player.ChatSay(64,"Making a harvest run in 90 seconds.")
            Misc.Pause(90000)
        worldSave() 
        Items.UseItem(0x42EA55BA)
        Misc.Pause(500)
        getStaff()
  
invasionCheck()

# List of possible locations
locations = ["Jhelom Cemetary", "Britain Cemetary", "Yew Cemetary","Moonglow Cemetary","Deceit","Lizards","Mummies"] #remove hot zones here
# Shuffle the list of locations to create a randomized order
random.shuffle(locations)

for location in locations:
    attempt_recall(location)
    Misc.Pause(2500)
    killGame()
    checkWeight()
    worldSave()
    killGame()
    lootGame()
    
if farmRun:
    attempt_recall("Occlo Farm")
    killChickens()
    worldSave()
    Misc.Pause(1000)
    Player.PathFindTo(3711, 2659, 20)
    Misc.Pause(2000)
    Player.PathFindTo(3711, 2662, 20) #north field
    Misc.Pause(3000)
    killGame()
    lootGame()
    worldSave()
    reapTrash()
    Player.PathFindTo(3711, 2670, 20) #north field
    Misc.Pause(6000)
    reapField()
    Player.PathFindTo(3711, 2683, 20) #south field
    Misc.Pause(6000)
    killGame()
    worldSave()
    reapField()
    Player.PathFindTo(3711, 2683, 20) #south field
    Misc.Pause(6000)
    reapTrash()
    Player.PathFindTo(3710, 2693, 20) #south-south field
    Misc.Pause(6000)
    killGame()
    lootGame()
    worldSave()
    reapField()
    checkWeight()
    Player.PathFindTo(3710, 2693, 20) #south-south field
    Misc.Pause(6000)
    reapTrash()
    worldSave()
    goHome()
    Player.ChatSay("[recall bulls")
    Misc.Pause(2500)
    killGame()
    checkWeight()
    worldSave()
    killGame()
    lootGame()
    Player.PathFindTo(4469, 1310, 8)
    Misc.Pause(7000)
    Misc.ClearIgnore()
    killGame()
    checkWeight()
    worldSave()
    killGame()
    lootGame()
    Player.PathFindTo(4456, 1325, 9)
    Misc.Pause(5000)
    Misc.ClearIgnore()
    killGame()
    checkWeight()
    worldSave()
    killGame()
    lootGame()
    Player.PathFindTo(4467, 1331, 8)
    Misc.Pause(6000) 
    Misc.ClearIgnore()   
    killGame()
    checkWeight()
    worldSave()
    killGame()
    lootGame()
    Player.PathFindTo(4469, 1345, 8)
    Misc.Pause(7000) 
    Misc.ClearIgnore() 
    killGame()
    checkWeight()
    worldSave()
    killGame()
    lootGame()
    Player.PathFindTo(4487, 1333, 8)  
    Misc.Pause(6000) 
    Misc.ClearIgnore() 
    killGame()
    checkWeight()
    worldSave()
    killGame()
    lootGame()
    Player.PathFindTo(4498, 1315, 8)
    Misc.Pause(6000)  
    Misc.ClearIgnore()
    killGame()
    checkWeight()
    worldSave()
    killGame()
    lootGame()

goHome()
Misc.ClearIgnore()

if looping:
    Misc.SendMessage("Looping in 7 minutes")
    Misc.Pause(360000)


