from Scripts.glossary.spells import spells
from Scripts.glossary.items.spellScrolls import spellScrolls
spellScrollIDs = [ spellScrolls[ scroll ].itemID for scroll in spellScrolls ]
from Scripts.utilities.items import MoveItem
import re
from System import Int32 as int
from System import Byte
from System.Collections.Generic import List
import time
import random

greenchest = Items.FindBySerial(0x412FB2AC)
trashbarrel = Items.FindBySerial(0x43DCB065)
regchest = Items.FindBySerial(0x4043C469)
IDchest = Items.FindBySerial(0x4342B03E)
sellchest = Items.FindBySerial(0x43DCE16C)
gemchest = Items.FindBySerial(0x4189A2CC)
scrollchest = Items.FindBySerial(0x4043AE0E)
tmapchest = Items.FindBySerial(0x408E8DA8)
lockpick = Items.FindByID(0x14FC,-1,Player.Backpack.Serial)

regs = {
0x0F7A, 0x0F7B,0x0F86,0x0F8C,0x0F84,0x0F88,0x0F85,0x0F8D,0x2260
}
#Regs includes skill scroll ID

pchest = [0x0E41,0x09AB,0x0E7C,0x0E40]
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
    0x13B0, 0x1405, 0x1439, 0x1407, 0x1B7A, 0x1C04, 0x0F52
]

def clean_item_name(item_name):
    """Strips HTML tags from the item name."""
    return re.sub(r'<.*?>', '', item_name)

def worldSave():
    if (Journal.SearchByType('The world will save in 1 minute.', 'System') or Journal.SearchByType('pause', 'Regular')):
        Misc.Pause(700)
        Misc.SendMessage('Pausing for world save or player-called break.', 33)
        while (not Journal.SearchByType('World save complete.', 'System') and not Journal.SearchByType('play', 'Regular')):
            Misc.Pause(1000)
        Misc.Pause(2500)
        Misc.SendMessage('Continuing run', 33)
        Misc.Pause(1000)
    Journal.Clear()
    
def sortScrolls(item):
    Items.UseItem(scrollchest)
    Misc.Pause(500)

def pickChest(item):
    Journal.Clear()
    if lockpick:
        while True:
            Items.UseItem(lockpick)
            Target.WaitForTarget(10000, False)
            Target.TargetExecute(item)

            # Short pause to allow the journal message to register
            Misc.Pause(500)

            # Check immediately after attempting to pick the lock
            if Journal.SearchByType('This does not appear to be locked.', 'System'):
                Misc.Pause(500)  # Additional short pause if unlocked
                break
            else:
                Misc.Pause(3500)  # Remaining part of the cooldown for lock picking

            if lockpick is None:
                Player.HeadMessage(colors['red'], 'Ran out of lockpicks!')
                return

        while True:
            Player.UseSkill("Remove Trap")
            Target.WaitForTarget(10000, False)
            Target.TargetExecute(item)

            # Short pause to allow the journal message to register
            Misc.Pause(500)

            # Check immediately after attempting to remove the trap
            if Journal.SearchByName(" appear to be trapped.", "System"):
                Misc.Pause(500)  # Additional short pause if untrapped
                break
            else:
                Misc.Pause(9500)  # Remaining part of the cooldown for trap removal

    else:
        Player.HeadMessage(54, "I need more lockpicks")
        Misc.Pause(500)



               
def IDweapons():
    Journal.Clear()

    # Find the chest containing the items to identify
    IDchest = Items.FindBySerial(0x4342B03E)

    while True:
        # Get the number of items in the chest and check if there are enough items to identify
        toID = Items.GetPropStringList(IDchest.Serial)
        toID = str(toID[5])
        toID = toID.split("items")[0]
        toID = int(toID)

        if toID < 5:
            Misc.SendMessage("Not enough arms to identify.")
            Misc.Pause(1000)
            return

        if toID > 5:
            Player.ChatSay("There are enough items to identify.")
            Misc.Pause(1000)
                # Open the chest once to start the identification process
            Items.UseItem(IDchest)
            Misc.Pause(1000)

            # Check if the player is overloaded
            if Player.Weight > 270:
                Player.ChatSay("I am overloaded to take arms.")
                Misc.Pause(1000)
                return

