Misc.Pause(2000)
Misc.ScriptRun("bandageAssist.py")
Misc.Pause(500)
Misc.ScriptRun("auto_lumberjack.py")


while True:
    while Misc.ScriptStatus("auto_lumberjack.py"):
        Misc.Pause(1000)

    Misc.Pause(500)
    Player.ChatSay("All follow me")
    Misc.Pause(500)
    Player.ChatSay("[recall Winter Lodge")
    Misc.Pause(2500)
    Player.PathFindTo(6802, 3901, 12)
    Misc.Pause(1500)
    Player.PathFindTo(6803, 3899, 17)
    Misc.Pause(1500)
    if Player.Mount:
        Mobiles.UseMobile( Player.Serial )
        Misc.Pause( 500 )
    Misc.WaitForContext(0x001523D4, 10000)
    Misc.ContextReply(0x001523D4, 10)
    Misc.Pause(500)
        

    beetle = Mobiles.FindBySerial(0x001523D4)
    wood_pouch = Items.FindBySerial(0x41132AE2)
    leather_pouch = Items.FindBySerial(0x435ED948)
    wood_box = Items.FindBySerial(0x42E87E92) 
    Items.UseItem(wood_box)
    Misc.Pause(500)
    Items.UseItem(wood_pouch)
    Misc.Pause(500)
    Items.UseItem(leather_pouch)
    Misc.Pause(500)


    # Move items from players backpack
    for i in Player.Backpack.Contains:
        if i.ItemID == 0x1BDD: #wood
            Items.Move(i,0x41132AE2,-1)
            Misc.Pause(1000)
        elif i.ItemID == 0x0EED: #gold
            Items.Move(i,0x42E87E92,-1)
            Misc.Pause(1000)
        elif i.ItemID == 0x0F7E: #bone
            Items.Move(i,0x42E87E92,-1)
            Misc.Pause(1000)
        elif i.ItemID == 0x1081: #leather
            Items.Move(i,0x435ED948,-1)
            Misc.Pause(1000)
    # Move items from beetles backpack
    for i in beetle.Backpack.Contains:
        if i.ItemID == 0x1BDD: #wood
            Items.Move(i,0x41132AE2,-1)
            Misc.Pause(1000)
        elif i.ItemID == 0x1081: #leather
            Items.Move(i,0x435ED948,-1)
            Misc.Pause(1000)
        
    bandages = Items.BackpackCount(0x0E21,-1)
    bolts = Items.FindByID(0x0F95,-1,0x435ED948)
    if bandages < 100:
        Misc.Pause(500)
        Items.UseItem(leather_pouch)
        Misc.Pause(500)
        bolts = Items.FindByID(0x0F95,-1,0x435ED948)
        Items.Move(bolts,Player.Backpack.Serial,2)
        Misc.Pause(1000)
        Items.UseItemByID(0x0F9F,-1)
        Misc.Pause(500)
        packbolts = Items.FindByID(0x0F95,-1,Player.Backpack.Serial)
        Target.TargetExecute(packbolts)
        Misc.Pause(500)
        packcloth = Items.FindByID(0x1766,-1,Player.Backpack.Serial)
        Items.UseItemByID(0x0F9F,-1)
        Misc.Pause(500)
        Target.TargetExecute(packcloth)
        Misc.Pause(500) 
        
    #read runebook charges
    runebook = Items.FindBySerial(0x43F88669)
    rbcharges = Items.GetPropStringByIndex(runebook,6)
    parts = rbcharges.split()  # parts = ["Charges", "10/10"]
    charge_info = parts[1]  # charge_info = "10/10"
    numerator, _ = charge_info.split('/')  # numerator = "10"
    emergency_charges = int(numerator)
    #move exact amount of recall scrolls
    if emergency_charges < 83:
        scrollstomove = 83 - emergency_charges
        scrollsupply = Items.FindByID(0x1F4C,0x0000,0x42E87E92)
        Items.Move(scrollsupply,runebook,scrollstomove)
        Misc.Pause(1000)
   
            
    if not Player.Mount:
        Mobiles.UseMobile( beetle )
        Misc.Pause( 500 )
        
    Misc.ScriptRun("auto_lumberjack.py")
