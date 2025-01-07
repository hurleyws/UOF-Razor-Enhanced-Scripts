from System import Int32 as int
from System.Collections.Generic import List

# Define constants
logID = 0x1BDD
boardID = 0x1BD7
corpse_ID = 0x2006
hide_ID = 0x1081
rawhide_ID = 0x1079
gold_ID = 0x0EED
feathers_ID = 0x1BD1
wood_ID = 0x1BDD
meat_ID = 0x09F1
bone_ID = 0x0F7E
statue_ID = 0x25BF
lootList = [hide_ID, gold_ID, wood_ID, meat_ID, rawhide_ID, bone_ID, statue_ID]

def CheckEnemy():
    # Create a filter for enemies
    enemyFilter = Mobiles.Filter()
    enemyFilter.Bodies = List[int]([0x00E1,0x00ED])  # Replace with appropriate mob IDs
    enemyFilter.RangeMax = 15  # Set the search range for enemies
    enemyList = Mobiles.ApplyFilter(enemyFilter)
    
    while enemyList.Count > 0:  # While there are enemies in the list
        enemy = enemyList[0]  # Get the first enemy
        if enemy:
            Misc.SendMessage("Engaging " + enemy.Name)
            Misc.Pause(500)
            Player.Attack(enemy)
            Misc.Pause(500)
            Misc.SendMessage("Attacking")
            Misc.Pause(500)

            # Combat loop
            while enemy and enemy.Hits > 0:
                if Player.DistanceTo(enemy) > 1:
                    Misc.SendMessage("Moving closer to " + enemy.Name)
                    Misc.Pause(500)
                    enemyPosition = enemy.Position
                    enemyCoords = PathFinding.Route()
                    enemyCoords.MaxRetry = 5
                    enemyCoords.StopIfStuck = False
                    enemyCoords.X = enemyPosition.X
                    enemyCoords.Y = enemyPosition.Y - 1
                    PathFinding.Go( enemyCoords )
                    Misc.Pause(500)
                Player.Attack(enemy)
                Misc.Pause(500)
                enemy = Mobiles.FindBySerial(enemy.Serial)  # Update enemy status

            # Looting phase
            LootCorpses()
        
        # Refresh the enemy list
        enemyList = Mobiles.ApplyFilter(enemyFilter)

def LootCorpses():
    # Filter for corpses
    corpseFilter = Items.Filter()
    corpseFilter.Graphics = List[int]([corpse_ID])  # Corpse graphic ID
    corpseFilter.Movable = False
    corpses = Items.ApplyFilter(corpseFilter)

    for corpse in corpses:
        Misc.SendMessage("Looting corpse at " + str(corpse.Position))
        Items.UseItem(corpse)  # Open corpse
        Misc.Pause(500)

        # Loot items from the corpse
        for item in corpse.Contains:
            if item.ItemID in lootList:
                Misc.SendMessage("Looting item: " + str(item.Name))
                Items.Move(item.Serial, Player.Backpack.Serial, 0)
                Misc.Pause(500)

        # Skin the corpse if a knife is available
        knife = Items.FindByID(0x0EC4, -1, Player.Backpack.Serial)  # Knife ID
        if knife:
            Items.UseItem(knife)
            Misc.Pause(500)
            Target.TargetExecute(corpse)
            Misc.Pause(500)

# Run the enemy check and combat loop
CheckEnemy()
