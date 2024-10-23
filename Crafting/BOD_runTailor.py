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
Player.HeadMessage(64,"Running tailor bods in 90 seconds")
Misc.Pause(90000)       
worldSave()

Items.UseItem(0x42E88440)
Misc.Pause(500)
Items.UseItem(0x4194BF9C)
Misc.Pause(500)
bodbox = Items.FindBySerial(0x4194BF9C)

for i in bodbox.Contains:
    if i and i.ItemID == 0x14EF and i.Hue == 1155:
        Misc.Pause(500)
        Items.Move(i,Player.Backpack.Serial,1)
        Misc.Pause(1000)
    else:
        Misc.Pause(500)

Misc.Pause(500)
Items.UseItem(0x42E87E92) #open cloth cabinet
Misc.Pause(400)
Items.UseItem(0x435ED948) #open cloth bag
Misc.Pause(400)
Items.UseItem(0x42E8832C) #open trash bin
Misc.Pause(1000)
Items.UseItem(0x42E87E92) #open ingot bag
Misc.Pause(1000)
ingotcount = Items.BackpackCount(0x1BF2,0x0000)

if ingotcount < 50:
    ingots = Items.FindByID(0x1BF2,0x0000,0x42E87E92)
    if ingots:
        Items.Move(ingots,Player.Backpack.Serial,50 - ingotcount)
        Misc.Pause(500)
    else:
        Player.ChatSay(64,"Out of ingots!")
        Misc.Pause(500)
        Misc.ScriptStop("BOD_runTailor.py")

worldSave()   

logs = Items.FindByID(0x1BDD,-1,Player.Backpack.Serial)
if logs:
    Items.UseItem(0x42E87E92)
    Misc.Pause(500)
    Items.Move(logs,0x41132AE2,-1)
    Misc.Pause(1000)
    
Misc.ScriptRun("BOD_demigodTailor.py")

while Misc.ScriptStatus("BOD_demigodTailor.py"):
    Misc.Pause(10000)

worldSave()  
Gumps.SendAction(1425364447, 0)
Misc.Pause(500)
Gumps.SendAction(949095101, 0)
Misc.Pause(500)
Misc.ScriptRun("master_Organizer.py")

    



