from System.Collections.Generic import List
from System import Int32 as int

getResourcesFlag = False
lootHides = False
lootScales = False

CORPSE_ID = 0x2006
GOLD_ID = 0x0EED

LOOTABLE_ITEMS = {
    0x26B4: 'Hide', 0x0E86: 'Pickaxe', 0x2100: 'Wisp', 0x25B6: 'Pixie',
    0x2581: 'Centaur', 0x1767: 'Cloth', 0x0EED: 'Gold', 0x0DCA: 'Net',
    0x099F: 'SOS', 0x14F8: 'Rope', 0xBB7C: 'Oxygen', 0x1BF2: 'Ingot',
    0x1081: 'Horned Leather', 0x14EC: 'Treasure Map', 0x2831: 'Recipe',
    0x14F0: 'Power Scroll', 0x0EF3: 'Blank Scroll', 0x1F4C: 'Recall Scroll',
    0x2260: 'Skill Scroll', 0x2AA2: 'Relic', 0x0F21: 'Gem',
    0x0F16: 'Gem 2', 0x0F19: 'Gem 3', 0x0F13: 'Gem 4', 0x0F10: 'Gem 5',
    0x0F25: 'Gem 6', 0x0F2D: 'Gem 7', 0x0F15: 'Gem 8', 0x0F26: 'Gem 9',
    0x0F86: "root", 0x0F7B: "moss", 0x0F7A: "pearl", 0x0F88: "shade",
    0x0F84: "garlic", 0x0F85: "ginseng", 0x0F8C: "ash", 0x0F8D: "silk",
    0x0E41: 'Paragon Chest 1', 0x09AB: 'Paragon Chest 2', 0x0E7C: 'Paragon Chest 3',
    0x0E40: 'Paragon Chest 4', 0x0DF8: 'wool', 0x14FC: 'lockpick'
}


EXCLUSION_LIST = {
    0x19B9, 0x141B, 0x13EC, 0x13EB, 0x1544, 0x1711, 0x1F03, 0x5744, 0x1718,
    0x170F, 0x170D, 0x26B8, 0x1EA7, 0x1516, 0x1539, 0x1EFD, 0x1F7B,
    0x0672, 0x1517, 0x152E, 0x0C65
}

LOOT_TOOLS = {
    'salvage_hook': 0x0EC4,
    'hatchet': 0x0F52
}

def should_loot_item(item):
    item_id = item.ItemID
    item_hue = item.Hue

    if item_id == 0x19B9:
        return item_hue in [0x06D8, 0x097E]
    if item_id in EXCLUSION_LIST:
        return False
    return item_id in LOOTABLE_ITEMS or item_hue != 0x0000

def find_corpses():
    corpse_filter = Items.Filter()
    corpse_filter.IsCorpse = True
    corpse_filter.OnGround = True
    corpse_filter.RangeMax = 2
    corpse_filter.Graphics = List[int]([CORPSE_ID])
    corpse_filter.CheckIgnoreObject = True

    return Items.ApplyFilter(corpse_filter)

def loot_corpse(corpse):
    looted_items = []
    paragon_chest_ids = {0x0E41, 0x09AB, 0x0E7C, 0x0E40}
    
    for item in corpse.Contains:
        if not should_loot_item(item):
            continue

        is_paragon_chest = item.ItemID in paragon_chest_ids

        if is_paragon_chest:
            chest_weight = item.Weight
            projected_weight = Player.Weight + chest_weight

            if projected_weight > Player.MaxWeight:
                weight_to_free = projected_weight - Player.MaxWeight
                gold_needed = int(weight_to_free * 50)  # 50 gold = 1 stone

                gold_coins = Items.FindByID(GOLD_ID, -1, Player.Backpack.Serial)
                total_gold_available = Items.BackpackCount(GOLD_ID,-1)

                if total_gold_available >= gold_needed:
                    Items.MoveOnGround(gold_coins, gold_needed, Player.Position.X, Player.Position.Y, Player.Position.Z)
                    Misc.Pause(1000)
                    Misc.SendMessage(f"Dropped gold to make room for Paragon Chest ({chest_weight} stones)", 33)
                    Misc.Pause(500)
                else:
                    Misc.SendMessage(f"Not enough gold to drop for chest ({chest_weight} stones) – skipping", 33)
                    Misc.Pause(500)
                    continue  # Skip looting chest

            # Weight is now OK – loot chest
            Items.Move(item, Player.Backpack.Serial, -1)
            Misc.Pause(1000)
            continue

        # Regular item
        Items.Move(item, Player.Backpack.Serial, -1)
        Misc.Pause(1000)

def is_gold_still_on_corpse(corpse):
    return any(item.ItemID == GOLD_ID for item in corpse.Contains)

def getResources(corpse):
    knife = Items.FindByID(0x0EC4, -1, Player.Backpack.Serial)
    scissors = Items.FindByID(0x0F9F, -1, Player.Backpack.Serial)

    if not knife or not scissors:
        Player.HeadMessage(64, "Need scissors or knife.")
        Misc.Pause(300)
        return

    Misc.Pause(250)
    Items.UseItem(knife)
    Misc.Pause(500)
    Target.TargetExecute(corpse)
    Misc.Pause(500)

    corpse_items = corpse.Contains
    for item in corpse_items:
        if lootHides and item.ItemID == 0x1079 and item.Hue == 0x0000:
            Misc.SendMessage(f"Looting hides: {item.Serial}", 77)
            Items.Move(item, Player.Backpack.Serial, -1)
            Misc.Pause(1000)
            Items.UseItem(scissors)
            Misc.Pause(500)
            Target.TargetExecute(Items.FindByID(0x1079, -1, Player.Backpack.Serial))
            Misc.Pause(500)

        if lootScales and item.ItemID == 0x26B4:
            Misc.SendMessage(f"Looting scales: {item.Serial}", 77)
            Items.Move(item, Player.Backpack.Serial, -1)
            Misc.Pause(1000)

def main():
    corpses = find_corpses()
    if not corpses:
        Misc.Pause(500)
        return

    for corpse in corpses:
        Items.UseItem(corpse)
        Misc.Pause(400)
        loot_corpse(corpse)

        if getResourcesFlag:
            getResources(corpse)

        if not is_gold_still_on_corpse(corpse):
            Misc.IgnoreObject(corpse)

# RUN LOOP
while True:
    main()
    Misc.Pause(800)
