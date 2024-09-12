from System.Collections.Generic import List
from System import Byte
filterExample = Mobiles.Filter()
filterExample.Enabled = True
filterExample.RangeMin = 0 # optional

#filterExample.IsHuman = True # Optional
#filterExample.Bodies = List[int]([0x0190])) #optional, use mobile IDs
filterExample.Notorieties = List[Byte](bytes([3,4,6])) # optional, numbers = notoritety codes
filterExampleList = Mobiles.ApplyFilter(filterExample)

filterSelection = Mobiles.Select(filterExampleList, 'Nearest') # multiple selectors possible

if filterSelection:    
    Spells.CastMagery( 'Energy Bolt' )
    Target.WaitForTarget( 2000, False )
    Target.TargetExecute(filterSelection)




    
    