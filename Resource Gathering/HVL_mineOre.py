#standard imports
import sys
from System.Collections.Generic import List

beetle = 0x002B1782 # watches = 0x000CDBE0
beetlepack = 0x467F1254 # watches = 0x423495E0
door = 0x402F1C41
ingotbox = Items.FindBySerial(0x40FA9D34)

##
ore = Items.FindByID(0x19B9,-1,Player.Backpack.Serial,True,True)

##types lists
forgesList = List[int]((0x197A, 0x197E, 0x19A2, 0x1982, 0x1992, 0x1996, 0x0FB1, 0x199A, 0x0FB1))
tinkerTools = [0x1EB8, 0x1EBC]
minerTools = [0x0F39, 0x0E86,0x0E85]
## msg stubs
smeltSuccess = 'You smelt the ore removing the impurities and put the metal in your backpack.'
smeltFail = 'You burn away the impurities but are left with less useable metal.'
pickaxe = Items.FindByID(0x0E86,0x0000, -1 ) #can I put minerTools here to search all of these?
gem_ids = [0x0F21,0x0F16,0x0F19,0x0F13,0x0F10,0x0F25,0x0F2D,0x0F15,0x0F26]


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
    
def stowegems():
    for i in Player.Backpack.Contains:
        if i.ItemID in gem_ids:
            Items.Move(i,0x42476FAA,-1)
            Misc.Pause(1000)

def toolCheck():
    axecount = Items.ContainerCount(Player.Backpack.Serial,0x0E86,-1)
    axecount = int(axecount)
    prospcount = Items.ContainerCount(Player.Backpack.Serial,0x0FB4,-1)
    prospcount = int(prospcount)
    if axecount < 1:
        Items.UseItem(ingotbox)
        Misc.Pause(500)
        for x in range (3-axecount):
            Items.Move(Items.FindByID(0x0E86,0x0000,ingotbox.Serial),Player.Backpack.Serial,1)
            Misc.Pause(1000)
    if prospcount < 3:
        Items.UseItem(ingotbox)
        Misc.Pause(500)
        for x in range (3-prospcount):
            Items.Move(Items.FindByID(0x0FB4,0x0000,ingotbox.Serial),Player.Backpack.Serial,3-prospcount)
            Misc.Pause(1000)

def smeltAll():
    Mobiles.UseMobile(Player.Serial) 
    Misc.Pause(1000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10) #bonded = 10, non-bonded = 9
    Misc.Pause(2000)
    ore = Items.FindByID(0x19B9,-1,beetlepack)
    while ore:
        Items.UseItem(ore)
        Misc.Pause(350)
        ore = Items.FindByID(0x19B9,-1,beetlepack)   
    ore = Items.FindByID(0x19B9,-1,Player.Backpack.Serial)
    while ore:
        Items.UseItem(ore)
        Misc.Pause(350)
        ore = Items.FindByID(0x19B9,-1,Player.Backpack.Serial)
    granite = Items.FindByID(0x1779,-1,beetlepack)
    while granite:
        Items.Move(granite,0x43545500,-1)
        Misc.Pause(1000)
        granite = Items.FindByID(0x1779,-1,beetlepack)  
    granite = Items.FindByID(0x1779,-1,Player.Backpack.Serial)
    while granite:
        Items.Move(granite,0x43545500,-1)
        Misc.Pause(1000)
        granite = Items.FindByID(0x1779,-1,Player.Backpack.Serial)    

def goInside():
    Player.PathFindTo(2117, 359, 7)
    Misc.Pause(4500)
    Player.PathFindTo(2120, 355, 7)
    Misc.Pause(1500)
    door = Items.FindBySerial(0x402F1C41)
    if door.ItemID == 0x067D:
        Items.UseItem(door)
        Misc.Pause(500)
    Player.PathFindTo(2127, 355, 7)
    Misc.Pause(2000)

def storeAll():
    Items.UseItem(ingotbox)
    Misc.Pause(500)
    ingots = Items.FindByID(0x1BF2,-1,Player.Backpack.Serial)
    while ingots:
        Items.Move(ingots,ingotbox.Serial,-1)
        Misc.Pause(1000)
        ingots = Items.FindByID(0x1BF2,-1,Player.Backpack.Serial)

