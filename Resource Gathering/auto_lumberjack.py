# OG from AbelGoodwin https://github.com/hampgoodwin/razorenhancedscripts
# Modified by Matsamilla
#
# Last updated: 12/2/21

from System import Int32 as int
from System.Collections.Generic import List

if Player.GetRealSkillValue('Lumberjacking') < 40:
    Misc.SendMessage('No skill, stopping',33)
    Stop

#********************
# serial of your beetle, logs go here when full
beetle = 0x001523D4

# Attack nearest grey script name (must be exact)
autoFightMacroName = 'attack_nearest_Zastore.py'

# you want boards or logs?
logsToBoards = False

# Trees where there is no longer enough wood to be harvested will not be revisited until this much time has passed
treeCooldown = 1200000 # 1,200,000 ms is 20 minutes

# Want this script to alert you for humaniods?
alert = False
#********************

# Parameters
scanRadius = 15
treeStaticIDs = [ 0x0C95, 0x0C96, 0x0C99, 0x0C9B, 0x0C9C, 0x0C9D, 0x0C8A, 0x0CA6,
    0x0CA8, 0x0CAA, 0x0CAB, 0x0CC3, 0x0CC4, 0x0CC8, 0x0CC9, 0x0CCA, 0x0CCB,
    0x0CCC, 0x0CCD, 0x0CD0, 0x0CD3, 0x0CD6, 0x0CD8, 0x0CDA, 0x0CDD, 0x0CE0,
    0x0CE3, 0x0CE6, 0x0CF8, 0x0CFB, 0x0CFE, 0x0D01, 0x0D25, 0x0D27, 0x0D35,
    0x0D37, 0x0D38, 0x0D42, 0x0D43, 0x0D59, 0x0D70, 0x0D85, 0x0D94, 0x0D96,
    0x0D98, 0x0D9A, 0x0D9C, 0x0D9E, 0x0DA0, 0x0DA2, 0x0DA4, 0x0DA8, ]
    
if Misc.ShardName() == 'Ultima Forever':
    treeStaticIDsToRemove = [ 0x0C99, 0x0C9A, 0x0C9B, 0x0C9C, 0x0C9D, 0x0CA6, 0x0CC4, ]
    for treeStaticIDToRemove in treeStaticIDsToRemove:
        if treeStaticIDToRemove in treeStaticIDs:
            treeStaticIDs.remove( treeStaticIDToRemove )
    
axeSerial = None
EquipAxeDelay = 1000
TimeoutOnWaitAction = 4000
ChopDelay = 3500
runebookBank = 0x402AD4BD # Runebook for bank
runebookTrees = 0x43F88669 # Runebook for tree spots
recallPause = 4000
dragDelay = 2000
bones = [
    0x1B17, 0x1B18, 0x1B09, 0x1B0F, 0x1B0A, 0x1B0B, 0x1B0C, 0x1B0D,
    0x1B0E, 0x1B0F, 0x1B10, 0x1B15, 0x1B16, 0x1451, 0x1450, 0x144E,
    0x1452, 0x144F
]
logID = 0x1BDD
boardID = 0x1BD7
corpse_ID = 0x2006
hide_ID = 0x1081
rawhide_ID = 0x1079
gold_ID = 0x0EED
feathers_ID = 0x1BD1
wood_ID = 0x1BDD
meat_ID = 0x09F1
bone_ID = 0x0F7E
statue_ID = 0x25BF
lootList = [hide_ID, gold_ID, wood_ID, meat_ID,rawhide_ID,bone_ID,statue_ID]
lootList.extend(bones)
logBag = 0x401FA597 # Serial of log bag in bank
otherResourceBag = 0x40191C19 # Serial of other resource in bank
weightLimit = Player.MaxWeight - 10
bankX = 2051
bankY = 1343
axeList = [ 0x0F49, 0x13FB, 0x0F47, 0x1443, 0x0F45, 0x0F4B, 0x0F43 ]
rightHand = Player.CheckLayer( 'RightHand' )
leftHand = Player.CheckLayer( 'LeftHand' )


#sos_ID = 

loot_list  = [hide_ID, gold_ID,feathers_ID, wood_ID]

