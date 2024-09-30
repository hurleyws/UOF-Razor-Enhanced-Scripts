#MUST be able to carry the item

def stockRegs():
    root = Items.BackpackCount(0x0F86,-1)
    moss = Items.BackpackCount(0x0F7B,-1)
    pearl = Items.BackpackCount(0x0F7A,-1)
    ash = Items.BackpackCount(0x0F8C,-1)
    rods = Items.BackpackCount(0x0DBF,-1)
    bandages = Items.BackpackCount(0x0E21,-1)
    arrows = Items.BackpackCount(0x0F3F,-1)
    
  
    Items.UseItem(0x43DE1F06)
    Misc.Pause(500)
    Items.UseItem(0x45465912)
    Misc.Pause(500)
    Items.UseItem(0x4043C469)
    Misc.Pause(500)
    
    if root < 15:
        Items.Move(Items.FindByID(0x0F86,-1,0x4043C469),Player.Backpack.Serial,15-root)
        Misc.Pause(1000)
    elif root > 15:
        Items.Move(Items.FindByID(0x0F86,-1,Player.Backpack.Serial),0x42E88440,root-15)
        Misc.Pause(1000)
    else:
        Misc.Pause(200)
    
    if moss < 15:
        Items.Move(Items.FindByID(0x0F7B,-1,0x4043C469),Player.Backpack.Serial,15-moss)
        Misc.Pause(1000)
    elif moss > 15:
        Items.Move(Items.FindByID(0x0F7B,-1,Player.Backpack.Serial),0x42E88440,moss-15)
        Misc.Pause(1000)
    else:
        Misc.Pause(200)
        
    if pearl < 15:
        Items.Move(Items.FindByID(0x0F7A,-1,0x4043C469),Player.Backpack.Serial,15-pearl)
        Misc.Pause(1000)
    elif pearl > 15:
        Items.Move(Items.FindByID(0x0F7A,-1,Player.Backpack.Serial),0x42E88440,pearl-15)
        Misc.Pause(1000)
        
    if ash < 15:
        Items.Move(Items.FindByID(0x0F8C,-1,0x4043C469),Player.Backpack.Serial,15-ash)
        Misc.Pause(1000)
    elif ash > 15:
        Items.Move(Items.FindByID(0x0F8C,-1,Player.Backpack.Serial),0x42E88440,ash-15)
        Misc.Pause(1000)
        
    if rods < 4:
        for x in range(0,4-rods):
            Items.Move(Items.FindByID(0x0DBF,-1,0x45465912),Player.Backpack.Serial,1)
            Misc.Pause(1000)
            
    if bandages < 150:
        Items.Move(Items.FindByID(0x0E21,-1,0x4043C469),Player.Backpack.Serial,150-bandages)
        Misc.Pause(1000)
        
    if arrows < 250:
        Items.Move(Items.FindByID(0x0F3F,-1,0x4043C469),Player.Backpack.Serial,250-arrows)
        Misc.Pause(1000)
    
    else:
        Misc.Pause(200)

seaChests = Items.Filter()
seaChests.Enabled = True
seaChests.OnGround = True
seaChests.Movable = True
seaChests.RangeMax = 2
seaChests.Name = "treasure chest"
seaChestList = Items.ApplyFilter(seaChests)

gate = Items.Filter()
gate.Enabled = True
gate.OnGround = True
gate.Movable = False
gate.RangeMax = 1.5


Items.UseItemByID(0x0F09,0x0000)
Misc.Pause(500)
Player.ChatSay("[gate Winter Lodge")
Misc.Pause(2750)

Misc.SendMessage(len(seaChestList))
Misc.Pause(500)
for index, i in enumerate(seaChestList):
    if index == len(seaChestList) -1:
        gate = Items.FindByID(0x0F6C,0x0000,-1,3,False) # Find a gate near player
        Misc.Pause(500)
        Items.UseItem(gate) # Use the gate
        Misc.Pause(500)
        Items.Lift(i,-1)
        Misc.Pause(1000)
        Items.MoveOnGround(Items.FindBySerial(0x40A0A98D),-1,Player.Position.X+1,Player.Position.Y,Player.Position.Z)
        Misc.Pause(1500)

    else:
        gate = Items.FindByID(0x0F6C,0x0000,-1,3,False) # Find a gate near player
        Misc.Pause(500)
        Items.UseItem(gate) # Use the gate
        Misc.Pause(500)
        Items.Lift(i,-1)
        Misc.Pause(1000)
        Items.MoveOnGround(Items.FindBySerial(0x40A0A98D),-1,Player.Position.X+1,Player.Position.Y,Player.Position.Z)
        Misc.Pause(1000)
        #check here to see.. are you hands really empty? can you use the gate again?
        gate = Items.FindByID(0x0F6C,0x0000,-1,3,False) # Find a gate near player
        Items.UseItem(gate) # Use the gate
        Misc.Pause(2000)

  


Player.PathFindTo(6783, 3900, 17)
Misc.Pause(2000)
seaChestList = Items.ApplyFilter(seaChests)
for index,i in enumerate(seaChestList):
    if index == len(seaChestList) -1:
        #Final chest
        Items.MoveOnGround(i,1,6782, 3900, 17)
        Misc.Pause(1000)
        Player.PathFindTo(6783, 3899, 17)
        Misc.Pause(1500)
        Player.PathFindTo(6783, 3898, 17)
        Misc.Pause(1500)
        Items.MoveOnGround(i,1,6782, 3896, 17)
        Misc.Pause(1000)
        Player.PathFindTo(6782, 3897, 17)
        Misc.Pause(1500)
        Items.MoveOnGround(i,1,6780, 3897, 17)
        Misc.Pause(1000)
        gold_found = Items.FindByID(0x0EED,-1,Player.Backpack.Serial)
        if gold_found:
           Player.PathFindTo(6783,3897,17)
           Misc.Pause(1500)
           Items.Move(gold_found,0x408E8DA8,-1)
           Misc.Pause(1000)
        Player.PathFindTo(6780, 3893, 17)
        regchest = Items.FindBySerial(0x4043C469)
        while Player.DistanceTo(regchest) > 2:
            Misc.Pause(1000)
        Misc.Pause(1000)
        stockRegs()
        chair = Items.FindBySerial(0x42F7B4D0)
        Player.PathFindTo(6784, 3884, 17)
        while Player.DistanceTo(chair) > 1:
            Misc.Pause(1000)
        break
    else:
        #Go back for more
        Items.MoveOnGround(i,1,6782, 3900, 17)
        Misc.Pause(1000)
        Player.PathFindTo(6783, 3899, 17)
        Misc.Pause(1500)
        door = Items.FindBySerial(0x42F89EBD)
        if door.ItemID == 0x06A7:
            Items.UseItem(door)
            Misc.Pause(500)
        Player.PathFindTo(6783, 3898, 17)
        Misc.Pause(1500)
        Items.MoveOnGround(i,1,6782, 3896, 17)
        Misc.Pause(1000)
        Player.PathFindTo(6782, 3897, 17)
        Misc.Pause(1500)
        Items.MoveOnGround(i,1,6780, 3897, 17)
        Misc.Pause(1000)
        Player.PathFindTo(6783, 3900, 17)
        Misc.Pause(3000)

            
  
        

    


