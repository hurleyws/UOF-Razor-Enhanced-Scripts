
from System import Int32 as int
from System import Byte
from System.Collections.Generic import List
import time
import random

#Editorial notes: Really just playing with the top two fucntions. Commented out if catches for low health and if the distance opens up on a mob im fighting

excluded_names = ["a dog"]

#Mark false if you want to run cemetaries 
#Mark saveDelay false if you want to skip the 90 second wait
farmRun = True
saveDelay = False
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
wolfStatue_ID = 0x25CFe
grizzlyStatue_ID = 0x211E
eagleStatue_ID = 0x211D
birdStatue_ID = 0x20EE
deerStatue_ID = 0x20D4
lizardStatue_ID = 0x20DE
skill_scroll_id = 0x2260
relic_ID = 0x2AA2
skeleStatue_ID = 0x20E7
zombieStatue_ID = 0x20EC
zombieStatue2_ID = 0x25D5
crystal_ID = 0x2244
bandage_ID = 0x0E21
chickenStatue_ID = 0x20D1

trash_dict = {
    0x0DE1: "kindling",
    0x1EBD: "bushel",
    0x0F49: "axe",
    0x0FF0: "book1",
    0x0FF1: "book2",
    0x0FF2: "book3",
    0x0FF3: "book4",
    0x0FEF: "book5",
    0x0F93: "spoon",       # assuming 0x0F93 is the spoon item ID
    0x09F9: "torch",
    0x0F6B: "mug",
    0x0FFF: "firehorn",
    0x0FC7: "fork",
    0x09F4: "hops",
    0x3184: "bowl",
    0x104F: "clock parts",
    0x1F7B: "doublet",
    0x15F8: "dirtypan"
}


regs = [
0x0F7A, 0x0F7B,0x0F86,0x0F8C,0x0F84,0x0F88,0x0F85,0x0F8D,
]

rune_ids = [0x483B,0x483E,0x4841,0x4844,0x4847,0x484A,0x484D,0x4850,0x4853,0x4856,0x4859,0x485C,0x485F,0x4862,0x4865,0x4868,0x486B,0x4871,0x486E,0x4874,0x4877,0x487A,0x487D,0x4880,0x4883]

loot_list  = [
    grizzlyStatue_ID, eagleStatue_ID, birdStatue_ID, deerStatue_ID, hide_ID, gold_ID,
    wood_ID, arrow_ID, wool_ID, pile_ID, cloth_ID,
    chickenStatue_ID, lizardStatue_ID, skill_scroll_id, wolfStatue_ID, relic_ID, skeleStatue_ID, zombieStatue_ID, zombieStatue2_ID, bandage_ID
]

special_list  = [
    grizzlyStatue_ID, eagleStatue_ID, birdStatue_ID, deerStatue_ID, hide_ID, gold_ID,
    wood_ID, arrow_ID, wool_ID, pile_ID, cloth_ID,
    chickenStatue_ID, lizardStatue_ID, skill_scroll_id, wolfStatue_ID, relic_ID, skeleStatue_ID, zombieStatue_ID, zombieStatue2_ID
]

# New bones list
bones = [
    0x1B17, 0x1B18, 0x1B09, 0x1B0F, 0x1B0A, 0x1B0B, 0x1B0C, 0x1B0D,
    0x1B0E, 0x1B0F, 0x1B10, 0x1B15, 0x1B16, 0x1451, 0x1450, 0x144E,
    0x1452, 0x144F
]

# Extend the loot list with the bones list
loot_list.extend(bones)
loot_list.extend(rune_ids)
loot_list.extend(regs)
special_list.extend(rune_ids)

fragIDs = [0x2244,0x2243,0x2242,0x2241,0x223D,0x223C,0x2244,0x5349]

