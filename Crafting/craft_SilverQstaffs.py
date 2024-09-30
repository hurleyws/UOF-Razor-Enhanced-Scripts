
# Wep crafter by MatsaMilla; Last edit: Matsamilla 5/27/22 - fixed tossing exceptionals
#
# Only have 1 type of wood on you at a time, it adjusts wood type automagically
#
# will restock same wood type from beetle
#
# crafts weps for fletching and carpentry, wep list below (comment out ones not crafting)
#
# Moves good weps to beetle *must be exceptional, trashes all non exceptional

################## SETUP SECTION ####################################

import clr
clr.AddReference('System.Speech')
from System.Speech.Synthesis import SpeechSynthesizer

spk = SpeechSynthesizer()

def say(text):
    spk.Speak(text)

# Will automatically ID items if toon has ItemID skill
useIDWands = True # true to use ID wands to ID magic items as
                  # you craft, otherwise move all to beetle
                  # Wands must be in backpack, not in bag in pack

# update with your beetles serial to move good weps to
beetle = 0x00121BEB

#inspect an item in the bag of your beetle, copy root container serial here. used to restock wood
beetleContainer = 0x417EFFFD

# turn to true if client has tool tips enabled, more reliable
toolTipsOn = True

#Settings
checkVanquishing = False
checkSlayerWithDamageMod = False
checkDeedability = False
trashAllItems = True  # Just looking for XP? Mark true.

# Set wep choice below (comment out others)

weapToCraft = 'comp'
#weapToCraft = 'bow'
#weapToCraft = 'xbow'
#weapToCraft = 'qstaff'
#weapToCraft = 'club'

################ Items to keep Setup Section #########################

# Anything in this list will be moved to beetle
keepProps = ['Vanquishing','Power']

# slayer props, take out the ones you dont want to keep, if you want. Will keep all slayers in list.
slayerProps = ['Silver']
# You can move slayers you do not want to keep down here, or just delete them. 
#'Dragon Slaying','Balron Damnation','Daemon Dismissal','Water Dissipation','Elemental Ban','Reptilian Death','Terathan','Exorcism','Repond','Fey','Water Dissipation'
# Just make sure they have a # in front so the code will ignore them.
#'Orc Slaying','Ogre Trashing','Earth Shatter','Arachnid', 'Blood Drinking','Lizardman Slaughter','Scorpion\'s Bane','Vacuum','Gargoyle\'s Foe','Troll Slaughter','Flame Dousing','Summer Wind','Spider\'s Death','Elemental Health','Ophidian','Snake\'s Bane'

#Any item in this list will be kept if paired with a durability or accuracy mod, does not count if on other side of #
wepDmgMods = ['Vanquishing','Power', 'Force','Ruin','Might'] # 'Ruin','Might'

######################### Do not touch anything below here# #######################################
from System.Collections.Generic import List
from System import Int32 as int
#disregaurd list below
wepDurabilityMods = ['Indestructable', 'Fortified', 'Massive', 'Substantial', 'Durable']
wepAccuracyMods = ['Supremely Accurate','Exceedingly Accurate','Eminently Accurate', 'Surpassingly Accurate', 'Accurate']

#the order of these is the order of how wood will be used
woodHues = [ 1193 , 1194 , 1151 , 1192 , 1191 ,2010 ] # heartwood, bloodwood, frostwood, yew, ash, oak
 
dragTime = 1200
fletchTool = 0x1022
saw = 0x1034
tink = 0x1EB8
wood = 0x1BD7
logs = 0x1BDD
ignot = 0x1BF2
comp = 0x26C2
xbow = 0x0F50
bow = 0x13B2
qstaff = 0x0E89
club = 0x13B4
noColor = 0x0000
self_pack = Player.Backpack.Serial
self = Player.Serial
rightHand = Player.CheckLayer('RightHand')
leftHand = Player.CheckLayer('LeftHand')
wands = [0xdf5,0xdf3,0xdf4,0xdf2]

# Will use ID Wand if skill Item ID below 75
if Player.GetRealSkillValue('Item ID') > 75:
    idItems = True
    useIDWands = False
elif useIDWands:
    idItems = True
else:
    idItems = False
    
# Use neraby trashcan
trashBarrelFilter = Items.Filter()
trashBarrelFilter.OnGround = 1
trashBarrelFilter.Movable = False
trashBarrelFilter.RangeMin = 0
trashBarrelFilter.RangeMax = 2
trashBarrelFilter.Graphics = List[int]( [ 0x0E77 ] )
trashBarrelFilter.Hues = List[int]( [ 0x03B2 ] )
trashcanhere = Items.ApplyFilter( trashBarrelFilter )

