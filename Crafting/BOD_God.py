import time
import random
from System.Collections.Generic import List
from System import Int32 as int
from System import Byte

def checkPositionAndMobiles(expectedX, expectedY, maxWait=10000):
    """
    Check if the player is at the expected position and ensure no mobiles are within 3 tiles.
    If not, wait up to `maxWait` milliseconds and retry the `goHome()` function if needed.

    :param expectedX: Expected X coordinate of the player.
    :param expectedY: Expected Y coordinate of the player.
    :param maxWait: Maximum wait time in milliseconds for lag to clear or mobiles to leave.
    """
    Misc.SendMessage(f"Checking position: Expected ({expectedX}, {expectedY}), Current ({Player.Position.X}, {Player.Position.Y})", 77)
    Misc.Pause(500)
    
    elapsedTime = 0
    retryInterval = 1000  # Check every 500 ms

    while elapsedTime < maxWait:
        # Check if the player is in the correct position
        if Player.Position.X == expectedX and Player.Position.Y == expectedY:
            # Filter for mobiles within 3 tiles
            mobilesFilter = Mobiles.Filter()
            mobilesFilter.RangeMax = 2
            mobilesFilter.Notorieties = List[Byte](bytes([1,2,3,4]))

            nearbyMobiles = Mobiles.ApplyFilter(mobilesFilter)

            if len(nearbyMobiles) == 0:
                Misc.SendMessage("Pass: Player is in the correct position and no mobiles are nearby.", 77)
                return  # Exit the function when in the correct position and no mobiles are nearby
            else:
                Misc.SendMessage(f"Waiting for mobiles to leave: {len(nearbyMobiles)} detected.", 33)
        
        Misc.Pause(retryInterval)
        elapsedTime += retryInterval
    
    # If the player is still not at the correct position or mobiles are still present, retry goHome()
    Misc.SendMessage("Fail: Conditions not met. Retrying goHome().", 33)
    goHome()  # Retry the goHome function


def unloadResources():
    Items.UseItem(0x42E87E92)  # Artisan tool or container
    Misc.Pause(500)
    Items.UseItem(0x41132AE2)  # Wood pouch
    Misc.Pause(500)
    Items.UseItem(0x42EA4E24)  # Ingot pouch
    Misc.Pause(500)
    ingot_count_in_backpack = Items.BackpackCount(0x1BF2, 0x0000)
    ingot_in_backpack = Items.FindByID(0x1BF2, 0x0000, Player.Backpack.Serial)
    log_in_backpack = Items.FindByID(0x1BDD, 0x0000, Player.Backpack.Serial)
    if log_in_backpack:
        Items.Move(log_in_backpack, 0x41132AE2, -1)  # Move all logs from backpack back to storage
        Misc.Pause(1000)
    if ingot_in_backpack:
        Items.Move(ingot_in_backpack, 0x42EA4E24, ingot_count_in_backpack - 200)  # Move excess ingots back to storage
        Misc.Pause(1000)

def bodbagCheck():
    Items.UseItem(0x42E87E92)
    Misc.Pause(1000)
    Items.UseItem(0x49A27509)
    Misc.Pause(1000)
    ironExcept = Items.ContainerCount(0x49A27509,0x14EF,0x044e)
    Misc.Pause(500)
    Misc.SendMessage("Iron Exceptional "+str(ironExcept))
    Misc.Pause(1000)
    if ironExcept > 9:
        unloadResources()
        Misc.ScriptRun("BOD_runIronExcept.py")
    Misc.Pause(1000)
    while Misc.ScriptStatus("BOD_runIronExcept.py"):
        Misc.Pause(10000)
    Misc.Pause(1000)
    Items.UseItem(0x42369679)
    Misc.Pause(1000)
    PreshExcept = Items.ContainerCount(0x42369679,0x14EF,0x044e)
    Misc.Pause(1000)
    Misc.SendMessage("Precious Exceptionals "+str(PreshExcept))
    if PreshExcept > 9:
        unloadResources()
        Misc.ScriptRun("BOD_runPreshExcept.py")
    Misc.Pause(1000)
    while Misc.ScriptStatus("BOD_runPreshExcept.py"):
        Misc.Pause(10000)   
    Misc.Pause(1000)
    Items.UseItem(0x4194BF9C)
    Misc.Pause(1000)
    Tailor = Items.ContainerCount(0x4194BF9C,0x14EF,0x0483)
    Misc.Pause(1000)
    Misc.SendMessage("Tailor BODs "+str(Tailor))
    if Tailor > 9:
        unloadResources()
        Misc.ScriptRun("BOD_runTailor.py")
    Misc.Pause(1000)
    while Misc.ScriptStatus("BOD_runTailor.py"):
        Misc.Pause(10000) 
    Misc.Pause(1000)
    Player.ChatSay(64,"I will acquire additional BODs in 5 hours.")

