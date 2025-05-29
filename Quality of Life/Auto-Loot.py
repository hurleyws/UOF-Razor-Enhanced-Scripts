from System.Collections.Generic import List
from System import Int32 as int

getResourcesFlag = False  # Toggle resource collection on/off
lootHides = False  # Toggle for looting hides
lootScales = False  # Toggle for looting scales

# SETTINGS
CORPSE_ID = 0x2006
GOLD_ID = 0x0EED  # Gold Item ID

# LOOTABLE ITEMS
LOOTABLE_ITEMS = {
    0x26B4: 'Hide',
    0x0E86: 'Pickaxe',
    0x2100: 'Wisp',
    0x25B6: 'Pixie',
    0x2581: 'Centaur',
    0x1767: 'Cloth',
    0x0EED: 'Gold',
    0x0DCA: 'Net',
    0x099F: 'SOS',
    0x14F8: 'Rope',
    0xBB7C: 'Oxygen',
    0x1BF2: 'Ingot',
    0x1081: 'Horned Leather',
    0x14EC: 'Treasure Map',
    0x2831: 'Recipe',
    0x14F0: 'Power Scroll',
    0x0EF3: 'Blank Scroll',
    0x1F4C: 'Recall Scroll',
    0x2260: 'Skill Scroll',
    0x2AA2: 'Relic',
    0x0F21: 'Gem 1',
    0x0F16: 'Gem 2',
    0x0F19: 'Gem 3',
    0x0F13: 'Gem 4',
    0x0F10: 'Gem 5',
    0x0F25: 'Gem 6',
    0x0F2D: 'Gem 7',
    0x0F15: 'Gem 8',
    0x0F26: 'Gem 9',
    0x0F21: 'Gem 10',
    0x0F86: "root",
    0x0F7B: "moss",
    0x0F7A: "pearl",
    0x0F88: "shade",
    0x0F84: "garlic",
    0x0F85: "ginseng",
    0x0F8C: "ash",
    0x0F8D: "silk",
    0x0E41: 'chest 1',
    0x09AB: 'chest 2',
    0x0E7C: 'chest 3',
    0x0E40: 'chest 4',
    0x0DF8: 'wool',
    0x14FC: 'lockpick'
}

# EXCLUSION LIST (Items that should NEVER be looted even if they have a non-zero hue)
EXCLUSION_LIST = {
    0x19B9,  # ore
    0x141B, # orc mask
    0x13EC, #ringmail tunic  
    0x13EB, #gloves
    0x1544, #skullcap
    0x1711, #thighboots
    0x1F03, #robe
    0x5744, #worm
    0x1718, #wizard hat
    0x170F, #shoes
    0x170D, #sandals
    0x26B8, #seer powder
    0x1EA7, #obsidian
    
    
}

LOOT_TOOLS = {
    'salvage_hook': 0x0EC4,
    'hatchet': 0x0F52
}

# FUNCTIONS

def should_loot_item(item):
    """
    Checks if the item should be looted.
    - Ore (0x19B9) is only looted if it has a specific hue (bronze or agapite).
    - All other items must not be in the exclusion list and must be in the loot list or have a non-zero hue.
    """
    # Special case: allow specific ore hues
    if item.ItemID == 0x19B9:  # Ore
        return item.Hue in [0x06D8, 0x097E]  # bronze or agapite

    # Skip all other items in the exclusion list
    if item.ItemID in EXCLUSION_LIST:
        return False

    # Loot if explicitly listed or has a non-zero hue
    return item.ItemID in LOOTABLE_ITEMS or item.Hue != 0x0000

def find_corpses():
    """Finds all nearby corpses matching the specified filter."""
    corpse_filter = Items.Filter()
    corpse_filter.IsCorpse = True
    corpse_filter.OnGround = True
    corpse_filter.RangeMax = 2
    corpse_filter.Graphics = List[int]([CORPSE_ID])
    corpse_filter.CheckIgnoreObject = True

    return Items.ApplyFilter(corpse_filter)

def loot_corpse(corpse):
    """Loots items from the given corpse based on the loot list."""
    looted_items = []
    
    for item in corpse.Contains:
        if should_loot_item(item):
            Items.Move(item, Player.Backpack.Serial, -1)  # Move stackable items (-1 for all)
            item_name = LOOTABLE_ITEMS.get(item.ItemID, f"Unknown ({hex(item.ItemID)})")
            looted_items.append(item_name)
            Misc.Pause(750)

    if looted_items:
        Misc.SendMessage(f"Looted: {', '.join(looted_items)}", 33)
        Misc.Pause(500)

def is_gold_still_on_corpse(corpse):
    """Checks if gold is still present on the corpse."""
    return any(item.ItemID == GOLD_ID for item in corpse.Contains)

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
        if lootHides and item.ItemID == 0x1079 and item.Hue == 0x0000:  # Hides
            Misc.SendMessage(f"Looting hides: {item.Serial}", 77)
            Items.Move(item, Player.Backpack.Serial, -1)
            Misc.Pause(1000)
            Items.UseItem(scissors)
            Misc.Pause(500)
            Target.TargetExecute(Items.FindByID(0x1079,-1,Player.Backpack.Serial))
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

        if getResourcesFlag:
            getResources(corpse)

        if not is_gold_still_on_corpse(corpse):
            Misc.IgnoreObject(corpse)

# RUN SCRIPT
while True:
    main()
    Misc.Pause(1000)