# System Variables
from System.Collections.Generic import List
from System import Byte
from math import sqrt
import clr
clr.AddReference('System.Speech')
from System.Speech.Synthesis import SpeechSynthesizer
tileinfo = List[Statics.TileInfo]
trees = []
treeCoords = None
blockCount = 0
lastRune = 2
onLoop = True

class Tree:
    x = None
    y = None
    z = None
    id = None
    
    def __init__ ( self, x, y, z, id ):
        self.x = x
        self.y = y
        self.z = z
        self.id = id


def RecallNextSpot():
    global lastRune

    Gumps.ResetGump()

    Misc.SendMessage('--> Recall to Spot', 77)

    Items.UseItem( runebookTrees )
    Gumps.WaitForGump( 1431013363, TimeoutOnWaitAction )
    Gumps.SendAction( 1431013363, lastRune )

    Misc.Pause( recallPause )

    lastRune = lastRune + 6
    if lastRune > 32:
        lastRune = 2

    EquipAxe()

def ScanStatic():
    global treenumber
    global trees
    Misc.SendMessage('--> Scan Tile Started', 77)
    minX = Player.Position.X - scanRadius
    maxX = Player.Position.X + scanRadius
    minY = Player.Position.Y - scanRadius
    maxY = Player.Position.Y + scanRadius

    x = minX
    y = minY

    while x <= maxX:
        while y <= maxY:
            staticsTileInfo = Statics.GetStaticsTileInfo( x, y, Player.Map )
            if staticsTileInfo.Count > 0:
                for tile in staticsTileInfo:
                    for staticid in treeStaticIDs:
                        if staticid == tile.StaticID and not Timer.Check( '%i,%i' % ( x, y ) ):
                            #Misc.SendMessage( '--> Tree X: %i - Y: %i - Z: %i' % ( minX, minY, tile.StaticZ ), 66 )
                            trees.Add( Tree( x, y, tile.StaticZ, tile.StaticID ) )
            y = y + 1
        y = minY
        x = x + 1

    trees = sorted( trees, key = lambda tree: sqrt( pow( ( tree.x - Player.Position.X ), 2 ) + pow( ( tree.y - Player.Position.Y ), 2 ) ) )
    Misc.SendMessage( '--> Total Trees: %i' % ( trees.Count ), 77 )


def RangeTree():
    playerX = Player.Position.X
    playerY = Player.Position.Y
    treeX = trees[ 0 ].x
    treeY = trees[ 0 ].y
    if ( ( treeX >= playerX - 1 and treeX <= playerX + 1 ) and ( treeY >= playerY - 1 and treeY <= playerY + 1 )  ):
        return True
    else:
        return False


def MoveToTree():
    global trees
    global treeCoords
    pathlock = 0
    Misc.SendMessage( '--> Moving to TreeSpot: %i, %i' % ( trees[ 0 ].x, trees[ 0 ].y ), 77 )
    Misc.Pause(200)
    Misc.Resync()
    worldSave()
    treeCoords = PathFinding.Route()
    treeCoords.MaxRetry = 5
    treeCoords.StopIfStuck = False
    treeCoords.X = trees[ 0 ].x
    treeCoords.Y = trees[ 0 ].y + 1
    #Items.Message(trees[0], 1, "Here")
    
    
    if PathFinding.Go( treeCoords ):
        Misc.SendMessage('First Try')
        Misc.Pause( 1000 )
    else:
        Misc.Resync()
        treeCoords.X = trees[ 0 ].x + 1
        treeCoords.Y = trees[ 0 ].y
        if PathFinding.Go( treeCoords ):
            Misc.SendMessage( 'Second Try' )
            Misc.Pause(1000)
        else:
            treeCoords.X = trees[ 0 ].x - 1
            treeCoords.Y = trees[ 0 ].y
            if PathFinding.Go( treeCoords ):
                Misc.SendMessage( 'Third Try' )
                Misc.Pause(1000)
            else:
                treeCoords.X = trees[ 0 ].x
                treeCoords.Y = trees[ 0 ].y - 1
                Misc.SendMessage( 'Final Try' )
                if PathFinding.Go( treeCoords ):
                    Misc.NoOperation()
                    Misc.Pause(1000)
                else:
                    return
                

    Misc.Resync()

    while not RangeTree():
        CheckEnemy()
        Misc.Pause( 500 )
        pathlock = pathlock + 1
        if pathlock > 350:
            Misc.Resync()
            treeCoords = PathFinding.Route()
            treeCoords.MaxRetry = 5
            treeCoords.StopIfStuck = False
            treeCoords.X = trees[ 0 ].x
            treeCoords.Y = trees[ 0 ].y + 1
            
            if PathFinding.Go( treeCoords ):
                Misc.SendMessage('First Try')
                Misc.Pause( 1000 )
            else:
                treeCoords.X = trees[ 0 ].x + 1
                treeCoords.Y = trees[ 0 ].y
                if PathFinding.Go( treeCoords ):
                    Misc.SendMessage( 'Second Try' )
                    Misc.Pause( 1000 )
                else:
                    treeCoords.X = trees[ 0 ].x - 1
                    treeCoords.Y = trees[ 0 ].y
                    if PathFinding.Go( treeCoords ):
                        Misc.SendMessage( 'Third Try' )
                        Misc.Pause( 1000 )
                    else:
                        treeCoords.X = trees[ 0 ].x
                        treeCoords.Y = trees[ 0 ].y - 1
                        Misc.SendMessage( 'Final Try' )
                        PathFinding.Go( treeCoords )
                        Misc.Pause( 1000 )

            pathlock = 0
            return

    Misc.SendMessage( '--> Reached TreeSpot: %i, %i' % ( trees[ 0 ].x, trees[ 0 ].y ), 77 )
    worldSave()

