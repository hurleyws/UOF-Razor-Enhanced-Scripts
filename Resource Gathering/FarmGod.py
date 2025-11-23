
from System import Int32 as int
from System import Byte
from System.Collections.Generic import List
import time
import datetime 
import random
import os
import inspect

#Editorial notes: Really just playing with the top two fucntions. Commented out if catches for low health and if the distance opens up on a mob im fighting

excluded_names = ["a dog"]

#Mark false if you want to run cemetaries 
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
    0x0C2D: "debris",
    0x153B: "half apron",
    0x15F8: "dirtypan"
}


regs = [
0x0F7A, 0x0F7B,0x0F86,0x0F8C,0x0F84,0x0F88,0x0F85,0x0F8D,
]

# Define rune IDs
rune_ids = [
    0x483B, 0x483E, 0x4841, 0x4844, 0x4847, 0x484A, 0x484D, 0x4850, 0x4853,
    0x4856, 0x4859, 0x485C, 0x485F, 0x4862, 0x4865, 0x4868, 0x486B, 0x4871,
    0x486E, 0x4874, 0x4877, 0x487A, 0x487D, 0x4880, 0x4883
]

# Define bone item IDs
bones = [
    0x1B17, 0x1B18, 0x1B09, 0x1B0F, 0x1B0A, 0x1B0B, 0x1B0C, 0x1B0D,
    0x1B0E, 0x1B0F, 0x1B10, 0x1B15, 0x1B16, 0x1451, 0x1450, 0x144E,
    0x1452, 0x144F
]

# List of rares (includes relics, runes, statues, skill scrolls, cloth, gold)
rares_list = [
    relic_ID,
    skill_scroll_id,
    gold_ID,
    cloth_ID,
    grizzlyStatue_ID,
    eagleStatue_ID,
    birdStatue_ID,
    deerStatue_ID,
    chickenStatue_ID,
    lizardStatue_ID,
    wolfStatue_ID,
    skeleStatue_ID,
    zombieStatue_ID,
    zombieStatue2_ID
] + rune_ids

# Common loot list (hides, arrows, wood, bones, pile, bandage, etc.)
common_loot_list = [
    hide_ID,
    wood_ID,
    arrow_ID,
    wool_ID,
    pile_ID,
    bandage_ID
] + bones

loot_list = rares_list + common_loot_list + regs

fragIDs = [0x2244,0x2243,0x2242,0x2241,0x223D,0x223C,0x2244,0x5349]

goldLog = 'C:/Users/Hurley/Documents/GitHub/UOF-Razor-Enhanced-Scripts/Resource Gathering/goldLog.USR'

# Define cities to check for invasions
invasion_cities = ["Moonglow", "Yew", "Jhelom", "Britain", "Vesper"]

def SafePathFindTo(x, y, z):
    try:
        Player.PathFindTo(x, y, z)
        log_debug(f"SafePathFindTo succeeded to ({x}, {y}, {z})")
    except Exception as e:
        log_debug(f"SafePathFindTo first attempt failed to ({x}, {y}, {z}): {e}")
        Misc.Pause(5000)
        try:
            Player.PathFindTo(x, y, z)
            log_debug(f"SafePathFindTo retry succeeded to ({x}, {y}, {z})")
        except Exception as e2:
            log_debug(f"SafePathFindTo retry failed to ({x}, {y}, {z}): {e2}")


def get_invasion_cities():
    """Checks the [invasions gump and returns a set of cities with active invasions."""
    Player.ChatSay("[invasions")
    Gumps.WaitForGump(0, 5000)
    Misc.Pause(1000)

    gumpID = Gumps.CurrentGump()
    if gumpID == 0:
        Misc.SendMessage("No gump opened.", 33)
        Misc.Pause(1000)
        return set()

    active_cities = set()
    page_count = 0

    while True:
        lines = Gumps.LastGumpGetLineList()

        for i, line in enumerate(lines):
            if "Running" in line and i >= 3:
                city_line = lines[i - 3]
                for city in invasion_cities:
                    if city in city_line:
                        active_cities.add(city)

        # Try to go to next page
        Gumps.SendAction(gumpID, 2)
        Misc.Pause(1000)
        page_count += 1
        if page_count > 10:
            break

    return active_cities

