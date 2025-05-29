

while True:
    granite = Items.FindByID(0x1779,-1,0x42C25944)
    tool = Items.FindByID(0x12B3,-1,Player.Backpack.Serial)

    Items.Move(granite,Player.Backpack.Serial,200)
    Misc.Pause(1000)
    Misc.WaitForContext(tool.Serial, 10000)
    Misc.ContextReply(tool.Serial, 0)
    Misc.Pause(500)
    Target.TargetExecute(0x403D6218)
    Misc.Pause(8000)