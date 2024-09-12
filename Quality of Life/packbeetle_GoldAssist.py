gold = Items.FindByID(0x0EED,-1,0x415801EC,-1,True)
player_serial = Player.Serial
beetle_backpack_serial = 0x423DA363
beetle_gold = Items.FindByID(0x0EED,-1,0x42175E42,-1,False)
loot = [0x0EED,0x05e4]

while Player.Weight > 350:
    if Player.Mount:
        Player.HeadMessage(65,'Beetle transfer, 3 seconds')
        Misc.Pause(3000)
        Mobiles.UseMobile(player_serial)
        Misc.Pause(500)
        Misc.WaitForContext(0x001523D4, 10000)
        Misc.ContextReply(0x001523D4, 10)
        Misc.Pause(500)
        for i in Player.Backpack.Contains:
            if i in loot:
                Items.Move(i,beetle_backpack_serial, -1)
        try:
            Items.Move(gold, beetle_backpack_serial,Player.Gold-1)
            Misc.Pause(750)
        except:
            Misc.Pause(500)
        Player.HeadMessage(65,Items.ContainerCount(beetle_backpack_serial,0x0EED,-1,True))
        Mobiles.UseMobile(0x001523D4)
        Misc.Pause(10000)
        
    
    

