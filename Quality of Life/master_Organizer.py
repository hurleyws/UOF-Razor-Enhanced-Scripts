regs = [0x0F85, 0x0F86, 0x0F84, 0x0F88, 0x0F8C, 0x0F7B, 0x0F8D, 0x0F7A]
pots = [0x0F0B,0x0F09,0x0F0C,0x0F07,0x09F1] #pots+meat
scrolls = [0x1F69]
tools = [0x13E3,0x1034,0x1EB8]
wands = [0x0DF2,0x0DF4,0x0DF3,0x0DF5]
ingots = [0x1BF2]      


# Define a reusable function to move items, but only if theyre not already in the correct position
def move_items(item_list, item_id, target_x, target_y, pause=750):
    for item in item_list:
        # Check if the item ID matches (handles both lists and single values)
        if isinstance(item_id, list) and item.ItemID in item_id or item.ItemID == item_id:
            # If the items position matches the target position, skip moving it
            if item.Position.X == target_x and item.Position.Y == target_y:
                continue  # Skip this item, it's already in place
            
            # Move the item to the new position if its not already there
            Items.Move(item, Player.Backpack.Serial, -1, target_x, target_y)
            Misc.Pause(pause)

# Realtree-specific item placement
if Player.Name == 'Realtree':
    player_items = Player.Backpack.Contains

    # Sewing kits to top right
    move_items(player_items, 0x0F9D, 158, 64)

    # Ingots to top center-left
    move_items(player_items, ingots, 67, 64)

    # Reagents (regs) to top left
    move_items(player_items, regs, 43, 64)
    
    # Ethereal to left center
    move_items(player_items, 0x20DD, 43, 77)

    # Tinker tools to bottom right
    move_items(player_items, tools, 172, 124)

    # Wands to center right
    move_items(player_items, wands, 159, 98)

    # Fletching tools to top right
    move_items(player_items, 0x1022, 134, 64)
    
# ToolmanTailor-specific item placement
if Player.Name == 'ToolmanTailor':
    player_items = Player.Backpack.Contains

    # Reagents (regs) to top left
    move_items(player_items, regs, 43, 64)
    
    # Ethereal to left center
    move_items(player_items, 0x20F6, 43, 77)

    # Bandages to top right
    move_items(player_items, 0x0E21, 158, 64)

    # Staff to bottom right
    move_items(player_items, wands, 143, 125)



# Zastore-specific item placement
if Player.Name == 'Zastore':
    player_items = Player.Backpack.Contains

    # Bandages to top right
    move_items(player_items, 0x0E21, 158, 64)

    # Pots to bottom left
    move_items(player_items, pots, 43, 137)

            