from System.Collections.Generic import List
from System import Int32 as int


def stockRegs():
    root = Items.BackpackCount(0x0F7A,-1)
    moss = Items.BackpackCount(0x0F7B,-1)
    pearl = Items.BackpackCount(0x0F86,-1)
  
    
    if root < 15:
        Items.Move(Items.FindByID(0x0F7A,-1,0x42E88440),Player.Backpack.Serial,15-root)
        Misc.Pause(1000)
    
    if moss < 15:
        Items.Move(Items.FindByID(0x0F7B,-1,0x42E88440),Player.Backpack.Serial,15-moss)
        Misc.Pause(1000)
        
    if pearl < 15:
        Items.Move(Items.FindByID(0x0F86,-1,0x42E88440),Player.Backpack.Serial,15-pearl)
        Misc.Pause(1000)
        
    else:
        Player.HeadMessage(64,"Regs look good")
        Misc.Pause(500)

# World Save Handling
def worldSave():
    if Journal.SearchByType('The world will save in 1 minute.', 'System') or Journal.SearchByType('pause', 'Regular'):
        Misc.Pause(700)
        Misc.SendMessage('Pausing for world save or player-called break.', 33)
        while not Journal.SearchByType('World save complete.', 'System') and not Journal.SearchByType('play', 'Regular'):
            Misc.Pause(1000)
        Misc.Pause(2500)
        Misc.SendMessage('Continuing run', 33)
        Misc.Pause(1000)
    Journal.Clear()

# Re-Tooling Process
def reTool():
    tool_needed = 2  # Number of tools to keep in backpack

    # Re-stock smith hammers if below required count
    if Items.ContainerCount(Player.Backpack.Serial, 0x13E3, -1) < tool_needed:
        while Items.ContainerCount(Player.Backpack.Serial, 0x13E3, -1) < tool_needed:
            Items.UseItemByID(0x1EB8, 0x0000)  # Open smith tools container
            Misc.Pause(500)
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, 93)  # Select Smith Hammer
            Misc.Pause(2000)

    # Re-stock tinker tools if below required count
    if Items.ContainerCount(Player.Backpack.Serial, 0x1EB8, -1) < tool_needed:
        while Items.ContainerCount(Player.Backpack.Serial, 0x1EB8, -1) < tool_needed:
            Items.UseItemByID(0x1EB8, 0x0000)  # Open tinker tools container
            Misc.Pause(200)
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, 23)  # Select Tinker Tool
            Misc.Pause(2000)

# Crafting and Storage Process
def main():
    while True:
        # Recalling to anvil
        Player.ChatSay("[recall Anvil")
        Misc.Pause(2500)

        # Use smith hammer and set to iron
        Items.UseItemByID(0x13E3, 0x0000)
        Misc.Pause(500)
        Gumps.WaitForGump(949095101, 10000)
        Gumps.SendAction(949095101, 7)  # Set material to iron
        Gumps.WaitForGump(949095101, 10000)
        Gumps.SendAction(949095101, 6)

        # Crafting while ingots are available
        while Items.BackpackCount(0x1BF2, -1) > 25:
            worldSave()  # Check for world save
            reTool()     # Ensure tools are stocked

            # Craft item
            Items.UseItemByID(0x13E3, 0x0000)
            Misc.Pause(500)
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, 36)  # Craft option
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, 16)
            Misc.Pause(1500)
            Journal.Clear()

            # Recycle unwanted items
            while Items.BackpackCount(0x0F52, -1) > 0:
                Items.UseItemByID(0x13E3, 0x0000)
                Misc.Pause(500)
                Gumps.WaitForGump(949095101, 10000)
                Gumps.SendAction(949095101, 14)  # Recycle option
                Target.WaitForTarget(2000)
                item_to_recycle = Items.FindByID(0x0F52, -1, Player.Backpack.Serial)
                if item_to_recycle:
                    Target.TargetExecute(item_to_recycle)
                    Misc.Pause(350)
                Misc.Pause(100)

        # Recalling to storage (Winter)
        Player.ChatSay("[recall Winter Lodge")
        Misc.Pause(2500)

        # Pathfinding to storage location
        Player.PathFindTo(6802, 3901, 12)
        Misc.Pause(1500)
        door = Items.FindBySerial(0x42F89EDC)
        if door.ItemID == 0x0677:
            Items.UseItem(door)
            Misc.Pause(500)
        Player.PathFindTo(6803, 3899, 17)
        Misc.Pause(2000)      
        Items.UseItem(0x42E88440) #Open box by door
        Misc.Pause(1000)
        stockRegs()

        # Transfer items to storage
        Items.UseItem(0x42E87E92)
        Misc.Pause(500)
        ingots_in_storage = Items.FindByID(0x1BF2, -1, 0x42E87E92)
        if ingots_in_storage:
            available_space = 2500 - Items.BackpackCount(0x1BF2, -1)
            Items.Move(ingots_in_storage, Player.Backpack.Serial, available_space)
            Misc.Pause(1000)
        else:
            # Handle the case where no ingots are found
            Player.PathFindTo(2138, 338, 7)
            Misc.Pause(4000)
            Player.Walk("West")
            Misc.Pause(500)
            Misc.ScriptStop("runImbuologist.py")

# RUN SCRIPT
main()