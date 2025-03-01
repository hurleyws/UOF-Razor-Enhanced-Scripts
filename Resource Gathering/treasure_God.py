from System.Collections.Generic import List
from System import Byte
from System import Int32 as int
import time
import keyboard
import datetime


#KILL 

#KILL

gem_ids = [0x0F21,0x0F16,0x0F19,0x0F13,0x0F10,0x0F25,0x0F2D,0x0F15,0x0F26,0x0F21] #includes RDA frag 0x0F21
arms_ids = [
    0x0DF2, 0x0F49, 0x0F4D, 0x0F4D, 0x140E, 0x0F47, 0x0DF0, 0x13B2, 0x0F5E, 
    0x1B72, 0x1B73, 0x13F6, 0x13BB, 0x13BE, 0x13BF, 0x0EC3, 0x0EC3, 0x1408, 
    0x13B4, 0x0F50, 0x1441, 0x1441, 0x0F52, 0x0F4B, 0x0F4B, 0x0F45, 0x0F45, 
    0x13F8, 0x13F8, 0x13F8, 0x143E, 0x143D, 0x0F43, 0x1B76, 0x13FD, 0x140A, 
    0x13FF, 0x1B74, 0x1B79, 0x1B79, 0x1401, 0x13FB, 0x1C06, 0x1C0A, 0x1C0A, 
    0x1DB9, 0x13C6, 0x13C7, 0x13CB, 0x1C00, 0x1C08, 0x13CD, 0x13CC, 0x0F62, 
    0x0F61, 0x0F5C, 0x143B, 0x1B7B, 0x1B7B, 0x140C, 0x0E86, 0x0E87, 
    0x1C04, 0x1412, 0x1415, 0x1410, 0x1414, 0x1413, 0x1411, 0x0E89, 0x13EB, 
    0x13F0, 0x13EE, 0x13EC, 0x13B6, 0x13B6, 0x0E81, 0x1403, 0x1C02, 
    0x1C0C, 0x13D5, 0x13D5, 0x13D6, 0x13DA, 0x13DC, 0x13DB, 0x1443, 0x13B9, 
    0x13B0, 0x1405, 0x1439, 0x1407, 0x1B7A, 0x1C04, 0x0F52,
]
regs = [
0x0F7A, 0x0F7B,0x0F86,0x0F8C,0x0F84,0x0F88,0x0F85,0x0F8D,
]

leather_ids = [0x13C7,0x13CC,0x13CB,0x13C6,0x13CD,0x1DB9,0x13D6,0x13DA,0x13DB,0x13DC,0x1DB9,0x13D5,0x1C02,0x1C06,0x1C0A,0x1C0C,0x1C00,0x1C08]

metalArms = [id for id in arms_ids if id not in leather_ids]

scrolls = [0x1f2d,0x1f2e,0x1f2f,0x1f30,0x1f31,0x1f32,0x1f33,0x1f34,0x1f35,0x1f36,0x1f37,0x1f38,0x1f39,
0x1f3a,0x1f3b,0x1f3c,0x1f3d,0x1f3e,0x1f3f,0x1f40,0x1f41,0x1f42,0x1f43,0x1f44,0x1f45,0x1f46,0x1f47,0x1f48,
0x1f49,0x1f4a,0x1f4b,0x1f4d,0x1f4e,0x1f4f,0x1f50,0x1f51,0x1f52,0x1f53,0x1f54,0x1f55,0x1f56,0x1f57,0x1f58,
0x1f59,0x1f5a,0x1f5b,0x1f5c,0x1f5d,0x1f5e,0x1f5f,0x1f60,0x1f61,0x1f62,0x1f63,0x1f64,0x1f65,0x1f66,0x1f67,
0x1f68,0x1f69,0x1f6a,0x1f6b,0x1f6c]

skill_scroll_id = 0x2260
gold_id = 0x0EED
blankscroll_id = 0x0EF3
rdafrag_id = 0x0F21
relic_id = 0x2AA2

