Items.UseItem(0x42B6C094)
Misc.Pause(2000)

##remove
#Journal.Clear()
#while True:
#    Gumps.WaitForGump(3738072638, 10000)
#    Gumps.SendAction(3738072638, 1)
#    while not Journal.SearchByType("You have removed the Treasure Map","System"):
#        Misc.Pause(200)
#    Misc.Pause(200)
#    Journal.Clear()
    
##add sos 0x14EE add tmap 0x14EC
Gumps.WaitForGump(3738072638, 10000)
Gumps.SendAction(3738072638, 1000)
Misc.Pause(1000)
#
for i in Player.Backpack.Contains:
    if i.ItemID == 0x14EC:
        Misc.Pause(1000)
        Target.TargetExecute(i)
        while not Journal.SearchByType("Added, please choose another.","System"):
            Misc.Pause(200)
        Misc.Pause(200)
        Journal.Clear()
        