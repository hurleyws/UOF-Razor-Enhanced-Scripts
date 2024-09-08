
bodbox = Items.FindBySerial(0x4236967B)

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

def sortBods():
    # Sort the items in the backpack based on whether they match keywords
    backpack_items = Player.Backpack.Contains
    keywords = ["halberd", "helmet", "bascinet", "hammer pick", "axe", "bardiche", "spear", "bascinet", "war", "scimitar", "maul", "sword", "katana", "kryss", "shield", "broadsword", "close", "dagger", "longsword", "buckler", "armor", "cutlass", "mace"]
    sorted_items = sorted(backpack_items, key=lambda item: any(keyword.lower() in str(Items.GetPropStringList(item)).lower() for keyword in keywords), reverse=True)

    for i in sorted_items:
        prop_list = Items.GetPropStringList(i)
        len_det = len(prop_list)
        
        if i.ItemID == 0x14EF:
            if any(keyword.lower() in str(prop_list).lower() for keyword in keywords):
                sellbook = Items.FindByName("Sell", 0x0000, Player.Backpack.Serial, 4)
                Misc.Pause(200)
                Items.Move(i, sellbook, 1)
                Misc.Pause(1000)
            else:
                sortbook = Items.FindByName("Sort", 0x0000, Player.Backpack.Serial, 4)
                Items.Move(i, sortbook, 1)
                Misc.Pause(1000)
                
    Gumps.WaitForGump(1425364447, 10000)
    Gumps.SendAction(1425364447, 0)
    Misc.Pause(200)    
    
Journal.Clear()
Player.HeadMessage(64,"Running normal iron in 90 seconds.")
Misc.Pause(90000)       
worldSave()

Items.UseItem(0x42E88440)
Misc.Pause(400)
Items.UseItem(0x4236967B)
Misc.Pause(400)
bodbox = Items.FindBySerial(0x4236967B)


for i in bodbox.Contains:
    if i and i.ItemID == 0x14EF and i.Hue == 1102 and i:
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
iron = Items.FindByID(0x1BF2,-1,Player.Backpack.Serial)
if iron:
    Items.Move(iron,0x42E90238,-1) #this script doesn't like it when iron is in the backpack to start
    Misc.Pause(1000)
worldSave()    
Misc.ScriptRun("BOD_demigod_nonexceptional.py")
while Misc.ScriptStatus("BOD_demigod_nonexceptional.py"):
    Misc.Pause(10000)

worldSave()  
Gumps.SendAction(1526454082, 1)
Misc.Pause(500)
Gumps.SendAction(1425364447, 0)
Misc.Pause(500)
Gumps.SendAction(949095101, 0)
Misc.Pause(500)
#close all gumps before going back to stool
Player.PathFindTo(6804, 3897, 17)
Misc.Pause(4000)
Player.Run("North")
Misc.Pause(500)
sortBods()
Misc.ScriptRun("master_Organizer.py")
    



