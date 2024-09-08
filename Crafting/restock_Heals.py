plantA = 0x411A2010
plantB = 0x411A1E33
plantC = 0x411A2091
plantD = 0x411A1EF7
plantE = 0x411B5CD2


def resupply():
    if Items.BackpackCount(0x1EB8,-1) < 2: #tinker tools
        Items.UseItemByID(0x1EB8,-1)
        Misc.Pause(500)
        while Items.BackpackCount(0x1EB8,-1) < 2:
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, 23)
            Misc.Pause(2500)
        Journal.Clear()
        
    if Items.BackpackCount(0x0E9B,-1) < 2: #mortal & pestal
        Items.UseItemByID(0x1EB8,-1)
        Misc.Pause(500)
        while Items.BackpackCount(0x0E9B,-1) < 2:
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, 9)
            Misc.Pause(2500)
        Journal.Clear()
        
    if Items.BackpackCount(0x0F0E,-1) < 50: #garlic for cure
        Items.UseItem(0x4043C469)
        Misc.Pause(500)
        bottles = Items.FindByID(0x0F0E,-1,0x4043C469)
        Items.Move(bottles,Player.Backpack.Serial,50-Items.BackpackCount(0x0F0E,-1))
        Misc.Pause(1000)
        
    if Items.BackpackCount(0x0F84,-1) < 50: #bottles
        Items.UseItem(0x4043C469)
        Misc.Pause(500)
        garlic = Items.FindByID(0x0F84,-1,0x4043C469)
        Items.Move(garlic,Player.Backpack.Serial,50-Items.BackpackCount(0x0F84,-1))
        Misc.Pause(1000)
        
        
def makePotion():
    Items.UseItemByID(0x0E9B,-1)
    Misc.Pause(500)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, 43) #cure
    Misc.Pause(500)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, 16) #greater cure
    Misc.Pause(2000)
    if Items.BackpackCount(0x0F07,-1) >= 10:
        heal = Items.FindByID(0x0F07,-1,Player.Backpack.Serial)
        Items.Move(heal,0x4043C469,10,9,77)
        Misc.Pause(1000)
        Misc.SendMessage(Items.ContainerCount(0x4043C469,0x0F07,-1))  

Misc.SendMessage(Items.ContainerCount(0x4043C469,0x0F07,-1))  
    
while Items.ContainerCount(0x4043C469,0x0F07,-1) < 130:  
    resupply()   
    makePotion()
    