plantA = 0x411A2010
plantB = 0x411A1E33
plantC = 0x411A2091
plantD = 0x411A1EF7
plantE = 0x411B5CD2

def stockRegs():
    root = Items.BackpackCount(0x0F7A,-1)
    moss = Items.BackpackCount(0x0F7B,-1)
    pearl = Items.BackpackCount(0x0F86,-1)
    garlic = Items.BackpackCount(0x0F84,-1)
    nightshade = Items.BackpackCount(0x0F88,-1)
    ginseng = Items.BackpackCount(0x0F85,-1)
    ingots = Items.BackpackCount(0x1BF2,-1)
  
    
    if root < 15:
        Items.Move(Items.FindByID(0x0F7A,-1,0x42E88440),Player.Backpack.Serial,15-root)
        Misc.Pause(1000)
    
    if moss < 15:
        Items.Move(Items.FindByID(0x0F7B,-1,0x42E88440),Player.Backpack.Serial,15-moss)
        Misc.Pause(1000)
        
    if pearl < 15:
        Items.Move(Items.FindByID(0x0F86,-1,0x42E88440),Player.Backpack.Serial,15-pearl)
        Misc.Pause(1000)
        
    if garlic < 50:
        Items.Move(Items.FindByID(0x0F84,-1,0x42E88440),Player.Backpack.Serial,50-garlic)
        Misc.Pause(1000)
    
    if nightshade < 50:
        Items.Move(Items.FindByID(0x0F88,-1,0x42E88440),Player.Backpack.Serial,50-nightshade)
        Misc.Pause(1000)
        
    if ginseng < 50:
        Items.Move(Items.FindByID(0x0F85,-1,0x42E88440),Player.Backpack.Serial,50-ginseng)
        Misc.Pause(1000)
        
    if ingots < 20:
        Items.Move(Items.FindByID(0x1BF2,-1,0x42E88440),Player.Backpack.Serial,20-ingots)
        Misc.Pause(1000)
        
    else:
        Player.HeadMessage(64,"Regs look good")
        Misc.Pause(500)

def resupply():
    if Items.BackpackCount(0x1EB8,-1) < 2: #tinker tools
        Items.UseItemByID(0x1EB8,-1)
        Misc.Pause(500)
        while Items.BackpackCount(0x1EB8,-1) < 2:
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, 23)
            Misc.Pause(2500)
        Journal.Clear()
        
    if Items.BackpackCount(0x0E9B,-1) < 2: #mortal & pestal
        Items.UseItemByID(0x1EB8,-1)
        Misc.Pause(500)
        while Items.BackpackCount(0x0E9B,-1) < 2:
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, 9)
            Misc.Pause(2500)
        Journal.Clear()

def makePotion(potionType):
    # Mapping potion types to their respective item IDs and Gump actions
    potionDetails = {
        'Cure': {'itemid': 0x0F07, 'actions': (43, 16)},
        'Strength': {'itemid': 0x0F09, 'actions': (29, 9)},
        'Poison': {'itemid': 0x0F0A, 'actions': (36, 16)},
        'Heal': {'itemid': 0x0F0C, 'actions': (22, 16)}
    }
    
    if potionType in potionDetails:
        itemid = potionDetails[potionType]['itemid']
        action1, action2 = potionDetails[potionType]['actions']
        
        # Keep trying to make the potion until at least one is in the backpack
        while Items.BackpackCount(itemid, -1) < 1:
            # Common initial steps for potion making
            Items.UseItemByID(0x0E9B)  # Assuming this is the common starting action
            Misc.Pause(500)
            
            # Execute the actions specific to the potion type
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, action1)
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, action2)
            
            # Wait a bit before checking if the potion was made
            Misc.Pause(2000)
        
        # Common final steps for potion making
        Gumps.SendAction(949095101, 0)
    else:
        Player.HeadMessage(64,f"Potion type '{potionType}' is not recognized.")
    
    
    
            

plantdata = Gumps.LastGumpRawData()
#print(plantdata)
#poison, cure, heal, strength = Lines 3,4,5,6
    
