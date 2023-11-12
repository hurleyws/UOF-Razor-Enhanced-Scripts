from System.Collections.Generic import List
from System import Byte
from System import Int32 as int

filterExample = Mobiles.Filter()
filterExample.Enabled = True
filterExample.Name != "Watches"
filterExample.Name != "Salty McFishface"
filterExample.Name != "Hurlpea"
filterExample.Name != "Alyer Base"
filterExample.Notorieties = List[Byte](bytes([3,4,6]))

filterDeeps = Mobiles.Filter()
filterDeeps.Enabled = True
filterDeeps.Name != "Watches"
filterDeeps.Name != "Salty McFishface"
filterDeeps.Name != "Hurlpea"
filterDeeps.Name != "Alyer Base"
filterDeeps.Notorieties = List[Byte](bytes([3,4,6]))
filterDeeps.Name = "a deep water elemental"



def getpositionx():
   return Player.Position.X
def getpositiony():
   return Player.Position.Y

def FollowMobile( mobile, maxDistanceToMobile = 4):
    
    mobilePosition = mobile.Position
    playerPosition = Player.Position
    directionToWalk = ''
    if mobilePosition.X > playerPosition.X and mobilePosition.Y > playerPosition.Y:
        directionToWalk = 'back one'
    if mobilePosition.X < playerPosition.X and mobilePosition.Y > playerPosition.Y:
        directionToWalk = 'left one'
    if mobilePosition.X > playerPosition.X and mobilePosition.Y < playerPosition.Y:
        directionToWalk = 'right one'
    if mobilePosition.X < playerPosition.X and mobilePosition.Y < playerPosition.Y:
        directionToWalk = 'forward one'
    if mobilePosition.X > playerPosition.X and mobilePosition.Y == playerPosition.Y:
        directionToWalk = 'right one'
    if mobilePosition.X < playerPosition.X and mobilePosition.Y == playerPosition.Y:
        directionToWalk = 'left one'
    if mobilePosition.X == playerPosition.X and mobilePosition.Y > playerPosition.Y:
        directionToWalk = 'back one'
    if mobilePosition.X == playerPosition.X and mobilePosition.Y < playerPosition.Y:
        directionToWalk = 'forward one'

    playerPosition = Player.Position
    Misc.Pause(200)
    Player.ChatSay( directionToWalk )
    
def FindCorpse( corpse ):
    
    mobilePosition = corpse.Position
    playerPosition = Player.Position
    directionToWalk = ''
    if mobilePosition.X > playerPosition.X and mobilePosition.Y > playerPosition.Y:
        directionToWalk = 'back one'
    if mobilePosition.X < playerPosition.X and mobilePosition.Y > playerPosition.Y:
        directionToWalk = 'left one'
    if mobilePosition.X > playerPosition.X and mobilePosition.Y < playerPosition.Y:
        directionToWalk = 'right one'
    if mobilePosition.X < playerPosition.X and mobilePosition.Y < playerPosition.Y:
        directionToWalk = 'forward one'
    if mobilePosition.X > playerPosition.X and mobilePosition.Y == playerPosition.Y:
        directionToWalk = 'right one'
    if mobilePosition.X < playerPosition.X and mobilePosition.Y == playerPosition.Y:
        directionToWalk = 'left one'
    if mobilePosition.X == playerPosition.X and mobilePosition.Y > playerPosition.Y:
        directionToWalk = 'back one'
    if mobilePosition.X == playerPosition.X and mobilePosition.Y < playerPosition.Y:
        directionToWalk = 'forward one'

    playerPosition = Player.Position
    Misc.Pause(200)
    Player.ChatSay( directionToWalk )

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
    
