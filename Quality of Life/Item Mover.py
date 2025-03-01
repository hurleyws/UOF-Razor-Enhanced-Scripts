wands = [0x0DF2, 0x0DF4, 0x0DF3, 0x0DF5]

def move():
    itemtomove = Target.PromptTarget("Select item to move.", 64)
    itemtomove = Items.FindBySerial(itemtomove)
    source = Target.PromptTarget("Select source.", 64)
    destination = Target.PromptTarget("Select destination.", 64)
    destination = Items.FindBySerial(destination)
    beetle = Mobiles.FindBySerial(0x00121BEB)

    if Misc.IsItem(source):
        source = Items.FindBySerial(source)
        for i in source.Contains:
            # Move the selected item OR any wand if the selected item is a wand
            if i.ItemID == itemtomove.ItemID or i.ItemID in wands:
                Items.Move(i, destination, -1)  # add x, y coordinates here if desired
                Misc.Pause(800)
        return
        
    if Misc.IsMobile(source):
        source = Mobiles.FindBySerial(source)
        if source.Name == "a giant beetle":
            for i in source.Backpack.Contains:
                if i.ItemID == itemtomove.ItemID or i.ItemID in wands:
                    Items.Move(i, destination, -1)  # add x, y coordinates here if desired
                    Misc.Pause(800)

move()
