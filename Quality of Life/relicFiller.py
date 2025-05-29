relic = Items.FindByID(0x2AA3,-1,Player.Backpack.Serial)

while True:
    Items.UseItem(relic)
    Misc.Pause(300)
    spiderFood = Items.FindByID(0x14F0,0x0481,Player.Backpack.Serial)
    if spiderFood:
        Target.TargetExecute(spiderFood)
        Misc.Pause(300)
    else:
        Player.ChatSay("No spider food!")
        Misc.Pause(500)
        break