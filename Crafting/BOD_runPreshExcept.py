ingots = Items.FindByID(0x1BF2,0,0x40826F73)

def worldSave():
    if (Journal.SearchByType('The world will save in 1 minute.', 'System') or Journal.SearchByType('pause', 'Regular')):
        Misc.Pause(700)
        Misc.SendMessage('Pausing for world save or player-called break.', 33)
        while (not Journal.SearchByType('World save complete.', 'System') and not Journal.SearchByType('play', 'Regular')):
            Misc.Pause(1000)
        Misc.Pause(2500)
        Misc.SendMessage('Continuing run', 33)
        Misc.Pause(1000)
    Journal.Clear()   

Journal.Clear()
Player.HeadMessage(64,"Running precious exceptionals in 90 seconds")
Misc.Pause(90000)       
worldSave()

Items.UseItem(0x42E88440) #crate by door
Misc.Pause(500)
Items.UseItem(0x42369679)
Misc.Pause(500)
bodbox = Items.FindBySerial(0x42369679)

for i in bodbox.Contains:
    if i and i.ItemID == 0x14EF and i.Hue == 1102:
        Items.Move(i,Player.Backpack.Serial,1)
        Misc.Pause(1000)
    else:
        Misc.Pause(500)


Misc.Pause(500)
Player.PathFindTo(6803, 3892, 17)
Misc.Pause(4000)
Items.UseItem(0x42E90238) #new ingot box
Misc.Pause(700)
worldSave()
hammercount = Items.BackpackCount(0x13E3,0x0000)
if hammercount < 7:
    ingots = Items.FindByID(0x1BF2,0,0x42E90238)
    Items.Move(ingots,Player.Backpack.Serial,4*(7-hammercount))
    Misc.Pause(500)
    for i in range(7-hammercount):
        Items.UseItemByID(0x1EB8,0)
        Misc.Pause(500)
        Gumps.SendAction(949095101, 93)
        Misc.Pause(2000)
    Misc.Pause(500)
    Gumps.SendAction(949095101, 0)
    Misc.Pause(200)
    
myingots = Items.FindByID(0x1BF2,0,Player.Backpack.Serial)
if myingots:
    Items.Move(myingots,0x42E90238,-1)
    Misc.Pause(1000)
worldSave()
Misc.ScriptRun("BOD_demigod_preciousMetals.py")

while Misc.ScriptStatus("BOD_demigod_preciousMetals.py"):
    Misc.Pause(10000)

worldSave()
Gumps.SendAction(1526454082, 1)
Misc.Pause(500)
Gumps.SendAction(1425364447, 0)
Misc.Pause(500)
Gumps.SendAction(949095101, 0)
Misc.Pause(500)
Player.PathFindTo(6804, 3897, 17)
Misc.Pause(4000)
Player.Run("North")
Misc.Pause(500)
for i in Player.Backpack.Contains:
    if i.ItemID == 0x14EF and i.Hue == 1102:
        Items.Move(i,0x406954AF,1)
        Misc.Pause(1000)
Misc.Pause(2000)
Gumps.SendAction(1425364447, 0)
Misc.Pause(500)
Misc.ScriptRun("master_Organizer.py")

    