loot = scrolls + gem_ids + arms_ids + regs + [skill_scroll_id, gold_id, blankscroll_id,rdafrag_id,relic_id]
goldLog = 'C:/Users/Hurley/Documents/GitHub/UOF-Razor-Enhanced-Scripts/Resource Gathering/goldLog.USR'

# Constants for chest graphics
CHEST_GRAPHICS = [0x74F0,0x0E40,0x6466,0x0E77,0x0E42,0x09AB,0x0E3C,0x0E40,0x09A9,0x0E7C,0x0E7F,0x0E3D,0x0E3F,0x0E43,0x0E7E,0x0E3E,0x0E41]  # Add all graphics here

# Configuration parameters
TIMEOUT = 15
MAX_RETRY = 5
RANGE_MAX = 10
ITEM_ID_SKILL = "Item ID"

def log_gold_amount():
    """
    Gets the current gold count in the backpack and appends it to the log file with a timestamp.
    """
    gold_amount = Items.BackpackCount(0x0EED, -1)  # Get gold count (0x0EED is the gold coin ID)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current date and time

    with open(goldLog, 'a') as file:  # 'a' mode appends instead of overwriting
        file.write(f"{timestamp}, {gold_amount}, ImaTool\n") # Write timestamp and gold amount

    Misc.SendMessage(f"Logged: {timestamp} - Gold: {gold_amount}", 53)
    
def transferGold():
    Items.UseItem(0x42E87E92)
    Misc.Pause(500)
    if Items.ContainerCount(0x42E87E92,0x0EED,-1) >50000:
        gold = Items.FindByID(0x0EED,-1,0x42E87E92)
        if gold:
            Items.MoveOnGround(gold,50000,6802, 3898, 17)
            Misc.Pause(1000)
            Misc.SendMessage("Moving")
            Misc.Pause(500)
            Player.PathFindTo(6802, 3899, 17)
            Misc.Pause(1500)
            door = Items.FindBySerial(0x42F89EBF)
            if door.ItemID == 0x0675:
                Items.UseItem(door)
                Misc.Pause(500)
            Player.PathFindTo(6802, 3900, 17)
            Misc.Pause(750)
            gold = Items.FindByID(0x0EED,0x0000,-1,2)
            Items.MoveOnGround(gold,50000,6802, 3901, 12)
            Misc.Pause(1000)
            Player.PathFindTo(6802, 3901, 12)
            Misc.Pause(750)
            Items.Move(gold,0x002C21FF,50000)
            Misc.Pause(1000)
            if door.ItemID == 0x0675:
                Items.UseItem(door)
                Misc.Pause(500)
            Player.PathFindTo(6803, 3898, 17)
            Misc.Pause(1500)

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

def checkATM():
    Mobiles.UseMobile(0x002C21FF)
    Misc.Pause(500)
    line = Gumps.LastGumpGetLine(12)
    line = line.replace(',', '')  # Remove commas from the string
    line = int(line)  # Now this should work without error

    if line > 500000:
        Misc.Pause(500) #clear speech line
        keyboard.press('return')
        keyboard.release('return')
        Misc.Pause(500)
        Misc.Pause(500)
        Gumps.SendAction(474654352, 6)
        Misc.Pause(1000)
        Misc.SendToClient("500000")
        Misc.Pause(500)
        keyboard.press('return')
        keyboard.release('return')
        Misc.Pause(500)


def weightCheck():
    if Player.Weight >= 370:
        worldSave()
        sellArms()
        sellGems()
        goHome()
        worldSave()
        stockRegs()
        takeSeat()
        Misc.ScriptStop("treasure_God.py")

