from Scripts.glossary.spells import spells
from Scripts.glossary.items.spellScrolls import spellScrolls
spellScrollIDs = [ spellScrolls[ scroll ].itemID for scroll in spellScrolls ]
from Scripts.utilities.items import MoveItem
import re

greenchest = Items.FindBySerial(0x412FB2AC)
trashbarrel = Items.FindBySerial(0x43DCB065)
regchest = Items.FindBySerial(0x4043C469)
IDchest = Items.FindBySerial(0x43DC9B86)
sellchest = Items.FindBySerial(0x43DCE16C)
keepchest = Items.FindBySerial(0x43DCE0C5)
gemchest = Items.FindBySerial(0x4189A2CC)
scrollchest = Items.FindBySerial(0x4043AE0E)
tmapchest = Items.FindBySerial(0x408E8DA8)
lockpick = Items.FindByID(0x14FC,-1,Player.Backpack.Serial)

regs = {
0x0F7A, 0x0F7B,0x0F86,0x0F8C,0x0F84,0x0F88,0x0F85,0x0F8D,
}

pchest = [0x0E41,0x09AB,0x0E7C,0x0E40]
gem_ids = [0x0F21,0x0F16,0x0F19,0x0F13,0x0F10,0x0F25,0x0F2D,0x0F15,0x0F26,0x0F21] #includes RDA frag 0x0F21
arms_ids = [
    0x0DF2, 0x0F49, 0x0F4D, 0x0F4D, 0x140E, 0x0F47, 0x0DF0, 0x13B2, 0x0F5E, 
    0x1B72, 0x1B73, 0x13F6, 0x13BB, 0x13BE, 0x13BF, 0x0EC3, 0x0EC3, 0x1408, 
    0x13B4, 0x0F50, 0x1441, 0x1441, 0x0F52, 0x0F4B, 0x0F4B, 0x0F45, 0x0F45, 
    0x13F8, 0x13F8, 0x13F8, 0x143E, 0x143D, 0x0F43, 0x1B76, 0x13FD, 0x140A, 
    0x13FF, 0x1B74, 0x1B79, 0x1B79, 0x1401, 0x13FB, 0x1C06, 0x1C0A, 0x1C0A, 
    0x1DB9, 0x13C6, 0x13C7, 0x13CB, 0x1C00, 0x1C08, 0x13CD, 0x13CC, 0x0F62, 
    0x0F61, 0x0F5C, 0x143B, 0x1B7B, 0x1B7B, 0x140C, 0x1F0B, 0x0E86, 0x0E87, 
    0x1C04, 0x1412, 0x1415, 0x1410, 0x1414, 0x1413, 0x1411, 0x0E89, 0x13EB, 
    0x13F0, 0x13EE, 0x13EC, 0x13B6, 0x13B6, 0x0E81, 0x1403, 0x1C02, 
    0x1C0C, 0x13D5, 0x13D5, 0x13D6, 0x13DA, 0x13DC, 0x13DB, 0x1443, 0x13B9, 
    0x13B0, 0x1405, 0x1439, 0x1407, 0x1B7A, 0x1C04, 0x0F52, 0x1544
]

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
            if Journal.SearchByName("That doesn\'t appear to be trapped.", "System"):
                Misc.Pause(500)  # Additional short pause if untrapped
                break
            else:
                Misc.Pause(9500)  # Remaining part of the cooldown for trap removal

    else:
        Player.HeadMessage(54, "I need more lockpicks")
        Misc.Pause(500)



               
def IDweapons():
    Journal.Clear()
    while True:
        #If there are weaponsarmor to identify, identify them
        toID = Items.GetPropStringList(IDchest.Serial) 
        toID = str(toID[5])
        toID = toID.split("items")
        toID = toID[0]
        toID = int(toID)
        if toID == 0:
            Misc.SendMessage("Weapons check")
            Misc.Pause(500)
            break
        if toID > 0:
            Player.ChatSay("There are items to identify")
            Misc.Pause(500)
            Items.UseItem(IDchest)
            Misc.Pause(500)
            for item in IDchest.Contains:
                worldSave()
                Player.UseSkill('Item ID')
                Target.WaitForTarget( 2000, True )
                Target.TargetExecute( item )
                Misc.Pause(1200)
                
                while Journal.SearchByType( 'You are not certain...', 'Regular' ):
                    # Failed to ID the item, keep trying until we succeed
                    Journal.Clear()

                    Player.UseSkill( 'Item ID' )
                    Target.WaitForTarget( 2000, True )
                    Target.TargetExecute( item )

                    # Wait for the skill cooldown
                    Misc.Pause( 1200 )
                    
                propList = Items.GetPropStringList(item)
                if "Vanquishing" and "Supremely" in str(propList):
                    Player.HeadMessage(64,"Vanq +25, KEEPER!")
                    Misc.Pause(500)
                    Items.Move(item,keepchest.Serial,1)
                    Misc.Pause(1000)
                elif "Identification" in str(propList):
                    Player.HeadMessage(64,"ID Wand, KEEPER!")
                    Misc.Pause(500)
                    Items.Move(item,keepchest.Serial,1)
                    Misc.Pause(1000)

                else:
                    Items.Move(item,sellchest.Serial,1)
                    Misc.Pause(1000)
                    
                if Journal.SearchByType("That container cannot hold more items.","System"):
                    Player.ChatSay("Sell chest is full.")
                    Misc.Pause(500)
                    Items.UseItem(IDchest)
                    Misc.Pause(500)
                    break
            
            Items.UseItem(IDchest)
            Misc.Pause(500)        
    
    Misc.Pause(1000)
            