def log_debug(message=""):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_dir = r"C:\Users\Hurley\Documents\GitHub\UOF-Razor-Enhanced-Scripts\Debug_logs"
    log_file = "farmGod_debug_log.txt"
    log_path = os.path.join(log_dir, log_file)

    # Create folder if it doesnt exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    try:
        with open(log_path, "a") as log:
            log.write(f"[{timestamp}] {message}\n")
    except Exception as e:
        Misc.SendMessage(f"Logging error: {e}", 33)

def waitForRightOfWay(max_attempts=10):
    log_debug("waitForRightOfWay")
    priority_order = ["Realtree", "Tool Time", "ToolmanTailor", "ImaTool"]
    me = Player.Name
    my_priority = priority_order.index(me)

    excluded_coords = [(6804, 3897), (6800, 3898), (6800, 3892), (6805, 3892), (6803, 3892)]

    attempt = 0
    while attempt < max_attempts:
        blocking = False
        
        mobilesFilter = Mobiles.Filter()
        mobilesFilter.IsHuman = True
        allNearby = Mobiles.ApplyFilter(mobilesFilter)
        

        for mob in allNearby:
            if not mob or not mob.Name or mob.Serial == Player.Serial:
                continue

            if (mob.Position.X, mob.Position.Y) in excluded_coords:
                continue  # Ignore characters in known resting spots

            if mob.Name in priority_order:
                their_priority = priority_order.index(mob.Name)
                if their_priority < my_priority:
                    log_debug(f"Waiting for {mob.Name} to go first.")
                    Misc.Pause(1000)
                    blocking = True
                    break

        if not blocking:
            return True

        wait_time = random.randint(10000, 20000)
        seconds = wait_time // 1000

        for i in range(seconds, 0, -1):
            log_debug(f"Waiting... {i}s")
            Misc.Pause(1000)

        attempt += 1

    log_debug("Too crowded. Giving up.")
    Misc.Pause(500)
    return False

def detectMobiles():
    log_debug("detectMobiles")
    mobFilter = Mobiles.Filter()
    mobFilter.Enabled = True
    mobFilter.IsHuman = True
    mobFilter.CheckLineOfSight = True

    mobilesList = Mobiles.ApplyFilter(mobFilter)

    ignored_names = {"a restless soul", "realtree", "toolmantailor", "imatool", "alyer base"}

    filteredMobiles = [mob for mob in mobilesList if mob.Name and mob.Name.lower() not in ignored_names]

    if filteredMobiles:
        mob = filteredMobiles[0]
        Misc.SendMessage("Mobile detected: {}".format(mob.Name), 33)
        Misc.Pause(1000)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp}, {mob.Name}\n"
        with open(goldLog, 'a') as file:
            file.write(log_entry)
        return True  # Mobile detected
    return False  # No mobile detected



            
def harvestWood():
    log_debug("harvestWood")
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
            Misc.Pause(1000)
            Dress.UnDressFStart() 
            Misc.Pause(1000)
            Dress.ChangeList("tooltime")
            Misc.Pause(1000)
               
    else:
        Misc.Pause(500)
            
        
def barricade():
    log_debug("barricade")
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

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Directions to try: Down, Up, Right, Left
        for dx, dy in directions:
            # Check if the overall timer has exceeded 15 seconds
            if time.time() - overall_start_time > 15:
                return  # Exit the function if the overall timer exceeds 15 seconds

            targetCoords = PathFinding.Route()
            targetCoords.MaxRetry = max_retry
            targetCoords.StopIfStuck = False
            targetCoords.X = targetPosition.X + dx
            targetCoords.Y = targetPosition.Y + dy
            
            try:
                Player.PathFindTo(targetCoords.X,targetCoords.Y,targetPosition.Z)
                Misc.Pause(500)
            except:
                Misc.Pause(500)
                
            deadCheck()
            
            startTime = time.time()
            while Player.DistanceTo(target) > 2:
                # Check if the overall timer has exceeded 15 seconds
                if time.time() - overall_start_time > 15:
                    return  # Exit the function if the overall timer exceeds 15 seconds

                currentTime = time.time()
                if currentTime - startTime > timeout:
                    break
                    
            
            # Check if the player is now close enough to the target
            if Player.DistanceTo(target) <= 2:
                return  # Exit the function once the target is reached
        
        # If all directions fail, log a message