def trainArtisan():
    # Constants
    TOOL_CONTAINER = 0x42E87E92
    WOOD_POUCH = 0x41132AE2
    CRAFTING_INGOT_POUCH = 0x42EA4E24
    TOOLING_INGOT_POUCH = 0x42E87E92
    LOG_ID = 0x1BDD
    INGOT_ID = 0x1BF2
    DEFAULT_HUE = 0x0000

    # Use containers
    Items.UseItem(TOOL_CONTAINER)
    Misc.Pause(500)
    Items.UseItem(WOOD_POUCH)
    Misc.Pause(500)
    Items.UseItem(CRAFTING_INGOT_POUCH)
    Misc.Pause(500)

    # Get counts from storage pouches
    logs_in_pouch = Items.ContainerCount(WOOD_POUCH, LOG_ID, DEFAULT_HUE)
    ingots_in_pouch = Items.ContainerCount(CRAFTING_INGOT_POUCH, INGOT_ID, DEFAULT_HUE)

    # Option 1: Enough logs to proceed with artisan training
    if logs_in_pouch > 1000:
        # Ensure backpack has 1000 logs
        logs_in_backpack = Items.BackpackCount(LOG_ID, DEFAULT_HUE)
        if logs_in_backpack < 1000:
            log_item = Items.FindByID(LOG_ID, DEFAULT_HUE, WOOD_POUCH)
            Items.Move(log_item, Player.Backpack.Serial, 1000 - logs_in_backpack)
            Misc.Pause(1000)

        # Ensure backpack has exactly 200 ingots
        ingots_in_backpack = Items.BackpackCount(INGOT_ID, DEFAULT_HUE)
        ingot_item = Items.FindByID(INGOT_ID, DEFAULT_HUE, TOOLING_INGOT_POUCH)

        if ingots_in_backpack < 200:
            Items.Move(ingot_item, Player.Backpack.Serial, 200 - ingots_in_backpack)
            Misc.Pause(1000)
        elif ingots_in_backpack > 200:
            excess = ingots_in_backpack - 200
            ingot_in_backpack = Items.FindByID(INGOT_ID, DEFAULT_HUE, Player.Backpack.Serial)
            Items.Move(ingot_in_backpack, TOOLING_INGOT_POUCH, excess)
            Misc.Pause(1000)

        # Recall to trainer and restart script
        Player.ChatSay("[recall Trainer")
        Misc.Pause(3000)
        Misc.ScriptRun("trainArtisan.py")

    # Option 2: Not enough logs, but enough ingots to run imbuologist
    elif ingots_in_pouch > 2500:
        # Move logs out of backpack
        log_in_backpack = Items.FindByID(LOG_ID, DEFAULT_HUE, Player.Backpack.Serial)
        if log_in_backpack:
            Items.Move(log_in_backpack, WOOD_POUCH, -1)
            Misc.Pause(1000)

        # Ensure 2000 ingots in backpack
        ingots_in_backpack = Items.BackpackCount(INGOT_ID, DEFAULT_HUE)
        ingot_item = Items.FindByID(INGOT_ID, DEFAULT_HUE, CRAFTING_INGOT_POUCH)

        if ingots_in_backpack < 2000:
            Items.Move(ingot_item, Player.Backpack.Serial, 2000 - ingots_in_backpack)
            Misc.Pause(1000)

        # Run dagger training
        Misc.ScriptRun("daggerTrain_Imbuologist.py")


        