def getGroundLoot(maxRange=10):
    groundLootFilter = Items.Filter()
    groundLootFilter.Enabled = True
    groundLootFilter.Movable = True
    groundLootFilter.OnGround = True
    groundLootFilter.Graphics = List[int]([0x1BDD,0x2260,0x0EED,0x0F21,0x0F16,0x0F19,0x0F13,0x0F10,0x0F25,0x0F2D,0x0F15,0x0F26,0x0F21,0x0F7A,0x0F7B,0x0F86,0x0F8C,0x0F84,0x0F88,0x0F85,0x0F8D, 0x0DF2, 0x0F49, 0x0F4D, 0x0F4D, 0x140E, 0x0F47, 0x0DF0, 0x13B2, 0x0F5E, 0x1B72, 0x1B73, 0x13F6, 0x13BB, 0x13BE, 0x13BF, 0x0EC3, 0x0EC3, 0x1408, 0x13B4, 0x0F50, 0x1441, 0x1441, 0x0F52, 0x0F4B, 0x0F4B, 0x0F45, 0x0F45, 0x13F8, 0x13F8, 0x13F8, 0x143E, 0x143D, 0x0F43, 0x1B76, 0x13FD, 0x140A, 0x13FF, 0x1B74, 0x1B79, 0x1B79, 0x1401, 0x13FB, 0x1C06, 0x1C0A, 0x1C0A, 0x1DB9, 0x13C6, 0x13C7, 0x13CB, 0x1C00, 0x1C08, 0x13CD, 0x13CC, 0x0F62, 0x0F61, 0x0F5C, 0x143B, 0x1B7B, 0x1B7B, 0x140C, 0x0E86, 0x0E87, 0x1C04, 0x1412, 0x1415, 0x1410, 0x1414, 0x1413, 0x1411, 0x0E89, 0x13EB, 0x13F0, 0x13EE, 0x13EC, 0x13B6, 0x13B6, 0x0E81, 0x1403, 0x1C02, 0x1C0C, 0x13D5, 0x13D5, 0x13D6, 0x13DA, 0x13DC, 0x13DB, 0x1443, 0x13B9, 0x13B0, 0x1405, 0x1439, 0x1407, 0x1B7A, 0x1C04, 0x0F52, 0x1544]) 
    groundLootFilter.RangeMax = maxRange
    groundLootFilterList = Items.ApplyFilter(groundLootFilter)
    for i in groundLootFilterList:
        mobCheck()
        moveToChest(i)
        Player.UseSkill("Item ID")
        Misc.Pause(500)
        Target.TargetExecute(i)
        Misc.Pause(500)
        Items.Move(i,Player.Backpack.Serial,-1)
        Misc.Pause(1000)
    Target.Cancel()
    moveToOriginalPosition(originalPosition)
    weightCheck()

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
        Misc.Pause(2000)
        while Player.Mana < 11:
            Misc.Pause(1000)
        Misc.Pause(200)
        worldSave()
        goHome()
        stockRegs()
        takeSeat()
    
def goHome():
    attempt_recall("Winter Lodge")
    Misc.Pause(3000)
    log_gold_amount()
    gold = Items.FindByID(0x0EED,-1,Player.Backpack.Serial)
    if gold:
        Items.Move(gold,0x002C21FF,-1)
        Misc.Pause(1000)
    checkATM()
    Misc.Pause(500)
    Player.PathFindTo(6802,3901,12)
    Misc.Pause(2000)
    Player.PathFindTo(6803,3899,17)
    Misc.Pause(2000)

def takeSeat():
    Player.PathFindTo(6805,3892,17)
    Misc.Pause(6000)
    Player.Run("North")
    Misc.Pause(500)
    