def moveOre():
    ingotbox = Items.FindBySerial(0x40FA9D34)
    if ingotbox and Player.DistanceTo(ingotbox) < 2:
        Items.UseItem(ingotbox)
        Misc.Pause(1500)
    
    # Check if players weight exceeds 350
    if Player.Weight > 350:
        # Move all ore (ID: 0x19B9) to the beetle
        ore = Items.FindByID(0x19B9, -1, Player.Backpack.Serial, True, True)
        while ore:
            Items.Move(ore, beetle, -1)
            Misc.Pause(1000)
            ore = Items.FindByID(0x19B9, -1, Player.Backpack.Serial, True, True)
        
        # Move all granite (ID: 0x1779) to the beetle
        granite = Items.FindByID(0x1779, -1, Player.Backpack.Serial, True, True)
        while granite:
            Items.Move(granite, beetle, -1)
            Misc.Pause(1000)
            granite = Items.FindByID(0x1779, -1, Player.Backpack.Serial, True, True)
        
def mineAtLocation(*args):
    while (not Journal.SearchByName('There is no metal here to mine.', 'System') and
           not Journal.SearchByName('Target cannot be seen.', 'System') and
           not Journal.SearchByName('You cant mine there.', 'System') and
           Items.ContainerCount(beetlepack, 0x19B9, -1) < 130):
        worldSave()
        Items.UseItemByID(0x0E86, -1)
        Target.WaitForTarget( 1000, True )
        Target.TargetExecute(*args)
        Misc.Pause(1000)  # Pass all received arguments to TargetExecute
        moveOre()