def IDweapons():
    Journal.Clear()

    # Find the chest containing the items to identify
    IDchest = Items.FindBySerial(0x4342B03E)

    # Open the chest once to start the identification process
    Items.UseItem(IDchest)
    Misc.Pause(1000)

    while True:
        # Get the number of items in the chest and check if there are enough items to identify
        toID = Items.GetPropStringList(IDchest.Serial)
        toID = str(toID[5])
        toID = toID.split("items")[0]
        toID = int(toID)

        if toID < 5:
            Misc.SendMessage("Not enough arms to identify.")
            Misc.Pause(500)
            return

        if toID > 5:
            Player.ChatSay("There are enough items to identify.")
            Misc.Pause(1000)

            # Check if the player is overloaded
            if Player.Weight > 270:
                Player.ChatSay("I am overloaded to take arms.")
                Misc.Pause(1000)
                return

        # Only proceed if the player is not overloaded and there are items in the chest
        while len(IDchest.Contains) > 0:
            # Check if weight exceeds 270 during the loop


            IDchest = Items.FindBySerial(0x4342B03E)  # Ensure we have the correct chest reference

            for item in IDchest.Contains:
                # Use the 'Item ID' skill to identify the item
                Player.UseSkill('Item ID')
                Target.WaitForTarget(2000, True)
                Target.TargetExecute(item)
                Misc.Pause(1200)

                # Retry identifying if the first attempt failed
                while Journal.SearchByType('You are not certain...', 'Regular'):
                    Journal.Clear()
                    Player.UseSkill('Item ID')
                    Target.WaitForTarget(2000, True)
                    Target.TargetExecute(item)
                    Misc.Pause(1200)

                # Move the item to the players backpack after successful identification
                Items.Move(item, Player.Backpack.Serial, 1)
                Misc.Pause(1000)
                if Player.Weight >= 270:
                    Player.ChatSay("I am overloaded.")
                    Misc.Pause(1000)
                    return  # Exit the function when overloaded

        # Exit the loop if chest is empty
        if len(IDchest.Contains) == 0:
            Player.ChatSay("Chest is empty.")
            return



                    
                
            
def sellArms():
    Journal.Clear() 
    if Player.Weight < 270:
        Misc.SendMessage("Not yet ready to sell arms.")
        Misc.Pause(1000)
        return
            
    SellAgent.Enable()
    worldSave()
    Player.ChatSay(75,"[recall Sell Arms")
    Misc.Pause(3000)
    Misc.WaitForContext(0x00136620, 10000) 
    Misc.ContextReply(0x00136620, 2) #Guild master sale
    Misc.Pause(1000)
    Player.ChatSay(26, 'I thank thee.')
    Misc.Pause(200)
    Player.EmoteAction("bow")
    Misc.WaitForContext(0x000012C1, 10000)
    Misc.ContextReply(0x000012C1, 2) #Arms sale
    Misc.Pause(2000)
    Player.ChatSay(75,"[recall Sell Hide")
    Misc.Pause(3000)
    Misc.WaitForContext(0x00026014, 10000)
    Misc.ContextReply(0x00026014, 2)
    Misc.Pause(1000)
    Player.ChatSay(26, 'Cheers, to you.')
    Misc.Pause(300)
    Player.EmoteAction("bow")
    Misc.Pause(1500)
    Player.ChatSay(75,"[recall Winter Lodge")
    Misc.Pause(2500)
    Player.PathFindTo(6782, 3899, 17)
    Misc.Pause(1500)
    gold_found = Items.FindByID(0x0EED,-1,Player.Backpack.Serial)
    if gold_found:
        Player.PathFindTo(6783, 3897, 17)
        Misc.Pause(1500)
        Items.Move(gold_found,tmapchest.Serial,-1)
        Misc.Pause(1000)
    Player.PathFindTo(6779, 3892, 17)
    while Player.DistanceTo(regchest) > 1:
        Misc.Pause(500)
    Items.UseItem(0x4043C469)
    Misc.Pause(500)
    pickcount = Items.BackpackCount(0x14FC,-1)
    picks = Items.FindByID(0x14FC,-1,regchest.Serial)
    if pickcount < 10:
        Items.Move(picks,Player.Backpack.Serial,10-pickcount)
        Misc.Pause(1000)
    Items.Move(Items.FindByID(0x0F86,-1,0x4043C469),Player.Backpack.Serial,3)
    Misc.Pause(1000)
    Items.Move(Items.FindByID(0x0F7B,-1,0x4043C469),Player.Backpack.Serial,3)
    Misc.Pause(1000)
    Items.Move(Items.FindByID(0x0F7A,-1,0x4043C469),Player.Backpack.Serial,3)
    Misc.Pause(1000)
    Journal.Clear()
    Items.UseItem(greenchest) 
    Misc.Pause(1000)
        