def stockRegs():
    root = Items.BackpackCount(0x0F86,-1)
    moss = Items.BackpackCount(0x0F7B,-1)
    pearl = Items.BackpackCount(0x0F7A,-1)
    picks = Items.BackpackCount(0x14FC,-1)
    shade = Items.FindByID(0x0F88,-1,Player.Backpack.Serial)
    garlic = Items.FindByID(0x0F84,-1,Player.Backpack.Serial)
    ginseng = Items.FindByID(0x0F85,-1,Player.Backpack.Serial)
    ash = Items.FindByID(0x0F8C,-1,Player.Backpack.Serial)
    silk = Items.FindByID(0x0F8D,-1,Player.Backpack.Serial)
    gold = Items.FindByID(0x0EED,-1,Player.Backpack.Serial)
    scrolls = Items.FindByID(0x0EF3,-1,Player.Backpack.Serial)
    logs = Items.FindByID(0x1BDD,-1,Player.Backpack.Serial)
  
    Items.UseItem(0x42E88440)
    Misc.Pause(500)
    Items.UseItem(0x42E87E92)
    Misc.Pause(500)
    
    
    if picks < 15:
        Items.Move(Items.FindByID(0x14FC,-1,0x42E88440),Player.Backpack.Serial,15-picks)
        Misc.Pause(1000)  

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
        Items.Move(gold,0x42E87E92,-1)
        Misc.Pause(1000)
    if scrolls:
        Items.Move(scrolls,0x42E87E92,-1)
        Misc.Pause(1000)
    if logs:
        for l in Player.Backpack.Contains:
            if l.ItemID == 0x1BDD:
                Items.Move(l,0x41132AE2,-1)
                Misc.Pause(1000)

def sellArms():
    totalScrolls = countItemsByID(scrolls)
    if totalScrolls > 30:
        SellAgent.Enable()
        attempt_recall("Sell Scrolls")
        Misc.Pause(3000)
        Misc.WaitForContext(0x0026C71B, 10000)
        Misc.ContextReply(0x0026C71B, 2)
        Misc.Pause(1000)
        BuyAgent.Enable()        
        Misc.WaitForContext(0x0026D40E, 10000)
        Misc.ContextReply(0x0026D40E, 1)
        Misc.Pause(500)
        Player.ChatSay(26, 'I thank thee')
        Misc.Pause(500)       
    totalArms = countItemsByID(metalArms)
    if totalArms > 15:
        SellAgent.Enable()
        attempt_recall("Sell Arms")
        Misc.Pause(3000)
        Misc.WaitForContext(0x00136620, 10000) 
        Misc.ContextReply(0x00136620, 2) #guildmistress
        Misc.Pause(1000)
        Misc.WaitForContext(0x000012C1, 10000) 
        Misc.ContextReply(0x000012C1, 3) #weaponsmith
        Misc.Pause(1000)
        Player.ChatSay(26, 'I thank thee.')
        Misc.Pause(500)
        Player.EmoteAction("bow")
        Misc.Pause(500)
#        Misc.WaitForContext(0x000012C1, 10000)
#        Misc.ContextReply(0x000012C1, 3) #Weaponsmith
#        Misc.Pause(2000)
    totalLeather = countItemsByID(leather_ids)
    if totalLeather > 15:
        attempt_recall("Sell Leather")
        Misc.Pause(3000)
        Misc.WaitForContext(0x00000556, 10000) 
        Misc.ContextReply(0x00000556, 2) 
        Misc.Pause(1000)
        Player.ChatSay(26, 'I thank thee.')
        Misc.Pause(500)
        
def sellGems():
    totalGems = countItemsByID(gem_ids)
    if totalGems > 35:
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

