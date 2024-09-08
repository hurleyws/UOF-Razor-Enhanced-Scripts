    #To unload beetle, comment out both sources and activate the beetle line - beetle.Backpack.Countains

itemtomove = Target.PromptTarget("Select item to move.",64)
itemtomove = Items.FindBySerial(itemtomove)
source = Target.PromptTarget("Select source.",64)
source = Items.FindBySerial(source)
destination = Target.PromptTarget("Select destination.",64)
destination = Items.FindBySerial(destination)
#beetle = Mobiles.FindBySerial(0x00121BEB)

for i in source.Contains:
    if i.ItemID == itemtomove.ItemID:
        Items.Move(i,destination,1) #add x, y coordinates here if desired
        Misc.Pause(800)