if trashcanhere:
    global trashcan
    for t in trashcanhere:
        trashcan = t
else:
    Misc.SendMessage('No trashcan nearby, stopping',33)
    Misc.Beep()
    Stop

# sets wep to craft
if weapToCraft == 'comp':
    wepType = 16
    craftWepID = comp
    carp = False
    fletch = True
    Player.HeadMessage(33, 'Crafting '+weapToCraft)
elif weapToCraft == 'xbow':
    wepType = 9
    craftWepID = xbow
    carp = False
    fletch = True
    Player.HeadMessage(33, 'Crafting '+weapToCraft)
elif weapToCraft == 'bow':
    wepType = 2
    craftWepID = bow
    carp = False
    fletch = True
elif weapToCraft == 'qstaff':
    wepType = 9
    craftWepID = qstaff
    carp = True
    fletch = False
elif weapToCraft == 'club':
    wepType = 30
    craftWepID = club
    carp = True
    fletch = False
    
def setWood():
    global woodHue
    Misc.Pause(500)
    # check for tools    
    if Items.BackpackCount(fletchTool, noColor) < 1:
        craftTools()
    # sets wood type
    packWood = FindItem(wood, Player.Backpack)
    packLogs = FindItem(logs, Player.Backpack)
    if packWood:
        if packWood.Hue == 0:
            woodGumpAction = 6
            woodType = 'Regular Wood'
        elif packWood.Hue == 2010:
            woodType = 'oak'
            woodGumpAction = 13
        elif packWood.Hue == 1191:
            woodType = 'ash'
            woodGumpAction = 20
        elif packWood.Hue == 1192:
            woodType = 'yew'
            woodGumpAction = 27
        elif packWood.Hue == 1193:
            woodType = 'heartwood'
            woodGumpAction = 34
        elif packWood.Hue == 1194:
            woodType = 'bloodwood'
            woodGumpAction = 41
        elif packWood.Hue == 1151:
            woodType = 'frostwood'
            woodGumpAction = 48
        woodHue = packWood.Hue
    elif packLogs:
        if packLogs.Hue == 0:
            woodGumpAction = 6
            woodType = 'Regular Wood'
        elif packLogs.Hue == 2010:
            woodType = 'oak'
            woodGumpAction = 13
        elif packLogs.Hue == 1191:
            woodType = 'ash'
            woodGumpAction = 20
        elif packLogs.Hue == 1192:
            woodType = 'yew'
            woodGumpAction = 27
        elif packLogs.Hue == 1193:
            woodType = 'heartwood'
            woodGumpAction = 34
        elif packLogs.Hue == 1194:
            woodType = 'bloodwood'
            woodGumpAction = 41
        elif packLogs.Hue == 1151:
            woodType = 'frostwood'
            woodGumpAction = 48
        woodHue = packLogs.Hue
    else:
        Misc.SendMessage('NO WOOD, Stopping!', 33)
        Misc.Beep()
        Stop
    Misc.SendMessage('Crafting with ' + woodType, 33)
    if fletch:
        currentFletch =  FindItem( fletchTool , Player.Backpack )
        if currentFletch:
            if Gumps.CurrentGump() != 949095101:
                Items.UseItem(currentFletch)
                Misc.Pause(dragTime)
            Gumps.WaitForGump(949095101, 2000)
            Gumps.SendAction(949095101, 7)
            Gumps.WaitForGump(949095101, 2000)
            Gumps.SendAction(949095101, woodGumpAction)
            Gumps.WaitForGump(949095101, 2000)
            Misc.Pause(dragTime)
        else:
            craftTools()
    elif carp:
        currentSaw =  FindItem( saw , Player.Backpack )
        if currentSaw:
            Items.UseItem(currentSaw)
            Misc.Pause(120)
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, 7)
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, woodGumpAction)
            Misc.Pause(dragTime)
        else:
            craftTools()
        
def moveToBeetle(item):
    if Player.Mount:
        Mobiles.UseMobile(self)
        Misc.Pause(dragTime)
    Items.Move(item, beetle, 1)
    Misc.Pause(dragTime)
    Mobiles.UseMobile(beetle)
    Misc.Pause(dragTime)
    