def pickChest(item):
    Journal.Clear()
    lockpick = Items.FindByID(0x14FC, -1, Player.Backpack.Serial)

    if lockpick:
        startTime = time.time()  # Start timer

        # Lock picking loop
        while True:
            if time.time() - startTime > 60:  # Check if 30 seconds have passed
                Player.HeadMessage(64, "Lock picking took too long")
                Misc.Pause(500)
                Target.Cancel()
                return False

            if item:
                Items.UseItem(lockpick)
                Target.WaitForTarget(10000, False)
                Target.TargetExecute(item)

                Misc.Pause(10000)  # Short pause to allow the journal message to register

                if Journal.SearchByType('This does not appear to be locked.', 'System') or Journal.SearchByName('The lock quickly yields to your skill.', ''):
                    Misc.Pause(500)  # Additional short pause if unlocked
                    break
                else:
                    Misc.Pause(1500)  # Remaining part of the cooldown for lock picking

                if lockpick is None:
                    Player.HeadMessage(colors['red'], 'Ran out of lockpicks!')
                    return False
            else:
                Player.HeadMessage(64, "Where did the chest go?")
                Misc.Pause(500)
                return False

        startTime = time.time()  # Reset timer for trap removal

        # Trap removal loop
        while True:
            if time.time() - startTime > 60:  # Check if 30 seconds have passed
                Player.HeadMessage(64, "Trap removal took too long")
                Misc.Pause(500)
                Target.Cancel()
                return False

            if item:
                Player.UseSkill("Remove Trap")
                Target.WaitForTarget(10000, False)
                Target.TargetExecute(item)

                Misc.Pause(1000)  # Short pause to allow the journal message to register

                if Journal.SearchByName("appear to be trapped.", "System") or Journal.SearchByName("You carefully remove the trigger", "System"):
                    Misc.Pause(500)  # Additional short pause if untrapped
                    return True
                else:
                    Misc.Pause(9500)  # Remaining part of the cooldown for trap removal
            else:
                Player.HeadMessage(64, "Where did the chest go?")
                Misc.Pause(500)
                return False
    else:
        Player.HeadMessage(54, "I need more lockpicks")
        Misc.Pause(500)
        return False

def lootDamageable(chest):
    if Player.DistanceTo(chest) < 2:
        hatchet = Items.FindBySerial(0x41AB24F5)
        while not Player.CheckLayer("LeftHand"):
            Player.EquipItem(hatchet)
            Misc.Pause(500)
            deadCheck()
        Player.SetWarMode(True)
        while Items.FindBySerial(chest.Serial):
            Misc.Pause(1000)
            deadCheck()
            Items.UseItem(chest)
            danger = mobCheck()
            if danger:
                return
        danger = mobCheck()
        if danger:
            return
        Player.SetWarMode(False)
        Misc.Pause(2000)
        groundLootFilter = Items.Filter()
        groundLootFilter.Enabled = True
        groundLootFilter.Movable = True
        groundLootFilter.OnGround = True
        groundLootFilter.Graphics = List[int]([0x2260,0x0EED,0x0F21,0x0F16,0x0F19,0x0F13,0x0F10,0x0F25,0x0F2D,0x0F15,0x0F26,0x0F21,0x0F7A,0x0F7B,0x0F86,0x0F8C,0x0F84,0x0F88,0x0F85,0x0F8D, 0x0DF2, 0x0F49, 0x0F4D, 0x0F4D, 0x140E, 0x0F47, 0x0DF0, 0x13B2, 0x0F5E, 0x1B72, 0x1B73, 0x13F6, 0x13BB, 0x13BE, 0x13BF, 0x0EC3, 0x0EC3, 0x1408, 0x13B4, 0x0F50, 0x1441, 0x1441, 0x0F52, 0x0F4B, 0x0F4B, 0x0F45, 0x0F45, 0x13F8, 0x13F8, 0x13F8, 0x143E, 0x143D, 0x0F43, 0x1B76, 0x13FD, 0x140A, 0x13FF, 0x1B74, 0x1B79, 0x1B79, 0x1401, 0x13FB, 0x1C06, 0x1C0A, 0x1C0A, 0x1DB9, 0x13C6, 0x13C7, 0x13CB, 0x1C00, 0x1C08, 0x13CD, 0x13CC, 0x0F62, 0x0F61, 0x0F5C, 0x143B, 0x1B7B, 0x1B7B, 0x140C, 0x0E86, 0x0E87, 0x1C04, 0x1412, 0x1415, 0x1410, 0x1414, 0x1413, 0x1411, 0x0E89, 0x13EB, 0x13F0, 0x13EE, 0x13EC, 0x13B6, 0x13B6, 0x0E81, 0x1403, 0x1C02, 0x1C0C, 0x13D5, 0x13D5, 0x13D6, 0x13DA, 0x13DC, 0x13DB, 0x1443, 0x13B9, 0x13B0, 0x1405, 0x1439, 0x1407, 0x1B7A, 0x1C04, 0x0F52, 0x1544]) 
        groundLootFilter.RangeMax = 2
        groundLootFilterList = Items.ApplyFilter(groundLootFilter)
        for i in groundLootFilterList:
            Player.UseSkill("Item ID")
            Misc.Pause(500)
            Target.TargetExecute(i)
            Misc.Pause(500)
            Items.Move(i,Player.Backpack.Serial,-1)
            Misc.Pause(1000)
        Target.Cancel()
    else:
        Misc.SendMessage("Too far away, moving on.")
        Misc.Pause(200)
        return
        