def EquipAxe():
    global axeSerial

    if not rightHand:
        for item in Player.Backpack.Contains:
            if item.ItemID in axeList:
                Player.EquipItem( item.Serial )
                Misc.Pause( 1000 )
                axeSerial = Player.GetItemOnLayer( 'LeftHand' ).Serial
    elif Player.GetItemOnLayer( 'LeftHand' ).ItemID in axeList:
        axeSerial = Player.GetItemOnLayer( 'LeftHand' ).Serial
    else:
        Player.HeadMessage( 35, 'You must have an axe to chop trees!' )
        Misc.Pause( 1000 )


def CutTree():
    global blockCount
    global trees
    if Target.HasTarget():
        Misc.SendMessage( '--> Detected block, canceling target!', 77 )
        Target.Cancel()
        Misc.Pause( 500 )

    if Player.Weight >= weightLimit:
        MoveToBeetle()
        MoveToTree()

    CheckEnemy()

    Journal.Clear()

    Items.UseItem( Player.GetItemOnLayer( 'LeftHand' ) )
    Target.WaitForTarget( TimeoutOnWaitAction , True )
    #EXPERIMENTAL PAUSE ADD
    Misc.Pause(1000)
    Target.TargetExecute( trees[ 0 ].x, trees[ 0 ].y, trees[ 0 ].z, trees[ 0 ].id )
    Timer.Create('chopTimer', 10000)
    while not ( Journal.SearchByType( 'You hack at the tree for a while, but fail to produce any useable wood.', 'System' ) or 
        Journal.SearchByType( 'You chop some', 'System' ) or 
            Journal.SearchByType( 'There\'s not enough wood here to harvest.', 'System' ) or
            Timer.Check('chopTimer') == False ):
        Misc.Pause( 500 )
        

    if Journal.SearchByType( 'There\'s not enough wood here to harvest.', 'System' ):
        Misc.SendMessage( '--> Tree change', 77 )
        Misc.Pause(500)
        Timer.Create( '%i,%i' % ( trees[ 0 ].x, trees[ 0 ].y ), treeCooldown )
    elif Journal.Search( 'That is too far away' ):
        blockCount = blockCount + 1
        Journal.Clear()
        if blockCount > 3:
            blockCount = 0
            Misc.SendMessage( '--> Possible block detected tree change', 77 )
            Misc.Pause(500)
            Timer.Create( '%i,%i' % ( trees[ 0 ].x, trees[ 0 ].y ), treeCooldown )
        else:
            CutTree()
    elif Journal.Search( 'bloodwood' ):
        Player.HeadMessage( 1194, 'BLOODWOOD!' )
        Timer.Create('chopTimer', 10000)
        CutTree()
    elif Journal.Search( 'heartwood' ):
        Player.HeadMessage( 1193, 'HEARTWOOD!' )
        Timer.Create('chopTimer', 10000)
        CutTree()
    elif Journal.Search( 'frostwood' ):
        Player.HeadMessage( 1151, 'FROSTWOOD!' )
        Timer.Create('chopTimer', 10000)
        CutTree()
    elif Timer.Check('chopTimer') == False:
        Misc.SendMessage( '--> Tree change', 77 )
        Timer.Create( '%i,%i' % ( trees[ 0 ].x, trees[ 0 ].y ), treeCooldown )
    else:
        CutTree()

