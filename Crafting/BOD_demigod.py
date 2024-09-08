
##TO DO: Go get the if bod capacity function from your apostle scripts.
#Must have a bag containing the bods that you would like to fill. 

bod_bag = Player.Backpack.Serial
#ingot_container = Target.PromptTarget('Target your ingot storage')
ingot_container_serial = 0x42E90238

Items.UseItem(bod_bag)
Misc.Pause(1200)
Items.UseItem(ingot_container_serial)
Misc.Pause(500)


smith_hammer = 0x13E3
tinker_tools = 0x1EB9
sewing_kit = 0x0F9D
ingots = ' ' 
number_to_make = ' '
craft = ' ' 
cat_dict = {            
            'ringmail gloves':1, 'ringmail leggings':1, 'ringmail sleeves':1,
            'ringmail tunic':1, 'chainmail coif':8, 'chainmail leggings':8, 'chainmail tunic':8,
            'platemail arms':15, 'platemail gloves':15, 'platemail gorget':15, 'platemail legs':15,
            'platemail tunic':15, 'plate armor':15, 'bascinet':22, 'close helmet':22, 'helmet':22,
            'norse helm':22, 'plate helm':22, 'buckler ':29, 'bronze shield':29, 'heater shield':29,
            'metal shield':29, 'metal kite shield': 29, 'wooden kite shield':29, 'broadsword':36,
            'cutlass':36, 'dagger':36, 'katana':36, 'kryss':36, 'longsword':36, 'scimitar':36, 
            'viking sword':36, 'axe':43, 'battle axe':43, 'double axe':43, 'executioner\'s axe':43, 
            'large battle axe':43, 'two handed axe':43, 'war axe':43, 'bardiche':50, 'halberd':50, 'short spear':50,
            'long spear':50, 'war fork':50, 'hammer pick':57, 'mace':57, 'maul':57, 'war mace':57, 
            'war hammer':57
        }
        
smith_dict = {
            'ringmail gloves':2, 'ringmail leggings':9, 'ringmail sleeves':16,
            'ringmail tunic':23, 'chainmail coif':2, 'chainmail leggings':9, 'chainmail tunic':16,
            'platemail arms':2, 'platemail gloves':9, 'platemail gorget':16, 'platemail legs':23,
            'platemail tunic':30, 'plate armor':37, 'bascinet':2, 'close helmet':9, 'helmet':16,
            'norse helm':23, 'plate helm':30, 'buckler ':2, 'bronze shield':9, 'heater shield':16,
            'metal shield':23, 'metal kite shield': 30, 'wooden kite shield':37, 'broadsword':2,
            'cutlass':9, 'dagger':16, 'katana':23, 'kryss':30, 'longsword':37, 'scimitar':44, 
            'viking sword':51, 'axe':2, 'battle axe':9, 'double axe':16, 'executioner\'s axe':23, 
            'large battle axe':30, 'two handed axe':37, 'war axe':44, 'bardiche':2, 'halberd':9, 'short spear':16,
            'long spear':23, 'war fork':30, 'hammer pick':2, 'mace':9, 'maul':16, 'war mace':23, 
            'war hammer':30
        }

itemid_dict = {
            'ringmail gloves':0x13EB, 'ringmail leggings':0x13F0, 'ringmail sleeves':0x13EE,
            'ringmail tunic':0x13EC, 'chainmail coif':0x13BB, 'chainmail leggings':0x13BE, 'chainmail tunic':0x13BF,
            'platemail arms':0x1410, 'platemail gloves':0x1414, 'platemail gorget':0x1413, 'platemail legs':0x1411,
            'platemail tunic':0x1415, 'plate armor':0x1C04, 'bascinet':0x140C, 'close helmet':0x1408, 'helmet':0x140A,
            'norse helm':0x140E, 'plate helm':0x1412, 'buckler ':0x1B73, 'bronze shield':0x1B72, 'heater shield':0x1B76,
            'metal shield':0x1B7B, 'metal kite shield': 0x1B74, 'wooden kite shield':0x1B79, 'broadsword':0x0F5E,
            'cutlass':0x1441, 'dagger':0x0F52, 'katana':0x13FF, 'kryss':0x1401, 'longsword':0x0F61, 'scimitar':0x13B6, 
            'viking sword':0x13B9, 'axe':0x0F49, 'battle axe':0x0F47, 'double axe':0x0F4B, 'executioner\'s axe':0x0F45, 
            'large battle axe':0x13FB, 'two handed axe':0x1443, 'war axe':0x13B0, 'bardiche':0x0F4D, 'halberd':0x143E, 'short spear':0x1403,
            'long spear':0x0F62, 'war fork':0x1405, 'hammer pick':0x143D, 'mace':0x0F5C, 'maul':0x143B, 'war mace':0x1407, 
            'war hammer':0x1439
        }        
        