def sellArms():
    Journal.Clear()  
    while True:
        #If there are enough weapons to sell, sell them
        toSell = Items.GetPropStringList(sellchest.Serial) 
        toSell = str(toSell[5])
        toSell = toSell.split("items")
        toSell = toSell[0]
        toSell = int(toSell)   
        if toSell < 50:
            Misc.SendMessage("Sell weapons check")
            Misc.Pause(500)
            break
        Items.UseItem(sellchest)
        Misc.Pause(500)
        for item in sellchest.Contains:
            Items.Move(item,Player.Backpack.Serial,1)
            Misc.Pause(1000)
            if Player.Weight > 310:
                break
                
        SellAgent.Enable()
        worldSave()
        Player.ChatSay(75,"[recall Sell Arms")
        Misc.Pause(3000)
        Misc.WaitForContext(0x0013C3E0, 10000) 
        Misc.ContextReply(0x0013C3E0, 2) #Guild master sale
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
        Player.ChatSay(26, 'Ive done unspeakable things for this gold.')
        Journal.Clear()
        
    Misc.Pause(1000)
        
def unloadParagons():
    Misc.SendMessage("Paragon check")
    Misc.Pause(500)
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
            paragonChest.Name = "metal chest"
            paragonChestList = Items.ApplyFilter(paragonChest)
            

            for c in paragonChestList:
                contents = list(c.Contains)
                #sort arms
                for i in contents:
                    if i.ItemID in arms_ids:
                        Items.Move(i,IDchest,1)
                        Misc.Pause(1000)
                Misc.Pause(200)
                #sort regs
                for i in contents:
                    if i.ItemID in regs:
                        Items.Move(i,regchest,-1)
                        Misc.Pause(1000)
                Misc.Pause(200)
                #sort relics
                for i in contents:
                    if i.ItemID == 0x2AA2:
                        Items.Move(i,keepchest,1)
                        Misc.Pause(1000)
                Misc.Pause(200)
                #get gold/tmaps
                for i in contents:
                    if i.ItemID in [0x0EED,0x14EC]:
                        Items.Move(i,Player.Backpack.Serial,-1)
                        Misc.Pause(1000)
                Misc.Pause(200)
                #find ID wands
                for i in contents:
                    iprops = Items.GetPropStringList(i)
                    if "Identification" in str(iprops):
                        Player.ChatSay("ID wand!")
                        Misc.Pause(500)
                        Items.Move(i,keepchest,1)
                        Misc.Pause(1000)
                Misc.Pause(200)
                #sort gems/RDAs
                for i in contents:
                    if i. ItemID in gem_ids:
                        Player.PathFindTo(6779, 3890, 17)
                        Misc.Pause(1500)
                        Items.Move(i,gemchest,1)
                        Misc.Pause(1000)
                Misc.Pause(200)
                #sort scrolls
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
                for i in Player.Backpack.Contains:
                    if i.ItemID == 0x0EED:
                        if Player.DistanceTo(tmapchest) > 2:
                            Player.PathFindTo(6785, 3896, 17)
                            while Player.DistanceTo(tmapchest) > 1:
                                Misc.Pause(500)
                        Items.Move(i,tmapchest,-1)
                        Misc.Pause(1000)
                Misc.Pause(200)
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
                for i in Player.Backpack.Contains:
                    if i.ItemID in pchest:
                        if Player.DistanceTo(trashbarrel) > 2:
                            Player.PathFindTo(6780, 3897, 17)
                            while Player.DistanceTo(trashbarrel) > 1:
                                Misc.Pause(500)
                        Misc.Pause(500)
                        Items.Move(i,trashbarrel,1)
                        Misc.Pause(1000)
                Player.PathFindTo(6779, 3892, 17)
                while Player.DistanceTo(IDchest) > 1:
                    Misc.Pause(500)
    Misc.Pause(1000)                    
            
