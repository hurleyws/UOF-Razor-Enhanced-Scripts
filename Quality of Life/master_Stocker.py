import re

#######################################################################
# Define restocking needs and runebook serials for each character
restock_requirements = {
    "Alyer Base": {
        "items": {"root": 50, "moss": 50, "pearl": 50, "ash": 50, "garlic": 50, "shade": 50, "gins": 50, "silk": 50, "bandages": 100, "emergency_charges": 10},
        "runebook_serial": 0x4106CD0C,  # Replace
        "index": 5  # Replace with the correct index for Alyer Base
    },
    "Hurlpea": {
        "items": {"root": 100, "moss": 100, "pearl": 100, "ash": 30, "garlic": 30, "shade": 100, "gins": 30, "silk": 50, "bandages": 0, "emergency_charges": 100},
        "runebook_serial": 0x476C14DB,  # Replace
        "index": 6  # Replace with the correct index for Hurlpea
    },
    "Realtree": {
        "items": {"root": 50, "moss": 50, "pearl": 50, "ash": 30, "garlic": 30, "shade": 30, "gins": 30, "silk": 30, "bandages": 0, "emergency_charges": 10},
        "runebook_serial": 0x41769B12,  # Replace
        "index": 4  # Replace with the correct index for Realtree
    },
    "Servant": {
        "items": {"root": 50, "moss": 50, "pearl": 50, "ash": 30, "garlic": 30, "shade": 30, "gins": 30, "silk": 30, "bandages": 0, "emergency_charges": 10},
        "runebook_serial": 0x4297635A,
        "index": 6  # Replace with the correct index for Servant
    },
    # Add other characters and their needs here
}
########################################################################

#gold definitions
gold_id = 0x0EED
banker_serial = 0x000B03AE

#skill scroll definitions
skill_scroll_id = 0x2260
skill_scroll_bookcase_serial = 0x406177BE

#gem storage definitions
gem_storage_serial = 0x4189A2CC
gem_ids = [0x0F21,0x0F16,0x0F19,0x0F13,0x0F10,0x0F25,0x0F2D,0x0F15,0x0F26]

#glowing rune definitions
rune_storage_serial = 0x423A9768
rune_ids = [0x483B,0x483E,0x4841,0x4844,0x4847,0x484A,0x484D,0x4850,0x4853,0x4856,0x4859,0x485C,0x485F,0x4862,0x4865,0x4868,0x486B,0x4871,0x486E,0x4874,0x4877,0x487A,0x487D,0x4880,0x4883]

#power scroll definitions
power_scroll_bookcase_serial = 0x41899B34
power_scroll_id = 0x14F0

arms_ids = [
    0x0DF2, 0x0F49, 0x0F4D, 0x0F4D, 0x140E, 0x0F47, 0x0DF0, 0x13B2, 0x0F5E, 
    0x1B72, 0x1B73, 0x13F6, 0x13BB, 0x13BE, 0x13BF, 0x0EC3, 0x0EC3, 0x1408, 
    0x13B4, 0x0F50, 0x1441, 0x1441, 0x0F52, 0x0F4B, 0x0F4B, 0x0F45, 0x0F45, 
    0x13F8, 0x13F8, 0x13F8, 0x143E, 0x143D, 0x0F43, 0x1B76, 0x13FD, 0x140A, 
    0x13FF, 0x1B74, 0x1B79, 0x1B79, 0x1401, 0x13FB, 0x1C06, 0x1C0A, 0x1C0A, 
    0x1DB9, 0x13C6, 0x13C7, 0x13CB, 0x1C00, 0x1C08, 0x13CD, 0x13CC, 0x0F62, 
    0x0F61, 0x0F5C, 0x143B, 0x1B7B, 0x1B7B, 0x140C, 0x1F0B, 0x0E86, 0x0E87, 
    0x1C04, 0x1412, 0x1415, 0x1410, 0x1414, 0x1413, 0x1411, 0x0E89, 0x13EB, 
    0x13F0, 0x13EE, 0x13EC, 0x13B6, 0x13B6, 0x0E81, 0x1403, 0x1C02, 
    0x1C0C, 0x13D5, 0x13D5, 0x13D6, 0x13DA, 0x13DC, 0x13DB, 0x1443, 0x13B9, 
    0x13B0, 0x1405, 0x1439, 0x1407, 0x1B7A, 0x1C04, 0x0F52, 0x1544
]