def repairCheck():
    repairPouch = Items.FindBySerial(0x41547DA9)

    if repairPouch:
        prop_list = Items.GetPropStringByIndex(repairPouch, 4)
        prop_list_split = prop_list.split()
        items = int(prop_list_split[0]) if prop_list_split else 0

        if items > 0:
            Player.ChatSay("Looks like repairs are in order.")
            Misc.Pause(1500)
            Player.PathFindTo(6802, 3892, 17)
            Misc.Pause(4000)
            Items.UseItem(repairPouch)
            Misc.Pause(500)

            # Find all daggers in the repair pouch
            dagger_candidates = Items.FindItemsByID(0x0F52, -1, repairPouch.Serial)

            silver_dagger = None
            for dagger in dagger_candidates:
                props = Items.GetPropStringList(dagger)
                if any("silver" in prop.lower() for prop in props):
                    silver_dagger = dagger
                    break

            if silver_dagger:
                Items.Move(silver_dagger, Player.Backpack.Serial, 1)
                Misc.Pause(1000)

                # Confirm it's in the backpack
                dagger = Items.FindBySerial(silver_dagger.Serial)
                if dagger:
                    Misc.Pause(200)
                    Items.UseItemByID(0x13E3, -1)  # Repair deed
                    Misc.Pause(500)
                    Gumps.WaitForGump(0x38920abd, 10000)
                    Gumps.SendAction(0x38920abd, 42)  # Repair option
                    Target.WaitForTarget(10000, False)
                    Target.TargetExecute(dagger)
                    Misc.Pause(500)
                    Gumps.WaitForGump(0x38920abd, 10000)
                    Gumps.SendAction(0x38920abd, 0)  # Close
                    Misc.Pause(500)
                    Items.Move(dagger, 0x411F0FDE, 1)  # Move back to original container
                    Misc.Pause(1000)
                    Player.ChatSay("This looks good as new.")
                    Misc.Pause(1000)

            Player.PathFindTo(6804, 3897, 17)
            Misc.Pause(2000)


def trashCheck():
    weapon_keywords = ["mace", "axe", "katana", "halberd", "kryss"]

    for item in Player.Backpack.Contains:
        if item.ItemID != 0x14EF:
            continue  # Skip items that are not the specified type

        prop_list = Items.GetPropStringList(item)

        # Check for exceptional keyword
        if "exceptional" not in str(prop_list):
            Items.MoveOnGround(item, 1, Player.Position.X - 1, Player.Position.Y, Player.Position.Z)
            continue  # Skip further checks if not exceptional

        # Check for Q20, 4-piece cloths
        is_specific_property = "20" in str(prop_list) and len(prop_list) == 11
        is_correct_hue = item.Hue == 0x0483

        if is_specific_property and is_correct_hue:
            Misc.Pause(1000)
            Items.MoveOnGround(item, 1, Player.Position.X - 1, Player.Position.Y, Player.Position.Z)
            Misc.Pause(1000)
            continue  # Skip further checks if Q20 cloths

        # Check for large weapon BOD
        has_min_length = len(prop_list) >= 9
        contains_weapon_keyword = any(keyword in prop.lower() for prop in prop_list for keyword in weapon_keywords)

        if has_min_length and contains_weapon_keyword:
            Player.HeadMessage(64, "Large weapon BOD! Tossing...")
            Misc.Pause(1000)
            Items.MoveOnGround(item, 1, Player.Position.X - 1, Player.Position.Y, Player.Position.Z)




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
    root = Items.BackpackCount(0x0F7A,-1)
    moss = Items.BackpackCount(0x0F7B,-1)
    pearl = Items.BackpackCount(0x0F86,-1)
  
    
    if root < 15:
        Items.Move(Items.FindByID(0x0F7A,-1,0x42E88440),Player.Backpack.Serial,15-root)
        Misc.Pause(1000)
    
    if moss < 15:
        Items.Move(Items.FindByID(0x0F7B,-1,0x42E88440),Player.Backpack.Serial,15-moss)
        Misc.Pause(1000)
        
    if pearl < 15:
        Items.Move(Items.FindByID(0x0F86,-1,0x42E88440),Player.Backpack.Serial,15-pearl)
        Misc.Pause(1000)
        
    else:
        Player.HeadMessage(64,"Regs look good")
        Misc.Pause(500)
    