def unloadParagons():
    Misc.SendMessage("Checking for paragon chests.")
    Misc.Pause(1000)     

    for item in greenchest.Contains:
        if item.ItemID in pchest:
            Player.ChatSay("A paragon chest, how exciting!")
            Misc.Pause(500)
            Items.MoveOnGround(item,1,6780, 3891, 17)
            Misc.Pause(1000)
            pickChest(item)
            Items.UseItem(item)
            Misc.Pause(500)
            
            #find the paragon chest which is now on the ground
            paragonChest = Items.Filter()
            paragonChest.Enabled = True
            paragonChest.OnGround = True
            paragonChest.Movable = True
            paragonChest.RangeMax = 2
            paragonChest.Graphics = List[int]([0x0E41,0x09AB,0x0E7C,0x0E40])
            paragonChestList = Items.ApplyFilter(paragonChest)
            

            for c in paragonChestList:
                contents = list(c.Contains)
                #sort arms
                worldSave()
                for i in contents:
                    if i.ItemID in arms_ids:
                        Items.Move(i,IDchest,1)
                        Misc.Pause(1000)
                Misc.Pause(200)
                #sort regs
                worldSave()
                for i in contents:
                    if i.ItemID in regs:
                        Items.Move(i,regchest,-1)
                        Misc.Pause(1000)
                Misc.Pause(200)
                #sort relics
                worldSave()
                for i in contents:
                    if i.ItemID == 0x2AA2:
                        Items.Move(i,IDchest,1)
                        Misc.Pause(1000)
                Misc.Pause(200)
                #get gold/tmaps
                worldSave()
                for i in contents:
                    if i.ItemID in [0x0EED,0x14EC]:
                        Items.Move(i,Player.Backpack.Serial,-1)
                        Misc.Pause(1000)
                Misc.Pause(200)
                #find ID wands
                worldSave()
                for i in contents:
                    iprops = Items.GetPropStringList(i)
                    if "Identification" in str(iprops):
                        Player.ChatSay("ID wand!")
                        Misc.Pause(500)
                        Items.Move(i,greenchest,1)
                        Misc.Pause(1000)
                Misc.Pause(200)
                #sort gems/RDAs
                worldSave()
                Player.PathFindTo(6779, 3890, 17)
                Misc.Pause(1500)
                for i in contents:
                    if i. ItemID in gem_ids:
                        Items.Move(i,gemchest,1)
                        Misc.Pause(1000)
                Misc.Pause(200)
                #sort scrolls
                worldSave()
                for i in contents:
                    circleOneBag = 0x4BA61CBF
                    circleTwoBag = 0x4BA61CC0
                    circleThreeBag = 0x4BA61CBE
                    circleFourBag = 0x4BA61CC2
                    circleFiveBag = 0x4BA61CBD
                    circleSixBag = 0x4BA61CC3
                    circleSevenBag = 0x4BA61CC1
                    circleEightBag = 0x4BA61CBC
                    if i.ItemID in spellScrollIDs:
                        if Player.DistanceTo(scrollchest) > 2:
                            Player.PathFindTo(6779, 3890, 17)
                            Misc.Pause(1500)
                        Items.UseItem(scrollchest)
                        Misc.Pause(500)
                        scrollType = None
                        for scroll in spellScrolls:
                            if spellScrolls[ scroll ].itemID == i.ItemID:
                                scrollType = spellScrolls[ scroll ]
                                break
                        
                        spell = spells[ scrollType.name.replace( ' scroll', '' ) ]
                        if spell.circle == 1:
                            MoveItem( Items, Misc, i, circleOneBag )
                        elif spell.circle == 2:
                            MoveItem( Items, Misc, i, circleTwoBag )
                        elif spell.circle == 3:
                            MoveItem( Items, Misc, i, circleThreeBag )
                        elif spell.circle == 4:
                            MoveItem( Items, Misc, i, circleFourBag )
                        elif spell.circle == 5:
                            MoveItem( Items, Misc, i, circleFiveBag )
                        elif spell.circle == 6:
                            MoveItem( Items, Misc, i, circleSixBag )
                        elif spell.circle == 7:
                            MoveItem( Items, Misc, i, circleSevenBag )
                        elif spell.circle == 8:
                            MoveItem( Items, Misc, i, circleEightBag )
                
                Misc.Pause(500)
                Items.Move(c,Player.Backpack.Serial,1)
                Misc.Pause(1000)
                worldSave()
                for i in Player.Backpack.Contains:
                    if i.ItemID == 0x0EED:
                        if Player.DistanceTo(tmapchest) > 2:
                            Player.PathFindTo(6785, 3896, 17)
                            while Player.DistanceTo(tmapchest) > 1:
                                Misc.Pause(500)
                        Items.Move(i,tmapchest,-1)
                        Misc.Pause(1000)
                Misc.Pause(200)
                worldSave()
                for i in Player.Backpack.Contains:
                    if i.ItemID == 0x14EC:
                        if Player.DistanceTo(tmapchest) > 2:
                            Player.PathFindTo(6785, 3896, 17)
                            while Player.DistanceTo(tmapchest) > 1:
                                Misc.Pause(500)
                        while not Journal.SearchByName("The treasure is marked by the red pin.",""):
                            Items.UseItem(i)
                            Misc.Pause(1000)
                        Misc.SendMessage("Map decoded")
                        Misc.Pause(500)
                        Journal.Clear()
                        Items.UseItem(tmapchest)
                        Misc.Pause(500)
                        linelevel = Items.GetPropStringByIndex(i,1)
                        match = re.search(r'Level (\d+)', linelevel)
                        if match:
                            level = int(match.group(1))
                            if level in range(1, 7):
                                storage_serial = [0x40C2F465, 0x40C2F467, 0x40C2F466, 0x40C2F46A, 0x40C2F464, 0x40C2F469][level - 1]
                                Items.Move(i, storage_serial, 1)
                                Misc.Pause(1000)
                Misc.Pause(200)
                worldSave()
                for i in Player.Backpack.Contains:
                    if i.ItemID in pchest:
                        if Player.DistanceTo(trashbarrel) > 2:
                            Player.PathFindTo(6780, 3896, 17)
                            while Player.DistanceTo(trashbarrel) > 2:
                                Misc.Pause(500)
                        Misc.Pause(500)
                        Items.Move(i,trashbarrel,1)
                        Misc.Pause(1000)
                Player.PathFindTo(6779, 3892, 17)
                while Player.DistanceTo(IDchest) > 1:
                    Misc.Pause(500)
    
                Items.UseItem(greenchest)            
                Misc.Pause(1000)
      
            
