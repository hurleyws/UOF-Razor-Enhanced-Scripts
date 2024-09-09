from System.Collections.Generic import List
from System import Int32 as int


corpse_ID = 0x2006
bone_ID = 0x0F7E
gold_ID = 0x0EED
beetle_backpack_serial = 0x4128BBCA

loot_list  = [bone_ID, gold_ID, 0x0F2D,0x0F19,0x0F26,0x0F15,0x0F10,0x0F25,0x0F13,0x0F21,0x0F16]
loot_names = ['Rare','Artifact','bread']

def checkItemByID(item_to_check, valid_ids):
    if item_to_check.ItemID in loot_list:
        return True
    return False
    

def lootCorpse(corpse):
    for item_to_loot in corpse.Contains:
        Misc.SendMessage("found a {} with ID {}".format(item_to_loot.Name, item_to_loot.ItemID),130)
        Misc.Pause(10)
        shouldLoot = False
        if checkItemByID(item_to_loot, loot_list):
            shouldLoot = True
#        if checkItemByName(item_to_loot, loot_names):
#            shouldLoot = True
        
        
        if shouldLoot:
            Items.Move(item_to_loot,Player.Backpack,-1 ) # -1 -> all, for stackable items
            Misc.Pause(750)

def findContracts():
    contract_filter = Items.Filter()
    contract_filter.IsCorpse = True 
    contract_filter.OnGround = True 
    contract_filter.RangeMin = 0 
    contract_filter.RangeMax = 2 
    ##########################################
    #CHANGE CORPSE NAME ACCORDING TO CONTRACT#
    ##########################################
    contract_filter.Name = "<BASEFONT COLOR=#CCCCCC> gilbarta corpse <BASEFONT COLOR=#FFFFFF>"
    contract_filter.Graphics = List[int]([0x2006,0x2006]) # kraken, deep water

    contract_list = Items.ApplyFilter(contract_filter) # returns list of items, manipulate list after this as you wish
    
    return contract_list

def findCorpses():
    corpses_filter = Items.Filter()
    corpses_filter.IsCorpse = True # optional
    corpses_filter.OnGround = True # Questionably optional
    corpses_filter.RangeMin = 0 # optional
    corpses_filter.RangeMax = 2 # optoinal
    corpses_filter.Graphics = List[int]([0x2006,0x2006]) # kraken, deep water
    corpses_filter.CheckIgnoreObject = True # optioinal, if you use Misc.IgnoreObject(item) the fitler will ignore if true.

    corpse_list = Items.ApplyFilter(corpses_filter) # returns list of items, manipulate list after this as you wish

    return corpse_list
    
def main(): # define the function
    
    crps_list = findCorpses()
    contract_list = findContracts()

    for current_corpse in crps_list:
        Items.Message(current_corpse,170,"loot this")
        Misc.Pause(200)
        Items.UseItem(current_corpse)
        Misc.Pause(500)
        lootCorpse(current_corpse)
        Misc.Pause(500)
        if len(contract_list) > 0:
            for i in contract_list:
                Items.UseItemByID(0x14EF,-1)
                Misc.Pause(500)
                Gumps.WaitForGump(1075948522, 10000)
                Gumps.SendAction(1075948522, 1)
                Misc.Pause(1000)
                Target.TargetExecute(i)
                Misc.Pause(500)
                findContracts()
        Misc.IgnoreObject(current_corpse)
                
while True:
    main()
    Misc.Pause(500)