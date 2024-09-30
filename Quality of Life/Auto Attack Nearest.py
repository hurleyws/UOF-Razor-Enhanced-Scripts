from System.Collections.Generic import List
from System import Byte

# Set up the mobile filter
filterExample = Mobiles.Filter()
filterExample.Enabled = True
filterExample.Notorieties = List[Byte](bytes([3, 4, 6]))  # Notoriety codes

while True:  # Run indefinitely
    filterExampleList = Mobiles.ApplyFilter(filterExample)  # Refresh the list of mobiles that match the filter

    # Find the closest mobile
    closest_mobile = None
    closest_distance = float('inf')

    for mobile in filterExampleList:
        if mobile:  # Ensure the mobile is valid and alive
            distance = Player.DistanceTo(mobile)
            if distance < closest_distance:
                closest_distance = distance
                closest_mobile = mobile

    # If we found a closest mobile, attack it
    if closest_mobile:
        Player.Attack(closest_mobile)
        Misc.Pause(500)  # Pause between attacks
    else:
        Misc.Pause(1000)  # If no mobiles found, wait before refreshing