#tileData 882 = patch (infestation)
#tileData 3350 = mushroom (fungus)
#tileData 6884 = skull (poison)
#tileData 5927 = dates (disease)
#tileData 8093 = water pitcher (partched)

#The yellow/red symbol is never going to jump lines... itll always be on line one. But it looks like this;
# { text 95 116 53 0 } - mushroom +
# { text 95 92 53 0 } - patch +
# { text 196 67 53 1 } - water pitcher -
# { text 95 164 53 0 } - dates +
# ( text x, y, color, ID )

def checkBugs(plant):
    if "{ text 95 92 53 0 }" in plantdata:
        Player.ChatSay("Insects! This will not do...")
        Misc.Pause(2000)
        if "{ text 196 91 2101 1 }" in plantdata:
            Player.ChatSay("...the poison will surely be their death.")
            Misc.Pause(2000)
            return
        makePotion("Poison")
        Misc.Pause(1000)
        Items.UseItem(plant)
        Misc.Pause(1000)
        Gumps.SendAction(2847473961, 7) #push the poison button
        Misc.Pause(500)
        Player.ChatSay(67,"*Applies insecticide*")
        Misc.Pause(1500)
        Player.ChatSay("Just a touch will be the end of these pests.")
        Misc.Pause(2000)
    else:
        Misc.Pause(500)

def checkFungus(plant):
    if "{ text 95 116 53 0 }" in plantdata:
        Player.ChatSay("Ah, I see we have a fungal outbreak...")
        Misc.Pause(2000)
        if "{ text 196 115 2101 1 }" in plantdata:
            Player.ChatSay("...appears well treated, however.")
            Misc.Pause(2000)
            return
        makePotion("Cure")
        Misc.Pause(1000)
        Items.UseItem(plant)
        Misc.Pause(1000)
        Gumps.SendAction(2847473961, 8) #push the cure button
        Misc.Pause(500)
        Player.ChatSay(47,"*Applies curing solution*")
        Misc.Pause(1500)
        Player.ChatSay("This should help.")
        Misc.Pause(2000)
    else:
        Misc.Pause(500)

def checkPoison(plant):
    if "{ text 95 140 53 0 }" in plantdata:
        Player.ChatSay("I see the side affects of the insecticide...")
        Misc.Pause(2000)
        if "{ text 196 139 2101 1 }" in plantdata:
            Player.ChatSay("...the anecdote seems to be working.")
            Misc.Pause(2000)
            return
        makePotion("Heal")
        Misc.Pause(1000)
        Items.UseItem(plant)
        Misc.Pause(1000)
        Gumps.SendAction(2847473961, 9) #push the heal button
        Misc.Pause(500)
        Player.ChatSay(54,"*Adds anecdote*")
        Misc.Pause(1500)
    else:
        Misc.Pause(500)
                
              
def checkDisease(plant):
    if "{ text 95 164 53 0 }" in plantdata:
        Player.ChatSay("Looking sickly...")
        Misc.Pause(2000)
        if "{ text 196 163 2101 1 }" in plantdata:
            Player.ChatSay("...the fertilizer solution appears to be doing its job.")
            Misc.Pause(2000)
            return
        makePotion("Strength")
        Misc.Pause(1000)
        Items.UseItem(plant)
        Misc.Pause(1000)
        Gumps.SendAction(2847473961, 10) #push the strength button
        Misc.Pause(500)
        Player.ChatSay(54,"*Adds fertilizer*")
        Misc.Pause(1500)
    else:
        Misc.Pause(500)
        
    
def checkWater():
    if "{ text 196 67 33 0 }" in plantdata:
        Player.ChatSay("The soil is bone dry...")
        Misc.Pause(2000)
        for x in range(0,2):
            Gumps.WaitForGump(2847473961, 10000)
            Gumps.SendAction(2847473961, 6) #push the water button
            Misc.Pause(500)
            Player.ChatSay(93,"*Pours water*")
            Misc.Pause(1500)
    if "{ text 196 67 53 1 }" in plantdata or "{ text 196 67 53 0 }" in plantdata:
        Player.ChatSay("The soil is a bit dry...")
        Misc.Pause(2000)
        Gumps.WaitForGump(2847473961, 10000)
        Gumps.SendAction(2847473961, 6) #push the water button
        Misc.Pause(500)
        Player.ChatSay(93,"*Pours water*")
        Misc.Pause(1500)
    else:
        Misc.Pause(500)
        