metals_dict = {
            0000:6, 1045:13, 1109:20, 1119:27, 1752:34, 
            1719:41, 2430:48, 2002:55, 1348:62
        }

def errorCheck():
    if Journal.SearchByType("That container cannot hold more items.","System"):
        Misc.SendMessage("Error detected, stopping script")
        Misc.Pause(500)
        Misc.ScriptStop("BOD_demigod.py")

        
def material_type():
    global ingots 
    if i.ItemID == 0x14EF: 
        Items.WaitForProps(i, 5000) 
        props = Items.GetPropStringList(i)
        try:
            metal_type = str(props[6])
            metal_split = metal_type.split("with ")
            metal_prop = metal_split[1]
            if 'valorite ingots.' in metal_prop: 
                ingots = 1348
            elif 'dull copper ingots.' in metal_prop: 
                ingots = 1045 
            elif 'shadow iron ingots.' in metal_prop: 
                ingots = 1109  
            elif 'copper ingots.' in metal_prop:  
                ingots = 1119 
            elif 'bronze ingots.' in metal_prop:  
                ingots = 1752 
            elif 'gold ingots.' in metal_prop:  
                ingots = 1719 
            elif 'agapite ingots.' in metal_prop:  
                ingots = 2430 
            elif 'verite ingots.'  in metal_prop:  
                ingots = 2002 
        except:
                ingots = 0000

def worldSave():
    if (Journal.SearchByType('The world will save in 1 minute.', 'System') or Journal.SearchByType('pause', 'Regular')):
        Misc.Pause(700)
        Misc.SendMessage('Pausing for world save or player-called break.', 33)
        while (not Journal.SearchByType('World save complete.', 'System') and not Journal.SearchByType('play', 'Regular')):
            Misc.Pause(1000)
        Misc.Pause(2500)
        Misc.SendMessage('Continuing run', 33)
        Misc.Pause(1000)
    Journal.Clear()                
                
def hammer_check():
        hammercount = Items.ContainerCount(Player.Backpack.Serial,smith_hammer,-1)
        if hammercount < 2:
            Items.Move(Items.FindByID(0x1BF2,0000,ingot_container_serial),Player.Backpack.Serial,4)
            Misc.Pause(1000)
            errorCheck()
            Items.UseItemByID(tinker_tools)
            Misc.Pause(500)
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, 93)
            Misc.Pause(2000)
            for i in Player.Backpack.Contains:
                if i.ItemID == 0x13E3:
                    Misc.Pause(500)
                    Items.Move(i,Player.Backpack.Serial,-1,159, 141)
                    Misc.Pause(500)
                    errorCheck()
                    
def tinker_check():
    tinkercount = Items.ContainerCount(Player.Backpack.Serial,tinker_tools,-1)
    if tinkercount < 2:
            Items.Move(Items.FindByID(0x1BF2,0000,ingot_container_serial),Player.Backpack.Serial,2)
            Misc.Pause(500)
            errorCheck()
            Items.UseItemByID(tinker_tools)
            Misc.Pause(500)
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, 23)
            Misc.Pause(2000)
            for i in Player.Backpack.Contains:
                if i.ItemID == 0x1EB8:
                    Misc.Pause(500)
                    Items.Move(i,Player.Backpack.Serial,-1,172, 124)
                    Misc.Pause(1000)
                    errorCheck()
                    