def harvestWood():
    harvestFilter = Items.Filter()
    harvestFilter.RangeMax = 3
    harvestFilter.Graphics = List[int]([0x74EC]) 
    harvestFilter.Movable = False
    harvestableList = Items.ApplyFilter(harvestFilter)
    
    if len(harvestableList) > 0:
        Player.ChatSay("!")
        Misc.Pause(500)
        hatchet = Items.FindBySerial(0x4204BE97)
        while not Player.CheckLayer("LeftHand"):
            Player.EquipItem(hatchet)
            Misc.Pause(500)
            deadCheck()
        Items.UseItem(0x4204BE97)
        Misc.Pause(500)
        for i in harvestableList:
            Target.TargetExecute(i)
            Misc.Pause(500)
            while len(harvestableList) > 0:
                Misc.Pause(1000)
                harvestableList = Items.ApplyFilter(harvestFilter)
            Misc.Pause(5000)
                
            groundLootFilter = Items.Filter()
            groundLootFilter.Enabled = True
            groundLootFilter.Movable = True
            groundLootFilter.OnGround = True
            groundLootFilter.Graphics = List[int]([0x2260,0x0F21,0x2AA2,0x1BDD,0x1BD7,0xAADD]) 
            groundLootFilter.RangeMax = 2
            groundLootFilterList = Items.ApplyFilter(groundLootFilter)
            
            for i in groundLootFilterList:
                Items.Move(i,Player.Backpack.Serial,-1)
                Misc.Pause(1000)
                
            Dress.ChangeList("hatchet")
            Misc.Pause(500)
            Dress.UnDressFStart() 
            Misc.Pause(500)
            Dress.ChangeList("tooltime")
            Misc.Pause(500)
               
    else:
        Misc.Pause(500)
        Misc.SendMessage("No barricade found")
            
        
def barricade():
    groundLootFilter = Items.Filter()
    groundLootFilter.Enabled = True
    groundLootFilter.Movable = True
    groundLootFilter.OnGround = True
    groundLootFilter.Graphics = List[int]([0x1EB1]) 
    groundLootFilter.RangeMax = 2
    groundLootFilter.CheckIgnoreObject = True
    groundLootFilterList = Items.ApplyFilter(groundLootFilter)
    
    if len(groundLootFilterList) > 0:
        for i in groundLootFilterList:
            Items.MoveOnGround(i,1,5459,739,5)
            Misc.Pause(1000)
            Misc.IgnoreObject(i)
            
    else:
        Misc.Pause(1000)

def moveToTarget(target, max_retry, timeout):
    """
    Moves to a target (e.g., chest or corpse) while checking for danger.
    """
    overall_start_time = time.time()  # Start the overall timer

    targetPosition = target.Position
    if Player.DistanceTo(target) > 2:
        Misc.SendMessage("Original target position: {}".format(targetPosition))
        Misc.Pause(500)

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Directions to try: Down, Up, Right, Left
        for dx, dy in directions:
            # Check if the overall timer has exceeded 15 seconds
            if time.time() - overall_start_time > 15:
                Misc.SendMessage("Overall timeout exceeded. Exiting function.")
                Misc.Pause(500)
                return  # Exit the function if the overall timer exceeds 15 seconds

            targetCoords = PathFinding.Route()
            targetCoords.MaxRetry = max_retry
            targetCoords.StopIfStuck = False
            targetCoords.X = targetPosition.X + dx
            targetCoords.Y = targetPosition.Y + dy
            
            success = PathFinding.Go(targetCoords)
            Misc.Pause(250)
            deadCheck()
            
            startTime = time.time()
            while Player.DistanceTo(target) > 2:
                # Check if the overall timer has exceeded 15 seconds
                if time.time() - overall_start_time > 15:
                    Misc.SendMessage("Overall timeout exceeded. Exiting function.")
                    return  # Exit the function if the overall timer exceeds 15 seconds

                currentTime = time.time()
                if currentTime - startTime > timeout:
                    Misc.SendMessage("Timed out, trying next position.")
                    Misc.Pause(500)
                    break
            
            # Check if the player is now close enough to the target
            if Player.DistanceTo(target) <= 2:
                Misc.SendMessage("Successfully moved to target.")
                Misc.Pause(500)
                return  # Exit the function once the target is reached
        
        # If all directions fail, log a message
        Misc.SendMessage("Unable to move to target. All directions tried.")




import time
import random

def followMobile(mobile):
    """
    Follows a mobile until the player is within 1 tile of it or the timer times out.
    """
    start_time = time.time()  # Record the start time for the timeout

    # Define possible (dx, dy) offsets to move around the mobile
    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while mobile:
        elapsed_time = time.time() - start_time
        if elapsed_time > 20:
            Misc.SendMessage("Timeout exceeded. Stopping follow.")
            break

        if Player.DistanceTo(mobile) > 1:
            mobilePosition = mobile.Position
            route = PathFinding.Route()
            route.MaxRetry = 5
            route.StopIfStuck = False

            dx, dy = random.choice(offsets)
            route.X = mobilePosition.X + dx
            route.Y = mobilePosition.Y + dy

            PathFinding.Go(route)
            Misc.Pause(250)
            Misc.SendMessage(f"Pathfinding to offset ({dx}, {dy})")
            Misc.Pause(250)
            deadCheck()
        else:
            Misc.SendMessage("Distance check OK")
            Misc.Pause(750)
            break


    
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
        matchingFrag = Items.FindByID(fragID, fragHue, 0x411F0FDE, -1, False)
        if matchingFrag:
            break
    
    if not matchingFrag:
        Player.HeadMessage(33, "No matching fragments found in the container.")
        Items.Move(originalFrag,0x411F0FDE,-1)
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
        Items.Move(combinedFrag,0x411F0FDE,1,155,50)
        Misc.Pause(600)
    else:
        Player.HeadMessage(33, "No combined fragment found in the backpack.")
            
            
            
            