def lootHarvestable(chest):
    if Player.DistanceTo(chest) < 2:
        hatchet = Items.FindBySerial(0x41AB24F5)
        while not Player.CheckLayer("LeftHand"):
            Player.EquipItem(hatchet)
            Misc.Pause(500)
            deadCheck
        Player.SetWarMode(True)
        Misc.Pause(200)
        while Items.FindBySerial(chest.Serial):
            Items.UseItem(hatchet)
            Misc.Pause(500)
            Target.TargetExecute(chest)
            Misc.Pause(10000)
            deadCheck
            danger = mobCheck()
            if danger:
                return
        danger = mobCheck()
        if danger:
            return
        Player.SetWarMode(False)
        Misc.Pause(2000)
        groundLootFilter = Items.Filter()
        groundLootFilter.Enabled = True
        groundLootFilter.Movable = True
        groundLootFilter.OnGround = True
        groundLootFilter.Graphics = List[int]([0x1BDD,0x2260,0x0EED,0x0F21,0x0F16,0x0F19,0x0F13,0x0F10,0x0F25,0x0F2D,0x0F15,0x0F26,0x0F21,0x0F7A,0x0F7B,0x0F86,0x0F8C,0x0F84,0x0F88,0x0F85,0x0F8D, 0x0DF2, 0x0F49, 0x0F4D, 0x0F4D, 0x140E, 0x0F47, 0x0DF0, 0x13B2, 0x0F5E, 0x1B72, 0x1B73, 0x13F6, 0x13BB, 0x13BE, 0x13BF, 0x0EC3, 0x0EC3, 0x1408, 0x13B4, 0x0F50, 0x1441, 0x1441, 0x0F52, 0x0F4B, 0x0F4B, 0x0F45, 0x0F45, 0x13F8, 0x13F8, 0x13F8, 0x143E, 0x143D, 0x0F43, 0x1B76, 0x13FD, 0x140A, 0x13FF, 0x1B74, 0x1B79, 0x1B79, 0x1401, 0x13FB, 0x1C06, 0x1C0A, 0x1C0A, 0x1DB9, 0x13C6, 0x13C7, 0x13CB, 0x1C00, 0x1C08, 0x13CD, 0x13CC, 0x0F62, 0x0F61, 0x0F5C, 0x143B, 0x1B7B, 0x1B7B, 0x140C, 0x0E86, 0x0E87, 0x1C04, 0x1412, 0x1415, 0x1410, 0x1414, 0x1413, 0x1411, 0x0E89, 0x13EB, 0x13F0, 0x13EE, 0x13EC, 0x13B6, 0x13B6, 0x0E81, 0x1403, 0x1C02, 0x1C0C, 0x13D5, 0x13D5, 0x13D6, 0x13DA, 0x13DC, 0x13DB, 0x1443, 0x13B9, 0x13B0, 0x1405, 0x1439, 0x1407, 0x1B7A, 0x1C04, 0x0F52, 0x1544]) 
        groundLootFilter.RangeMax = 2
        groundLootFilterList = Items.ApplyFilter(groundLootFilter)
        for i in groundLootFilterList:
            Player.UseSkill("Item ID")
            Misc.Pause(500)
            Target.TargetExecute(i)
            Misc.Pause(500)
            Items.Move(i,Player.Backpack.Serial,-1)
            Misc.Pause(1000)
        Target.Cancel()
    else:
        Misc.SendMessage("Too far away, moving on.")
        Misc.Pause(200)
        return
        