def quantity():  
    global number_to_make 
    Items.WaitForProps(bod, 5000) 
    props = Items.GetPropStringList(bod) 
    whole_prop = props[6] 
    whole_prop_split = whole_prop.split() 
    number_to_make = whole_prop_split[3] 
       
def item_to_craft(): 
    global craft  
    Items.WaitForProps(bod, 5000) 
    props = Items.GetPropStringList(bod) 
    craftable = str(props[7]) 
    craftable_split = craftable.split(": ") 
    craft = craftable_split[0]

def change_metal():
    Misc.Pause(1200)
    Items.UseItemByID(smith_hammer, 0000)
    Misc.Pause(500)
    Gumps.WaitForGump(949095101, 5000)
    while Gumps.HasGump() == False:
        Items.UseItemByID(smith_hammer, 0000)
        Gumps.WaitForGump(949095101, 5000)
    Gumps.SendAction(949095101,7)
    Misc.Pause(500)
    Gumps.SendAction(949095101, metals_dict.get(ingots))

def items_added(): 
    global bod_capacity
    global inbod  
    Items.WaitForProps(bod, 5000) 
    props = Items.GetPropStringList(bod) 
    craftable = str(props[6]) 
    craftable_split = craftable.split(": ") 
    bod_capacity = craftable_split[1]
    togo = str(props[7]) 
    togo_split = togo.split(": ") 
    inbod = togo_split[1]

def fill_bod():
    targetid = itemid_dict.get(craft)
    Items.UseItem(bod)
    Misc.Pause(500)
    Gumps.WaitForGump(1526454082, 10000)
    Gumps.SendAction(1526454082, 2)
    Misc.Pause(1000)
    for i in Player.Backpack.Contains:
        if i.ItemID == targetid:
            Target.TargetExecute(i)
            Misc.Pause(100)

    
def craft_items():
    restock()
    Misc.Pause(1000)
    Items.UseItemByID(smith_hammer, 0000)
    Misc.Pause(500)
    Gumps.SendAction(949095101, cat_dict.get(craft))
    Misc.Pause(1000)
    #use the hammer, get to the right menu page
    items_added()
    while True:
        worldSave()
        items_added()
        restock()
        if int(inbod) == int(bod_capacity):
            Misc.SendMessage(str(inbod)+" of "+ str(bod_capacity))
            break
        else:
            Misc.SendMessage(str(inbod)+" of "+ str(bod_capacity))
            Misc.SendMessage('Not full yet')
        Misc.Pause(500)
        Items.UseItemByID(smith_hammer, 0000)
        Misc.Pause(500)
        Gumps.SendAction(949095101, smith_dict.get(craft))
        #use hammer, create the specific item
        Misc.Pause(2000)
        #what to do if the tool breaks
        if Journal.Search('You have worn out your tool!'):
            Misc.Pause(1000)
            Journal.Clear()
            Items.UseItemByID(smith_hammer, 0000)
            Misc.Pause(500)
            Gumps.WaitForGump(949095101, 5000)
        #find the crafted item
        target_item = Items.FindByID(itemid_dict.get(craft),-1,Player.Backpack.Serial,-1)
        #verify that it's exceptional
        if target_item and Items.GetPropValue(target_item,'Crafted By') == 1:
            Misc.Pause(500)
            #if it is, open the BOD menu
            Items.UseItem(bod)
            Misc.Pause(500)
            Gumps.WaitForGump(1526454082, 10000)
            Gumps.SendAction(1526454082, 2)
            Misc.Pause(500)
            Target.TargetExecute(target_item)
            #add it to the BOD
            Misc.Pause(500)
            if Journal.SearchByType('The item has been combined with the deed.', 'System'):
                continue
            else:
                #if the item didn't add try again
                Misc.SendMessage('Misfire')
                Misc.Pause(500)
                Items.UseItem(bod)
                Misc.Pause(500)
                Gumps.WaitForGump(1526454082, 10000)
                Gumps.SendAction(1526454082, 2)
                Misc.Pause(500)
                Target.TargetExecute(target_item)
                Misc.Pause(500)
                Items.UseItemByID(smith_hammer, 0000)
                Misc.Pause(500)
            if Journal.SearchByType('The item has been combined with the deed.', 'System'):
                continue
            else:
                #if 2nd try fails, break loop
                Misc.SendMessage('Second attempt failure, breaking loop.')
            
        else:
           #if not exceptional, smelt it 
            Misc.Pause(500)
            target_item = Items.FindByID(itemid_dict.get(craft),-1,Player.Backpack.Serial,-1)
            #first, make sure you have an item to smelt
            if target_item:
                Player.HeadMessage(64,"SHITTY!")
                Items.UseItemByID(smith_hammer)
                Misc.Pause(500)
                Gumps.SendAction(949095101, 14)
                Misc.Pause(500)
                Target.TargetExecute(target_item)
                Misc.Pause(500)
            else:
                Misc.Pause(500)
                