def storeValuables():
    EXCLUDED_HUED_ITEMS = {0x22C5, 0x0E79, 0x3679, 0x108A,0x2F5A,0x13DB,0x13DC,0x13D6,0x13DA,0x170B,0x13D5,0x2244,0x2243,0x2242,0x2241,0x223D,0x223C,0x2244,0x5349}
    for i in Player.Backpack.Contains:
        if i.ItemID == relic_ID or i.ItemID == skill_scroll_id:
            Items.Move(i,0x411F0FDE,1)
            Misc.Pause(1000)
        elif i.Hue != 0x0000 and i.ItemID not in EXCLUDED_HUED_ITEMS:
            Items.Move(i,0x411F0FDE,1)
            Misc.Pause(1000)
        elif i.ItemID in special_list:
            Items.Move(i,0x411F0FDE,1)
            Misc.Pause(1000)
    
def repairCheck():
    Dagger = Items.FindByID(0x0F52, -1, Player.Backpack.Serial)
    if Dagger is not None:
        prop_list = Items.GetPropStringByIndex(Dagger, 8) #7 if non-slayer
        if prop_list:
            prop_list_split = prop_list.split()
            if len(prop_list_split) >= 4:  # Making sure the list has enough items to avoid IndexError
                items = int(prop_list_split[1])
                durability = int(prop_list_split[3])

                if items < 20:
                    Items.Move(Dagger, 0x41547DA9, 1)
                    Misc.Pause(1500)
                    getDagger()
    else:
        # Handle the case where no Dagger was found
        Misc.SendMessage("No Dagger found")

    

def manaCheck():
    if Journal.SearchByType("Insufficient mana for this spell.","System"):
        Misc.Pause(8000)
        killGame()
        Misc.Pause(8000)
        Journal.Clear()
    
def findCorpses(move_enabled):
    """
    Find corpses within a specified range.
    :param move_enabled: Boolean to determine the RangeMax value (True for 10, False for 2)
    :return: List of corpses found within the range
    """
    # Set RangeMax based on move_enabled
    range_max = 10 if move_enabled else 2

    corpses_filter = Items.Filter()
    corpses_filter.IsCorpse = True  # optional
    corpses_filter.OnGround = True  # optional
    corpses_filter.RangeMin = 0  # optional
    corpses_filter.RangeMax = range_max  # Dynamically set based on move_enabled
    corpses_filter.Graphics = List[int]([0x2006])  # Corpses only
    corpses_filter.CheckIgnoreObject = True  # optional

    corpse_list = Items.ApplyFilter(corpses_filter)  # returns list of items

    return corpse_list


def lootCorpse(corpse):
    Misc.SendMessage("lootCorpse begin")
    Misc.Pause(500)
    for item_to_loot in corpse.Contains:
        Misc.SendMessage("found a {} with ID {}".format(item_to_loot.Name, item_to_loot.ItemID),130)
        Misc.Pause(10)
        shouldLoot = False
        if checkItemByID(item_to_loot, loot_list):
            shouldLoot = True
                
        if shouldLoot:
            Items.Move(item_to_loot,Player.Backpack,-1 ) # -1 -> all, for stackable items
            Misc.Pause(750)
    Misc.SendMessage("lootCorpse end")
    Misc.Pause(500)

            
def checkItemByID(item_to_check, valid_ids):
    excluded_ids = [0x5744]  # e.g., worm
    # ❌ Always skip if in excluded list
    if item_to_check.ItemID in excluded_ids:
        return False

    # ✅ Loot if in valid list OR has non-zero hue
    return item_to_check.ItemID in valid_ids or item_to_check.Hue != 0x0000

