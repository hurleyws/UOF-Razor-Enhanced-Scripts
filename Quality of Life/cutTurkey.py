from System import Int32 as int
from System import Byte
from System.Collections.Generic import List

corpseFilter = Items.Filter()
corpseFilter.OnGround = True
corpseFilter.RangeMax = 2
corpseFilter.Graphics = List[int]([0x2006])
corpseFilter.CheckIgnoreObject = True
corpse_list = Items.ApplyFilter(corpseFilter)


while True:

    for i in corpse_list:
        if i:
            Dress.DressFStart()
            Misc.Pause(500)
            knife = Items.FindBySerial(0x412AA370)
            Items.UseItem(knife)
            Misc.Pause(500)
            Target.TargetExecute(i)
            Misc.Pause(500)
            Misc.IgnoreObject(i)
        Misc.Pause(500)
    corpse_list = Items.ApplyFilter(corpseFilter)