def followMobile(mobile):
    log_debug("followMobile")
    """
    Follows a mobile until the player is within 1 tile of it or the timer times out.
    """
    start_time = time.time()  # Record the start time for the timeout

    # Define possible (dx, dy) offsets to move around the mobile
    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while mobile:
        elapsed_time = time.time() - start_time
        if elapsed_time > 20:
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
            deadCheck()
        else:
            break


    
def combineFrags():
    log_debug("combineFrags")
    # Step 1: Search the players backpack for a fragment
    originalFrag = None
    for item in Player.Backpack.Contains:
        if item.ItemID in fragIDs:
            originalFrag = item
            break
    
    if not originalFrag:
        return
    
    fragHue = originalFrag.Hue
    
    # Step 2: Search the container for matching fragments
    matchingFrag = None
    for fragID in fragIDs:
        matchingFrag = Items.FindByID(fragID, fragHue, 0x411F0FDE, -1, False)
        if matchingFrag:
            break
    
    if not matchingFrag:
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
            
            
            
            
def storeValuables():
    log_debug("storeValuables")
    EXCLUDED_HUED_ITEMS = {0x22C5, 0x0E79, 0x3679, 0x108A,0x2F5A,0x13DB,0x13DC,0x13D6,0x13DA,0x170B,0x13D5,0x2244,0x2243,0x2242,0x2241,0x223D,0x223C,0x2244,0x5349}
    for i in Player.Backpack.Contains:
        if i.ItemID == relic_ID or i.ItemID == skill_scroll_id:
            Items.Move(i,0x411F0FDE,1)
            Misc.Pause(1000)
        elif i.Hue != 0x0000 and i.ItemID not in EXCLUDED_HUED_ITEMS:
            Items.Move(i,0x411F0FDE,1)
            Misc.Pause(1000)
        elif i.ItemID in rares_list:
            Items.Move(i,0x411F0FDE,1)
            Misc.Pause(1000)
    
            
def repairCheck():
    log_debug("repairCheck")
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

    

def manaCheck():
    log_debug("manaCheck")
    if Journal.SearchByType("Insufficient mana for this spell.","System"):
        Misc.Pause(8000)
        killGame()
        Misc.Pause(8000)
        Journal.Clear()
    
def findCorpses(move_enabled):
    log_debug("findCorpses")
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
    log_debug("lootCorpse begin")
    for item_to_loot in corpse.Contains:

        shouldLoot = False
        current_weight = Player.Weight

        if current_weight < 300:
            if checkItemByID(item_to_loot, loot_list):  # loot_list contains both common and rare
                shouldLoot = True
        else:
            if checkItemByID(item_to_loot, rares_list):  # only loot rares over weight limit
                shouldLoot = True

        if shouldLoot:
            Items.Move(item_to_loot, Player.Backpack, -1)  # -1 -> all, for stackables
            Misc.Pause(1000)



            
def checkItemByID(item_to_check, valid_ids):
    log_debug("checkItemByID")
    excluded_ids = [0x5744]  # e.g., worm
    # ❌ Always skip if in excluded list
    if item_to_check.ItemID in excluded_ids:
        return False

    # ✅ Loot if in valid list OR has non-zero hue
    return item_to_check.ItemID in valid_ids or item_to_check.Hue != 0x0000

def lootGame(move_enabled=True):  # Add a parameter to control movement
    log_debug("lootGame begin")
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
            Misc.Pause(500)
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

    
def healthCheck():
    log_debug("healthCheck")
    if Player.Hits < 35:
        goHome()
        Misc.ScriptStop("FarmGod.py")
        

