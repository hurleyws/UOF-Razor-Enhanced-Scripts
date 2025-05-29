oreBox = 0x42C25944
intakeBox = 0x403DC417
oreID = 0x19B9  # Ore ID
logID = 0x1BDD  # Log ID
oreMoveAmount = 250
logMinThreshold = 500
logMaxAmount = 1000

def get_item_count(container, item_id):
    """Returns the count of a specific item inside a container."""
    items = Items.FindByID(item_id, -1, container)
    if items:
        return Items.ContainerCount(container, item_id, -1)
    return 0

def move_item(source, destination, item_id, amount):
    """Moves a specified amount of an item from source to destination."""
    item = Items.FindByID(item_id, -1, source)
    if item:
        Items.Move(item, destination, amount)
        Misc.Pause(1000)

# Open the ore and intake box
Items.UseItem(oreBox)
Misc.Pause(500)
Items.UseItem(intakeBox)
Misc.Pause(500)

# Check if intake box already contains ore
if get_item_count(intakeBox, oreID) > 0:
    Misc.SendMessage("Ore is already in the intake box. Stopping script.", 33)
else:
    # Ensure at least 500 logs are in the intake box before starting
    logCount = get_item_count(intakeBox, logID)
    if logCount < logMinThreshold:
        Misc.SendMessage("Not enough logs in intake box. Stopping script.", 33)
    else:
        # Move initial 250 ore to intake box
        move_item(oreBox, intakeBox, oreID, oreMoveAmount)

        while True:
            # Wait until the intake box is empty (ore has been processed)
            while get_item_count(intakeBox, oreID) > 0:
                Misc.Pause(2000)  # Check every 2 seconds
            
            # Check log count in intake box
            logCount = get_item_count(intakeBox, logID)
            if logCount < logMinThreshold:
                logsToMove = logMaxAmount - logCount  # Restore logs to 1000
                move_item(oreBox, intakeBox, logID, logsToMove)

            # Ensure intake box is empty before moving next ore batch
            if get_item_count(intakeBox, oreID) == 0 and get_item_count(intakeBox, logID) >= logMinThreshold:
                move_item(oreBox, intakeBox, oreID, oreMoveAmount)
            else:
                Misc.SendMessage("Issue detected with intake box. Stopping script.", 33)
                break