Scavenger.Start()
Misc.Pause(500)
BandageHeal.Start()
Misc.Pause(500)
Misc.ScriptRun("PK Radar Crowsnest.py")
Misc.Pause(500)


    
while True:
    Misc.Pause(500)
    Items.UseItemByID( 0x0DCA )
    Misc.Pause(1000)
    Target.WaitForTarget( 2000, True )
    x = Player.Position.X - 3
    y = Player.Position.Y - 3
    statics = Statics.GetStaticsTileInfo( Player.Position.X+3, Player.Position.Y+3, 0 )
    if len( statics ) > 0:
        water = statics[ 0 ]
        Target.TargetExecute( x, y, water.StaticZ, water.StaticID )
        Misc.Pause(500)
        if Journal.SearchByType("You can only use this in deep water!","System"):
            Player.ChatSay(64,"We must go to deeper waters")
        Journal.Clear()
    else:
        Target.TargetExecute( x, y, -5, 0x0000 )
        Misc.Pause(500)
        if Journal.SearchByType("You can only use this in deep water!","System"):
            Player.ChatSay(64,"We must go to deeper waters")
            Journal.Clear()
        Journal.Clear()

    Misc.Pause(17500)

    while True:
        filterDeepsList = Mobiles.ApplyFilter(filterDeeps)
        
        if len(filterDeepsList) == 0:
            break

        for i in filterDeepsList:
            while Mobiles.FindBySerial(i.Serial):
                Player.Attack(i)
                Misc.Pause(500)
                if Player.DistanceTo(i) > 4:   
                    Misc.Pause( 300 )
                    Player.ChatSay("Following")
                    FollowMobile(i,4)
                    
    Misc.Pause(500)
    while True:    
        filterExampleList = Mobiles.ApplyFilter(filterExample)
        
        if len(filterExampleList) == 0:
            break

        for i in filterExampleList:

            while Mobiles.FindBySerial(i.Serial):
                Player.Attack(i)
                Misc.Pause(500)
                if Player.DistanceTo(i) > 4:   
                    Misc.Pause( 300 )
                    Player.ChatSay("Following")
                    FollowMobile(i,4)
                       
                    
                
                    
    Misc.Pause(500)
    itemFilter = Items.Filter()
    itemFilter.Enabled = True
    itemFilter.IsCorpse = True # optional
    itemFilter.OnGround = True # Questionably optional
    itemFilter.Movable = False # Questionably optional
    itemFilter.RangeMin = 3 # optional
    itemFilter.RangeMax = 15 # optoinal
    itemFilter.Graphics = List[int]([0x2006]) # optional, use item IDs
    itemsFilterList = Items.ApplyFilter(itemFilter) # returns list of items, manipulate list after this as you wish
    for i in itemsFilterList:
        while i.Position != Player.Position:
            FindCorpse(i)
            Misc.Pause(1000)
            itemsFilterList = Items.ApplyFilter(itemFilter)
    Misc.ScriptRun("autoLoot_fish.py")
    while Misc.ScriptStatus("autoLoot_fish.py"):
        Misc.Pause(500)
    Player.ChatSay(64,"Calm seas.")
    Misc.Pause(500)
   
#    if getpositionx() < 2272:
#        Player.ChatSay(64,"Yonder lies the shore!")
#        Misc.Pause(200)
#        Player.ChatSay("Right")
#        while getpositionx() < 2303:
#            Misc.Pause(500)
#        Player.ChatSay("Stop")
#        Misc.Pause(500)
#    if getpositiony() < 265:
#        Player.ChatSay(64,"Yonder lies the shore!")
#        Misc.Pause(200)
#        Player.ChatSay("Back")
#        while getpositiony() < 300:
#            Misc.Pause(500)
#        Player.ChatSay("Stop")
#        Misc.Pause(500)
#    Player.ChatSay(64,"We be in a fair berth")
#    
        
    Misc.Pause(500)
    if Player.Weight > Player.MaxWeight - 30 or Items.BackpackCount(0x0DCA,-1) < 2 or Items.BackpackCount(0x0F3F,-1) < 25:
        worldSave()
        Misc.ScriptStop("PK Radar.py")
        Misc.Pause(500)
        Player.ChatSay("[recall HVL")
        Misc.Pause(2500)
        Player.PathFindTo(2109, 369, 7)
        Misc.Pause(7000)
        Player.PathFindTo(2107, 361, 7)
        Misc.Pause(4000)
        Misc.ScriptRun("unload_netbooty.py")
        while Misc.ScriptStatus("unload_netbooty.py"):
            Misc.Pause(1000)
        Player.PathFindTo(2107, 369, 7)
        Misc.Pause(7000)
        gold = Items.FindByID(0x0EED,-1,Player.Backpack.Serial)
        if gold:
            Items.Move(gold,0x000118C9,-1)
            Misc.Pause(850)
        Misc.Pause(1000)
        Spells.Cast("Recall")
        Misc.Pause(2500)
        Target.TargetExecute(Items.FindByID(0x1F14,0x003d,Player.Backpack.Serial))   
        Misc.Pause(2000)
        Player.EquipItem(Items.FindByID(0x26C2,-1,Player.Backpack.Serial))
        Misc.Pause(500)