def attempt_recall(location):
    log_debug("attempt_recall")
    while True:
        worldSave()
        Player.ChatSay(f"[recall {location}")
        Misc.Pause(3000)  # Wait for the spell to cast

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
                if Player.Hits < Player.HitsMax:
                    killGame()
                    Misc.Pause(500)
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
    log_debug("worldSave")
    if (Journal.SearchByType('The world will save in 1 minute.', 'System') or Journal.SearchByType('pause', 'Regular')):
        Misc.Pause(700)
        Misc.SendMessage('Pausing for world save or player-called break.', 33)
        Misc.Pause(500)
        while (not Journal.SearchByType('World save complete.', 'System') and not Journal.SearchByType('play', 'Regular')):
            Misc.Pause(1000)
        Misc.Pause(2500)
        Misc.SendMessage('Continuing run', 33)
        Misc.Pause(700)
    Journal.Clear()  

def stockRegs():
    log_debug("stockRegs")
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
    log_debug("deadCheck")
    if Player.IsGhost:
        Player.ChatSay("Im dead")
        Misc.Pause(500)
        Player.ChatSay("I seek forgiveness")
        Misc.Pause(2000)
        SafePathFindTo(1474, 1609, 20)
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
    log_debug("spinBolts")
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
    log_debug("goHome")
    EXCLUDED_HUED_ITEMS = [0x108A,0x22C5] #ring, rune book
    trashlist = [0x0DE1,0x1EBD,0x0F49,0x0FF0,0x0FF1,0x0FF2,0x0FF3,0x0FEF,0x09F9,0x0F6B,0x0FFF,0x0FC7,0x09F4,0x3184,0x15F8,0x09DE] #kindling, bushel, axe,book1-4,spoon, torch, mug, firehorn,fork,hops,bowl,dirtypan1
    attempt_recall("Winter Lodge")
    waitForRightOfWay()
    deadCheck()
    SafePathFindTo(6802, 3901, 12)
    Misc.Pause(1500)
    door = Items.FindBySerial(0x42F89EDC)
    if door and door.ItemID == 0x0677:
        Items.UseItem(door)
        Misc.Pause(500)
    SafePathFindTo(6802, 3900, 12)
    Misc.Pause(500)
    waitForRightOfWay()
    SafePathFindTo(6803, 3898, 17)
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
    SafePathFindTo(6800, 3892, 17)
    Misc.Pause(4500)
    Items.UseItem(0x411F0FDE)
    Misc.Pause(500)
    storeValuables()
    combineFrags()
    repairCheck()
    getDagger()

    
def armSelf():
    log_debug("armSelf")
    equipAttempts = 0
    while equipAttempts < 3:  # Limit the number of attempts to 3
        if Player.CheckLayer("RightHand"):
            Misc.Pause(500)
            # Weapon is already in hand, no need to continue.
            break
        else:
            Dagger = Items.FindByID(0x0F52, -1, Player.Backpack.Serial)
            if Dagger:
                Player.EquipItem(Dagger)
                Misc.Pause(1000)
                if Player.CheckLayer("RightHand"):
                    Misc.Pause(500)
                    # Dagger successfully equipped.
                    break
                else:
                    # Equip attempt failed, increment the counter.
                    equipAttempts += 1
            else:
                # Dagger not found in the backpack.
                equipAttempts += 1


    if equipAttempts >= 3:
        # Failed to equip the Dagger after 3 attempts or Dagger not found.
        goHome()
        Misc.ScriptStop("FarmGod.py")
                  

