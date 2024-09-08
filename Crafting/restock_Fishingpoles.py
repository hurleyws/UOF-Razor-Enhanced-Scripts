Items. UseItem(0x43DE1F06)
Misc.Pause(500)
Items. UseItem(0x40680829)
Misc.Pause(500)

tinkertoolcount = Items.BackpackCount(0x1EB8,0x0000)
carptoolcount = Items.BackpackCount(0x1034,0x0000)
stockcontainer = Items.FindBySerial(0x43DE1F06)
ingots = Items.FindByID(0x1BF2,-1,0x4082BBB7)

    
def restock():
    #restock ingots
    if Items.ContainerCount(Player.Backpack.Serial, 0x1BF2, -1) < 30:
        for i in stockcontainer.Contains:
            if i.Hue == 0 and i.ItemID == 0x1BF2:
                Items.Move(i, Player.Backpack.Serial, 200)
                Misc.Pause(500)
    #restock tools
    if Items.BackpackCount(0x1EB8,0x0000) < 3: #tinker
        ingots = Items.FindByID(0x1BF2,-1,0x43DE1F06)
        tinkertoolcount = Items.BackpackCount(0x1EB8,0x0000)
        if ingots:
            Player.ChatSay("Ingots found")
            Misc.Pause(500)
        else:
            Player.ChatSay("Where are the ingots?")
            Misc.Pause(500)
            
        Items.Move(ingots,Player.Backpack.Serial,4*(3-tinkertoolcount))
        Misc.Pause(500)
        for i in range(3-tinkertoolcount):
            Items.UseItemByID(0x1EB8,0)
            Misc.Pause(500)
            Gumps.SendAction(949095101, 8) #tools
            Misc.Pause(500)
            Gumps.SendAction(949095101, 23) #tinker tools
            Misc.Pause(2000)
        Misc.Pause(500)
        Gumps.SendAction(949095101, 0) #close gump
        Misc.Pause(500)
        
    if Items.BackpackCount(0x1034,0x0000) < 3: #saw
        ingots = Items.FindByID(0x1BF2,0,stockcontainer.Serial)
        carptoolcount = Items.BackpackCount(0x1034,0x0000)
        Items.Move(ingots,Player.Backpack.Serial,4*(3-carptoolcount))
        Misc.Pause(500)
        for i in range(3-carptoolcount):
            Items.UseItemByID(0x1EB8,0)
            Misc.Pause(500)
            Gumps.SendAction(949095101, 8) #tools
            Misc.Pause(500)
            Gumps.SendAction(949095101, 51) #saw
            Misc.Pause(2000)
        Misc.Pause(500)
        Gumps.SendAction(949095101, 0) #close gump
        Misc.Pause(500)
        

Items.UseItem(stockcontainer) #open ingot box
Misc.Pause(500)
Items.UseItem(0x40680829) #tackle box
Misc.Pause(500)
restock()
Player.ChatSay(65,Items.ContainerCount(0x40680829,0x0DBF,0x0000,True)) #count poles
Misc.Pause(300)       
while Items.ContainerCount(0x40680829,0x0DBF,-1) < 81:
    Items.UseItemByID(0x1034) #use saw
    Misc.Pause(500)
    Gumps.SendAction(949095101, 22) #weapons
    Misc.Pause(500)
    Gumps.SendAction(949095101, 37) #fishing pole, lol
    Misc.Pause(2500)
    Items.Move(Items.FindByID(0x0DBF,-1,Player.Backpack.Serial),0x40680829,-1)
    Misc.Pause(500)
    Player.ChatSay(65,Items.ContainerCount(0x40680829,0x0DBF,0x0000,True))
    Misc.Pause(500)
    restock()
    
    #close gump & return extra ingots
Gumps.SendAction(949095101, 0)
Misc.Pause(500)
Items.Move(Items.FindByID(0x1BF2,-1,Player.Backpack.Serial),stockcontainer,-1)
Misc.Pause(500)

    