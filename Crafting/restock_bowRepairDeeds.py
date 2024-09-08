def retool():
    #tinker tools
    if Items.BackpackCount(0x1EB8,-1) < 2:
        Items.UseItemByID(0x1EB8,-1)
        Misc.Pause(500)
        Gumps.WaitForGump(949095101, 10000)
        Gumps.SendAction(949095101, 23) #make tinker tools
        Misc.Pause(1500)
        for i in Player.Backpack.Contains:
            if i.ItemID == 0x1EB8:
                Items.Move(i,Player.Backpack.Serial,1,174,124)
                Misc.Pause(1000)
    #fletching tools
    if Items.BackpackCount(0x1022,-1) < 2:
        Items.UseItemByID(0x1EB8,-1)
        Misc.Pause(500)
        Gumps.WaitForGump(949095101, 10000)
        Gumps.SendAction(949095101, 149) #make fletching tools
        Misc.Pause(1500)
        for i in Player.Backpack.Contains:
            if i.ItemID == 0x1022:
                Items.Move(i,Player.Backpack.Serial,1,159,92)
                Misc.Pause(1000)
                
Items.UseItem(0x4253709D)
Misc.Pause(500)
Items.UseItem(0x432F3DDA)
Misc.Pause(500)
repairdeeds = Items.ContainerCount(0x432F3DDA,0x01bc,0x01bc)
scrolls = Items.FindByID(0x0EF3,-1,Player.Backpack.Serial)
while repairdeeds < 100:
    Items.UseItemByID(0x1022,-1)
    Misc.Pause(500)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, 42)
    Target.WaitForTarget(10000, False)
    if scrolls:
        Target.TargetExecute(scrolls)
        Misc.Pause(500)
    else:
        Player.HeadMessage(64,"Out of scrolls!")
        break
    deed = Items.FindByID(0x14F0,0x01bc,Player.Backpack.Serial)
    Items.Move(deed,0x432F3DDA,1)
    Misc.Pause(1000)
    repairdeeds = Items.ContainerCount(0x432F3DDA,0x14F0,0x01bc)
    Player.HeadMessage(64,str(repairdeeds)+" repair deeds available")
    Misc.Pause(1000)
    
    
    
    