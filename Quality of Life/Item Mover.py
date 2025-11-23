wands = [0x0DF2, 0x0DF4, 0x0DF3, 0x0DF5]
statues = [0x20D4,0x2100,0x210B, 0x25B6, 0x2581,0x25D7,0x20ED,0x20E7,0x20D1,0x20DE,0x20EE,0x25D5,0x25DB,0x25A2,0x211D,0x20EC]
rune_ids = [
    0x483B, 0x483E, 0x4841, 0x4844, 0x4847, 0x484A, 0x484D, 0x4850, 0x4853,
    0x4856, 0x4859, 0x485C, 0x485F, 0x4862, 0x4865, 0x4868, 0x486B, 0x4871,
    0x486E, 0x4874, 0x4877, 0x487A, 0x487D, 0x4880, 0x4883
]

def move():
    itemtomove = Target.PromptTarget("Select item to move.", 64)
    itemtomove = Items.FindBySerial(itemtomove)
    source = itemtomove.Container
    destination = Target.PromptTarget("Select destination container.", 64)
    destination = Items.FindBySerial(destination)

    item_id = itemtomove.ItemID
    category = None

    if item_id in wands:
        category = wands
    elif item_id in statues:
        category = statues
    elif item_id in rune_ids:
        category = rune_ids
    else:
        category = [item_id]  # treat as a one-off ID list

    # Resolve source container
    if Misc.IsItem(source):
        source = Items.FindBySerial(source)
        container_items = source.Contains
    elif Misc.IsMobile(source):
        source = Mobiles.FindBySerial(source)
        container_items = source.Backpack.Contains
    else:
        Misc.SendMessage("Invalid source selected.", 33)
        return

    for item in container_items:
        if item.ItemID in category:
            Items.Move(item, destination, -1)
            Misc.Pause(800)

move()
