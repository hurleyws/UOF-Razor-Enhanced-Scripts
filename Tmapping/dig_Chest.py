tmap_id = 0x14EC  # Treasure Map ID

# Journal messages for different outcomes
msg_blocked = [
    "The chest can't be dug up because you are standing on top of it.",
    "You have found the treasure chest but something is keeping it from being dug up."
]
msg_no_treasure = "You dig but no treasure can be found here."

# Directions for movement (Clockwise: North, East, South, West, NE, SE, SW, NW)
directions = [
    (0, -1),  # North
    (1, 0),   # East
    (0, 1),   # South
    (-1, 0),  # West
    (1, -1),  # Northeast
    (1, 1),   # Southeast
    (-1, 1),  # Southwest
    (-1, -1)  # Northwest
]  

# Find treasure map in backpack
tmap = Items.FindByID(tmap_id, -1, Player.Backpack.Serial)

if not tmap:
    Misc.SendMessage("No treasure map found in backpack!", 33)
    exit()

# Use the treasure map
Items.UseItem(tmap.Serial)
Misc.Pause(1000)

# Context menu interaction
Misc.WaitForContext(tmap.Serial, 10000)
Misc.ContextReply(tmap.Serial, 2)
Target.WaitForTarget(10000, False)

# Digging routine
start_x, start_y, start_z = Player.Position.X, Player.Position.Y, Player.Position.Z
search_attempts = 0

while search_attempts < len(directions):  # Try all 8 surrounding tiles
    Journal.Clear()
    
    # Calculate new tile coordinates
    move_x, move_y = directions[search_attempts]
    dig_x, dig_y = start_x + move_x, start_y + move_y

    # Execute digging attempt
    Misc.SendMessage(f"Trying to dig at ({dig_x}, {dig_y})", 55)
    Target.TargetExecute(dig_x, dig_y, start_z)
    Misc.Pause(2000)  # Give time for the message to appear

    # Check the journal for messages
    if Journal.SearchInList(msg_blocked):
        Misc.SendMessage("Blocked! Moving to a new tile...", 33)
        Player.WalkRandom(1)  # Move randomly to a new tile and try again
        Misc.Pause(1500)
    elif Journal.Search(msg_no_treasure):
        Misc.SendMessage("No treasure here, trying next tile.", 55)
    else:
        Misc.SendMessage("Chest found or digging successful!", 75)
        break  # Stop script when chest is found

    Misc.Pause(1000)
    search_attempts += 1

Misc.SendMessage("Treasure hunting complete!", 75)