#supply counts
IDchest_serial = 0x43DC9B86
regchest = Items.FindBySerial(0x4043C469)
tinkchest = Items.FindBySerial(0x43DE1F06)
root = Items.BackpackCount(0x0F7A,-1)
moss = Items.BackpackCount(0x0F7B,-1)
pearl = Items.BackpackCount(0x0F86,-1)
ash = Items.BackpackCount(0x0F8C,-1)
garlic = Items.BackpackCount(0x0F84,-1)
shade = Items.BackpackCount(0x0F88,-1)
gins = Items.BackpackCount(0x0F85,-1)
silk = Items.BackpackCount(0x0F8D,-1)
bandages = Items.BackpackCount(0x0E21,-1)
greater_heal = Items.BackpackCount(0x0F0C,-1)
greater_cure = Items.BackpackCount(0x0F07,-1)
greater_strength = Items.BackpackCount(0x0F09,-1)
greater_refresh = Items.BackpackCount(0x0F0B,-1)
greater_explosion = Items.BackpackCount(0x0F0D,-1)
empty_bottle = Items.BackpackCount(0x0F0E,-1)
flute = Items.BackpackCount(0x2805,-1)
emergency_charge_id = 0x1F4C

Journal.Clear()
emergency_charges = 0
Items.UseItem(regchest)
Misc.Pause(500)


# Function to restock an item
def restock_item(item_id, current_quantity, desired_quantity, container_serial, destination_serial, runebook_serial, x=1, y=1):
    if current_quantity < desired_quantity:
        quantity_to_move = desired_quantity - current_quantity

        # Special case for restocking emergency charges
        if item_id == emergency_charge_id:
            destination_serial = runebook_serial

        Items.Move(Items.FindByID(item_id, -1, container_serial), destination_serial, quantity_to_move)
        Misc.Pause(1000)

# Item ID Mapping
item_ids = {
    "root": 0x0F7A, "moss": 0x0F7B, "pearl": 0x0F86, "ash": 0x0F8C,
    "garlic": 0x0F84, "shade": 0x0F88, "gins": 0x0F85, "silk": 0x0F8D,
    "bandages": 0x0E21, "emergency_charges": 0x1F4C
}

# Current quantities for each item
current_quantities = {"root": root, "moss": moss, "pearl": pearl, "ash": ash, "garlic": garlic, "shade": shade, "gins": gins, "silk": silk, "bandages": bandages, "emergency_charges": emergency_charges}

# Restock items based on the current characters requirements
character_name = Player.Name
if character_name in restock_requirements:
    character_config = restock_requirements[character_name]
    runebook_serial = character_config["runebook_serial"]
    index = character_config["index"]  # Get the correct index for this character
    
    runebook = Items.FindBySerial(runebook_serial)
    rbcharges = Items.GetPropStringByIndex(runebook, index)  # Use the character-specific index
    Misc.SendMessage(rbcharges)
    
    parts = rbcharges.split()  # parts = ["Charges", "10/10"]
    charge_info = parts[1]  # charge_info = "10/10"
    numerator, _ = charge_info.split('/')  # numerator = "10"
    emergency_charges = int(numerator)
    
    # Update current quantities for each item
    current_quantities["emergency_charges"] = emergency_charges

    # Loop through each item and restock as needed
    for item_name, desired_quantity in character_config["items"].items():
        item_id = item_ids[item_name]
        restock_item(item_id, current_quantities[item_name], desired_quantity, regchest.Serial, Player.Backpack.Serial, runebook_serial)