def restockWood( color ):
    global restocked
    if Player.Mount:
        Mobiles.UseMobile(self)
        Misc.Pause(dragTime)
        Mobiles.SingleClick(beetle)
        Misc.WaitForContext(beetle, 1500)
        if Player.Visible:
            Misc.ContextReply(beetle, 10)
        else:
            Misc.ContextReply(beetle, 0)
        Misc.Pause(dragTime)
        beetleLogs = Items.FindByID(logs, color, beetleContainer)
        beetleWood = Items.FindByID(wood, color, beetleContainer)
        if beetleLogs:
            Player.HeadMessage (66, 'Restocking')
            Items.Move(beetleLogs, self_pack, 1000)
            Misc.Pause(dragTime)
            restocked = True
        elif beetleWood:
            Player.HeadMessage (66, 'Restocking')
            Items.Move(beetleWood, self_pack, 1000)
            Misc.Pause(dragTime)
            restocked = True
        else:
            restocked = False
    
    if not Player.Mount:
        Mobiles.UseMobile(beetle)
        Misc.Pause(dragTime)

        
def trashItem(item):
    if trashcan:
        Items.Move(item, trashcan.Serial, 1)
        Misc.Pause(1000)
    else:
        Misc.SendMessage('No trashcan nearby, stopping',33)
        Misc.Beep()
        Stop
    
# Checks to see if you have enough materials, stopps if not.
def checkMats():
    worldSave()
    if fletch:
        # check for tools 
        if Items.BackpackCount(fletchTool, noColor) < 1:
            craftTools()
        # check for wood
        if weapToCraft == 'comp':
            if Items.BackpackCount(wood, -1) < 12 and Items.BackpackCount(logs, -1) < 12:
                restockWood( woodHue )
                if Items.BackpackCount(wood, -1) < 12 and Items.BackpackCount(logs, -1) < 12:
                    Misc.SendMessage('Out of Wood',33)
                    Gumps.CloseGump(949095101)
                    Misc.ScriptStop("craft_SilverQstaffs.py")
        else:
            if Items.BackpackCount(wood, -1) < 7 and Items.BackpackCount(logs, -1) < 7:
                restockWood (woodHue)
                if Items.BackpackCount(wood, -1) < 7 and Items.BackpackCount(logs, -1) < 7:
                    Misc.SendMessage('Out of Wood',33)
                    Gumps.CloseGump(949095101)
                    Misc.ScriptStop("craft_SilverQstaffs.py")
        
    elif carp:
        # check for tools 
        if Items.BackpackCount(saw, noColor) < 1:
            craftTools()
        # check for wood
        if Items.BackpackCount(wood, -1) < 6 and Items.BackpackCount(logs, -1) < 7:
                restockWood (woodHue)
                if Items.BackpackCount(wood, -1) < 6 and Items.BackpackCount(logs, -1) < 7:
                    Misc.SendMessage('Out of Wood',33)
                    Gumps.CloseGump(949095101)
                    Misc.Beep()
                    Misc.ScriptStop("craft_SilverQstaffs.py")
            
def craftTools():
    worldSave()
    currentTink = FindItem( tink , Player.Backpack )
    # stops script if not enough ignots to craft tools
    packIgnots = FindItem (ignot , Player.Backpack)
    if packIgnots == None or packIgnots.Amount < 10:
        Misc.SendMessage('Need more ignots for tools', 33)
        Misc.Beep()
        Stop
    # crafts tinker set if you only have 1
    if Items.BackpackCount(tink, noColor) < 2:
        Items.UseItem(currentTink.Serial)
        Misc.Pause(500)
        Gumps.SendAction(949095101, 8)
        Misc.Pause(500)
        Gumps.SendAction(949095101, 23)
        Misc.Pause(2500)
        Gumps.CloseGump(949095101)
    if fletch:
        # crafts fletch
        if Items.BackpackCount(fletchTool, noColor) < 1:
            Items.UseItem(currentTink.Serial)
            Misc.Pause(500)
            Gumps.SendAction(949095101, 8)
            Misc.Pause(500)
            Gumps.SendAction(949095101, 149)
            Misc.Pause(2500)
            Gumps.CloseGump(949095101)
            Misc.Pause(2000)
    elif carp:
        # crafts saw
        if Items.BackpackCount(saw, noColor) < 1:
            Items.UseItem(currentTink.Serial)
            Misc.Pause(500)
            Gumps.SendAction(949095101, 8)
            Misc.Pause(500)
            Gumps.SendAction(949095101, 51)
            Misc.Pause(2500)
            Gumps.CloseGump(949095101)
            Misc.Pause(2000)