def findChests():
    chestFilter = Items.Filter()
    chestFilter.Enabled = True
    chestFilter.Movable = False
    chestFilter.OnGround = True
    chestFilter.Graphics = List[int](CHEST_GRAPHICS)
    chestFilter.RangeMax = RANGE_MAX
    return Items.ApplyFilter(chestFilter)

def moveToChest(chest):
    danger = mobCheck()
    if danger:
        return
    chestPosition = chest.Position
    Misc.SendMessage("Original chest position: {}".format(chestPosition))

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Directions to try: Down, Up, Right, Left
    for dx, dy in directions:
        chestCoords = PathFinding.Route()
        chestCoords.MaxRetry = MAX_RETRY
        chestCoords.StopIfStuck = False
        chestCoords.X = chestPosition.X + dx
        chestCoords.Y = chestPosition.Y + dy
        PathFinding.Go(chestCoords)
        
        startTime = time.time()
        while Player.DistanceTo(chest) > 1:
            currentTime = time.time()
            if currentTime - startTime > TIMEOUT:
                Misc.SendMessage("Timed out, trying next position")
                break
            Misc.Pause(500)
        
        # Check if the player has successfully moved close enough
        if Player.DistanceTo(chest) <= 1:
            break

def checkLeather():
    for i in Player.Backpack.Contains:
        if i.ItemID in leather_ids:
            return True

    return False
            

def handleChest(chest):
    danger = mobCheck()
    if danger:
        return
    if Player.DistanceTo(chest) < 2:
        success = pickChest(chest)
        if not success:
            Player.HeadMessage(64,"Disarming chest failed, moving on.")
            Misc.Pause(1000)
            return
        Items.UseItem(chest)
        Misc.Pause(10000)  # Wait for the chest to open
        for item in chest.Contains:
            if item.ItemID in arms_ids:
                Player.UseSkill(ITEM_ID_SKILL)
                Misc.Pause(500)
                Target.TargetExecute(item)
                Misc.Pause(1000)
                Items.Move(item, Player.Backpack.Serial, -1)
                Misc.Pause(1000)
                danger = mobCheck()
                if danger:
                    return
            elif item.ItemID in loot:
                Items.Move(item, Player.Backpack.Serial, -1)
                Misc.Pause(1000)
                danger = mobCheck()
                if danger:
                    return
        Target.Cancel()
    else:
        Misc.SendMessage("Too far away, moving on.")
        Misc.Pause(200)
        return #exit the function

def lootTreasure():
    """
    Function to loot treasure chests, including handling damageable chests.
    """
    chests = findChests()
    for chest in chests:
        props = Items.GetPropStringList(chest)

        # Check if the chest is damageable and handle accordingly
        if "Damageable" in str(props):
            moveToChest(chest)
            worldSave()
            lootDamageable(chest)  # Assuming this function handles finding damageable chests internally
            weightCheck()
            
        elif "Harvestable" in str(props):
            Player.PathFindTo(5841, 1417, 0)
            Misc.Pause(5000)
            worldSave()
            lootHarvestable(chest)
            weightCheck()
            
        else:
            # Handle regular chests
            if len(props) == 2 and chest.Name == "barrel":
                moveToChest(chest)
                worldSave()
                handleChest(chest)
                weightCheck()
            elif len(props) == 1:
                moveToChest(chest)
                worldSave()
                handleChest(chest)
                weightCheck()
                
    

