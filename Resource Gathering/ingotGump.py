# Iron Ingot Counter Gump Script
# Counts the number of iron ingots in a specific container and shows a gump

# Configuration
target_container = 0x40FA9D34  # Replace with your chest's serial
item_id = 0x1BF2               # Iron ingots
item_hue = 0x0000              # Standard iron color
gump_id = 9270               # Desired gumpID

def count_ingots():
    total = 0
    container_items = Items.FindBySerial(target_container).Contains
    for item in container_items:
        if item.ItemID == item_id and item.Hue == item_hue:
            total += item.Amount
    return total

def show_gump(count):
    gd = Gumps.CreateGump(True, True, False, False)
    Gumps.AddBackground(gd, 0, 0, 230, 90, 9270)
    Gumps.AddBackground(gd, 10, 13, 60, 70, 9012)
    Gumps.AddLabel(gd, 80, 25, 1152, "Iron Ingots in Chest:")
    Gumps.AddLabel(gd, 125, 45, 1153, str(count))

    Gumps.SendGump(gump_id, Player.Serial, 400, 300, gd.gumpDefinition, gd.gumpStrings)

# Run once
iron_ingot_count = count_ingots()
show_gump(iron_ingot_count)
