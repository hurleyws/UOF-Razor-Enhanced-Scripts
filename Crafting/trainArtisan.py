def empower():
    Items.UseItem(0x435ED948)
    Misc.Pause(500)
    cloth = Items.FindByID(0x1766,0x0000,0x435ED948)
    Items.Move(cloth,Player.Backpack.Serial,6)
    Misc.Pause(1000)
    for i in range(3):
        Items.UseItemByID(0x0F9D,-1)
        Misc.Pause(500)
        Gumps.WaitForGump(949095101, 10000)
        Gumps.SendAction(949095101, 1)
        Gumps.WaitForGump(949095101, 10000)
        Gumps.SendAction(949095101, 2)
        Misc.Pause(2500)
        cap = Items.FindByID(0x1544,0x0000,0x403B3933)
        CUO.PlayMacro('empower')
        Misc.Pause(500)
        Target.TargetExecute(cap)
        Misc.Pause(15000)
        Items.UseItemByID(0x0F9F,-1)
        Misc.Pause(500)
        Target.TargetExecute(cap)
        Misc.Pause(500)
    cloth = Items.FindByID(0x1766,0x0000,Player.Backpack.Serial)
    Items.Move(cloth,0x435ED948,-1)
    Misc.Pause(1000)
    
    

def worldSave():
    if (Journal.SearchByType('The world will save in 1 minute.', 'System') or Journal.SearchByType('pause', 'Regular')):
        Misc.Pause(700)
        Misc.SendMessage('Pausing for world save or player-called break.', 33)
        while (not Journal.SearchByType('World save complete.', 'System') and not Journal.SearchByType('play', 'Regular')):
            Misc.Pause(1000)
        Misc.Pause(2500)
        Misc.SendMessage('Continuing run', 33)
        Misc.Pause(700)
    Journal.Clear()  

def stockRegs():
    root = Items.BackpackCount(0x0F7A,-1)
    moss = Items.BackpackCount(0x0F7B,-1)
    pearl = Items.BackpackCount(0x0F86,-1)
  
    
    if root < 15:
        Items.Move(Items.FindByID(0x0F7A,-1,0x42E88440),Player.Backpack.Serial,15-root)
        Misc.Pause(1000)
    
    if moss < 15:
        Items.Move(Items.FindByID(0x0F7B,-1,0x42E88440),Player.Backpack.Serial,15-moss)
        Misc.Pause(1000)
        
    if pearl < 15:
        Items.Move(Items.FindByID(0x0F86,-1,0x42E88440),Player.Backpack.Serial,15-pearl)
        Misc.Pause(1000)
        
    else:
        Player.HeadMessage(64,"Regs look good")
        Misc.Pause(500)
        
while True:
    Journal.Clear()
    Misc.ScriptRun("artisanTrainer.py")
    Misc.Pause(500)
    while Misc.ScriptStatus("artisanTrainer.py"):
        Misc.Pause(1000)
        
    Misc.Pause(1000)
    worldSave()
    Player.ChatSay("[recall Winter Lodge")
    Misc.Pause(3000)
    Player.PathFindTo(6802, 3901, 12)
    Misc.Pause(1500)
    Player.PathFindTo(6803, 3899, 17)
    Misc.Pause(1500)      
    Items.UseItem(0x42E88440) #Open box by door
    Misc.Pause(500)
    stockRegs()
    if Player.Mount:
            Mobiles.UseMobile( Player.Serial )
            Misc.Pause( 500 )
    Misc.WaitForContext(0x00121BEB, 10000)
    Misc.ContextReply(0x00121BEB, 10)
    Misc.Pause(500)
    woodBox = Items.FindBySerial(0x42E87E92)
    beetle = Mobiles.FindBySerial(0x00121BEB)
    Items.UseItem(woodBox)
    Misc.Pause(500)
    Items.UseItem(0x41132AE2) #wood pouch
    Misc.Pause(500)
    Items.UseItem(0x42EA4E24) #ingot pouch
    Misc.Pause(500)
    
    wood = Items.FindByID(0x1BDD,0x0000,0x41132AE2)
    packwood = Items.ContainerCount(Player.Backpack.Serial,0x1BDD,0x0000)
    beetlewood = Items.ContainerCount(beetle.Backpack.Serial,0x1BDD,0x0000)
    meat = Items.FindByID(0x09F1,0x0000,0x42E87E92)
    ingots = Items.FindByID(0x1BF2,0x0000,0x42EA4E24)
    packingots = Items.ContainerCount(Player.Backpack.Serial,0x1BF2,0x0000)
    if beetlewood < 16000:
        Items.Move(wood,beetle,16000-beetlewood)
        Misc.Pause(1000)
    if packwood < 1000:
        Items.Move(wood,Player.Backpack.Serial,1000-packwood)
        Misc.Pause(1000)
    if packingots < 400:
        Items.Move(ingots,Player.Backpack.Serial,400-packingots)
        Misc.Pause(1000)
    Items.Move(meat,beetle,1)
    Misc.Pause(1000)
    Mobiles.UseMobile(beetle)
    Misc.Pause(500)
    Items.UseItem(0x42EA4E24)
    Misc.Pause(500)
    empower()
    Player.ChatSay("[recall Trainer")
    Misc.Pause(3000)




