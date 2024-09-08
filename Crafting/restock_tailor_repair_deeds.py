player_pack = Player.Backpack.Serial

def get_item_by_id(item_id):
    return Items.FindByID(item_id, -1, player_pack)

for x in range(0,36):   
    Items.UseItem(get_item_by_id(0x0F9D))
    Misc.Pause(200)    
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, 42)
    Target.WaitForTarget(10000, True)
    Misc.Pause(200)
    Target.TargetExecute(Items.FindByID(0x0EF3,-1,player_pack))
    Misc.Pause(200)
    Items.Move(Items.FindByID(0x14F0,0x01bc,player_pack),0x409F2C72,-1,116,9,)
