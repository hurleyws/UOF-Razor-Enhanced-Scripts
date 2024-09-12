from System.Collections.Generic import List
from System import Int32 as int

# SETTINGS
CORPSE_ID = 0x2006
GOLD_ID = 0x0EED  # Gold Item ID
LOOTABLE_ITEMS = {
    0x26B4: 'Hide',
    0x0EED: 'Gold',
    0x0DCA: 'Net',
    0x099F: 'SOS',
    0x14F8: 'Rope',
    0x1BF2: 'Ingot',
    0x1081: 'Horned Leather',
    0x14EC: 'Treasure Map',
    0x2831: 'Recipe',
    0x09F1: 'Meat'
}

LOOT_TOOLS = {
    'salvage_hook': 0x0EC4,  # Example item ID for salvage hook
    'hatchet': 0x0F52        # Example item ID for hatchet
}

# FUNCTIONS

def find_corpses():
    # Finds all nearby corpses matching the specified filter
    corpse_filter = Items.Filter()
    corpse_filter.IsCorpse = True
    corpse_filter.OnGround = True
    corpse_filter.RangeMax = 2  # Increase the range slightly to find corpses faster
    corpse_filter.Graphics = List[int]([CORPSE_ID])
    corpse_filter.CheckIgnoreObject = True
    
    return Items.ApplyFilter(corpse_filter)

def should_loot_item(item):
    # Checks if the item should be looted based on its ItemID
    return item.ItemID in LOOTABLE_ITEMS

def loot_corpse(corpse):
    # Loots items from the given corpse based on the loot list
    looted_items = []
    for item in corpse.Contains:
        if should_loot_item(item):
            Items.Move(item, Player.Backpack, -1)  # Move stackable items (-1 for all)
            looted_items.append(LOOTABLE_ITEMS[item.ItemID])
            Misc.Pause(500)  # Lower the pause after moving items
    
    # Send message for all looted items at once, not for every item
    if looted_items:
        Misc.SendMessage(f"Looted: {', '.join(looted_items)}", 33)

def is_gold_still_on_corpse(corpse):
    # Checks if gold is still present on the corpse
    for item in corpse.Contains:
        if item.ItemID == GOLD_ID:
            return True
    return False

def use_tool(tool_name):
    # Uses the specified tool (e.g., hatchet, salvage hook) from the players backpack
    tool_id = LOOT_TOOLS.get(tool_name)
    if Items.FindByID(tool_id, -1, Player.Backpack.Serial):
        Items.UseItemByID(tool_id, -1)
        Misc.Pause(200)

def main():
    # Main function to find and loot corpses
    corpses = find_corpses()
    
    for corpse in corpses:
        # Open the corpse and loot items
        Items.UseItem(corpse)
        Misc.Pause(500)
        loot_corpse(corpse)

        # Check if gold is still on the corpse
        if not is_gold_still_on_corpse(corpse):
            # Ignore the corpse only if gold is no longer present
            Misc.IgnoreObject(corpse)

# RUN SCRIPT
while True:
    main()
    Misc.Pause(1000)