def bod_run():
    Journal.Clear()
    # Randomly select a wait time between 90 and 120 seconds
    wait_time = random.randint(75, 300)
    # Inform the player about the wait time
    Player.ChatSay(64, f"Making a run in {wait_time} seconds.")
    # Convert wait time to milliseconds and pause
    Misc.Pause(wait_time * 1000)
    Misc.ScriptStopAll(True)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, 0)
    worldSave()
    Player.ChatSay(64,'[recall Britain Crafting')
    Misc.Pause(3000)
    Misc.WaitForContext(0x00029397, 10000)
    Misc.ContextReply(0x00029397, 1)
    Misc.Pause(1000)
    while Gumps.HasGump():
        Gumps.WaitForGump(2611865322, 1000)
        Misc.Pause(1200)
        Gumps.SendAction(2611865322, 1)
        Misc.Pause(500)
        Gumps.WaitForGump(3188567326, 1000)
        Gumps.SendAction(3188567326, 1)
        Misc.Pause(500)
    Player.ChatSay(64,'[recall Britain Crafting 2')
    Misc.Pause(3000)
    Misc.WaitForContext(0x0024A965, 10000)
    Misc.ContextReply(0x0024A965, 1)
    Misc.Pause(1000)
    while Gumps.HasGump():
        Gumps.WaitForGump(2611865322, 1000)
        Misc.Pause(1200)
        Gumps.SendAction(2611865322, 1)
        Misc.Pause(500)
        Gumps.WaitForGump(3188567326, 1000)
        Gumps.SendAction(3188567326, 1)
        Misc.Pause(500)
    Misc.Pause(2000)
    while Player.Mana < 11:
        Misc.Pause(1000)
    Player.ChatSay(64,'[recall Winter Lodge')
    Misc.Pause(3000)
    trashCheck()
    Player.PathFindTo(6802, 3901, 12)
    Misc.Pause(1500)
    door = Items.FindBySerial(0x42F89EDC)
    if door.ItemID == 0x0677:
        Items.UseItem(door)
        Misc.Pause(500)
    Player.PathFindTo(6802, 3900, 17)
    Misc.Pause(1500)      
    Items.UseItem(0x42E88440) #Open box by door
    Misc.Pause(1000)
    stockRegs()
    for i in Player.Backpack.Contains: #Sort/store tailor BODS
        if i.ItemID == 0x14EF and i.Hue == 1155:
            Items.Move(i,0x4194BF9C,-1)
            Misc.Pause(1000)
        
    for i in Player.Backpack.Contains: #Sort/store blacksmith BODS
        list = Items.GetPropStringList(i)
        len_det = len(list)
        keywords = ["mace", "axe", "katana", "halberd"]
        if i.ItemID == 0x14EF and len_det > 9:
            Items.Move(i,0x40C8592D,-1)
            Misc.Pause(1000)
        if i.ItemID == 0x14EF and len_det == 9:
            Items.Move(i,0x42369679,-1)
            Misc.Pause(1000)
        if i.ItemID == 0x14EF and len_det == 7:
            Items.Move(i,0x4236967B,-1)
            Misc.Pause(1000)
        if i.ItemID == 0x14EF and len_det == 8 and "exceptional." in str(list):
            Items.Move(i,0x49A27509,-1)
            Misc.Pause(1000)
        if i.ItemID == 0x14EF and len_det == 8 and not "exceptional." in str(list):
            Items.Move(i,0x4236967A,-1)
            Misc.Pause(1000)
    
    if Player.Name == 'ToolmanTailor':
        Player.PathFindTo(6800, 3898, 17)
        Misc.Pause(2000)
        Player.Run("West")
    elif Player.Name == 'Realtree':
        Player.PathFindTo(6804, 3897, 17)
        Misc.Pause(3000)
        Player.Run("North")
        Misc.Pause(500)
    elif Player.Name == 'Tool Time':
        Player.PathFindTo(6800, 3892, 17)
        Misc.Pause(5000)
        Player.Run("North")
    elif Player.Name == 'ImaTool':
        Player.PathFindTo(6805, 3892, 17)
        Misc.Pause(5000)
        Player.Run("North")          
            
    Player.ChatSay(64, 'Bod run complete')
    Misc.Pause(1000)
    if Journal.Search('You can ask for a bulk order deed in'):
        string = Journal.GetLineText('You can',False)
        string = string.split("in")
        string = string[1]
        string = string.split("h")
        string = string[0]
        hour = int(string)
        mstring = Journal.GetLineText('You can',False)
        mstring = mstring.split("in")
        mstring = mstring[1]
        mstring = mstring.split("m")
        mstring = mstring[0]
        mstring = mstring.split("h ")
        mstring = mstring[1]
        min = int(mstring)
        sleepTime = (hour*60) + min + 2
        Misc.Pause(500)
        Player.ChatSay(64,"I was too early. Will return in " + str(hour) + " hours and " + str(min) + " minutes.")
        Misc.Pause(1000)
        if Player.Name == 'ToolmanTailor':
            for x in range(hour):
                Player.ChatSay("I have more than an hour to wait, making a farm run.")
                Misc.Pause(1000)
                Misc.ScriptRun("FarmGod.py")
                time.sleep(60*60)
            time.sleep(60*min)
            Journal.Clear()
        elif Player.Name == "ImaTool":
            Player.ChatSay("I will make "+str(hour)+" treasure runs in the meantime.")
            Misc.Pause(1000)
            for x in range(0,hour * 2):
                Misc.ScriptRun("treasure_God.py")
                time.sleep(30*60)
            Player.ChatSay("Now just waiting the final "+str(min)+" minutes.")
            Misc.Pause(1000)
            time.sleep(60*(min+2))
            Journal.Clear()
        elif Player.Name == "Tool Time":
            for x in range(0,hour * 2):
                Player.ChatSay("I have more than an hour to wait, making a farm run.")
                Misc.Pause(1000)
                Misc.ScriptRun("FarmGod.py")
                time.sleep(30*60)
            time.sleep(60*min)
            Journal.Clear()
        elif Player.Name == "Realtree":
            trainArtisan()
            time.sleep(60*sleepTime)
            Journal.Clear()
        
        else:
            time.sleep(60*sleepTime)
            Journal.Clear()
        bod_run()
 


    
while True:
    bod_run()
    Misc.Pause(500)
    if Player.Name == 'Realtree':
        bodbagCheck()
        repairCheck()
        trainArtisan()
        time.sleep(5*60*60)

    elif Player.Name == 'ToolmanTailor':
        Misc.Pause(2000)
        for x in range(5):
            Misc.ScriptRun("FarmGod.py")
            time.sleep(60*60) 
            
    elif Player.Name == 'ImaTool':
        Misc.Pause(5000)
        for x in range(0,10):
            Misc.ScriptRun("treasure_God.py")
            time.sleep(30*60)
            
    elif Player.Name == 'Tool Time':
        Misc.Pause(2000)
        for x in range(10):
            Misc.ScriptRun("FarmGod.py")
            time.sleep(30*60) 
        
    else:
        Player.ChatSay(64,"I will acquire additional BODs in 5 hours.")
        time.sleep(5*60*60)


        


