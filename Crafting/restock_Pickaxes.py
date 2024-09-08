toolcount = Items.BackpackCount(0x1EB8,0x0000)
ingots = Items.FindByID(0x1BF2,0,0x40826F73)

    
def restock():
    #restock ingots
    if Items.ContainerCount(Player.Backpack.Serial, 0x1BF2, -1) < 30:
        for i in Items.FindBySerial(0x40826F73).Contains:
            if i.Hue == 0 and i.ItemID == 0x1BF2:
                Items.Move(i, Player.Backpack.Serial, 200)
                Misc.Pause(500)
    #restock tools
    if Items.BackpackCount(0x1EB8,0x0000) < 3:
        ingots = Items.FindByID(0x1BF2,0,0x40826F73)
        toolcount = Items.BackpackCount(0x1EB8,0x0000)
        Items.Move(ingots,Player.Backpack.Serial,4*(3-toolcount))
        Misc.Pause(500)
        for i in range(3-toolcount):
            Items.UseItemByID(0x1EB8,0)
            Misc.Pause(500)
            Gumps.SendAction(949095101, 23)
            Misc.Pause(2000)
        Misc.Pause(500)
        Gumps.SendAction(949095101, 0)
        Misc.Pause(500)

Items.UseItem(0x40826F73) #open ingot box
Misc.Pause(500)
restock()
Player.ChatSay(65,str(Items.ContainerCount(0x40826F73,0x0E86,0x0000,True))+" pickaxes")
Misc.Pause(300)       
while Items.ContainerCount(0x40826F73,0x0E86,-1) < 81:
    Items.UseItemByID(0x1EB8)
    Misc.Pause(500)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, 8)
    Misc.Pause(200)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, 121)
    Misc.Pause(2000)
    Items.Move(Items.FindByID(0x0E86,-1,Player.Backpack.Serial),0x40826F73,-1,9, 41)
    Misc.Pause(300)
    Player.ChatSay(65,str(Items.ContainerCount(0x40826F73,0x0E86,0x0000,True))+" pickaxes")
    Misc.Pause(300)
    restock()
Player.ChatSay(65,str(Items.ContainerCount(0x40826F73,0x0FB4,0x0000,True))+" prospector tools")
Misc.Pause(500)    
    #close gump & return extra ingots
Gumps.SendAction(949095101, 0)
Misc.Pause(500)
Items.Move(Items.FindByID(0x1BF2,-1,Player.Backpack.Serial),0x40826F73,-1)
Misc.Pause(500)

    