def restock():
    Misc.Pause(500)
    ingotcount = Items.ContainerCount(Player.Backpack.Serial, 0x1BF2, -1)
    if ingotcount < 30:
        for i in Items.FindBySerial(ingot_container_serial).Contains:
            if i.Hue == ingots and i.ItemID == 0x1BF2:
                Items.Move(i, Player.Backpack.Serial, 200)
                Misc.Pause(1000)
                errorCheck()
                ingotcount = Items.ContainerCount(Player.Backpack.Serial, 0x1BF2, -1)

                
def return_ingots():
    Misc.Pause(1100)
    for i in Player.Backpack.Contains:
        if i.ItemID == 0x1BF2:
            Items.Move(i, ingot_container_serial, 0)
            Misc.Pause(1200)
            errorCheck()
            
def sortBods():
    # Sort the items in the backpack based on whether they match keywords
    backpack_items = Player.Backpack.Contains
    keywords = ["norse","halberd", "helmet", "bascinet", "hammer pick", "axe", "bardiche", "spear", "bascinet", "war", "scimitar", "maul", "sword", "katana", "kryss", "shield", "broadsword", "close", "dagger", "longsword", "buckler", "armor", "cutlass", "mace"]
    sorted_items = sorted(backpack_items, key=lambda item: any(keyword.lower() in str(Items.GetPropStringList(item)).lower() for keyword in keywords), reverse=True)
    
    for i in sorted_items:
        
        if i.ItemID == 0x14EF:
            prop_list = Items.GetPropStringList(i)
            len_det = len(prop_list)
            whole_prop = prop_list[6] 
            whole_prop_split = whole_prop.split() 
            number_to_make = whole_prop_split[3] 
            
            if any(keyword.lower() in str(prop_list).lower() for keyword in keywords):
                sellbook = Items.FindByName("Sell", 0x0000, Player.Backpack.Serial, 4)
                Misc.Pause(200)
                Items.Move(i, sellbook, 1)
                Misc.Pause(1000)
                errorCheck()
            elif int(number_to_make) == 15:
                sortbook = Items.FindByName("Sort", 0x0000, Player.Backpack.Serial, 4)
                Items.Move(i, sortbook, 1)
                Misc.Pause(1000)
                errorCheck()
            else:
                sellbook = Items.FindByName("Sell", 0x0000, Player.Backpack.Serial, 4)
                Misc.Pause(200)
                Items.Move(i, sellbook, 1)
                Misc.Pause(1000)
                errorCheck()
                
    Gumps.WaitForGump(1425364447, 10000)
    Gumps.SendAction(1425364447, 0)
    Misc.Pause(200)    

Journal.Clear()
Misc.Pause(500)                
for i in Items.FindBySerial(bod_bag).Contains: 
    if i.ItemID == 0x14EF:
        bod = i.Serial
        worldSave()        
        material_type()
        quantity()
        item_to_craft()
        Misc.SendMessage(ingots)  
        Misc.SendMessage(number_to_make) 
        Misc.SendMessage(craft)
        change_metal()
        craft_items()
        return_ingots()
        Player.HeadMessage(64,'Order filled.')

sortBods()