def mobCheck():
    mobFilter = Mobiles.Filter()
    mobFilter.Enabled = True
    mobFilter.RangeMax = 4
    mobFilter.CheckLineOfSight = True
    mobList = Mobiles.ApplyFilter(mobFilter)
    
    if len(mobList) > 0:
        return True
    else:
        return False
 
def worldSave():
    danger = mobCheck()
    if danger:
        return
    if (Journal.SearchByType('The world will save in 1 minute.', 'System') or Journal.SearchByType('pause', 'Regular')):
        Misc.Pause(700)
        Misc.SendMessage('Pausing for world save or player-called break.', 33)
        while (not Journal.SearchByType('World save complete.', 'System') and not Journal.SearchByType('play', 'Regular')):
            Misc.Pause(1000)
        Misc.Pause(2500)
        Misc.SendMessage('Continuing run', 33)
        Misc.Pause(700)
    Journal.Clear()  

def attempt_recall(location):
    while True:
        Player.ChatSay(f"[recall {location}")
        Misc.Pause(2500)  # Wait for the spell to cast
        deadCheck()

        # Check if the spell was disturbed
        if Journal.SearchByType("Your concentration is disturbed, thus ruining thy spell.", "System"):
            Misc.SendMessage("Spell was disturbed. Recasting...")
            Journal.Clear()
            Misc.Pause(4000)
            deadCheck()
            continue  # Skip the rest of the loop and start over
        elif Journal.SearchByType("Insufficient mana for this spell.","System"):
            Misc.Pause(16000)
            deadCheck()
            Journal.Clear()
            continue
        else:
            break  # Exit the loop if no disturbance is detected
    
def moveToOriginalPosition(originalPosition):
    danger = mobCheck()  # Assuming mobCheck() is a function that checks for danger
    if danger:
        Misc.SendMessage("Danger detected, cannot move to original position.")
        return
    if Player.Position != originalPosition:
        targetCoords = PathFinding.Route()
        targetCoords.MaxRetry = MAX_RETRY  # Ensure MAX_RETRY is defined somewhere in your script
        targetCoords.StopIfStuck = False
        targetCoords.X = originalPosition.X
        targetCoords.Y = originalPosition.Y
        PathFinding.Go(targetCoords)
        
        startTime = time.time()  # Ensure you have imported the time module
        while Player.Position != originalPosition:
            currentTime = time.time()
            if currentTime - startTime > TIMEOUT:  # Ensure TIMEOUT is defined somewhere in your script
                Misc.SendMessage("Timed out, trying next position")
                break
            Misc.Pause(500)
    
    
 #Call the function
deadCheck()
Journal.Clear()
Misc.ClearIgnore()
Player.ChatSay(64,"Making a treasure run in 90 seconds.")
Misc.Pause(500)
Gumps.SendAction(474654352, 0)
Misc.Pause(85000)
worldSave()
attempt_recall("Deceit 2")
Misc.Pause(2500)
lootTreasure()
worldSave()
deadCheck()
attempt_recall("Fire 5")
Misc.Pause(2500)
lootTreasure()
worldSave()
deadCheck()
attempt_recall("Wrong 1")
Misc.Pause(2500)
lootTreasure()
Misc.Pause(500)
lootTreasure()
worldSave()
deadCheck()
attempt_recall("Wrong 3")
Misc.Pause(2500)
lootTreasure()
worldSave()
deadCheck()
Misc.Pause(4000)
attempt_recall("Despise 20")
Misc.Pause(2500)
lootTreasure()
Misc.Pause(500)
lootTreasure()
deadCheck()
attempt_recall("Despise 25")
Misc.Pause(2500)
lootTreasure()
Misc.Pause(500)
lootTreasure()
deadCheck()
worldSave()
sellArms()
sellGems()
goHome()
worldSave()
stockRegs()
transferGold()
takeSeat()

#
