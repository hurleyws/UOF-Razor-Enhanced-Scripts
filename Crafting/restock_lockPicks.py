storebox = 0x42E88440
supplybox = 0x42E87E92



def reStock():
    ingotcount = Items.BackpackCount(0x1BF2,0x0000)
    toolcount = Items.BackpackCount(0x1EB8,0x0000)
    
    if ingotcount < 25:
        ingots = Items.FindByID(0x1BF2,0x0000,supplybox)
        Items.Move(ingots,Player.Backpack.Serial,200-ingotcount)
        Misc.Pause(1000)
        
    if toolcount < 2:
        Items.UseItemByID(0x1EB8,-1)
        Misc.Pause(500)
        Gumps.SendAction(949095101, 8)
        Misc.Pause(500)
        Gumps.SendAction(949095101, 23)
        Misc.Pause(2000)
        
        
def makePicks():
    Items.UseItemByID(0x1EB8,-1)
    Misc.Pause(500)
    Gumps.SendAction(949095101, 8)
    Misc.Pause(500)
    Gumps.SendAction(949095101, 128)
    Misc.Pause(2000)

def transferPicks():
    pickcount = Items.BackpackCount(0x14FC,-1)
    if pickcount > 99:
        pick = Items.FindByID(0x14FC,-1,Player.Backpack.Serial)
        Items.Move(pick,storebox,-1)
        Misc.Pause(1000)
        
        
Items.UseItem(storebox)
Misc.Pause(500)
Items.UseItem(supplybox)
Misc.Pause(500)

pickStock = Items.ContainerCount(storebox,0x14FC,-1)

while pickStock < 1000:
    reStock()
    makePicks()
    transferPicks()
    pickStock = Items.ContainerCount(storebox,0x14FC,-1)