def lootGame(move_enabled=True):  # Add a parameter to control movement
    Misc.SendMessage("lootGame begin")
    Misc.Pause(500)
    crps_list = findCorpses(move_enabled)
    crps_list = sorted(crps_list, key=lambda corpse: Player.DistanceTo(corpse))

    for current_corpse in crps_list:
        if move_enabled:  # Check if movement is enabled
            moveToTarget(current_corpse, 5, 10)
        
        Items.UseItem(current_corpse)
        Misc.Pause(500)
        
        # Use knife or dagger to slice
        if Items.FindByID(0x0EC4, -1, Player.Backpack.Serial):
            Items.UseItemByID(0x0EC4, -1)
        else:
            Items.UseItemByID(0x0F52, -1)
        
        Misc.Pause(500)
        Target.TargetExecute(current_corpse)
        Misc.Pause(500)
        lootCorpse(current_corpse)
        Misc.Pause(500)
        
        # Process pile if found
        pile = Items.FindByID(0x1079, -1, Player.Backpack.Serial)
        if pile:
            Items.UseItemByID(0x0F9F, -1)
            Misc.Pause(500)
            Target.TargetExecute(pile)
            Misc.Pause(500)
        
        Misc.IgnoreObject(current_corpse)
        
        # Stop looting if player is overweight
        if Player.Weight > 340:
            break
        Misc.SendMessage("lootGame end")
        Misc.Pause(500)

    
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
            lootGame(move_enabled=True)
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
    bandages = Items.BackpackCount(0x0E21,-1)
    shade = Items.FindByID(0x0F88,-1,Player.Backpack.Serial)
    garlic = Items.FindByID(0x0F84,-1,Player.Backpack.Serial)
    ginseng = Items.FindByID(0x0F85,-1,Player.Backpack.Serial)
    ash = Items.FindByID(0x0F8C,-1,Player.Backpack.Serial)
    silk = Items.FindByID(0x0F8D,-1,Player.Backpack.Serial)
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
        
    if bandages > 200:
        Items.Move(Items.FindByID(0x0E21,-1,Player.Backpack.Serial),0x42E87E92,bandages-200)
        Misc.Pause(1000)        
    if silk:
        Items.Move(silk,0x42E88440,-1)
        Misc.Pause(1000)
    if ash:
        Items.Move(ash,0x42E88440,-1)
        Misc.Pause(1000)
    if ginseng:
        Items.Move(ginseng,0x42E88440,-1)
        Misc.Pause(1000)
    if garlic:
        Items.Move(garlic,0x42E88440,-1)
        Misc.Pause(1000)
    if shade:
        Items.Move(shade,0x42E88440,-1)
        Misc.Pause(1000)
    if gold:
        Items.Move(gold,0x42E87E92,-1,148, 84)
        Misc.Pause(1000)

    
    

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

def checkPositionAndMobiles(expectedX, expectedY):
    """
    Check if the player is at the expected position and ensure no mobiles are within 3 tiles,
    excluding those at specific coordinates. If mobiles are found, pause randomly 5 times 
    (30-60s in 5s steps) with countdown messages every 10 seconds. If still present, stop all scripts.
    """
    Misc.SendMessage(f"Checking position: Expected ({expectedX}, {expectedY}), Current ({Player.Position.X}, {Player.Position.Y})", 77)
    Misc.Pause(500)
    if Player.IsGhost:
        return

    # Confirm player is in correct position
    if Player.Position.X != expectedX or Player.Position.Y != expectedY:
        Misc.SendMessage("Player not at expected location. Retrying goHome().", 33)
        goHome()
        return

    # Set up mobile detection filter
    mobilesFilter = Mobiles.Filter()
    mobilesFilter.RangeMax = 2
    mobilesFilter.Notorieties = List[Byte](bytes([1, 2, 3, 4]))
    mobilesFilter.IsHuman = True

    # Apply filter and exclude specific coordinates
    excluded_coords = [(6804, 3897), (6800, 3898)]

    def getFilteredMobiles():
        allNearby = Mobiles.ApplyFilter(mobilesFilter)
        return [m for m in allNearby if (m.Position.X, m.Position.Y) not in excluded_coords]

    nearbyMobiles = getFilteredMobiles()

    if len(nearbyMobiles) == 0:
        Misc.SendMessage("Pass: Player is in the correct position and no valid mobiles are nearby.", 77)
        Misc.Pause(500)
        return

    # If mobiles are nearby, begin random pause attempts
    Misc.SendMessage(f"Mobiles detected: {len(nearbyMobiles)} (excluding known positions). Beginning random pause attempts.", 33)
    Misc.Pause(500)
    
    for attempt in range(5):
        delaySeconds = random.choice(range(30, 65, 5))
        Misc.SendMessage(f"Pause attempt {attempt + 1}/5: Total wait time {delaySeconds} seconds...", 33)
        Misc.Pause(500)
        # Countdown every 10 seconds
        secondsRemaining = delaySeconds
        while secondsRemaining > 0:
            Player.HeadMessage(33, f"Pausing... {secondsRemaining} seconds remaining")
            Misc.Pause(500)
            waitTime = min(10, secondsRemaining)
            Misc.Pause(waitTime * 1000)
            secondsRemaining -= waitTime

        # Recheck for filtered mobiles
        nearbyMobiles = getFilteredMobiles()
        if len(nearbyMobiles) == 0:
            Misc.SendMessage("Mobiles cleared. Resuming.", 77)
            Misc.Pause(500)
            return

    # After all 5 pauses, if mobiles still nearby, stop script
    Misc.SendMessage("Mobiles still present after 5 attempts. Stopping all scripts.", 33)
    Misc.Pause(500)
    Misc.ScriptStopAll(False)

                       

