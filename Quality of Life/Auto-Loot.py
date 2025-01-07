from System.Collections.Generic import List
from System import Int32 as int

getResourcesFlag = True  # Toggle resource collection on/off
lootHides = False  # Toggle for looting hides
lootScales = True  # Toggle for looting scales

# SETTINGS
CORPSE_ID = 0x2006
GOLD_ID = 0x0EED  # Gold Item ID


LOOTABLE_ITEMS = {
    0x26B4: 'Hide',
    0x1767: 'Cloth',
    0x0EED: 'Gold',
    0x0DCA: 'Net',
    0x099F: 'SOS',
    0x14F8: 'Rope',
    0x1BF2: 'Ingot',
    0x1081: 'Horned Leather',
    0x14EC: 'Treasure Map',
    0x2831: 'Recipe',
    0x09F1: 'Meat',
    0x14F0: 'Power Scroll',  # Power scroll ID
    0x483B: 'Rune 1',       # Rune IDs
    0x483E: 'Rune 2',
    0x4841: 'Rune 3',
    0x4844: 'Rune 4',
    0x4847: 'Rune 5',
    0x484A: 'Rune 6',
    0x484D: 'Rune 7',
    0x4850: 'Rune 8',
    0x4853: 'Rune 9',
    0x4856: 'Rune 10',
    0x4859: 'Rune 11',
    0x485C: 'Rune 12',
    0x485F: 'Rune 13',
    0x4862: 'Rune 14',
    0x4865: 'Rune 15',
    0x4868: 'Rune 16',
    0x486B: 'Rune 17',
    0x4871: 'Rune 18',
    0x486E: 'Rune 19',
    0x4874: 'Rune 20',
    0x4877: 'Rune 21',
    0x487A: 'Rune 22',
    0x487D: 'Rune 23',
    0x4880: 'Rune 24',
    0x4883: 'Rune 25',
    0x2260: 'Skill Scroll',  # Skill scroll ID
    0x2AA2: 'Relic',         # Relic ID
    0x0F21: 'Gem 1',
    0x0F16: 'Gem 2',
    0x0F19: 'Gem 3',
    0x0F13: 'Gem 4',
    0x0F10: 'Gem 5',
    0x0F25: 'Gem 6',
    0x0F2D: 'Gem 7',
    0x0F15: 'Gem 8',
    0x0F26: 'Gem 9',
    0x0F21: 'Gem 10'
}

LOOT_TOOLS = {
    'salvage_hook': 0x0EC4,  # Example item ID for salvage hook
    'hatchet': 0x0F52        # Example item ID for hatchet
}

# FUNCTIONS

def find_corpses():
    """Finds all nearby corpses matching the specified filter."""
    corpse_filter = Items.Filter()
    corpse_filter.IsCorpse = True
    corpse_filter.OnGround = True
    corpse_filter.RangeMax = 2
    corpse_filter.Graphics = List[int]([CORPSE_ID])
    corpse_filter.CheckIgnoreObject = True

    return Items.ApplyFilter(corpse_filter)

def should_loot_item(item):
    """Checks if the item should be looted based on its ItemID."""
    return item.ItemID in LOOTABLE_ITEMS

def loot_corpse(corpse):
    """Loots items from the given corpse based on the loot list."""
    looted_items = []
    for item in corpse.Contains:
        if should_loot_item(item):
            Items.Move(item, Player.Backpack, -1)  # Move stackable items (-1 for all)
            looted_items.append(LOOTABLE_ITEMS[item.ItemID])
            Misc.Pause(750)

    if looted_items:
        Misc.SendMessage(f"Looted: {', '.join(looted_items)}", 33)

def is_gold_still_on_corpse(corpse):
    """Checks if gold is still present on the corpse."""
    for item in corpse.Contains:
        if item.ItemID == GOLD_ID:
            return True
    return False

def use_tool(tool_name):
    """Uses the specified tool (e.g., hatchet, salvage hook) from the player's backpack."""
    tool_id = LOOT_TOOLS.get(tool_name)
    if Items.FindByID(tool_id, -1, Player.Backpack.Serial):
        Items.UseItemByID(tool_id, -1)
        Misc.Pause(200)


def getResources(corpse):
    """Collects resources from the specified corpse."""
    knife = Items.FindByID(0x0EC4, -1, Player.Backpack.Serial)
    scissors = Items.FindByID(0x0F9F, -1, Player.Backpack.Serial)
    
    if not knife or not scissors:
        Player.HeadMessage(64, "Need scissors or knife.")
        return
    
    Misc.Pause(250)
    Items.UseItem(knife)
    Misc.Pause(500)
    Target.TargetExecute(corpse)
    Misc.Pause(500)

    for item in corpse.Contains:
        if lootHides and item.ItemID == 0x1079:  # Hides
            Misc.SendMessage(f"Looting hides: {item.Serial}", 77)
            Items.Move(item, Player.Backpack.Serial, -1)
            Misc.Pause(1000)
            Items.UseItem(scissors)
            Misc.Pause(500)
            Target.TargetExecute(item)
            Misc.Pause(500)
        
        if lootScales and item.ItemID == 0x26B4:  # Scales
            Misc.SendMessage(f"Looting scales: {item.Serial}", 77)
            Items.Move(item, Player.Backpack.Serial, -1)
            Misc.Pause(1000)


def main():
    """Main function to find and loot corpses."""
    corpses = find_corpses()

    for corpse in corpses:
        Items.UseItem(corpse)
        Misc.Pause(500)
        loot_corpse(corpse)

        if getResourcesFlag:  # Check the toggle for resource collection
            getResources(corpse)

        if not is_gold_still_on_corpse(corpse):
            Misc.IgnoreObject(corpse)

# RUN SCRIPT
while True:
    main()
    Misc.Pause(1000)