def unloadSeaChests():
    Misc.SendMessage("Sea chest check")
    Misc.Pause(500)
    seaChests = Items.Filter()
    seaChests.Enabled = True
    seaChests.OnGround = True
    seaChests.Movable = True
    seaChests.RangeMax = 9
    seaChests.Name = "treasure chest"
    seaChestList = Items.ApplyFilter(seaChests)
    
    if len(seaChestList) > 0:
        Player.ChatSay("Ah, we have sea treasure to unload!")
        Misc.Pause(500)
        Player.PathFindTo(6781, 3896, 17)
        while Player.DistanceTo(trashbarrel) > 2:
            Misc.Pause(1000)
            
    Misc.Pause(1000)
    #chest drop location must be (6780,3897,17)
    for c in seaChestList:
        Journal.Clear()
        Items.MoveOnGround(c,-1,Player.Position.X,Player.Position.Y-2,Player.Position.Z)
        Misc.Pause(1000)
        Player.PathFindTo(6781, 3892, 17)
        Misc.Pause(2500)
        Items.MoveOnGround(c,-1,Player.Position.X-1,Player.Position.Y-1,Player.Position.Z)
        Misc.Pause(1000)
        Player.PathFindTo(6779, 3892, 17)
        Misc.Pause(1000)
        pickChest(c)
        Items.UseItem(c)
        Misc.Pause(500)
        seaChestList = Items.ApplyFilter(seaChests)
        for c in seaChestList:
            contents = list(c.Contains)
            #sort arms
            Misc.SendMessage("Checking for arms")
            for i in contents:
                if i.ItemID in arms_ids:
                    Items.Move(i, IDchest, 1)
                    Misc.Pause(1000)
            Misc.Pause(200)
            #sort regs
            for i in contents:
                if i.ItemID in regs:
                    Items.Move(i,regchest,-1)
                    Misc.Pause(1000)
            Misc.Pause(200)
            #sort relics
            for i in contents:
                if i.ItemID == 0x2AA2:
                    Items.Move(i,keepchest,1)
                    Misc.Pause(1000)
            Misc.Pause(200)
            #get gold/tmaps
            for i in contents:
                if i.ItemID in [0x0EED,0x14EC]:
                    Items.Move(i,Player.Backpack.Serial,-1)
                    Misc.Pause(1000)
            Misc.Pause(200)
            #find ID wands
            for i in contents:
                iprops = Items.GetPropStringList(i)
                if "Identification" in str(iprops):
                    Player.ChatSay("ID wand!")
                    Misc.Pause(500)
                    Items.Move(i,keepchest,1)
                    Misc.Pause(1000)
            Misc.Pause(200)
            #sort gems/RDAs
            for i in contents:
                if i. ItemID in gem_ids:
                    Player.PathFindTo(6779, 3890, 17)
                    Misc.Pause(1500)
                    Items.Move(i,gemchest,1)
                    Misc.Pause(1000)
            Misc.Pause(200)
            #sort scrolls
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
            for i in Player.Backpack.Contains:
                if i.ItemID == 0x0EED:
                    if Player.DistanceTo(tmapchest) > 2:
                        Player.PathFindTo(6785, 3896, 17)
                        while Player.DistanceTo(tmapchest) > 1:
                            Misc.Pause(500)
                    Items.Move(i,tmapchest,-1)
                    Misc.Pause(1000)
            Misc.Pause(200)
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
            for i in Player.Backpack.Contains:
                if i.ItemID in pchest:
                    if Player.DistanceTo(trashbarrel) > 2:
                        Player.PathFindTo(6780, 3897, 17)
                        while Player.DistanceTo(trashbarrel) > 1:
                            Misc.Pause(500)
                    Misc.Pause(500)
                    Items.Move(i,trashbarrel,1)
                    Misc.Pause(1000)
            Player.PathFindTo(6779, 3892, 17)
            while Player.DistanceTo(IDchest) > 1:
                Misc.Pause(500)
    Misc.Pause(1000)      

        
    
while True:
    Items.UseItem(greenchest)
    Misc.Pause(500)        
    IDweapons()
    sellArms()
    unloadParagons()
    unloadSeaChests()    
                
                
            
            
        
    
    
