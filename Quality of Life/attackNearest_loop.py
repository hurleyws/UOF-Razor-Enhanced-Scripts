from System.Collections.Generic import List
from System import Byte

# Setup the filter
filterExample = Mobiles.Filter()
filterExample.Enabled = True
filterExample.CheckLineOfSight = True
filterExample.Notorieties = List[Byte](bytes([3, 4, 6]))  # Notoriety codes

while True:
    # Refresh the list of filtered mobs
    filterExampleList = Mobiles.ApplyFilter(filterExample)

    nearest_mob = None
    nearest_distance = float('inf')  # Set the initial distance to a very large number

    # Iterate through the filtered list to find the nearest mob
    for mob in filterExampleList:
        if mob.Serial != 0x00029C76 and mob.Serial != 0x00136CD2:  # Exclude certain mobs by serial
            distance = Player.DistanceTo(mob)  # Calculate distance to the mob

            # Check if this mob is closer than the previously found mob
            if distance < nearest_distance:
                nearest_mob = mob
                nearest_distance = distance

    # If a valid nearest mob is found, attack it
    if nearest_mob:
        Player.Attack(nearest_mob)
        Misc.Pause(1500)  # Wait for the attack to take place

    Misc.Pause(300)  # Small pause before the next iteration
