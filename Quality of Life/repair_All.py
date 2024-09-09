Items.UseItem(0x409F2C72)
Misc.Pause(500)
Items.UseItem(0x41EA8A93)
Misc.Pause(500)
repairbag = Items.FindBySerial(0x41EA8A93)

for i in repairbag.Contains:
    Items.Move(i,Player.Backpack.Serial,1)
    Misc.Pause(1000)
    Items.UseItemByID(0x13E3,0x0000)
    Misc.Pause(500)
    Gumps.SendAction(949095101, 42)
    Misc.Pause(500)
    Target.TargetExecute(i)
    Misc.Pause(500)
    Items.Move(i,0x41EA8A93,1)

Player.ChatSay(64,"All items have been repaired.")