def CheckEnemy():
    enemy = Target.GetTargetFromList( 'enemywar' )
    if enemy != None:
        Player.HeadMessage(64,"Ah! Snake!")
        Misc.ScriptRun( autoFightMacroName )
        while enemy != None:
            Timer.Create('Fight', 2500)
            Misc.Pause( 1000 )
            enemy = Mobiles.FindBySerial( enemy.Serial )
            if enemy:
                Misc.Pause(100)
                if Player.DistanceTo( enemy ) > 1:
                    enemyPosition = enemy.Position
                    enemyCoords = PathFinding.Route()
                    enemyCoords.MaxRetry = 5
                    enemyCoords.StopIfStuck = False
                    enemyCoords.X = enemyPosition.X
                    enemyCoords.Y = enemyPosition.Y - 1
                    PathFinding.Go( enemyCoords )
                
                    Misc.ScriptRun( autoFightMacroName )
                elif Timer.Check('Fight') == False:
                    Misc.ScriptRun( autoFightMacroName )
                    Timer.Create('Fight', 2500)
            enemy = Target.GetTargetFromList( 'enemywar' )

        corpseFilter = Items.Filter()
        corpseFilter.Movable = False
        corpseFilter.RangeMax = 2
        corpseFilter.Graphics = List[int]( [ 0x2006 ] )
        corpses = Items.ApplyFilter( corpseFilter )
        corpse = None

        Misc.Pause( dragDelay )

        for corpse in corpses:
            Misc.Pause(100)
            knife = Items.FindByID(0x0EC4,-1,Player.Backpack.Serial)
            if knife:
                Items.UseItem(knife)
                Misc.Pause(500)
                Target.TargetExecute(corpse)
                Misc.Pause(500)            
            for item in corpse.Contains:
                if item.ItemID in lootList:
                    Misc.Pause(100)
                    Items.Move( item.Serial, Player.Backpack.Serial, 0 )
                    Misc.Pause( dragDelay )
        leather = Items.FindByID(rawhide_ID,-1,Player.Backpack.Serial)
        if leather:
            Items.UseItemByID(0x0F9F,-1)
            Misc.Pause(500)
            Target.TargetExecute(leather)
            Misc.Pause(500)
        #chop bones
        for i in Player.Backpack.Contains:
            if i.ItemID in bones:
                Items.UseItemByID(0x0F9F,-1)
                Misc.Pause(500)
                Target.TargetExecute(i)
                Misc.Pause(500)
                
            
            
                    
        PathFinding.Go( treeCoords )


def GetNumberOfBoardsInBeetle():
    global beetle
    global boardID
    global dragDelay

    remount = False
    if not Mobiles.FindBySerial( beetle ):
        remount = True
        Mobiles.UseMobile( Player.Serial )
        Misc.Pause( dragDelay )

    numberOfBoards = 0
    for item in Mobiles.FindBySerial( beetle ).Backpack.Contains:
        if item.ItemID == boardID:
            numberOfBoards += item.Amount

    if remount:
        Mobiles.UseItem( beetle )
        Misc.Pause( dragDelay )

    return numberOfBoards


def GetNumberOfLogsInBeetle():
    global beetle
    global logID
    global dragDelay

    remount = False
    if not Mobiles.FindBySerial( beetle ):
        remount = True
        Mobiles.UseMobile( Player.Serial )
        Misc.Pause( dragDelay )

    numberOfLogs = 0
    for item in Mobiles.FindBySerial( beetle ).Backpack.Contains:
        if item.ItemID == logID:
            numberOfLogs += item.Amount

    if remount:
        Mobiles.UseItem( beetle )
        Misc.Pause( dragDelay )

    return numberOfLogs

def filterItem(id,range=2, movable=True):
    fil = Items.Filter()
    fil.Movable = movable
    fil.RangeMax = range
    fil.Graphics = List[int](id)
    list = Items.ApplyFilter(fil)

    return list

    
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
    