def goHome():
    EXCLUDED_HUED_ITEMS = [0x108A,0x22C5] #ring, rune book
    trashlist = [0x0DE1,0x1EBD,0x0F49,0x0FF0,0x0FF1,0x0FF2,0x0FF3,0x0FEF,0x09F9,0x0F6B,0x0FFF,0x0FC7,0x09F4,0x3184,0x15F8,0x09DE] #kindling, bushel, axe,book1-4,spoon, torch, mug, firehorn,fork,hops,bowl,dirtypan1
    attempt_recall("Winter Lodge")
    checkPositionAndMobiles(6802, 3902)
    deadCheck()
    Player.PathFindTo(6802, 3901, 12)
    Misc.Pause(1500)
    door = Items.FindBySerial(0x42F89EDC)
    if door.ItemID == 0x0677:
        Items.UseItem(door)
        Misc.Pause(500)
    Player.PathFindTo(6802, 3900, 12)
    Misc.Pause(500)
    checkPositionAndMobiles(6802, 3900)
    Player.PathFindTo(6803, 3897, 17)
    Misc.Pause(2500)
    spinBolts()
    Items.UseItem(0x42E87E92)
    Misc.Pause(500)
    Items.UseItem(0x435ED948)
    Misc.Pause(500)
    cutBones()
    lootList = [0x1BD1,0x09F1,0x0EED,0x1BD7]
    for i in Player.Backpack.Contains:
        if i.ItemID in (0x0F95, 0x1081, 0x0F7E):  # bolt, leather, bones
            Items.Move(i, 0x435ED948, -1)
        elif i.ItemID in lootList:  # feather, meat, or gold, or boards
            Items.Move(i, 0x42E87E92, -1)
        elif i.ItemID == 0x1BDD:  # logs
            Items.Move(i, 0x41132AE2, -1)
        elif i.ItemID in trash_dict and i.ItemID not in EXCLUDED_HUED_ITEMS:
            Items.Move(i, 0x409C3212, -1)
        else:
            continue
        Misc.Pause(1000)  # Pause only if an item was moved
    
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
    Player.PathFindTo(6800, 3892, 17)
    Misc.Pause(4500)
    Items.UseItem(0x411F0FDE)
    Misc.Pause(500)
    storeValuables()
    combineFrags()
    repairCheck()
    getDagger()

    
def armSelf():
    equipAttempts = 0
    while equipAttempts < 3:  # Limit the number of attempts to 3
        if Player.CheckLayer("RightHand"):
            # Weapon is already in hand, no need to continue.
            break
        else:
            Dagger = Items.FindByID(0x0F52, -1, Player.Backpack.Serial)
            if Dagger:
                Player.EquipItem(Dagger)
                Misc.Pause(500)
                if Player.CheckLayer("RightHand"):
                    # Dagger successfully equipped.
                    break
                else:
                    # Equip attempt failed, increment the counter.
                    equipAttempts += 1
                    Player.HeadMessage(64, "Attempt to equip Dagger failed.")
            else:
                # Dagger not found in the backpack.
                Player.HeadMessage(64, "Dagger not found, looking again.")
                equipAttempts += 1
                Misc.Pause(750)

    if equipAttempts >= 3:
        # Failed to equip the Dagger after 3 attempts or Dagger not found.
        Player.HeadMessage(64, "Failed to equip Dagger or not found. Going home.")
        goHome()
        Misc.ScriptStop("FarmGod.py")
        
    
        
