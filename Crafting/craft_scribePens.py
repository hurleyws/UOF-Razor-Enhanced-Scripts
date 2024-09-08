def craftPens():
    restock()
    while Items.ContainerCount(0x42E88440,0x0FBF,-1) < 50:
        Items.UseItemByID(0x1EB8,-1)
        Misc.Pause(500)
        Gumps.WaitForGump(949095101, 10000)
        Gumps.SendAction(949095101, 163)
        Misc.Pause(2500)
        for i in Player.Backpack.Contains:
            if i.ItemID == 0x0FBF:
                Items.Move(i,0x42E88440,1,19,13)
                Misc.Pause(1000)
        restock()

def restock():
    #restock ingots
    if Items.ContainerCount(Player.Backpack.Serial, 0x1BF2, -1) < 30:
        Misc.SendMessage("trigger")
        Items.UseItem(0x42E87E92)
        Misc.Pause(500)
        Misc.SendMessage("trigger")
        box = Items.FindBySerial(0x42E87E92)
        for i in box.Contains:
            if i.Hue == 0 and i.ItemID == 0x1BF2:
                Misc.SendMessage("trigger")
                Items.Move(i, Player.Backpack.Serial, 200)
                Misc.Pause(500)
    #restock tools
    if Items.BackpackCount(0x1EB8,0x0000) < 3:
        Items.UseItem(0x42E88440)
        Misc.Pause(500)
        ingots = Items.FindByID(0x1BF2,0,0x42E88440)
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
        
craftPens()