def killChaseGame():
    log_debug("killChaseGame")
    excluded_names = ["a dog"]

    def calculate_distance(item):
        # Function to calculate distance from the player to an item
        return Player.DistanceTo(item)

    def restart_function():
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
        
        priority_names = ["a shade", "a wraith", "a skeletal knight"]

        # Assign priority based on name, then sort by distance
        gameList = sorted(
            gameList,
            key=lambda mob: (
                priority_names.index(mob.Name.lower()) if mob.Name.lower() in priority_names else float('inf'),
                calculate_distance(mob)
            )
        )

        if len(gameList) == 0:
            break

        for game in gameList:
            engagement_start_time = time.time()
            if Player.Weight > 340:
                goHome()
                Misc.ScriptStop("FarmGod.py")
                Misc.Pause(500)


            Player.Attack(game)
            elapsed_time = time.time() - overall_start_time
            Misc.Pause(500)
            # Check if the overall time limit has been exceeded
            if time.time() - overall_start_time > overall_time_limit:
                restart_function()
                return  # Exit the current function to restart it            

            

            # Wait for prey to approach
            while Player.DistanceTo(game) > 1:
                # Check overall timer
                if time.time() - overall_start_time > overall_time_limit:
                    return

                # Check engagement timer
                if time.time() - engagement_start_time > 20:
                    break
                    


                if game.Hits < 13:
                    break

                Misc.Pause(250)
                

            while Mobiles.FindBySerial(game.Serial):
                # Check overall timer
                elapsed_time = time.time() - overall_start_time
                if time.time() - overall_start_time > overall_time_limit:
                    restart_function()
                    return  # Exit the current function to restart it

                # Check engagement timer
                if time.time() - engagement_start_time > 25:
                    break

                Misc.Pause(500)
                followMobile(game)
                healthCheck()
                armSelf()


                deadCheck()

            deadCheck()
            break
        
                    
def killGame():
    log_debug("killGame")
    def calculate_distance(item):
        # Function to calculate distance from the player to an item
        return Player.DistanceTo(item)

    def restart_function():
        log_debug("Time limit exceeded, restarting killGame function.")
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
        gameList = Mobiles.ApplyFilter(gameFilter)
        
        priority_names = ["a shade", "a wraith", "a skeletal knight"]

        # Assign priority based on name, then sort by distance
        gameList = sorted(
            gameList,
            key=lambda mob: (
                priority_names.index(mob.Name.lower()) if mob.Name.lower() in priority_names else float('inf'),
                calculate_distance(mob)
            )
        )
        if len(gameList) == 0:
            break

        for game in gameList:
            engagement_start_time = time.time()
            if Player.Weight > 340:
                goHome()
                Misc.ScriptStop("FarmGod.py")
                Misc.Pause(500)


            if game.Hits < 5:
                Misc.IgnoreObject(game)
                continue

            Player.Attack(game)
            elapsed_time = time.time() - overall_start_time
            Misc.Pause(500)
            # Check if the overall time limit has been exceeded
            if time.time() - overall_start_time > overall_time_limit:
                restart_function()
                return  # Exit the current function to restart it            

            

            # Wait for prey to approach
            while Player.DistanceTo(game) > 1:
                # Check overall timer
                if time.time() - overall_start_time > overall_time_limit:
                    return


                # Check engagement timer
                if time.time() - engagement_start_time > 30:
                    break
                    


                if game.Hits < 13:
                    break

                Misc.Pause(250)
                

            while Mobiles.FindBySerial(game.Serial):
                # Check overall timer
                elapsed_time = time.time() - overall_start_time
                if time.time() - overall_start_time > overall_time_limit:
                    restart_function()
                    return  # Exit the current function to restart it

                # Check engagement timer
                if time.time() - engagement_start_time > 25:
                    break

                Misc.Pause(500)
                healthCheck()
                armSelf()

                if Player.DistanceTo(game) > 1:
                    break

                deadCheck()

            deadCheck()
            break

            
        
    
    Misc.ClearIgnore()
    checkWeight()
    
def calculate_distance(item):
    log_debug("calculate_distance")
    # Function to calculate distance from the player to an item
    return Player.DistanceTo(item)   
    
def checkWeight():
    log_debug("checkWeight")
    if Player.Weight > 370:
        goHome()
        Misc.ScriptStop("FarmGod.py")
        
def reapField():
    log_debug("reapField")
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
    log_debug("cutBones")
    for i in Player.Backpack.Contains:
        if i.ItemID in bones:
            Items.UseItemByID(0x0F9F,-1)
            Misc.Pause(500)
            Target.TargetExecute(i)
            Misc.Pause(500)
        