def MoveToBeetle():
    max_capacity = 15000
    
    # Chop logs into boards
    if logsToBoards:
        for item in Player.Backpack.Contains:
            if item.ItemID == logID:
                Items.UseItem( Player.GetItemOnLayer( 'LeftHand' ) )
                Target.WaitForTarget( 1500, False )
                Target.TargetExecute( item )
                Misc.Pause( dragDelay )

    if Player.Mount:
        Mobiles.UseMobile( Player.Serial )
        Misc.Pause( 500 )
        Misc.WaitForContext(0x001523D4, 10000)
        Misc.ContextReply(0x001523D4, 10)
        Misc.Pause(500)

    beetle = Mobiles.FindBySerial(0x001523D4)
    logs = Items.ContainerCount(beetle.Backpack.Serial, 0x1BDD, -1)
    logcount = int(logs)
    
    # Calculate the percentage of the beetles capacity
    percentage_filled = (logcount / max_capacity) * 100
    
    # Show the percentage filled as a player head message
    Player.HeadMessage(33, "{:.2f}% of beetle capacity filled".format(percentage_filled))
    Misc.Pause(500)
    
    if logcount > 13000:
        Player.HeadMessage(33, 'BEETLE FULL STOPPING')
        Misc.Pause(500)
        Misc.ScriptStop("auto_lumberjack.py")
        Misc.Pause(2000)
        return

    # Move boards to beetle, if they will fit in the beetle
    for item in Player.Backpack.Contains:
        if logsToBoards and item.ItemID == hide_ID:
            numberOfBoardsInBeetle = GetNumberOfBoardsInBeetle()
            if numberOfBoardsInBeetle + i.Amount < max_capacity:
                Items.Move(i, beetle, 0)
                Misc.Pause(dragDelay)
        elif not logsToBoards and (item.ItemID == logID or item.ItemID == hide_ID):
            numberOfLogsInBeetle = GetNumberOfLogsInBeetle()
            if numberOfLogsInBeetle + item.Amount < max_capacity:
                Items.Move(item, beetle, 0)
                Misc.Pause(dragDelay)

    groundItems = filterItem([hide_ID, logID])

    if groundItems:
        Player.HeadMessage(33, 'BEETLE FULL STOPPING')
        Misc.Pause(500)
        Misc.ScriptStop("auto_lumberjack.py")
        Misc.Pause(2000)
        
    meat = Items.FindByID(meat_ID, -1, Player.Backpack.Serial)
    if meat:
        Items.Move(meat, beetle, -1)
        Misc.Pause(1000)
    Misc.Pause(500)

    logs = Items.ContainerCount(beetle.Backpack.Serial, 0x1BDD, -1)
    logcount = int(logs)

    # Show the updated percentage after the move
    percentage_filled = (logcount / max_capacity) * 100
    Player.HeadMessage(33, "{:.2f}% of beetle capacity filled".format(percentage_filled))
    Misc.Pause(700)

    if not Player.Mount:
        Mobiles.UseMobile(beetle)
        Misc.Pause(dragDelay)

        
toonFilter = Mobiles.Filter()
toonFilter.Enabled = True
toonFilter.RangeMin = -1
toonFilter.RangeMax = -1
toonFilter.IsHuman = True 
toonFilter.Friend = False
toonFilter.Notorieties = List[Byte](bytes([1,2,3,4,5,6,7]))

invulFilter = Mobiles.Filter()
invulFilter.Enabled = True
invulFilter.RangeMin = -1
invulFilter.RangeMax = -1
invulFilter.Friend = False
invulFilter.Notorieties = List[Byte](bytes([7]))

        
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
    

Friend.ChangeList('lj')
Misc.Pause(500)
Misc.SendMessage('--> Start up Woods', 77)
Misc.Pause(500)
while onLoop:
    RecallNextSpot()
    ScanStatic()
    i = 0
    while trees.Count > 0:
        MoveToTree()
        CutTree()
        trees.pop( 0 )
        trees = sorted( trees, key = lambda tree: sqrt( pow( ( tree.x - Player.Position.X ), 2 ) + pow( ( tree.y - Player.Position.Y ), 2 ) ) )
    trees = []
    Misc.Pause(1000)
