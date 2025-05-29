from System.Collections.Generic import List
from System import Int32 as int
import winsound
import sys



npc = 0x0024A965 #blacksmith 0x00029397 #tailor 0x0024A965
trashlist = [0x0E85, 0x0E86, 0x0F39, 0x1006, 0x0544, 0x13C6, 0x13D5, 0x0FB4]
keeplist = [0x0EED, 0x14F0, 0x5738, 0x4CDB, 0x4CD8, 0x1767]
keephues = [0x06d8, 0x06b7, 0x097e, 0x07d2, 0x0544, 0x0482]
trashhues = [0x0415, 0x0455, 0x045f]
beetle = Mobiles.FindBySerial(0x004FEA0E)
beetlepack = 0x4B0936DA


# Find trash can nearby
trashBarrelFilter = Items.Filter()
trashBarrelFilter.OnGround = 1
trashBarrelFilter.Movable = False
trashBarrelFilter.RangeMin = 0
trashBarrelFilter.RangeMax = 2
trashBarrelFilter.Graphics = List[int]([0x0E77])
trashBarrelFilter.Hues = List[int]([0x03B2])
trashBarrels = Items.ApplyFilter(trashBarrelFilter)
trash = trashBarrels[0] if len(trashBarrels) > 0 else None

if not trash:
    Misc.SendMessage("No trash barrel found nearby!", 33)
    Misc.Pause(500)
    Misc.ScriptStop("bod_turninAll.py")
    
# Turn in BODs, trash immediately, batch keepers
for i in Player.Backpack.Contains:
    if i.ItemID == 0x14EF:
        Items.Move(i, npc, 1)
        Misc.Pause(650)

        # Move trash immediately
        for item in Player.Backpack.Contains:
            if item.ItemID in trashlist:
                Items.Move(item, trash, 1)
                Misc.Pause(650)
            elif item.ItemID == 0x13E3 and item.Hue in trashhues:
                Items.Move(item, trash, -1)
                Misc.Pause(650)
            elif item.ItemID == 0x13EB and item.Hue != 0x0000:
                Items.Move(item, trash, -1)
                Misc.Pause(650) 
            elif item.ItemID == 0x0F9D and item.Hue == 0x0900:
                Items.Move(item, trash, -1)
                Misc.Pause(650) 
         #checking plain deeds for tapestries
            elif item.ItemID == 0x14F0 and item.Hue == 0x0000:
                props = Items.GetPropStringList(item)
                Misc.Pause(250)
                if any("flower tapestry" in p.lower() for p in props):
                    Misc.Pause(250)
                    Items.Move(item, trash, -1)
                    Misc.Pause(650)   
                else: 
                    if Player.Mount:
                        Mobiles.UseMobile(Player.Serial)
                        Misc.Pause(500)
                    Items.Move(item, beetlepack, -1)
                    Misc.Pause(1000)
                    if not Player.Mount:
                        beetle = Mobiles.FindBySerial(0x004FEA0E)
                        Mobiles.UseMobile(beetle)
                        Misc.Pause(500)  
                
        # Move Power Scroll immediately
            elif item.ItemID == 0x14F0 and item.Hue == 0x0481:
                Items.UseItem(0x43F36393) #key
                Misc.Pause(500)
                Target.TargetExecute(0x43F36392)#trapped box
                Misc.Pause(500)
                Items.Move(item, 0x43F36392, -1)
                Misc.Pause(1000)
                Items.UseItem(0x43F36393) #key
                Misc.Pause(500)
                Target.TargetExecute(0x43F36392)#trapped box
                Misc.Pause(500)
            # Move hammers immediately        
            elif item.ItemID == 0x13E3 and item.Hue in keephues:
                if Player.Mount:
                    Mobiles.UseMobile(Player.Serial)
                    Misc.Pause(500)
                Items.Move(item, beetlepack, -1)
                Misc.Pause(1000)
                if not Player.Mount:
                    beetle = Mobiles.FindBySerial(0x004FEA0E)
                    Mobiles.UseMobile(beetle)
                    Misc.Pause(500)  
        

        # If overweight, now move all keeper items
        if Player.Weight > 350:
            if Player.Mount:
                Mobiles.UseMobile(Player.Serial)
                Misc.Pause(500)
            for item in Player.Backpack.Contains:
                if item.ItemID in keeplist:
                    Items.Move(item, beetlepack, -1)
                    Misc.Pause(1000)
                elif item.ItemID == 0x13E3 and item.Hue in keephues:
                    Items.Move(item, beetlepack, -1)
                    Misc.Pause(1000)
                elif item.ItemID == 0x13EB and item.Hue == 0x0000:
                    Items.Move(item, beetlepack, -1)
                    Misc.Pause(1000)
            if not Player.Mount:
                beetle = Mobiles.FindBySerial(0x004FEA0E)
                Mobiles.UseMobile(beetle)
                Misc.Pause(500)

            
#Once all turned in, finish up, trash first
for item in Player.Backpack.Contains:
    if item.ItemID in trashlist:
        Items.Move(item, trash, 1)
        Misc.Pause(650)
    elif item.ItemID == 0x13E3 and item.Hue in trashhues:
        Items.Move(item, trash, -1)
        Misc.Pause(650)
    elif item.ItemID == 0x13EB and item.Hue != 0x0000:
        Items.Move(item, trash, -1)
        Misc.Pause(650)        

#Now keepers
if Player.Mount:
    Mobiles.UseMobile(Player.Serial)
    Misc.Pause(500)
for item in Player.Backpack.Contains:
    if item.ItemID in keeplist:
        Items.Move(item, beetlepack, -1)
        Misc.Pause(1000)
    elif item.ItemID == 0x13E3 and item.Hue in keephues:
        Items.Move(item, beetlepack, -1)
        Misc.Pause(1000)
    elif item.ItemID == 0x13EB and item.Hue == 0x0000:
        Items.Move(item, beetlepack, -1)
        Misc.Pause(1000)                       
if not Player.Mount:
    beetle = Mobiles.FindBySerial(0x004FEA0E)
    Mobiles.UseMobile(beetle)
    Misc.Pause(500)
