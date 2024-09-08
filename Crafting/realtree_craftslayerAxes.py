smith_hammer = 0x13E3
beetle = 0x00121BEB
axe = Items.FindByID(0x0F4B,-1,Player.Backpack.Serial)


keepSlayerProps = ['Silver','Reptilian Death','Elemental Ban','Repond','Exorcism','Arachnid Doom','Fey Slayer',
    'Balron Damnation','Daemon Dismissal','Orc Slaying','Dragon Slaying'] 


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

def moveSlayerToBeetle():
    if Player.Mount:
        Mobiles.UseMobile(Player.Serial)
        Misc.Pause(500)
    Misc.WaitForContext(0x000E31D1, 10000)
    Misc.ContextReply(0x000E31D1, 10)
    Misc.Pause(500)
    Items.Move(axe,0x40FDDCA5, 1)
    Misc.Pause(500)
    Mobiles.UseMobile(beetle)
    Misc.Pause(500)    

Journal.Clear()    
Items.UseItemByID(smith_hammer,-1)
Misc.Pause(500)
Gumps.WaitForGump(949095101, 10000)
Gumps.SendAction(949095101, 43)
Misc.Pause(500)
                    
while True:
    worldSave()
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, 16)
    Misc.Pause(2500)
    axe = Items.FindByID(0x0F4B,-1,Player.Backpack.Serial)
    Items.WaitForProps(axe,1500)
    props = Items.GetPropStringList(axe)
    if any(elem in keepSlayerProps for elem in props):
        Player.HeadMessage(64, props[9])
        moveSlayerToBeetle()
    else:
        if Player.Mount:
            Mobiles.UseMobile(Player.Serial)
            Misc.Pause(500)
        Misc.Pause(500)
        Items.Move(axe,beetle, 1)
        Misc.Pause(500)
        Mobiles.UseMobile(beetle)
        Misc.Pause(500)   

    #Unload beetle into smelt box
##        
#beetle = 0x00121BEB
#beetlebag = 0x417EFFFD
#beetle = Items.FindBySerial( beetle )
#smeltBox = 0x409F2C72
#smeltBox = Items.FindBySerial( smeltBox )
#beetlebag = Items.FindBySerial ( beetlebag )
#
#for i in beetlebag.Contains:
#    if i.ItemID == 0x0F4B:
#        Items.Move(i,smeltBox,-1,131,81)
#        Misc.Pause(500)        
#        
        