def killChickens():
    armSelf()
    Misc.Pause(500)
    while True:
        chickenFilter = Mobiles.Filter()
        chickenFilter.Enabled = True
        chickenFilter.Notorieties = List[Byte](bytes([3,4,6]))
        chickenFilter.Hues = List[int]([0x0000])
        chickenFilter.RangeMax = 2
        chickenList = Mobiles.ApplyFilter(chickenFilter)
        
        if len(chickenList) == 0:
            break

        for chicken in chickenList:
            # Refresh the chicken just in case it's gone
            chicken = Mobiles.FindBySerial(chicken.Serial)
            if not chicken:
                continue

            Player.Attack(chicken)
            Misc.Pause(500)
            turn_opposite_to_mobile(chicken)

            while Player.DistanceTo(chicken) > 1:
                Misc.Pause(250)
                if not Mobiles.FindBySerial(chicken.Serial):
                    break

            while Mobiles.FindBySerial(chicken.Serial):
                Misc.Pause(500)
                if Player.DistanceTo(chicken) > 1:
                    break
                deadCheck()
            Misc.Pause(500)

        lootGame(move_enabled=True)

            

def killChaseGame():
    excluded_names = ["a dog"]

    def calculate_distance(item):
        # Function to calculate distance from the player to an item
        return Player.DistanceTo(item)

    def restart_function():
        Misc.SendMessage("Time limit exceeded, restarting killGame function.")
        Misc.ClearIgnore()
        killGame()
        

    armSelf()
    overall_start_time = time.time()
    overall_time_limit = 90  # 1.5 minute

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
        
        gameList = [mob for mob in gameList if mob.Name.lower() not in excluded_names]
        
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
                attempt_recall("Winter Lodge")
                deadCheck()
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
                Items.UseItem(0x411F0FDE)
                Misc.Pause(500)
                storeValuables()
                combineFrags()
                repairCheck()
                getDagger()
                Misc.ScriptStop("FarmGod.py")

            if game.Name == "a corpser":
                Misc.SendMessage("Corpser, ignoring.")
                Misc.Pause(500)
                Misc.IgnoreObject(game)
                continue


            Misc.SendMessage("Engaging " + str(game.Name))
            Player.Attack(game)
            elapsed_time = time.time() - overall_start_time
            Misc.Pause(500)
            Misc.SendMessage(f"Elapsed time: {elapsed_time:.2f} seconds", 33)
            # Check if the overall time limit has been exceeded
            if time.time() - overall_start_time > overall_time_limit:
                restart_function()
                return  # Exit the current function to restart it            

            

            # Wait for prey to approach
            while Player.DistanceTo(game) > 1:
                # Check overall timer
                if time.time() - overall_start_time > overall_time_limit:
                    goHome()
                    Player.ChatSay(64,"Likely provo trap found")
                    Misc.Pause(500)
                    Misc.ScriptStop("FarmGod.py")  # Exit the current function to restart it

                # Check engagement timer
                if time.time() - engagement_start_time > 20:
                    Misc.SendMessage("Combat timeout, disengaging.")
                    break
                    
                if time.time() - overall_start_time > overall_time_limit:
                    restart_function()
                    return  # Exit the current function to restart it


                if game.Hits < 13:
                    Misc.SendMessage("Target low health, disengaging.")
                    break

                Misc.Pause(250)
                
            turn_opposite_to_mobile(game)

            while Mobiles.FindBySerial(game.Serial):
                # Check overall timer
                elapsed_time = time.time() - overall_start_time
                Misc.SendMessage(f"Elapsed time: {elapsed_time:.2f} seconds", 33)
                Misc.Pause(500)
                if time.time() - overall_start_time > overall_time_limit:
                    restart_function()
                    return  # Exit the current function to restart it

                # Check engagement timer
                if time.time() - engagement_start_time > 25:
                    Misc.SendMessage("Combat timeout, disengaging.")
                    break

                Misc.Pause(500)
                followMobile(game)
                healthCheck()
                armSelf()


                deadCheck()

            deadCheck()
            break
        
                    
