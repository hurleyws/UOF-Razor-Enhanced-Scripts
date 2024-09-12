from System.Collections.Generic import List
from System import Int32 as int

def findMobileByIDInRange(mobileID, range):
    mobileFilter = Mobiles.Filter()
    mobileFilter.RangeMax = range
    mobileFilter.Bodies = List[int]((0x0009))
    return Mobiles.Select(Mobiles.ApplyFilter(mobileFilter), 'Nearest') # Returns found mobile or None
    
Spells.CastMagery( 'Summon Daemon' )
Misc.Pause(4000)
# Is this the one line of code thats needed? Do we even need all the filter stuff?    
vivy = findMobileByIDInRange(0x0009, 2)

Misc.PetRename( vivy , "ManBearPig" )  
Misc.Pause(500)
CUO.PlayMacro('Vivify')
Misc.Pause(500)
Target.TargetExecute(vivy)
Misc.Pause(500)
Player.ChatSay(75,"All guard me")
Misc.Pause(500)
Player.UseSkill('Meditation')
Player.HeadMessage(75,"Meditating")
