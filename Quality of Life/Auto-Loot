from System.Collections.Generic import List
from System import Int32 as int

# SETTINGS 
corpse_ID = 0x2006
hide_ID = 0x26B4
gold_ID = 0x0EED
net_ID = 0x0DCA
sos_ID = 0x099F
rope_ID = 0x14F8
ingot_ID = 0x1BF2
horned_ID = 0x1081
tmap_ID = 0x14EC
recipe_ID = 0x2831
meat_ID = 0x09F1

loot_list  = [hide_ID, gold_ID, net_ID, sos_ID, rope_ID, ingot_ID,horned_ID,tmap_ID,recipe_ID,meat_ID]
loot_names = ['Rare','Artifact','bread']


# SCRIPT

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

        
            
def checkItemByID(item_to_check, valid_ids):
    if item_to_check.ItemID in loot_list:
        return True
    return False
    
#def checkItemByName(item_to_check, valid_names):
#    for name in valid_names:
#        if name.lower() in str(item_to_check.Name).lower():
#            return True
#    return False
    
def main(): # define the function
    
    crps_list = findCorpses()

    for current_corpse in crps_list:
        Items.Message(current_corpse,170,"loot this")
        Misc.Pause(200)
        if Items.FindByID(0x0EC4,0x0494,Player.Backpack.Serial):
            Items.UseItemByID(0x0EC4,-1)
        else:
            Items.UseItemByID(0x0F52,-1)
        Misc.Pause(200)
        Target.WaitForTarget(2000)
        Target.TargetExecute(current_corpse)
        Misc.Pause(200)
        Items.UseItem(current_corpse)
        Misc.Pause(750)
        lootCorpse(current_corpse)
        Misc.IgnoreObject(current_corpse)
                
# RUN             
main() #call the function
Misc.Pause(1000)