def reapTrash():
    log_debug("reapTrash")
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
            
            
        starttime = time.time()        
        while Player.DistanceTo(trash) > 1:
            Misc.Pause(500)
            currenttime = time.time()
            if currenttime - starttime > 10:
                break
            
            
           

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
    log_debug("getDagger")

    # Check if dagger is in backpack
    dagger = Items.FindByID(0x0F52, -1, Player.Backpack.Serial)
    if dagger:
        return

    # Check if dagger is equipped
    equippedDagger = Player.GetItemOnLayer("LeftHand")
    if equippedDagger and equippedDagger.ItemID == 0x0F52:
        return

    # Attempt to retrieve dagger from storage
    storageBagSerial = 0x411F0FDE
    storageDagger = Items.FindByID(0x0F52, -1, storageBagSerial)

    if storageDagger:
        Items.Move(storageDagger, Player.Backpack.Serial, 1)
        Misc.Pause(1000)

        # Optional: double-check move success
        confirm = Items.FindByID(0x0F52, -1, Player.Backpack.Serial)
        if not confirm:
            log_debug("Failed to move dagger to backpack")
            Misc.ScriptStop("FarmGod.py")
    else:
        log_debug("No dagger found in storage!")
        Misc.ScriptStop("FarmGod.py")

            

# Define a function to turn the character in the opposite direction of the mobile



def invasionCheck():    
    log_debug("invasionCheck")
    if Journal.SearchByType("Defenders are needed ","System"):
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
            "Britain Cemetary": {"kill_function": "killChaseGame", "move_enabled": False},
            "Yew Cemetary": {"kill_function": "killGame", "move_enabled": False},
            "Britain Gap": {"kill_function": "killGame", "move_enabled": False},
            "Lizards": {"kill_function": "killChaseGame", "move_enabled": True},
            "Mummies": {"kill_function": "killGame", "move_enabled": False},
            "Moonglow Cemetary": {"kill_function": "killGame", "move_enabled": False},
            "Vesper": {"kill_function": "killGame", "move_enabled": False},
            "Britain Chamber": {"kill_function": "killGame", "move_enabled": False},
            "Yew Chamber": {"kill_function": "killChaseGame", "move_enabled": True},
        }

        # Get active invasions once
        active_invasions = get_invasion_cities()
        Misc.SendMessage(f"Skipping cities under invasion: {', '.join(active_invasions)}", 34)
        Misc.Pause(1000)

        # Shuffle the list of locations to create a randomized order
        locations = list(locations_settings.keys())
        random.shuffle(locations)

        # Loop through each location
        for location in locations:
            for city in active_invasions:
                if city in location:
                    Misc.SendMessage(f"Skipping {location} due to active invasion in {city}", 33)
                    Misc.Pause(1000)
                    break
            else:
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
    "Britain Gap": {"kill_function": "killGame", "move_enabled": False},
    "Lizards": {"kill_function": "killChaseGame", "move_enabled": True},
    "Mummies": {"kill_function": "killGame", "move_enabled": False},
    "Moonglow Cemetary": {"kill_function": "killGame", "move_enabled": False},
    "Vesper": {"kill_function": "killGame", "move_enabled": False},
    "Britain Chamber": {"kill_function": "killGame", "move_enabled": False},
    "Yew Chamber": {"kill_function": "killChaseGame", "move_enabled": True},
}

# Get active invasions once
active_invasions = get_invasion_cities()
Misc.SendMessage(f"Skipping cities under invasion: {', '.join(active_invasions)}", 34)
Misc.Pause(1000)

# Shuffle the list of locations to create a randomized order
locations = list(locations_settings.keys())
random.shuffle(locations)

# Loop through each locationSkip to next location
for location in locations:
    for city in active_invasions:
        if city in location:
            Misc.SendMessage(f"Skipping {location} due to active invasion in {city}", 33)
            Misc.Pause(1000)
            break
    else:
            # Attempt recall to the location
        attempt_recall(location)
        Misc.Pause(500)
        if detectMobiles():
            Misc.SendMessage("Skipping location due to mobile presence", 33)
            Misc.Pause(1000)
            continue  # Skip to next location

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
        if detectMobiles():
            Misc.SendMessage("Skipping location due to mobile presence", 33)
            Misc.Pause(1000)
            continue  # Skip to next location


