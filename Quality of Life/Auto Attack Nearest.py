from System.Collections.Generic import List
from System import Byte

filterExample = Mobiles.Filter()
filterExample.Enabled = True
filterExample.Name != "Watches"
#filterExample.IsHuman = True # Optional
#filterExample.Bodies = List[int]([0x0190])) #optional, use mobile IDs
filterExample.Notorieties = List[Byte](bytes([3,4,6])) # optional, numbers = notoritety codes

for x in range (1):
    filterExampleList = Mobiles.ApplyFilter(filterExample)  # Refresh the list of mobiles that match the filter
    more_filtered = list(filter(lambda mob: mob.Serial != 0x00029C76 and mob.Serial != 0x00136CD2, list(filterExampleList)))
    if len(more_filtered) == 0: Misc.Pause(10); continue
    sorted_by_distance = list(sorted(more_filtered , key=lambda mob: Player.DistanceTo(mob), reverse=False ))
    filterSelection = sorted_by_distance[0]
    if filterSelection:
        Player.Attack(filterSelection)
        Misc.Pause(500)
