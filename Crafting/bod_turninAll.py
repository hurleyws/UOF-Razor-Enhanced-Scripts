Mobiles.UseMobile(Player.Serial)
Misc.Pause(500)
Misc.WaitForContext(0x00121BEB, 10000)
Misc.ContextReply(0x00121BEB, 10)
Misc.Pause(500)

npc = Target.PromptTarget('Target NPC to give BODs to.',64)
trashlist = [0x0E85,0x0E86,0x0F39,0x1006, 0x0544,0x13C6,0x13D5,0x0FB4] #0x1006 (powder), 0x0FB4 (prospector), 0x0544 (gloves)
keeplist = [0x0EED,0x14F0,0x5738,0x4CDB,0x4CD8,0x1767] 
beetle = Mobiles.FindBySerial(0x00121BEB)
keephues = [0x06d8,0x06b7,0x097e,0x07d2,0x0544,0x0482] #bronze, gold, aggy, verite, valorite, ash
trashhues = [0x0415,0x0455,0x045f] #dull copper, shadow, copper
beetlepack = 0x417EFFFD
trash = Target.PromptTarget("Select bag to depost trash drops.",64)


for i in Player.Backpack.Contains:
        if i.ItemID == 0x14EF:
            Items.Move(i,npc,1)
            Misc.Pause(1000)
            if Player.Weight > 350:
                break
                
for i in Player.Backpack.Contains:
    if i.ItemID in trashlist:
        Items.Move(i,trash,1)
        Misc.Pause(1000)
for i in Player.Backpack.Contains:
    if i.ItemID in keeplist:
        Items.Move(i,beetlepack,-1)
        Misc.Pause(1000)
for i in Player.Backpack.Contains:
    if i.ItemID == 0x13E3 and i.Hue in keephues:
        Items.Move(i,beetlepack,-1)
        Misc.Pause(1000)
for i in Player.Backpack.Contains:
    if i.ItemID == 0x13E3 and i.Hue in trashhues:
        Items.Move(i,trash,-1)
        Misc.Pause(1000)
for i in Player.Backpack.Contains:
    if i.ItemID == 0x13EB and i.Hue == 0x0000:
        Items.Move(i,beetlepack,-1)
        Misc.Pause(1000)
for i in Player.Backpack.Contains:
    if i.ItemID == 0x13EB:
        Items.Move(i,trash,-1)
        Misc.Pause(1000)


 
 
