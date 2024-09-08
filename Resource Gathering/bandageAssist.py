while True:
    Misc.Pause(500)
    if Player.Hits < 90 or Player.Poisoned:
        bandages = Items.FindByID(0x0E21,-1,Player.Backpack.Serial)
        Items.UseItem(bandages)
        Misc.Pause(500)
        Target.TargetExecute(Player.Serial)
        Misc.Pause(9000)
    