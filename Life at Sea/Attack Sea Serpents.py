from System.Collections.Generic import List
from System import Byte

filterExample = Mobiles.Filter()
filterExample.Enabled = True
filterExample.Name != "Watches"
#filterExample.IsHuman = True # Optional
#filterExample.Bodies = List[int]([0x0190])) #optional, use mobile IDs
filterExample.Notorieties = List[Byte](bytes([3,4,6])) # optional, numbers = notoritety codes

while True:
    filterExampleList = Mobiles.ApplyFilter(filterExample)  # Refresh the list of mobiles that match the filter
    more_filtered = list(filter(lambda mob: mob.Serial != Player.Serial, list(filterExampleList)))
    if len(more_filtered) == 0: Misc.Pause(10); continue
    sorted_by_distance = list(sorted(more_filtered , key=lambda mob: Player.DistanceTo(mob), reverse=False ))
    filterSelection = sorted_by_distance[0]
    if filterSelection:
        Player.ChatSay(64,"Serpent on the horizon!")
        Misc.Pause(500)
        Misc.ScriptStop("train_Fishing.py")
        Misc.Pause(500)
        Player.Attack(filterSelection)
            #allow time to swim to boat
        Misc.Pause(4000)
            #eat buff fish if found
        if Items.FindByID(0x0DD6,-1,Player.Backpack.Serial):
            Items.UseItemByID(0x0DD6,-1)
            Misc.Pause(500)
        Dress.DressFStart()
        Misc.Pause(500)
        while Mobiles.FindBySerial(filterSelection.Serial):
            Player.Attack(filterSelection)
            Misc.Pause(500)

        Misc.Pause(500)
        Dress.UnDressFStart()
        Misc.Pause(500)
        Player.ChatSay(64,"right one")
        Misc.Pause(1000)
        Player.ChatSay(64,"left one")
        Misc.Pause(1000)
        Player.ChatSay(64,"left one")
        Misc.Pause(1000)
        Player.ChatSay(64,"right one")
        Misc.Pause(1000)
        Player.ChatSay(64,"forward one")
        Misc.Pause(1000)
        Player.ChatSay(64,"back one")
        Misc.Pause(1000)
        Player.ChatSay(64,"back one")
        Misc.Pause(1000)
        Player.ChatSay(64,"forward one")
        Misc.Pause(1000)
        Misc.ScriptRun("autoLoot_fish.py")
        Misc.Pause(5000)
        Player.ChatSay(64,"Calm seas.")
        Misc.Pause(200)
        Misc.ScriptRun("train_Fishing.py")
        Misc.Pause(200)
    Misc.Pause(300)