def fillWater():      
  for i in Player.Backpack.Contains:
    if i.ItemID == 0x0FF6: #If its a water pitcher
        water = Items.GetPropStringByIndex(i,2)
        if water == "It's empty.": #And its empty
            Items.UseItem(i)
            Misc.Pause(500)
            Target.TargetExecute(0x41202511) #Fill it
            Misc.Pause(500)  

Player.PathFindTo(6802, 3898, 17)
Misc.Pause(3500)
Items.UseItem(0x42E88440)
Misc.Pause(500)
stockRegs()
Player.PathFindTo(6802, 3899, 17)
Misc.Pause(1000)
Player.PathFindTo(6802, 3902, 10)
Misc.Pause(2000)
Player.PathFindTo(6808, 3902, 10)
Misc.Pause(3000)
Player.PathFindTo(6808, 3889, 10)
Misc.Pause(6000)
Player.PathFindTo(6808, 3884, 10) #at first plant
Misc.Pause(3000)
fillWater()

Items.UseItem(plantA)
Misc.Pause(500)
plantdata = Gumps.LastGumpRawData()
checkBugs(plantA)    
checkFungus(plantA)
checkPoison(plantA)
checkDisease(plantA)
checkWater()    
Player.ChatSay("Happy plant!")
Misc.Pause(1500)
Gumps.WaitForGump(2847473961, 10000)
Gumps.SendAction(2847473961, 0) 
Misc.Pause(500)

Items.UseItem(plantB)
Misc.Pause(500)
plantdata = Gumps.LastGumpRawData()
checkBugs(plantB)    
checkFungus(plantB)
checkPoison(plantB)
checkDisease(plantB)
checkWater()    
Player.ChatSay("Happy plant!")
Misc.Pause(1500)
Gumps.WaitForGump(2847473961, 10000)
Gumps.SendAction(2847473961, 0) 
Misc.Pause(500)  

Items.UseItem(plantC)
Misc.Pause(500)
plantdata = Gumps.LastGumpRawData()
checkBugs(plantC)    
checkFungus(plantC)
checkPoison(plantC)
checkDisease(plantC)
checkWater()    
Player.ChatSay("Happy plant!")
Misc.Pause(1500)
Gumps.WaitForGump(2847473961, 10000)
Gumps.SendAction(2847473961, 0) 
Misc.Pause(500) 
    
Player.PathFindTo(6808, 3881, 10)
Misc.Pause(2500)

Items.UseItem(plantD)
Misc.Pause(500)
plantdata = Gumps.LastGumpRawData()
checkBugs(plantD)    
checkFungus(plantD)
checkPoison(plantD)
checkDisease(plantD)
checkWater()    
Player.ChatSay("Happy plant!")
Misc.Pause(1500)
Gumps.WaitForGump(2847473961, 10000)
Gumps.SendAction(2847473961, 0) 
Misc.Pause(500) 

Items.UseItem(plantE)
Misc.Pause(500)
plantdata = Gumps.LastGumpRawData()
checkBugs(plantE)    
checkFungus(plantE)
checkPoison(plantE)
checkDisease(plantE)
checkWater()    
Player.ChatSay("Happy plant!")
Misc.Pause(1500)
Gumps.WaitForGump(2847473961, 10000)
Gumps.SendAction(2847473961, 0) 
Misc.Pause(500) 


Player.PathFindTo(6808, 3884, 10) #at first plant
Misc.Pause(3000)
Player.PathFindTo(6808, 3897, 10)
Misc.Pause(6000)
Player.PathFindTo(6808, 3902, 10)
Misc.Pause(3000)
Player.PathFindTo(6802, 3902, 10)
Misc.Pause(3000)
Player.PathFindTo(6802, 3901, 12)
Misc.Pause(2000)
Player.PathFindTo(6800, 3892, 17)
Misc.Pause(6000)
#
#