def craftWep():
    worldSave()
    trashcanhere = Items.ApplyFilter( trashBarrelFilter )

    if trashcanhere:
        global trashcan
        for t in trashcanhere:
            trashcan = t
    else:
        Misc.SendMessage('No trashcan nearby, stopping',33)
        Misc.Beep()
        Stop
    # makes sure you stay mounted
    if not Player.Mount:
        Mobiles.UseMobile(beetle)
        Misc.Pause(dragTime)
    if fletch:
        # find fletch tools in bag
        currentFletch = FindItem( fletchTool , Player.Backpack )
        if currentFletch:
            checkMats()
            worldSave()
            Items.UseItem(currentFletch)
            Misc.Pause(500)
            Gumps.SendAction(949095101, 15)
            Misc.Pause(500)
            Gumps.SendAction(949095101, wepType)
            Misc.Pause(2000)

    elif carp:
        # find saw in bag, uses & crafts qstaff
        currentSaw = FindItem( saw , Player.Backpack )
        if currentSaw:
            worldSave()
            Items.UseItem(currentSaw)
            Misc.Pause(500)
            Gumps.SendAction(949095101, 22)
            Misc.Pause(500)
            Gumps.SendAction(949095101, wepType)
            Misc.Pause(2000)
        
    
# IDs items as you craft, if applicable
# otherwise moves to beetle    
def idItem(item):
    worldSave()
    Journal.Clear() 
    if idItems:
        idTarget()
        Target.WaitForTarget(1500)
        Target.TargetExecute(item)
        Misc.Pause(500)
        Player.HeadMessage(64,"Single click")
        Misc.Pause(500)
        Items.SingleClick(item)
        Misc.Pause(dragTime)
        if Journal.Search('You are not certain'):
            idItem(item)
        if Journal.Search('Exceptional'):
            if any(Journal.Search(keep) for keep in keepProps):
                #** moves to beetle if has property in keepProps **
                moveToBeetle(item)
            elif any(Journal.Search(keep) for keep in slayerProps):
                #** moves slayers to beetle **
                moveToBeetle(item) 
            elif any(Journal.Search(slash) for slash in wepDmgMods):
                if any(Journal.Search(sub) for sub in wepAccuracyMods):
                    #** moves deedable weps to beetle **
                    moveToBeetle(item)
                if any(Journal.Search(sub) for sub in wepDurabilityMods):
                    #** Good Stuff Move **
                    moveToBeetle(item)
                else:
                    #** Trash **
                    Misc.Pause(500)
                    trashItem(item)
            else:
                #** Trash **
                Misc.Pause(500)
                trashItem(item)
        else:
            #** Trash **
            Misc.Pause(500)
            trashItem(item)
    else:
        moveToBeetle(item)
        
def idItemToolTips(item, checkVanquishing=checkVanquishing, checkSlayerWithDamageMod=checkSlayerWithDamageMod, checkDeedability=checkDeedability, trashAllItems=trashAllItems):
    worldSave()
    if idItems:
        if trashAllItems:
            Player.HeadMessage(33, "Trashing all items")
            Misc.Pause(500)
            trashItem(item)
            return

        idTarget()
        Target.WaitForTarget(1500)
        Target.TargetExecute(item)
        Misc.Pause(dragTime)
        if Journal.Search('You are not certain'):
            idItem(item)
        Items.WaitForProps(item, 2000)
        props = Items.GetPropStringList(item)
        
        # Always trash non-exceptional items
        if 'Exceptional' not in props:
            Player.HeadMessage(33, "FAIL Exceptional Check")
            Misc.Pause(500)
            trashItem(item)
            return
        
        Player.HeadMessage(74, "PASS Exceptional check")
        Misc.Pause(500)  # Pause for 5 seconds
        
        # Check for Vanquishing
        if checkVanquishing and 'Vanquishing' in props:
            Player.HeadMessage(74, "PASS Vanquishing check")
            moveToBeetle(item)
            return
        Misc.Pause(500)  # Pause for 5 seconds
        
        # Check for Slayer with Damage Modifier
        
        matched_slayer = next((elim for elim in slayerProps if elim in props), None)
        if matched_slayer:
            Player.HeadMessage(74, f"PASS slayerProps check: {matched_slayer}")
            Misc.Pause(500)
            say("{matched_slayer}")
            Misc.Pause(500)
            if not checkSlayerWithDamageMod:
                moveToBeetle(item)
                return
            else:
                if any(elim in wepDmgMods for elim in props):
                    Player.HeadMessage(74, "PASS damage modifier check")
                    moveToBeetle(item)
                    return
                    
        Misc.Pause(500)  # Pause for 5 seconds
        
        # Check for Deedability
        if checkDeedability:
            Player.HeadMessage(45, "Checking for deedability")
            has_damage_mod = any(elim in wepDmgMods for elim in props)
            has_accuracy_mod = any(elim in wepAccuracyMods for elim in props)
            has_durability_mod = any(elim in wepDurabilityMods for elim in props)
            
            # Check if at least two of the three conditions are met
            deedable = sum([has_damage_mod, has_accuracy_mod, has_durability_mod]) >= 2

            if deedable:
                Player.HeadMessage(64, "PASS deedability check")
                moveToBeetle(item)
                return
            else:
                Player.HeadMessage(33, "FAIL deedability check")
        Misc.Pause(500)  # Pause for 5 seconds
        
        # If none of the above conditions are met, trash the item
        Player.HeadMessage(33, "FAIL properties check")
        Misc.Pause(500)
        trashItem(item)
    else:
        moveToBeetle(item)

