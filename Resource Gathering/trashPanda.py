from System.Collections.Generic import List
from System import Byte
from System import Int32 as int
import time
import keyboard

#Future project: steal the mushroom cave bong: item filter 0xAF67

def goHome():
    attempt_recall("Winter Lodge")
    Misc.Pause(3000)
    Player.PathFindTo(6802,3901,12)
    Misc.Pause(2000)
    Player.PathFindTo(6803,3899,17)
    Misc.Pause(2000)
    
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


def mobCheck():
    mobFilter = Mobiles.Filter()
    mobFilter.Enabled = True
    mobFilter.RangeMax = 10
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

        # Check if the spell was disturbed
        if Journal.SearchByType("Your concentration is disturbed, thus ruining thy spell.", "System"):
            Misc.SendMessage("Spell was disturbed. Recasting...")
            Journal.Clear()
            Misc.Pause(4000)
            continue  # Skip the rest of the loop and start over
        elif Journal.SearchByType("Insufficient mana for this spell.","System"):
            Misc.Pause(16000)
            Journal.Clear()
            continue
        else:
            break  # Exit the loop if no disturbance is detected

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


def takeSeat():
    Player.PathFindTo(6800, 3892, 17)
    Misc.Pause(6000)
    Player.Run("North")
    Misc.Pause(500)

    
def harvestWood():
    harvestFilter = Items.Filter()
    harvestFilter.RangeMax = 3
    harvestFilter.Graphics = List[int]([0x74EC]) 
    harvestFilter.Movable = False
    harvestableList = Items.ApplyFilter(harvestFilter)
    
    if len(harvestableList) > 0:
    
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
               
    else:
        Misc.Pause(500)
            
        
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
        
crate_id = 0x09A9
cutlery_id = [0x09F4]
trash = []

Journal.Clear()   
deadCheck()         
Player.ChatSay("Making a trash run in 90 seconds.")
Misc.Pause(90000) 
worldSave()       
Player.ChatSay("[recall Safe Trash")
Misc.Pause(3000)
while Player.Visible:
    Player.UseSkill("Hiding")
    Misc.Pause(10000)
Misc.Pause(1000)

while True:
    deadCheck()
    Items.UseItem(0x400047A6)  # Presumably clicks the trash pile
    Misc.Pause(1000)
    harvestWood()
    barricade()
    # Wait for 30 minutes, checking for mobs every 10 seconds
    wait_time = 90 * 60  # Total wait time in seconds (30 minutes)
    start_time = time.time()  # Record the start time
    while (time.time() - start_time) < wait_time:
        if mobCheck():
            deadCheck()  # For example, calling deadCheck() to handle the situation
            goHome()  # Replace with your actual safety 
            stockRegs()
            takeSeat()
            Misc.ScriptStop("trashPanda.py")
            break  # Exit the loop if a mob is detected
        
        time.sleep(3)  # Wait for 3 seconds before checking again

# Optional: Include logic to handle what happens if a mob was detected, such as recalling or waiting longer.

Items.UseItem(0x400047A6)