def killGame():
    def calculate_distance(item):
        # Function to calculate distance from the player to an item
        return Player.DistanceTo(item)

    def restart_function():
        Misc.SendMessage("Time limit exceeded, restarting killGame function.")
        Misc.ClearIgnore()
        killGame()
        

    armSelf()
    overall_start_time = time.time()
    overall_time_limit = 60  # 1 minute

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
        gameFilter.Hues = List[int]([0x0000])
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
                attempt_recall("Winter Lodge")
                deadCheck()
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
                Items.UseItem(0x411F0FDE)
                Misc.Pause(500)
                storeValuables()
                combineFrags()
                repairCheck()
                getDagger()
                Misc.ScriptStop("FarmGod.py")

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
            elapsed_time = time.time() - overall_start_time
            Misc.Pause(500)
            Misc.SendMessage(f"Elapsed time: {elapsed_time:.2f} seconds", 33)
            # Check if the overall time limit has been exceeded
            if time.time() - overall_start_time > overall_time_limit:
                restart_function()
                return  # Exit the current function to restart it            

            

            # Wait for prey to approach
            while Player.DistanceTo(game) > 1:
                # Check overall timer
                if time.time() - overall_start_time > overall_time_limit:
                    goHome()
                    Player.ChatSay(64,"Likely provo trap found")
                    Misc.Pause(500)
                    Misc.ScriptStop("FarmGod.py")  # Exit the current function to restart it

                # Check engagement timer
                if time.time() - engagement_start_time > 30:
                    Misc.SendMessage("Combat timeout, disengaging.")
                    break
                    
                if time.time() - overall_start_time > overall_time_limit:
                    restart_function()
                    return  # Exit the current function to restart it


                if game.Hits < 13:
                    Misc.SendMessage("Target low health, disengaging.")
                    break

                Misc.Pause(250)
                
            turn_opposite_to_mobile(game)

            while Mobiles.FindBySerial(game.Serial):
                # Check overall timer
                elapsed_time = time.time() - overall_start_time
                Misc.SendMessage(f"Elapsed time: {elapsed_time:.2f} seconds", 33)
                Misc.Pause(500)
                if time.time() - overall_start_time > overall_time_limit:
                    restart_function()
                    return  # Exit the current function to restart it

                # Check engagement timer
                if time.time() - engagement_start_time > 25:
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
    
    for t in Player.Backpack.Contains:
        if t.ItemID in bundleList:
            Misc.Pause(200)
            Items.MoveOnGround(t, -1, Player.Position.X - 1, Player.Position.Y, Player.Position.Z)
            Misc.Pause(1000)

def getDagger():
    Dagger = Items.FindByID(0x0F52, -1, Player.Backpack.Serial)
    if Dagger:
        Misc.SendMessage("Dagger found in backpack")
        Misc.Pause(500)
        return

    equippedDagger = Player.GetItemOnLayer("LeftHand")
    if equippedDagger and equippedDagger.ItemID == 0x0F52:
        Misc.SendMessage("Dagger equipped.")
        Misc.Pause(500)
        return

    storageBagSerial = 0x411F0FDE
    storageDagger = Items.FindByID(0x0F52, -1, storageBagSerial)
    if storageDagger:
        Misc.SendMessage("Dagger found in storage bag, moving to backpack")
        Misc.Pause(500)
        Items.Move(storageDagger, Player.Backpack.Serial, 1)
        Misc.Pause(1000)
    else:
        Misc.SendMessage("No Dagger found in storage bag, terminating script")
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
        Items.UseItem(0x411F0FDE)
        Misc.Pause(500)
        getDagger()
        Misc.ScriptRun("bandageAssist.py")
        if saveDelay:
            Player.ChatSay(64,"Making a harvest run in 90 seconds.")
            Misc.Pause(90000)
        worldSave()
        
        # List of possible locations with settings for killGame type and move_enabled for lootGame
        locations_settings = {
            "Jhelom Cemetary": {"kill_function": "killGame", "move_enabled": False},
            "Britain Cemetary": {"kill_function": "killChaseGame", "move_enabled": True},
            "Yew Cemetary": {"kill_function": "killGame", "move_enabled": False},
            "Lizards": {"kill_function": "killChaseGame", "move_enabled": True},
            "Mummies": {"kill_function": "killGame", "move_enabled": True},
            "Moonglow Cemetary": {"kill_function": "killGame", "move_enabled": False},
            "Deceit": {"kill_function": "killChaseGame", "move_enabled": True},
        }

        # Shuffle the list of locations to create a randomized order
        locations = list(locations_settings.keys())
        random.shuffle(locations)

        # Loop through each location
        for location in locations:
            # Attempt recall to the location
            attempt_recall(location)
            Misc.Pause(2500)

            # Get the settings for the location
            settings = locations_settings[location]

            # Dynamically call the appropriate kill function
            if settings["kill_function"] == "killGame":
                killGame()
            elif settings["kill_function"] == "killChaseGame":
                killChaseGame()

            # Perform other actions
            checkWeight()
            worldSave()

            # Dynamically call lootGame with the appropriate move_enabled setting
            lootGame(move_enabled=settings["move_enabled"])
            
        goHome()
        Misc.ClearIgnore()    
        Misc.ScriptStop("FarmGod.py")
        Misc.Pause(2000)
    else:
        Journal.Clear()
        Misc.ClearIgnore()
        Misc.ScriptRun("bandageAssist.py")
        deadCheck()
        if saveDelay:
            Player.ChatSay(64,"Making a harvest run in 90 seconds.")
            Misc.Pause(90000)
        worldSave() 
        Items.UseItem(0x411F0FDE)
        Misc.Pause(500)
        getDagger()
  