def unloadSeaChests():
    seaChests = Items.Filter()
    seaChests.Enabled = True
    seaChests.OnGround = True
    seaChests.Movable = True
    seaChests.RangeMax = 9
    seaChests.Name = "treasure chest"
    seaChestList = Items.ApplyFilter(seaChests)
    
    if len(seaChestList) > 0:
        Player.ChatSay("Ah, we have sea treasure to unload!")
        Misc.Pause(5000)
        Player.PathFindTo(6780, 3896, 17)
        while Player.DistanceTo(trashbarrel) > 2:
            Misc.Pause(1000)
    else:
        Misc.SendMessage("No sea chests found.")
        Misc.Pause(1000)
        return
            
    Misc.Pause(1000)
    #chest drop location must be (6780,3897,17)
    for c in seaChestList:
        Journal.Clear()
        Items.MoveOnGround(c,1,6781, 3894, 24)
        Misc.Pause(1000)
        Player.PathFindTo(6779, 3892, 17)
        Misc.Pause(2500)
        Items.MoveOnGround(c,1,6780, 3891, 17)
        Misc.Pause(1000)
        pickChest(c)
        Items.UseItem(c)
        Misc.Pause(500)
        c = Items.FindBySerial(c.Serial)
        #sort arms
        worldSave()
        for i in c.Contains:
            if i.ItemID in arms_ids:
                Items.Move(i, IDchest, 1)
                Misc.Pause(1000)
        Misc.Pause(200)
        #sort regs
        worldSave()
        for i in c.Contains:
            if i.ItemID in regs:
                Items.Move(i,regchest,-1)
                Misc.Pause(1000)
        Misc.Pause(200)
        #sort nets
        worldSave()
        for i in c.Contains:
            if i.ItemID == 0x0DCA:
                Items.Move(i,greenchest,1,15,103)
                Misc.Pause(1000)
        Misc.Pause(200)
        #sort relics
        worldSave()
        for i in c.Contains:
            if i.ItemID == 0x2AA2:
                clean_name = clean_item_name(i.Name)  # Clean the item name
                Player.HeadMessage(64, "Ah, " + clean_name + " Relic!")  # Display the cleaned name
                Misc.Pause(500)
                Items.Move(i,greenchest,1)
                Misc.Pause(1000)
        Misc.Pause(200)
        #get gold/tmaps
        worldSave()
        for i in c.Contains:
            if i.ItemID in [0x0EED,0x14EC]:
                Items.Move(i,Player.Backpack.Serial,-1)
                Misc.Pause(1000)
        Misc.Pause(200)
        #find ID wands
        worldSave()
        for i in c.Contains:
            iprops = Items.GetPropStringList(i)
            if "Identification" in str(iprops):
                Player.ChatSay("ID wand!")
                Misc.Pause(500)
                Items.Move(i,greenchest,1)
                Misc.Pause(1000)
        Misc.Pause(200)
        #sort gems/RDAs
        worldSave()
        Player.PathFindTo(6779, 3890, 17)
        Misc.Pause(1500)
        for i in c.Contains:
            if i.ItemID in gem_ids:
                Items.Move(i,gemchest,1)
                Misc.Pause(1000)
        Misc.Pause(200)
        #sort scrolls
        worldSave()
        for i in c.Contains:
            circleOneBag = 0x4BA61CBF
            circleTwoBag = 0x4BA61CC0
            circleThreeBag = 0x4BA61CBE
            circleFourBag = 0x4BA61CC2
            circleFiveBag = 0x4BA61CBD
            circleSixBag = 0x4BA61CC3
            circleSevenBag = 0x4BA61CC1
            circleEightBag = 0x4BA61CBC
            if i.ItemID in spellScrollIDs:
                if Player.DistanceTo(scrollchest) > 2:
                    Player.PathFindTo(6779, 3890, 17)
                    Misc.Pause(1500)
                Items.UseItem(scrollchest)
                Misc.Pause(500)
                scrollType = None
                for scroll in spellScrolls:
                    if spellScrolls[ scroll ].itemID == i.ItemID:
                        scrollType = spellScrolls[ scroll ]
                        break
                
                spell = spells[ scrollType.name.replace( ' scroll', '' ) ]
                if spell.circle == 1:
                    MoveItem( Items, Misc, i, circleOneBag )
                elif spell.circle == 2:
                    MoveItem( Items, Misc, i, circleTwoBag )
                elif spell.circle == 3:
                    MoveItem( Items, Misc, i, circleThreeBag )
                elif spell.circle == 4:
                    MoveItem( Items, Misc, i, circleFourBag )
                elif spell.circle == 5:
                    MoveItem( Items, Misc, i, circleFiveBag )
                elif spell.circle == 6:
                    MoveItem( Items, Misc, i, circleSixBag )
                elif spell.circle == 7:
                    MoveItem( Items, Misc, i, circleSevenBag )
                elif spell.circle == 8:
                    MoveItem( Items, Misc, i, circleEightBag )
        
        Misc.Pause(500)
        Items.Move(c,Player.Backpack.Serial,1)
        Misc.Pause(1000)
        worldSave()
        for i in Player.Backpack.Contains:
            if i.ItemID == 0x0EED:
                if Player.DistanceTo(tmapchest) > 2:
                    Player.PathFindTo(6785, 3896, 17)
                    while Player.DistanceTo(tmapchest) > 1:
                        Misc.Pause(500)
                Items.Move(i,tmapchest,-1)
                Misc.Pause(1000)
        Misc.Pause(200)
        worldSave()
        for i in Player.Backpack.Contains:
            if i.ItemID == 0x14EC:
                if Player.DistanceTo(tmapchest) > 2:
                    Player.PathFindTo(6785, 3896, 17)
                    while Player.DistanceTo(tmapchest) > 1:
                        Misc.Pause(500)
                while not Journal.SearchByName("The treasure is marked by the red pin.",""):
                    Items.UseItem(i)
                    Misc.Pause(1000)
                Misc.SendMessage("Map decoded")
                Misc.Pause(500)
                Journal.Clear()

                Items.UseItem(tmapchest)
                Misc.Pause(500)
                linelevel = Items.GetPropStringByIndex(i,1)
                match = re.search(r'Level (\d+)', linelevel)
                if match:
                    level = int(match.group(1))
                    if level in range(1, 7):
                        storage_serial = [0x40C2F465, 0x40C2F467, 0x40C2F466, 0x40C2F46A, 0x40C2F464, 0x40C2F469][level - 1]
                        Items.Move(i, storage_serial, 1)
                        Misc.Pause(1000)
        Misc.Pause(200)
        if Player.DistanceTo(trashbarrel) > 2:
            Player.PathFindTo(6780, 3896, 17)
            while Player.DistanceTo(trashbarrel) > 2:
                Misc.Pause(500)
        Misc.Pause(500)
        Items.Move(c,trashbarrel,1)
        Misc.Pause(1000)       
    Misc.Pause(1000)
    worldSave()
    Player.PathFindTo(6779, 3892, 17)
    while Player.DistanceTo(IDchest) > 1:
        Misc.Pause(500)  
    Items.UseItem(greenchest)            
    Misc.Pause(1000)   
    
    
Items.UseItem(greenchest)
Misc.Pause(500)   
    
while True:    
    IDweapons()
    sellArms()
    unloadSeaChests() 
    unloadParagons()
   
                
                
            
            
        
    
    