goHome()
    
if farmRun:
    attempt_recall("Occlo Farm")
    if detectMobiles():
        Misc.SendMessage("There are people here, going home.", 33)
        Misc.Pause(1000)
        goHome()
    else:
        worldSave()
        reapTrash()
        reapField()
        SafePathFindTo(3711, 2683, 20) #south field
        Misc.Pause(6000)
    if detectMobiles():
        Misc.SendMessage("There are people here, going home.", 33)
        Misc.Pause(1000)
        goHome()
    else:
        worldSave()
        reapTrash()
        reapField()
        SafePathFindTo(3710, 2693, 20) #south-south field
        Misc.Pause(6000)
    if detectMobiles():
        Misc.SendMessage("There are people here, going home.", 33)
        Misc.Pause(1000)
        goHome()
    else:
        worldSave()
        reapTrash()
        reapField()
        worldSave()
        goHome()
        attempt_recall("Bulls")
    if detectMobiles():
        Misc.SendMessage("There are people here, going home.", 33)
        Misc.Pause(1000)
        goHome()
    else:
        killChaseGame()
        checkWeight()
        worldSave()
        killChaseGame()
        lootGame(move_enabled=True)
    if detectMobiles():
        Misc.SendMessage("There are people here, going home.", 33)
        Misc.Pause(1000)
        goHome()
    else:
        SafePathFindTo(4469, 1310, 8)
        Misc.Pause(7000)
        detectMobiles()
        killChaseGame()
        checkWeight()
        worldSave()
        killChaseGame()
        lootGame(move_enabled=True)
    if detectMobiles():
        Misc.SendMessage("There are people here, going home.", 33)
        Misc.Pause(1000)
        goHome()
    else:
        SafePathFindTo(4456, 1325, 9)
        Misc.Pause(5000)
        detectMobiles()
        killChaseGame()
        checkWeight()
        worldSave()
        killChaseGame()
        lootGame(move_enabled=True)
    if detectMobiles():
        Misc.SendMessage("There are people here, going home.", 33)
        Misc.Pause(1000)
        goHome()
    else:
        SafePathFindTo(4467, 1331, 8)
        Misc.Pause(6000)   
        detectMobiles()
        killChaseGame()
        checkWeight()
        worldSave()
        killGame()
        lootGame(move_enabled=True)
    if detectMobiles():
        Misc.SendMessage("There are people here, going home.", 33)
        Misc.Pause(1000)
        goHome()
    else:
        SafePathFindTo(4469, 1345, 8)
        Misc.Pause(7000) 
        killChaseGame()
        checkWeight()
        worldSave()
        killGame()
        lootGame(move_enabled=True)
    if detectMobiles():
        Misc.SendMessage("There are people here, going home.", 33)
        Misc.Pause(1000)
        goHome()
    else:
        SafePathFindTo(4487, 1333, 8)  
        Misc.Pause(6000) 
        killChaseGame()
        checkWeight()
        worldSave()
        killGame()
        lootGame(move_enabled=True)
    if detectMobiles():
        Misc.SendMessage("There are people here, going home.", 33)
        Misc.Pause(1000)
        goHome()
    else:
        SafePathFindTo(4498, 1315, 8)
        Misc.Pause(6000) 
        detectMobiles() 
        killChaseGame()
        checkWeight()
        worldSave()
        killGame()
        lootGame(move_enabled=True)

goHome()
attempt_recall("Safe Trash")
if detectMobiles():
    Misc.SendMessage("There are people here, going home.", 33)
    Misc.Pause(1000)
    goHome()
else:
    Items.UseItem(0x400047A6)  # Click the trash pile
    Misc.Pause(1000)          # Brief pause after clicking
    harvestWood()
    barricade()
attempt_recall("Safe Barricade")
if detectMobiles():
    Misc.SendMessage("There are people here, going home.", 33)
    Misc.Pause(1000)
    goHome()
else:
    harvestWood()
    goHome()

Misc.ClearIgnore()

if looping:
    Misc.SendMessage("Looping in 7 minutes")
    Misc.Pause(360000)


