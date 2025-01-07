from System.Collections.Generic import List
from System import Byte

# Define the filter for mobs
mobFilter = Mobiles.Filter()
mobFilter.Enabled = True
mobFilter.RangeMin = 0  # Minimum range to check
mobFilter.RangeMax = 12  # Maximum range to check
mobFilter.Notorieties = List[Byte](bytes([3, 4, 6]))  # Filter by notoriety (e.g., neutral, enemy)

# Apply the filter to get a list of matching mobs
filteredMobs = Mobiles.ApplyFilter(mobFilter)

# Select the nearest mob from the filtered list
nearestMob = Mobiles.Select(filteredMobs, 'Nearest')  # You can use other selection types, such as 'Strongest' or 'Weakest'

if nearestMob:    
    Spells.CastMagery('Energy Bolt')
    Target.WaitForTarget(2000, False)
    Target.TargetExecute(nearestMob)