# equips a wand, hopefully ID wand
def equipWand():
    global wandSerial
    if Player.CheckLayer('LeftHand') :
        Player.UnEquipItemByLayer('LeftHand')
        Misc.Pause(600)
    if not Player.CheckLayer('RightHand'):
        for i in Player.Backpack.Contains:
            if i.ItemID in wands:
                Items.WaitForProps(i, 500)
                if Items.GetPropValue(i, "Identification"):
                    Player.EquipItem(i.Serial)
                    Misc.Pause(600)
                    wandSerial = Player.GetItemOnLayer('RightHand').Serial
                    break
                else:
                    Player.ChatSay(33, "No Wands Found, No longer IDing")
                    Stop
    elif Player.GetItemOnLayer('RightHand').ItemID in wands:
        wandSerial = Player.GetItemOnLayer('RightHand').Serial
    else:
        Player.ChatSay(33, "No Wands Found, No longer IDing")
        Stop
        

# brings up ItemID Target, with wand or skill    
def idTarget():
    worldSave()
    if useIDWands:
        equipWand()
        Items.UseItem(wandSerial)
        Misc.Pause(200)
    else:
        Player.UseSkill('Item ID')
        Misc.Pause(dragTime)
    if not Target.HasTarget():
        idTarget()

# checks pack for wep you are crafting
# checks journal for special item, slayer or magic
# if special, ids item
def wepCheck():
    worldSave()
    craftedItem = FindItem( craftWepID , Player.Backpack )
    if toolTipsOn:
        if Journal.SearchByType('You have successfully crafted a slayer', 'System'):
            idItemToolTips(craftedItem)
        elif Journal.SearchByType('Your material and skill have added magical properties to this weapon.', 'System'):
            idItemToolTips(craftedItem)
        else:
            Misc.Pause(500)
            trashItem(craftedItem)
    else:
        Player.HeadMessage(64,"Non-tool tips")
        if Journal.SearchByType('You have successfully crafted a slayer', 'System'):
            idItem(craftedItem)
        elif Journal.SearchByType('Your material and skill have added magical properties to this weapon.', 'System'):
            idItem(craftedItem)
        else:
            Misc.Pause(500)
            trashItem(craftedItem)
    Journal.Clear()

# pauses during world save
def worldSave():
    if Journal.SearchByType('The world is saving, please wait.', 'System' ):
        Misc.SendMessage('Pausing for world save', 33)
        while not Journal.SearchByType('World save complete.', 'System'):
            Misc.Pause(1000)
        Misc.SendMessage('Continuing', 33)
        Journal.Clear()
        
def FindItem( itemID, container, color = -1, ignoreContainer = [] ):
    '''
    Searches through the container for the item IDs specified and returns the first one found
    Also searches through any subcontainers, which Misc.FindByID() does not
    '''

    ignoreColor = False
    if color == -1:
        ignoreColor = True

    if isinstance( itemID, int ):
        foundItem = next( ( item for item in container.Contains if ( item.ItemID == itemID and ( ignoreColor or item.Hue == color ) ) ), None )
    elif isinstance( itemID, list ):
        foundItem = next( ( item for item in container.Contains if ( item.ItemID in itemID and ( ignoreColor or item.Hue == color ) ) ), None )
    else:
        raise ValueError( 'Unknown argument type for itemID passed to FindItem().', itemID, container )

    if foundItem != None:
        return foundItem

    subcontainers = [ item for item in container.Contains if ( item.IsContainer and not item.Serial in ignoreContainer ) ]
    for subcontainer in subcontainers:
        foundItem = FindItem( itemID, subcontainer, color, ignoreContainer )
        if foundItem != None:
            return foundItem

setWood()
#restockWood (woodHue)     
while True:
    Journal.Clear() 
    worldSave()
    checkMats()           
    craftWep()
    while Items.BackpackCount(craftWepID, -1) > 0:
        wepCheck()