invasionCheck()
Misc.ScriptRun("bandageAssist.py")
Misc.Pause(500)

# List of possible locations with settings for killGame type and move_enabled for lootGame
locations_settings = {
    "Jhelom Cemetary": {"kill_function": "killGame", "move_enabled": False},
    "Britain Cemetary": {"kill_function": "killChaseGame", "move_enabled": False},
    "Yew Cemetary": {"kill_function": "killGame", "move_enabled": False},
    "Lizards": {"kill_function": "killChaseGame", "move_enabled": True},
    "Mummies": {"kill_function": "killGame", "move_enabled": True},
    "Moonglow Cemetary": {"kill_function": "killGame", "move_enabled": False},
    "Deceit": {"kill_function": "killChaseGame", "move_enabled": True},
}

# Shuffle the list of locations to create a randomized order
locations = list(locations_settings.keys())
random.shuffle(locations)

# Loop through each location
for location in locations:
    # Attempt recall to the location
    attempt_recall(location)
    Misc.Pause(500)

    # Get the settings for the location
    settings = locations_settings[location]

    # Dynamically call the appropriate kill function
    if settings["kill_function"] == "killGame":
        killGame()
    elif settings["kill_function"] == "killChaseGame":
        killChaseGame()

    # Perform other actions
    checkWeight()
    worldSave()

    # Dynamically call lootGame with the appropriate move_enabled setting
    lootGame(move_enabled=settings["move_enabled"])

    
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
    lootGame(move_enabled=False)
    worldSave()
    reapTrash()
    Player.PathFindTo(3711, 2670, 20) #north field
    Misc.Pause(6000)
    reapField()
    Player.PathFindTo(3711, 2683, 20) #south field
    Misc.Pause(6000)
    killChaseGame()
    worldSave()
    reapField()
    Player.PathFindTo(3711, 2683, 20) #south field
    Misc.Pause(6000)
    reapTrash()
    Player.PathFindTo(3710, 2693, 20) #south-south field
    Misc.Pause(6000)
    killChaseGame()
    lootGame(move_enabled=True)
    worldSave()
    reapField()
    checkWeight()
    Player.PathFindTo(3710, 2693, 20) #south-south field
    Misc.Pause(6000)
    reapTrash()
    worldSave()
    goHome()
    attempt_recall("Bulls")
    Misc.Pause(2500)
    killChaseGame()
    checkWeight()
    worldSave()
    killChaseGame()
    lootGame(move_enabled=True)
    Player.PathFindTo(4469, 1310, 8)
    Misc.Pause(7000)
    killChaseGame()
    checkWeight()
    worldSave()
    killChaseGame()
    lootGame(move_enabled=True)
    Player.PathFindTo(4456, 1325, 9)
    Misc.Pause(5000)
    killChaseGame()
    checkWeight()
    worldSave()
    killChaseGame()
    lootGame(move_enabled=True)
    Player.PathFindTo(4467, 1331, 8)
    Misc.Pause(6000)   
    killChaseGame()
    checkWeight()
    worldSave()
    killGame()
    lootGame(move_enabled=True)
    Player.PathFindTo(4469, 1345, 8)
    Misc.Pause(7000) 
    killChaseGame()
    checkWeight()
    worldSave()
    killGame()
    lootGame(move_enabled=True)
    Player.PathFindTo(4487, 1333, 8)  
    Misc.Pause(6000) 
    killChaseGame()
    checkWeight()
    worldSave()
    killGame()
    lootGame(move_enabled=True)
    Player.PathFindTo(4498, 1315, 8)
    Misc.Pause(6000)  
    killChaseGame()
    checkWeight()
    worldSave()
    killGame()
    lootGame(move_enabled=True)

goHome()
attempt_recall("Safe Trash")
Misc.SendMessage("Clicking the trash pile...")  # Debug message
Items.UseItem(0x400047A6)  # Click the trash pile
Misc.Pause(1000)          # Brief pause after clicking
harvestWood()
barricade()
attempt_recall("Safe Barricade")
harvestWood()
goHome()

Misc.ClearIgnore()

if looping:
    Misc.SendMessage("Looping in 7 minutes")
    Misc.Pause(360000)