while True:
    Journal.Clear()
    toolCheck()
    worldSave()
    Misc.Pause(200)
    
    ######### ROUTE 1 #########
      #1.1 - Dull Copper
    Player.HeadMessage(64,'Starting mining route 1.')
    Misc.Pause(500)
    if not Player.Mount:
        Mobiles.UseMobile(beetle)
        Misc.Pause(1000)
    Player.PathFindTo(2145,342,0)
    Misc.Pause(3000)
    #REFRESH EAST HOUSE
    Player.PathFindTo(2167,319,0)
    Misc.Pause(4000)
    Player.PathFindTo(2198,311,0)
    Misc.Pause(5000)
    Player.PathFindTo(2197,301,0)
    Misc.Pause(2000)
    Mobiles.UseMobile(Player.Serial) 
    Misc.Pause(1000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    worldSave()
    Journal.Clear()
    mineAtLocation(2198,300,0)

       #1.2 - Copper
    Player.PathFindTo(2189, 304, 0)
    Misc.Pause(2000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    worldSave()
    Journal.Clear()
    mineAtLocation(2189,303,0)
    
       #1.3 - Gold
    Player.PathFindTo(2174, 314, 0)
    Misc.Pause(5000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    worldSave()
    Journal.Clear()
    mineAtLocation(2174,313,0)
    
       #1.4 - Copper
    Player.PathFindTo(2168, 316, 0)
    Misc.Pause(2000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    Misc.Pause(500)
    worldSave()
    Journal.Clear()
    mineAtLocation(2169,316,0)
    
       #1.5 - Valorite
    Player.PathFindTo(2163, 316, 0)
    Misc.Pause(2000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    Items.UseItemByID(0x0FB4,-1)
    Misc.Pause(500)
    Target.TargetExecute(2163, 316, 0)
    Misc.Pause(500)
    worldSave()
    Journal.Clear()
    mineAtLocation(2163,316,0)   
    

     ####RUN HOME UNIQUE SEQUENCE  
    Mobiles.UseMobile(beetle)
    Misc.Pause(1000)
    Player.PathFindTo(2143,342,0)
    Misc.Pause(4000)
    Player.PathFindTo(2121,362,0)
    Misc.Pause(5000)

    goInside()
    smeltAll()
    storeAll()        
    toolCheck()   

    ######### ROUTE 2 #########    
        #2.1 - Shadow
    Player.HeadMessage(64,'Starting mining route 2.')
    Misc.Pause(500)
    Mobiles.UseMobile(beetle)
    Misc.Pause(1000)
    Player.PathFindTo(2146,320,0)
    Misc.Pause(6000)
    Player.PathFindTo(2149,302,0)
    Misc.Pause(3000)
    Mobiles.UseMobile(Player.Serial) 
    Misc.Pause(1000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    worldSave()
    Journal.Clear()
    mineAtLocation(2151,302,4)
    
       #2.2 - Dull Copper
    Player.PathFindTo(2152, 307, 0)
    Misc.Pause(2000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    Items.UseItemByID(0x0FB4,-1)
    Misc.Pause(500)
    Target.TargetExecute(2153,307,1)
    worldSave()
    Journal.Clear()
    mineAtLocation(2153,307,1)
    
       #2.3 - Shadow
    Player.PathFindTo(2154, 310, 0)
    Misc.Pause(2000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    worldSave()
    Journal.Clear()
    mineAtLocation(2154,311,6)

       #2.4 - Dull Copper
    Player.PathFindTo(2147, 310, 0)
    Misc.Pause(2000)
    Mobiles.UseMobile(Player.Serial) 
    Misc.Pause(1000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    Items.UseItemByID(0x0FB4,-1)
    Misc.Pause(500)
    Target.TargetExecute(2149,310,6)
    Misc.Pause(500)
    worldSave()
    Journal.Clear()
    mineAtLocation(2149,310,6)
    
       #2.5 - Dull Copper
    Player.PathFindTo(2147, 317, 0)
    Misc.Pause(2000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    Items.UseItemByID(0x0FB4,-1)
    Misc.Pause(500)
    Target.TargetExecute(2147,316,0)
    Misc.Pause(500)
    worldSave()
    Journal.Clear()
    mineAtLocation(2147,316,0)

     ####RUN HOME  
    Mobiles.UseMobile(beetle)
    Misc.Pause(1000)     
    Player.PathFindTo(2146,342,-2)
    Misc.Pause(4000)
    Player.PathFindTo(2134,353,0)
    Misc.Pause(3000)
    Player.PathFindTo(2121,362,0)
    Misc.Pause(3000)


    goInside()
    smeltAll()
    storeAll()
    toolCheck()   

        ######### ROUTE 3 #########
        #3.1 - Dull Copper
    Player.HeadMessage(64,'Starting mining route 3.')
    Misc.Pause(500)
    Mobiles.UseMobile(beetle)
    Misc.Pause(1000)
    Player.PathFindTo(2133,323,0)
    Misc.Pause(6000)
    Player.PathFindTo(2125,310,0)
    Misc.Pause(4000)
    Mobiles.UseMobile(Player.Serial) 
    Misc.Pause(1000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    Items.UseItemByID(0x0FB4,-1)
    Misc.Pause(500)
    Target.TargetExecute(2123,310,14)
    Misc.Pause(500)
    worldSave()
    Journal.Clear()
    mineAtLocation(2123,310,14) 
    
        #3.2 - Agapite
    Player.PathFindTo(2124, 316, 0)
    Misc.Pause(2000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    worldSave()
    Journal.Clear()
    mineAtLocation(2122,316,6)
    
        #3.3 - Shadow
    Player.PathFindTo(2124, 317, 0)
    Misc.Pause(2000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    worldSave()
    Journal.Clear()
    mineAtLocation(2123,315,0)

        #3.4  - Iron
    Player.PathFindTo(2125, 319, 0)
    Misc.Pause(4700)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    worldSave()
    Journal.Clear()
    mineAtLocation(2124,319,0)
    
        #3.5 - Dull Copper
    Player.PathFindTo(2136, 314, 0)
    Misc.Pause(6000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    Items.UseItemByID(0x0FB4,-1)
    Misc.Pause(500)
    Target.TargetExecute(2136,312,0)
    Misc.Pause(500)
    worldSave()
    Journal.Clear()
    mineAtLocation(2136,312,0)

        ##GO HOME SEQUENCE
    Mobiles.UseMobile(beetle)
    Misc.Pause(1000) 
    Player.PathFindTo(2146,336,0)
    Misc.Pause(4000)
    Player.PathFindTo(2123,361,0)
    Misc.Pause(6000)

    goInside()
    smeltAll() 
    storeAll()
    toolCheck()   
    
    ######### ROUTE 4 #########
        #4.1 - Dull Copper
    Player.HeadMessage(64,'Starting mining route 4.')
    Misc.Pause(500)
    Mobiles.UseMobile(beetle)
    Misc.Pause(1000)
    Player.PathFindTo(2125,325,0)
    Misc.Pause(5000)
    Mobiles.UseMobile(Player.Serial) 
    Misc.Pause(1000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    worldSave()
    Journal.Clear()
    mineAtLocation(2124,323,0)
    
        #4.2 - Dull Copper
    Player.PathFindTo(2124, 330, 0)
    Misc.Pause(2000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    Items.UseItemByID(0x0FB4,-1)
    Misc.Pause(500)
    Target.TargetExecute(2125,331,4)
    Misc.Pause(500)
    worldSave()
    Journal.Clear()
    mineAtLocation(2125,331,4)
    
        #4.3 - Copper
    Player.PathFindTo(2122, 329, 0)
    Misc.Pause(2000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    worldSave()
    Journal.Clear()
    mineAtLocation(2121,329,0)

       #4.4 - Dull Copper
    Player.PathFindTo(2116, 333, 0)
    Misc.Pause(2000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    worldSave()
    Journal.Clear()
    mineAtLocation(2117,332,8)
    
       #4.5 - Shadow
    Player.PathFindTo(2126, 337, 0)
    Misc.Pause(4000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    worldSave()
    Journal.Clear()
    mineAtLocation(2125, 337 ,0 ,6011)
    
        ##GO HOME
    Mobiles.UseMobile(beetle)
    Misc.Pause(1000)  
    Player.PathFindTo(2123,361,0)
    Misc.Pause(5000)

    goInside()
    smeltAll() 
    storeAll()
    toolCheck()   

    ######### ROUTE 5 #########    
        #5.1 - Bronze
    Player.HeadMessage(64,'Starting mining route 5.')
    Misc.Pause(500)
    Mobiles.UseMobile(beetle)
    Misc.Pause(1000)
    Player.PathFindTo(2102,375,0)
    Misc.Pause(5000)
    Player.PathFindTo(2082,361,0)
    Misc.Pause(5000)
    Mobiles.UseMobile(Player.Serial) 
    Misc.Pause(1000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    worldSave()
    Journal.Clear()
    mineAtLocation(2081, 362 ,0 ,6008)
    
        #5.2 - Dull Copper
    Player.PathFindTo(2082, 356, 0)
    Misc.Pause(4000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    worldSave()
    Journal.Clear()
    mineAtLocation(2081,356,0)
    
        #5.3 - Dull Copper
    Player.PathFindTo(2091, 346, 0)
    Misc.Pause(4000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    worldSave()
    Journal.Clear()
    mineAtLocation(2090,346,0)
    
        #5.4 - Copper
    Player.PathFindTo(2095, 343, 0)
    Misc.Pause(2000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    worldSave()
    Journal.Clear()
    mineAtLocation(2095,342,0)
    
        #5.5 - Shadow
    Player.PathFindTo(2108, 337, 0)
    Misc.Pause(2000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    worldSave()
    Journal.Clear()
    mineAtLocation(2106,337,7)

        ##GO HOME SEQUENCE
    Mobiles.UseMobile(beetle)
    Misc.Pause(1000)    
    Player.PathFindTo(2114,363,0)
    Misc.Pause(4000)

    goInside()
    smeltAll()
    storeAll()
    toolCheck()   

    Items.Move(Items.FindByID(0x09F1,-1,ingotbox.Serial),beetle,1) #feeding beetle
    Misc.Pause(1000)

    ######### ROUTE 6 #########    
       #6.1 - Shadow
    Player.HeadMessage(64,'Starting mining route 6.')
    Misc.Pause(500)
    Mobiles.UseMobile(beetle)
    Misc.Pause(1000)
    Player.PathFindTo(2106,375,0)
    Misc.Pause(4000)
    #REFRESH WEST HOUSE
    Player.PathFindTo(2071,393,0)
    Misc.Pause(6000)
    Player.PathFindTo(2050,389,0)
    Misc.Pause(4000)
    Mobiles.UseMobile(Player.Serial) 
    Misc.Pause(1000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    Items.UseItemByID(0x0FB4,-1)
    Misc.Pause(500)
    Target.TargetExecute(2050, 388 ,0 ,6003)
    Misc.Pause(500)
    worldSave()
    Journal.Clear()
    mineAtLocation(2050, 388 ,0 ,6003)
    
       #6.2 - Shadow
    Player.PathFindTo(2064,398,0)
    Misc.Pause(5000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    Items.UseItemByID(0x0FB4,-1)
    Misc.Pause(500)
    Target.TargetExecute(2063, 400 ,0 ,6012)
    Misc.Pause(500)
    worldSave()
    Journal.Clear()
    mineAtLocation(2063, 400 ,0 ,6012)
    
        #6.3 - Verite
    Player.PathFindTo(2069, 380, 0)
    Misc.Pause(4000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    Items.UseItemByID(0x0FB4,-1)
    Misc.Pause(500)
    Target.TargetExecute(2163,316,0)
    Misc.Pause(500)
    worldSave()
    Journal.Clear()
    mineAtLocation(2068, 380 ,0)
    
       #6.4 - Bronze
    Player.PathFindTo(2074, 372, 0)
    Misc.Pause(3000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    worldSave()
    Journal.Clear()
    mineAtLocation(2073, 373 ,0 ,6012)

       #6.5 - Dull Copper
    Player.PathFindTo(2073, 368, 0)
    Misc.Pause(3000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    worldSave()
    Journal.Clear()
    mineAtLocation(2072,368,0)
    
        #GO HOME SEQUENCE
    Mobiles.UseMobile(beetle)
    Misc.Pause(1000)    
    Player.PathFindTo(2097,361,0)
    Misc.Pause(4000)
    Player.PathFindTo(2113,362,0)
    Misc.Pause(3000)
    
    goInside()
    smeltAll()
    storeAll()
    toolCheck() 
  
    ######### ROUTE 7 #########
      #7.1 - Dull Copper
    Player.HeadMessage(64,'Starting mining route 7.')
    Misc.Pause(500)
    if not Player.Mount:
        Mobiles.UseMobile(beetle)
        Misc.Pause(1000)
    Player.PathFindTo(2145,338,0)
    Misc.Pause(3000)
    Player.PathFindTo(2167,319,0)
    Misc.Pause(4000)
    Player.PathFindTo(2198,311,0)
    Misc.Pause(5000)
    Player.PathFindTo(2202,301,0)
    Misc.Pause(2500)
    Mobiles.UseMobile(Player.Serial) 
    Misc.Pause(1000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    Items.UseItemByID(0x0FB4,-1)
    Misc.Pause(500)
    Target.TargetExecute(2204,301,4)
    Misc.Pause(500)
    worldSave()
    Journal.Clear()
    mineAtLocation(2204,301,4)

       #7.2 - Copper
    Player.PathFindTo(2202, 296, 0)
    Misc.Pause(2000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    Items.UseItemByID(0x0FB4,-1)
    Misc.Pause(500)
    Target.TargetExecute(2202,297,0,6003)
    Misc.Pause(500)
    worldSave()
    Journal.Clear()
    mineAtLocation(2202,297,0,6003)
    
       #7.3 - Shadow
    Player.PathFindTo(2205, 292, 0)
    Misc.Pause(2000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    Items.UseItemByID(0x0FB4,-1)
    Misc.Pause(500)
    Target.TargetExecute(2205,291,0)
    Misc.Pause(500)
    worldSave()
    Journal.Clear()
    mineAtLocation(2205,291,0)
    
       #7.4 - Dull Copper
    Player.PathFindTo(2207, 285, 0)
    Misc.Pause(2000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    Items.UseItemByID(0x0FB4,-1)
    Misc.Pause(500)
    Target.TargetExecute(2207,285,0)
    Misc.Pause(500)
    worldSave()
    Journal.Clear()
    mineAtLocation(2207,285,0)
    
       #7.5 - Iron
    Player.PathFindTo(2175, 300, 0)
    Misc.Pause(8000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    worldSave()
    Journal.Clear()
    mineAtLocation(2175,301,5)   
    
         ####RUN HOME UNIQUE SEQUENCE  
    Mobiles.UseMobile(beetle)
    Misc.Pause(1000)
    Player.PathFindTo(2163,316,0)
    Misc.Pause(5000)
    Player.PathFindTo(2143,342,0)
    Misc.Pause(4000)
    Player.PathFindTo(2121,362,0)
    Misc.Pause(5000)

    goInside()
    smeltAll()
    storeAll()        
    toolCheck()     

    ######### ROUTE 8 #########
      #8.1 - Iron
    Player.HeadMessage(64,'Starting mining route 8.')
    Misc.Pause(500)
    if not Player.Mount:
        Mobiles.UseMobile(beetle)
        Misc.Pause(1000)
    Player.PathFindTo(2103,338,7)
    Misc.Pause(7000)
    Mobiles.UseMobile(Player.Serial) 
    Misc.Pause(1000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    Misc.Pause(500)
    worldSave()
    Journal.Clear()
    mineAtLocation(2102, 338 ,12)

       #8.2 - Iron
    Player.PathFindTo(2099,341,7)
    Misc.Pause(3000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    Misc.Pause(500)
    worldSave()
    Journal.Clear()
    mineAtLocation(2097, 341 ,0)
    
       #8.3 - Iron
    Player.PathFindTo(2088,349,7)
    Misc.Pause(4000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    Misc.Pause(500)
    worldSave()
    Journal.Clear()
    mineAtLocation(2087, 350 ,0)
    
       #8.4 - Iron
    Player.PathFindTo(2083,353,7)
    Misc.Pause(3000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    Misc.Pause(500)
    worldSave()
    Journal.Clear()
    mineAtLocation(2082, 354 ,0)
    
       #8.5 - Iron
    Player.PathFindTo(2078,359,7)
    Misc.Pause(3000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    worldSave()
    Journal.Clear()
    mineAtLocation(2077, 360 ,0)

     ####GO HOME
    Mobiles.UseMobile(beetle)
    Misc.Pause(1000)
    Player.PathFindTo(2112, 359, 7)
    Misc.Pause(4500)

    goInside()
    smeltAll()
    storeAll()        
    toolCheck() 

    ######### ROUTE 9 #########
      #9.1 - Iron
    Player.HeadMessage(64,'Starting mining route 9.')
    Misc.Pause(500)
    if not Player.Mount:
        Mobiles.UseMobile(beetle)
        Misc.Pause(1000)
    Player.PathFindTo(2089,370,7)
    Misc.Pause(7000)
    Mobiles.UseMobile(Player.Serial) 
    Misc.Pause(1000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    Misc.Pause(500)
    worldSave()
    Journal.Clear()
    mineAtLocation(2088, 369 ,0 ,6012)

       #9.2 - Iron
    Player.PathFindTo(2099,363,7)
    Misc.Pause(5000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    Misc.Pause(500)
    worldSave()
    Journal.Clear()
    mineAtLocation(2100, 364 ,5)
    
       #9.3 - Iron
    Player.PathFindTo(2097,361,7)
    Misc.Pause(2500)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    Misc.Pause(500)
    worldSave()
    Journal.Clear()
    mineAtLocation(2096, 361 ,0 ,6012)

    
       #9.4 - Iron
    Player.PathFindTo(2108, 337, 7)
    Misc.Pause(6000)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    Misc.Pause(500)
    worldSave()
    Journal.Clear()
    mineAtLocation(2108, 336 ,12)
    
       #9.5 - Iron
    Player.PathFindTo(2111,336,7)
    Misc.Pause(2500)
    Misc.WaitForContext(beetle, 10000) 
    Misc.ContextReply(beetle, 10)
    worldSave()
    Journal.Clear()
    mineAtLocation(2112, 335 ,6)

     ####GO HOME
    Mobiles.UseMobile(beetle)
    Misc.Pause(1000)
    Player.PathFindTo(2111,363,7)
    Misc.Pause(4000)

    goInside()
    smeltAll()
    storeAll()        
    toolCheck() 
    stowegems()