else:
    Player.HeadMessage(64, "No restock configuration for this character.")



# Special handling for flute, as its not part of the generic restocking
if Player.Name in ["Alyer Base", "SnukeInSniz"] and flute < 1:
    Items.UseItem(tinkchest)
    Misc.Pause(500)
    Items.UseItem(0x40894A2D)
    Misc.Pause(500)
    Items.Move(Items.FindByID(0x2805,-1,0x40894A2D),Player.Backpack.Serial,1,156, 64)
    Misc.Pause(1000) 


# Function to collect all items of a specific ID or ID set
def collect_items(ids):
    return [item for item in Player.Backpack.Contains if item.ItemID in ids]

def unload_arms(ids, destination_serial):
    items_to_unload = collect_items(ids)
    if items_to_unload:
        Player.HeadMessage(64, "Unloading arms...")
        for item in items_to_unload:
            Items.Move(item.Serial, destination_serial, item.Amount)
            Misc.Pause(1000)    
            
unload_arms(arms_ids, IDchest_serial)

# Unload Skill Scrolls
skill_scrolls = collect_items([skill_scroll_id])
if skill_scrolls:
    Player.HeadMessage(64, "Skill scroll found!")
    Player.PathFindTo(6786, 3890, 17)
    while Player.DistanceTo(Items.FindBySerial(skill_scroll_bookcase_serial)) > 1:
        Misc.Pause(500)
    for scroll in skill_scrolls:
        Items.Move(scroll, skill_scroll_bookcase_serial, -1)
        Misc.Pause(1000)


# Unload Gems
gems = collect_items(gem_ids)
if gems:
    Player.HeadMessage(64, "Gems found!")
    Player.PathFindTo(6779, 3891, 17)
    while Player.DistanceTo(Items.FindBySerial(0x4189A2CC)) > 2:
        Misc.Pause(500)
    for gem in gems:
        Items.Move(gem, gem_storage_serial, -1)
        Misc.Pause(1000)

# Unload Glowing Runes
glowing_runes = collect_items(rune_ids)
if glowing_runes:
    Player.HeadMessage(64, "Glowing rune found!")
    Player.PathFindTo(6785, 3895, 17)
    while Player.DistanceTo(Items.FindBySerial(0x423A9768)) > 1:
        Misc.Pause(500)
    for rune in glowing_runes:
        Items.Move(rune, rune_storage_serial, 1)
        Misc.Pause(1000)
        if Journal.SearchByType("No more runes of that type can be stored.", "System"):
            runeletter = Items.GetPropStringByIndex(rune, 0)
            Player.HeadMessage(64, "We dont need anymore " + runeletter)
            Misc.Pause(500)
            Items.Move(rune, 0x408E8DA8, 1, 130, 80)
            Misc.Pause(1000)
            Journal.Clear()

# Unload Treasure Maps
treasure_maps = collect_items([0x14EC])
if treasure_maps:
    Player.HeadMessage(64, "Tmap found!")
    Player.PathFindTo(6785, 3896, 17)
    while Player.DistanceTo(Items.FindBySerial(0x408E8DA8)) > 1:
        Misc.Pause(500)
    Items.UseItem(0x408E8DA8)
    Misc.Pause(500)
    for tmap in treasure_maps:
        # Read tmap and sort
        linelevel = Items.GetPropStringByIndex(tmap, 1)
        match = re.search(r'Level (\d+)', linelevel)
        if match:
            level = int(match.group(1))
            if level in range(1, 7):
                storage_serial = [0x40C2F465, 0x40C2F467, 0x40C2F466, 0x40C2F46A, 0x40C2F464, 0x40C2F469][level - 1]
                Items.Move(tmap, storage_serial, 1)
                Misc.Pause(1000)     
            
Player.HeadMessage(64,"All items have been stored.")