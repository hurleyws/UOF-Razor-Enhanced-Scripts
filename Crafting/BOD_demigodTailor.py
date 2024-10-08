#############################
# Should fill all the clothing bods in your backpack (dont have it too full otherwise no room for materials 10/15 at a time)
# Tinker skill required to make tools
# *Should be able to start with a set of tinker tools
# All care given no responsibility taken*
# ~Klap
################
from System import Int32 as int
from System.Collections.Generic import List

matchest = 0x435ED948 ##material chest with cloth/hides/iron
recyclechest = 0x42E8832C #if it cant be cut back into resources, it will get stored here to hopefully get reused, will need cleaning out everynow and then


sort_bods = False #True/False  #If this is true, will sort the completed sbod into the below chest/books and only keep the ones that give decent rewards PS/CBD/runic kits
books={
"10":{"chest":0x403763EF,"cloth":0x4295042F,"leather":0x429505C9,"hides":0x42950467,"lbods":0x4295038E},    
"15":{"chest":0x43E1AEAC,"cloth":0x42950646,"leather":0x42950401,"hides":0x42950528,"lbods":0x429504A3},     
"20":{"chest":0x432733F7,"cloth":0x42950280,"leather":0x42950320,"hides":0x429506CF,"lbods":0x429505F4},
"bin":{"chest":0x4349E178,"book":0x4152944D}}  ## the book here also holds filled crap sbods for turn in


errorcolour = 150
dragTime = 450
moveitempause = 400
useitempause = 550
scissorsID = 0x0F9F

tailoring = {
"leather gorget":{"itemid":0x13C7,"menu":36,"submenu":0,"item":2,"defaultmat":"leather","mat1":4,"mat2":0,"secondarymat":None,"recycle":True},
"leather cap":{"itemid":0x1DB9,"menu":36,"submenu":0,"item":9,"defaultmat":"leather","mat1":2,"mat2":0,"secondarymat":None,"recycle":True},
"leather gloves":{"itemid":0x13C6,"menu":36,"submenu":0,"item":16,"defaultmat":"leather","mat1":3,"mat2":0,"secondarymat":None,"recycle":True},
"leather sleeves":{"itemid":0x13CD,"menu":36,"submenu":0,"item":23,"defaultmat":"leather","mat1":8,"mat2":0,"secondarymat":None,"recycle":True},
"leather leggings":{"itemid":0x13CB,"menu":36,"submenu":0,"item":30,"defaultmat":"leather","mat1":10,"mat2":0,"secondarymat":None,"recycle":True},
"leather tunic":{"itemid":0x13CC,"menu":36,"submenu":0,"item":37,"defaultmat":"leather","mat1":12,"mat2":0,"secondarymat":None,"recycle":True},
"leather shorts":{"itemid":0x1C00,"menu":50,"submenu":0,"item":2,"defaultmat":"leather","mat1":8,"mat2":0,"secondarymat":None,"recycle":True},
"leather skirt":{"itemid":0x1C08,"menu":50,"submenu":0,"item":9,"defaultmat":"leather","mat1":6,"mat2":0,"secondarymat":None,"recycle":True},
"leather bustier":{"itemid":0x1C0A,"menu":50,"submenu":0,"item":16,"defaultmat":"leather","mat1":6,"mat2":0,"secondarymat":None,"recycle":True},
"studded bustier":{"itemid":0x1C0C,"menu":50,"submenu":0,"item":23,"defaultmat":"leather","mat1":8,"mat2":0,"secondarymat":None,"recycle":True},
"leather armor":{"itemid":0x1C06,"menu":50,"submenu":0,"item":30,"defaultmat":"leather","mat1":8,"mat2":0,"secondarymat":None,"recycle":True},
"studded armor":{"itemid":0x1C02,"menu":50,"submenu":0,"item":37,"defaultmat":"leather","mat1":10,"mat2":0,"secondarymat":None,"recycle":True},
"studded gorget":{"itemid":0x13D6,"menu":43,"submenu":0,"item":2,"defaultmat":"leather","mat1":6,"mat2":0,"secondarymat":None,"recycle":True},
"studded gloves":{"itemid":0x13D5,"menu":43,"submenu":0,"item":16,"defaultmat":"leather","mat1":8,"mat2":0,"secondarymat":None,"recycle":True},
"studded sleeves":{"itemid":0x13DC,"menu":43,"submenu":0,"item":23,"defaultmat":"leather","mat1":10,"mat2":0,"secondarymat":None,"recycle":True},
"studded leggings":{"itemid":0x13DA,"menu":43,"submenu":0,"item":30,"defaultmat":"leather","mat1":12,"mat2":0,"secondarymat":None,"recycle":True},
"studded tunic":{"itemid":0x13DB,"menu":43,"submenu":0,"item":37,"defaultmat":"leather","mat1":14,"mat2":0,"secondarymat":None,"recycle":True},
"bone helmet":{"itemid":0x1451,"menu":57,"submenu":0,"item":2,"defaultmat":"leather","mat1":4,"mat2":2,"secondarymat":"bone","recycle":True},
"bone gloves":{"itemid":0x1450,"menu":57,"submenu":0,"item":9,"defaultmat":"leather","mat1":6,"mat2":2,"secondarymat":"bone","recycle":True},
"bone arms":{"itemid":0x144E,"menu":57,"submenu":0,"item":16,"defaultmat":"leather","mat1":8,"mat2":4,"secondarymat":"bone","recycle":True},
"bone leggings":{"itemid":0x1452,"menu":57,"submenu":0,"item":23,"defaultmat":"leather","mat1":10,"mat2":6,"secondarymat":"bone","recycle":True},
"bone armor":{"itemid":0x144F,"menu":57,"submenu":0,"item":30,"defaultmat":"leather","mat1":12,"mat2":10,"secondarymat":"bone","recycle":True},
"sandals":{"itemid":0x170D,"menu":29,"submenu":0,"item":2,"defaultmat":"leather","mat1":4,"mat2":0,"secondarymat":None,"recycle":False},
"shoes":{"itemid":0x170F,"menu":29,"submenu":0,"item":9,"defaultmat":"leather","mat1":6,"mat2":0,"secondarymat":None,"recycle":False},
"boots":{"itemid":0x170B,"menu":29,"submenu":0,"item":16,"defaultmat":"leather","mat1":8,"mat2":0,"secondarymat":None,"recycle":False},
"thigh boots":{"itemid":0x1711,"menu":29,"submenu":0,"item":23,"defaultmat":"leather","mat1":10,"mat2":0,"secondarymat":None,"recycle":False},
"skullcap":{"itemid":0x1544,"menu":1,"submenu":0,"item":2,"defaultmat":"cloth","mat1":2,"mat2":0,"secondarymat":None,"recycle":True},
"bandana":{"itemid":0x1540,"menu":1,"submenu":0,"item":9,"defaultmat":"cloth","mat1":2,"mat2":0,"secondarymat":None,"recycle":True},
"floppy hat":{"itemid":0x1713,"menu":1,"submenu":0,"item":16,"defaultmat":"cloth","mat1":11,"mat2":0,"secondarymat":None,"recycle":True},
"cap":{"itemid":0x1715,"menu":1,"submenu":0,"item":23,"defaultmat":"cloth","mat1":11,"mat2":0,"secondarymat":None,"recycle":True},
"wide-brim hat":{"itemid":0x1714,"menu":1,"submenu":0,"item":30,"defaultmat":"cloth","mat1":12,"mat2":0,"secondarymat":None,"recycle":True},
"straw hat":{"itemid":0x1717,"menu":1,"submenu":0,"item":37,"defaultmat":"cloth","mat1":10,"mat2":0,"secondarymat":None,"recycle":True},
"tall straw hat":{"itemid":0x1716,"menu":1,"submenu":0,"item":44,"defaultmat":"cloth","mat1":13,"mat2":0,"secondarymat":None,"recycle":True},
"wizard\'s hat":{"itemid":0x1718,"menu":1,"submenu":0,"item":51,"defaultmat":"cloth","mat1":15,"mat2":0,"secondarymat":None,"recycle":True},
"bonnet":{"itemid":0x1719,"menu":1,"submenu":0,"item":58,"defaultmat":"cloth","mat1":11,"mat2":0,"secondarymat":None,"recycle":True},
"feathered hat":{"itemid":0x171A,"menu":1,"submenu":0,"item":65,"defaultmat":"cloth","mat1":12,"mat2":0,"secondarymat":None,"recycle":True},
"tricorne hat":{"itemid":0x171B,"menu":1,"submenu":0,"item":72,"defaultmat":"cloth","mat1":12,"mat2":0,"secondarymat":None,"recycle":True},
"jester hat":{"itemid":0x171C,"menu":1,"submenu":0,"item":79,"defaultmat":"cloth","mat1":15,"mat2":0,"secondarymat":None,"recycle":True},

"doublet":{"itemid":0x1F7B,"menu":8,"submenu":0,"item":2,"defaultmat":"cloth","mat1":8,"mat2":0,"secondarymat":None,"recycle":True},
"shirt":{"itemid":0x1517,"menu":8,"submenu":0,"item":9,"defaultmat":"cloth","mat1":8,"mat2":0,"secondarymat":None,"recycle":True},
"fancy shirt":{"itemid":0x1EFD,"menu":8,"submenu":0,"item":16,"defaultmat":"cloth","mat1":8,"mat2":0,"secondarymat":None,"recycle":True},
"tunic":{"itemid":0x1FA1,"menu":8,"submenu":0,"item":23,"defaultmat":"cloth","mat1":12,"mat2":0,"secondarymat":None,"recycle":True},
"surcoat":{"itemid":0x1FFD,"menu":8,"submenu":0,"item":30,"defaultmat":"cloth","mat1":14,"mat2":0,"secondarymat":None,"recycle":True},
"plain dress":{"itemid":0x1F01,"menu":8,"submenu":0,"item":37,"defaultmat":"cloth","mat1":10,"mat2":0,"secondarymat":None,"recycle":True},
"fancy dress":{"itemid":0x1F00,"menu":8,"submenu":0,"item":44,"defaultmat":"cloth","mat1":12,"mat2":0,"secondarymat":None,"recycle":True},
"cloak":{"itemid":0x1515,"menu":8,"submenu":0,"item":51,"defaultmat":"cloth","mat1":14,"mat2":0,"secondarymat":None,"recycle":True},
"robe":{"itemid":0x1F03,"menu":8,"submenu":0,"item":58,"defaultmat":"cloth","mat1":16,"mat2":0,"secondarymat":None,"recycle":True},
"jester suit":{"itemid":0x1F9F,"menu":8,"submenu":0,"item":65,"defaultmat":"cloth","mat1":24,"mat2":0,"secondarymat":None,"recycle":True},
"short pants":{"itemid":0x152E,"menu":15,"submenu":0,"item":2,"defaultmat":"cloth","mat1":6,"mat2":0,"secondarymat":None,"recycle":True},
"long pants":{"itemid":0x1539,"menu":15,"submenu":0,"item":9,"defaultmat":"cloth","mat1":8,"mat2":0,"secondarymat":None,"recycle":True},
"kilt":{"itemid":0x1537,"menu":15,"submenu":0,"item":16,"defaultmat":"cloth","mat1":8,"mat2":0,"secondarymat":None,"recycle":True},
"skirt":{"itemid":0x1516,"menu":15,"submenu":0,"item":23,"defaultmat":"cloth","mat1":10,"mat2":0,"secondarymat":None,"recycle":True},
"body sash":{"itemid":0x1541,"menu":22,"submenu":0,"item":2,"defaultmat":"cloth","mat1":4,"mat2":0,"secondarymat":None,"recycle":True},
"half apron":{"itemid":0x153B,"menu":22,"submenu":0,"item":9,"defaultmat":"cloth","mat1":6,"mat2":0,"secondarymat":None,"recycle":True},
"full apron":{"itemid":0x153D,"menu":22,"submenu":0,"item":16,"defaultmat":"cloth","mat1":10,"mat2":0,"secondarymat":None,"recycle":True}}

lbod_grid = {
    "cloth":{
        "four":{"10":{"exc":True,"normal":0},
                "20":{"exc":0,"normal":0}},
        "five":{"10":{"exc":True,"normal":True},
                "20":{"exc":True,"normal":0}}},
    "leather":{
        "four":{"10":{"exc":True,"normal":True},
                "20":{"exc":0,"normal":0}},
        "five":{"10":{"exc":True,"normal":True},
                "20":{"exc":True,"normal":0}},
        "six":{"10":{"exc":True,"normal":True},
                "20":{"exc":True,"normal":True}}}}

            
sbod_grid = {
"tricorne hat":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},
"cap":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},
"wide-brim hat":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},
"tall straw hat":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},

"jester hat":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},
"jester suit":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},
"cloak":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},

"skullcap":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},
"doublet":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},
"kilt":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},

"bandana":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},
"shirt":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},
"skirt":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},

"bonnet":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},
"half apron":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},
"fancy dress":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},

"floppy hat":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},
"full apron":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},
"plain dress":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},

"wizard\'s hat":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},
"body sash":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},
"robe":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},

"straw hat":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},
"tunic":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},
"long pants":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},

"thigh boots":{"10":{"exc":True,"normal":True},"20":{"exc":True,"normal":0}},
"sandals":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},
"boots":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},
"shoes":{"10":{"exc":True,"normal":0},"20":{"exc":0,"normal":0}},


"feathered hat":{"10":{"exc":True,"normal":True},"20":{"exc":True,"normal":0}},
"surcoat":{"10":{"exc":True,"normal":True},"20":{"exc":True,"normal":0}},
"fancy shirt":{"10":{"exc":True,"normal":True},"20":{"exc":True,"normal":0}},
"short pants":{"10":{"exc":True,"normal":True},"20":{"exc":True,"normal":0}},

"studded gorget":{"10":{"exc":True,"normal":True},"20":{"exc":True,"normal":0}},
"studded gloves":{"10":{"exc":True,"normal":True},"20":{"exc":True,"normal":0}},
"studded sleeves":{"10":{"exc":True,"normal":True},"20":{"exc":True,"normal":0}},
"studded leggings":{"10":{"exc":True,"normal":True},"20":{"exc":True,"normal":0}},
"studded tunic":{"10":{"exc":True,"normal":True},"20":{"exc":True,"normal":0}},

"bone helmet":{"10":{"exc":True,"normal":True},"20":{"exc":True,"normal":0}},
"bone gloves":{"10":{"exc":True,"normal":True},"20":{"exc":True,"normal":0}},
"bone arms":{"10":{"exc":True,"normal":True},"20":{"exc":True,"normal":0}},
"bone leggings":{"10":{"exc":True,"normal":True},"20":{"exc":True,"normal":0}},
"bone armor":{"10":{"exc":True,"normal":True},"20":{"exc":True,"normal":0}},


"leather shorts":{"10":{"exc":True,"normal":True},"20":{"exc":True,"normal":True}},
"leather skirt":{"10":{"exc":True,"normal":True},"20":{"exc":True,"normal":True}},
"leather bustier":{"10":{"exc":True,"normal":True},"20":{"exc":True,"normal":True}},
"studded bustier":{"10":{"exc":True,"normal":True},"20":{"exc":True,"normal":True}},
"leather armor":{"10":{"exc":True,"normal":True},"20":{"exc":True,"normal":True}},
"studded armor":{"10":{"exc":True,"normal":True},"20":{"exc":True,"normal":True}},

"leather gorget":{"10":{"exc":True,"normal":True},"20":{"exc":True,"normal":True}},
"leather cap":{"10":{"exc":True,"normal":True},"20":{"exc":True,"normal":True}},
"leather gloves":{"10":{"exc":True,"normal":True},"20":{"exc":True,"normal":True}},
"leather sleeves":{"10":{"exc":True,"normal":True},"20":{"exc":True,"normal":True}},
"leather leggings":{"10":{"exc":True,"normal":True},"20":{"exc":True,"normal":True}},
"leather tunic":{"10":{"exc":True,"normal":True},"20":{"exc":True,"normal":True}}}           
            
            
tooling = {
"sewing":{"itemid":0x0F9D,"menu":8,"submenu":0,"item":44},
"tinker":{"itemid":0x1EB8,"menu":8,"submenu":0,"item":23}}            

the_mats = {
    "cloth":{"id":0x1766,"hue":0x0000,"weight":0.1},
    "bone":{"id":0x0F7E,"hue":0x0000,"weight":1},
    "leather":{"id":0x1081,"hue":0x0000,"weight":1},
    "spined":{"id":0x1081,"hue":0x05e4,"weight":1},
    "horned":{"id":0x1081,"hue":0x0900,"weight":1},
    "barbed":{"id":0x1081,"hue":0x059d,"weight":1},
    "iron":{"id":0x1BF2,"hue":0x0000,"weight":0.1}}


def get_iron():
    #Misc.SendMessage('Checking Iron for tools ',10)
    mchest = Items.FindBySerial(matchest)
    Misc.Pause(100)
    Items.UseItem(mchest)
    Misc.Pause(550)
    Items.WaitForContents(mchest,1000)
    Misc.Pause(100)
    mat1string = "iron"
    mat1_inbag = Items.BackpackCount(the_mats[mat1string]["id"],the_mats[mat1string]["hue"])
    inchest = Items.ContainerCount(mchest, the_mats[mat1string]["id"], the_mats[mat1string]["hue"])
    if inchest :
        keep = 50 - mat1_inbag
        if keep:
            if inchest < keep:
                Misc.SendMessage('Running low on '+str(mat1string),errorcolour)
            else:
                mat1 = Items.FindByID(the_mats[mat1string]["id"],the_mats[mat1string]["hue"],mchest.Serial)
                Misc.Pause(dragTime)
                Items.Move(mat1.Serial, Player.Backpack.Serial, keep)
                Misc.Pause(dragTime)
    else :
        Misc.SendMessage('Using last of '+str(mat1string),errorcolour)




def check_tools(thebod):
    get_iron()
    Misc.Pause(useitempause)
    thetool = Items.BackpackCount(tooling[thebod["Tool"]]["itemid"],-1)
    while thetool < 3:
        tinkerTool = find_tool(tooling['tinker']["itemid"])
        Items.UseItem(tinkerTool)
        Gumps.WaitForGump( 0, 2000 )
        Gumps.SendAction(  0, tooling[thebod["Tool"]]["menu"] )
        Gumps.WaitForGump( 0, 2000 )
        Gumps.SendAction(  0, tooling[thebod["Tool"]]["item"] )
        Misc.Pause(2200)
        thetool = Items.BackpackCount(tooling[thebod["Tool"]]["itemid"],-1)
    tinkerTool = Items.BackpackCount(tooling['tinker']["itemid"],-1)
    while tinkerTool < 2:
        tinkerTool = find_tool(tooling['tinker']["itemid"])
        Items.UseItem(tinkerTool)
        Gumps.WaitForGump( 0, 2000 )
        Gumps.SendAction(  0, tooling["tinker"]["menu"] )
        Gumps.WaitForGump( 0, 2000 )
        Gumps.SendAction(  0, tooling["tinker"]["item"] )
        Misc.Pause(2200)
        tinkerTool = Items.BackpackCount(tooling['tinker']["itemid"],-1)
    Gumps.SendAction( 0, 0 )








        
        
def ReadBod(bod):
    thebod = {"bod_serial":bod.Serial,
    "Status":0,
    "Itemstring":0,
    "ItemID":0,
    "Tool":0,
    "Exc":"normal",
    "Mat":0,
    "FinalHue":0,
    "Amount":0,
    "Made":0,
    "Able_to_make":0,
    "Lsize":0}
    
    det = Items.GetPropStringList(bod)
    len_det = len(det)
    #Player.HeadMessage(47,str(det))
    
    if bod.Hue == 0x0483:
        for i in range(len(det)):
            if "large bulk order" in det[i].lower() :
                Misc.SendMessage('Large BOD detected ',100)
                num = 1
                props = len(det)
                for i in range(len(det)):
                    if "amount to make:" in det[i].lower() :
                        thebod["Amount"] = int(det[i].split(':')[1])
#                        Misc.SendMessage('Its there size '+str(size),100)
#                        Misc.SendMessage('items in lbod '+str(props - num),100)
                        
                        ssize=[0,1,2,3,"four","five","six"]
                        thebod["Lsize"] = ssize[props - num]
                    if "exceptional" in det[i].lower() :
                        Misc.SendMessage('exceptional',100)
                        thebod["Exc"] = "exc"
                        #thebod["Exc"] = True
                    if "must be made with" in det[i]:
                        mat = det[i].split(' ')[-2]
                        thebod["Mat"] = mat
                    num +=1
                if not thebod["Mat"]:
                    if "tunic" in det[-1:][0].lower() or "armour" in det[-1:][0].lower() or "studded" in det[-1:][0].lower():
                        mat = "leather"
                    else:
                        mat = "cloth"
                    thebod["Mat"] = mat
                    #Misc.SendMessage('Made from  '+str(mat),100)    
            
                thebod["Status"] = "Complete"
                return thebod


        thebod["Tool"] = "sewing"
        
        if "exceptional." in det[5]:
            thebod["Exc"] = "exc"
            #Player.HeadMessage(10,det[6])
        else:
            thebod["Exc"] = "normal"
        thebod["Amount"] = int(det[len_det-2].split(' ')[3])
        thebod["Itemstring"]= det[len_det-1].split(':')[0].strip("'") #'
        thebod["Made"]= int(det[len_det-1].split(':')[1])
        thebod["Mat"] = tailoring[thebod["Itemstring"]]["defaultmat"]
        if "leather" in det[len_det-3]:
            #thebod["Mat"] = det[6].split(' ')[-2]
            thebod["Mat"] = det[len_det-3].split(' ')[-2]
            if thebod["Mat"] == "leather":
                thebod["FinalHue"] = 0x0000
            elif thebod["Mat"] == "spined":
                thebod["FinalHue"] = 0x05e4
            elif thebod["Mat"] == "horned":
                thebod["FinalHue"] = 0x0900
            elif thebod["Mat"] == "barbed":
                thebod["FinalHue"] = 0x059d

        #Player.HeadMessage(10,str(thebod))
        thebod["ItemID"] = tailoring[thebod["Itemstring"]]["itemid"]
        if thebod["Made"] == thebod["Amount"]:
            thebod["Status"] = "Complete"
        return thebod
    else:
        thebod["Status"] = "Type"
        
    return thebod



def dumpMats():
    dumpIDs = []
    for i in matIdList:
        ID = i[1]
        dumpIDs.append(ID)
    for item in Player.Backpack.Contains:
        if item.ItemID in dumpIDs:
            Items.Move(item,self.resCont.Serial,0)
            Misc.Pause(1200)


            

def find_tool(toolID):    
    for i in Player.Backpack.Contains:
        if i.IsContainer:
            for ii in i.Contains:
                if ii.ItemID == toolID:
                    return ii
        elif i.ItemID == toolID:
            return i               
    Player.HeadMessage(23, 'no tools found')

    
            

def make(thebod):
    if thebod["Tool"] == "sewing":
        toolID = 0x0F9D    
    tool = find_tool(toolID)
    Misc.Pause(250)
    if thebod["Mat"] in ["leather","spined","horned","barbed"]:
        Items.UseItem( tool )
        Gumps.WaitForGump( 0, 2000 )
        Gumps.SendAction(  0, 7 )
        Gumps.WaitForGump( 0, 2000 )
        if thebod["Mat"] == "leather":
            selection = 6
        elif thebod["Mat"] == "spined":
            selection = 13
        elif thebod["Mat"] == "horned":
            selection = 20
        elif thebod["Mat"] == "barbed":
            selection = 27
        Gumps.SendAction(  0, selection)        
        Gumps.WaitForGump( 0, 2000 )
        Gumps.SendAction( 0, 0 )
    Misc.Pause(450)    
    Player.HeadMessage( 20, 'Making '+str(thebod["Able_to_make"])+" "+str(thebod["Itemstring"]))  
    for i in range(thebod["Able_to_make"]):
        tool = find_tool(toolID)
        Items.UseItem( tool )
        Gumps.WaitForGump( 0, 2000 )
        Gumps.SendAction(  0, tailoring[thebod["Itemstring"]]["menu"] )
        Gumps.WaitForGump( 0, 2000 )
        Gumps.SendAction(  0, int(tailoring[thebod["Itemstring"]]["item"] ))
        Misc.Pause(2200)
        #guards()

    Misc.Pause(800)
    Gumps.SendAction( 0, 0 )
    return thebod

def add_to(thebod):
    Misc.SendMessage('Adding Items to Bod ',10)
    bod = Items.FindBySerial(thebod["bod_serial"])
    Misc.Pause(500)
    theitem = thebod["ItemID"]
    Items.UseItem(bod)
    ##Misc.SendMessage('Gets to here ',48)
    Misc.Pause(useitempause)
    Gumps.WaitForGump( 0, 2000 )
    Gumps.SendAction(  0, 2 )
    Target.WaitForTarget(2000)
    
    if thebod["Exc"] == "normal" :
        for i in Player.Backpack.Contains :
            if i.ItemID == theitem and thebod["FinalHue"] == i.Hue :
                #Misc.SendMessage('We have a match ',48)
                Target.WaitForTarget(500)
                Misc.Pause(300)
                Target.TargetExecute(i.Serial)
    else:     
        for i in Player.Backpack.Contains :
            if i.ItemID == theitem and thebod["FinalHue"] == i.Hue :
                Items.WaitForProps(i.Serial,1000)
                det = Items.GetPropStringList(i)              
                if "exceptional" in det[0].lower() or "exceptional" in det[-1:][0].lower() or "exceptional" in det :
                    Target.WaitForTarget(500)  
                    Misc.Pause(300)  
                    Target.TargetExecute(i)                  
    Misc.Pause(250)                
    if Target.HasTarget():
        Target.Cancel()
    Gumps.SendAction(  0, 0 )



def check_recycle(thebod):
    moved = 0
    Misc.SendMessage('Checking Recycle ',10)
    Player.HeadMessage(10,str(thebod))
    rchest = Items.FindBySerial(recyclechest)
    Misc.Pause(550)
    Items.UseItem(rchest)
    Misc.Pause(550)
    Items.WaitForContents(rchest,1000)
    Misc.Pause(550)
    theitem = thebod["ItemID"]
    #if thebod["Exc"] == False :
    if thebod["Exc"] == "normal":
        for i in rchest.Contains :
            #Misc.SendMessage(str(i),10)
            if i.ItemID == theitem and thebod["FinalHue"] == i.Hue :
                #Misc.SendMessage('We have a match ',48)
                Items.Move(i,Player.Backpack.Serial,1)
                Misc.Pause(moveitempause)
                moved += 1
    else:     
        for i in rchest.Contains :
            Items.WaitForProps(i.Serial,1000)
            #Player.HeadMessage(10,"ItemID "+str(i.ItemID)+" "+str(theitem))
            #Player.HeadMessage(10,"hue "+str(thebod["FinalHue"])+" "+str(i.Hue))

            if i.ItemID == theitem and thebod["FinalHue"] == i.Hue :
                #Player.HeadMessage(10,"GETS HRER")
                det = Items.GetPropStringList(i)              
                if "exceptional" in det[0].lower() or "exceptional" in det[-1:][0].lower() :
                    Items.Move(i,Player.Backpack.Serial,1)
                    Misc.Pause(moveitempause)
                    moved +=1
    Misc.Pause((moved*200))
    return moved
                 





        
GFilter = Items.Filter()
GFilter.RangeMax = 5
GFilter.OnGround = True
GFilter.Enabled = True
GFilter.Movable = True
garbagecan = List[int]([0x0E77, 0x0E77])
GFilter.Graphics = garbagecan        
        
def recycle(thebod):
    Misc.SendMessage('Recycling ',10)
    rchest = Items.FindBySerial(recyclechest)
    theitem = thebod["ItemID"]
    for i in Player.Backpack.Contains :
        Misc.Pause(20)
        if i.ItemID == theitem and thebod["FinalHue"] == i.Hue :
            if tailoring[thebod["Itemstring"]]["recycle"] == True:
                scissors = Items.FindByID(scissorsID,-1,Player.Backpack.Serial)
                Items.UseItem(scissors)
                Target.WaitForTarget(2000,False)
                Target.TargetExecute(i.Serial)
                Misc.Pause(1200)
            else:
                rchest = Items.FindBySerial(recyclechest)
                Misc.Pause(100)
                Items.Move(i,rchest,1)
                Misc.Pause(moveitempause)    

    Misc.Pause(500)
#cloth,hides, #scales, # chopped bones, # Dirt, #worms # feathers
resources = [0x1766,0x1081,0x26B4,0x0F7E,0x0F81,0x5744,0x1BD1,0x487D,0x4862]
                
def dump_materials():
    Misc.SendMessage('Returning leftover Materials ',10)
    mchest = Items.FindBySerial(matchest)
    for i in Player.Backpack.Contains :
        Misc.Pause(20)
        if i.ItemID in resources:
            Items.Move(i.Serial, mchest, 0)
            Misc.Pause(moveitempause)    
    Misc.Pause(700)
        
        


def weight_for_one(mat1,number1,mat2,number2):
    mone = max((the_mats[mat1]["weight"] * number1),1)
    if number2:
        mtwo = max((the_mats[mat2]["weight"] * number2),1)
    else:
        mtwo = 0
    return mone,mtwo    
    
def get_mats(thebod):
    Misc.SendMessage('Getting Mats ',10)
    mchest = Items.FindBySerial(matchest)
    Misc.Pause(500)
    Items.UseItem(mchest)
    Misc.Pause(550)
    Items.WaitForContents(mchest,1000)
    Misc.Pause(100)
    if thebod["Mat"]:
        mat1string = thebod["Mat"]
    else:
        mat1string = tailoring[thebod["Itemstring"]]["defaultmat"]
    mat1num = tailoring[thebod["Itemstring"]]["mat1"]
    mat2string = tailoring[thebod["Itemstring"]]["secondarymat"]
    mat2num = tailoring[thebod["Itemstring"]]["mat2"]
    thebod["ItemID"] = tailoring[thebod["Itemstring"]]["itemid"]
    mone,mtwo = weight_for_one(mat1string,mat1num,mat2string,mat2num)
    
    mat1_inbag = Items.BackpackCount(the_mats[mat1string]["id"],the_mats[mat1string]["hue"])
    if mtwo:
        mat2_inbag = Items.BackpackCount(the_mats[mat2string]["id"],the_mats[mat2string]["hue"])

    free_weight = Player.MaxWeight - Player.Weight
    left_to_make = int(thebod["Amount"])-int(thebod["Made"])

    inchest = Items.ContainerCount(mchest, the_mats[mat1string]["id"], the_mats[mat1string]["hue"])
    if inchest < left_to_make*mat1num:
        Misc.SendMessage('Not Enough '+str(mat1string),errorcolour)
        thebod["Status"] = "Resources"
        return thebod
    if mtwo:
        inchest2 = Items.ContainerCount(mchest, the_mats[mat2string]["id"], the_mats[mat2string]["hue"])
        if inchest2 < left_to_make*mat2num:
            Misc.SendMessage('Not Enough '+str(mat2string),errorcolour)
            thebod["Status"] = "Resources"
            return thebod
        
    able_to_make = left_to_make
    thebod["Able_to_make"] = able_to_make
    if ((mone+mtwo)*left_to_make)>free_weight:
        able_to_make = int(free_weight/(mone+mtwo))
        thebod["Able_to_make"] = able_to_make
        Misc.SendMessage('Only Moving enough materials for '+str(able_to_make),100)
    elif 50 > free_weight :
        Misc.SendMessage('Carrying too much weight',errorcolour)
        thebod["Status"] = "Weight"
        return thebod
    mat1 = Items.FindByID(the_mats[mat1string]["id"],the_mats[mat1string]["hue"],mchest.Serial)
    Misc.Pause(dragTime)
    if (able_to_make*mat1num)-mat1_inbag != 0 :
        Items.Move(mat1.Serial, Player.Backpack.Serial, int((able_to_make*mat1num)-mat1_inbag))
        Misc.Pause(dragTime)
    if mtwo:
        mat2 = Items.FindByID(the_mats[mat2string]["id"],the_mats[mat2string]["hue"],mchest.Serial)
        Misc.Pause(dragTime)
        if (able_to_make*mat2num)-mat2_inbag != 0 :
            Items.Move(mat2.Serial, Player.Backpack.Serial, int((able_to_make*mat2num)-mat2_inbag))
            Misc.Pause(dragTime)
                        
    return thebod            
    


                
                
    
  
    
                    
                
                
def move_sorted_to_book(amount,bodbook,bodserial):
   
    chests = books[amount]["chest"]
    bookss = books[amount][bodbook]
    bod  = Items.FindBySerial(bodserial)

    #Misc.Pause(useitempause)
    bchest = Items.FindBySerial(chests)
    #Misc.Pause(useitempause)
    Items.UseItem(bchest)
    Misc.Pause(useitempause)
    Items.WaitForContents(bchest,1000)
    Misc.Pause(useitempause)
    book = Items.FindBySerial(bookss)
    if book:
        
        Items.Move(book, Player.Backpack.Serial, 1)
        Misc.Pause(moveitempause)
        Misc.Pause(100)
        Items.Move(bod, book, 1)
        Misc.Pause(100)
        Misc.Pause(moveitempause)
        Items.Move(book, bchest, 1)
        Misc.Pause(100)
        Misc.Pause(moveitempause)
        Gumps.SendAction( 0, 0 )
    
def bod_sorter(thebod):
    Misc.SendMessage(str(thebod),98)
    Misc.Pause(useitempause)
    if thebod['Lsize']:
        samount = str(thebod['Amount'])
        if thebod['Amount'] == 15:
            samount = "10"
        if thebod['Mat'] in ["spined","barbed","horned"]:
            #Misc.SendMessage('Fuck yeah keep this one',78)
            move_sorted_to_book(str(thebod['Amount']),"lbods",thebod["bod_serial"])
        
        elif lbod_grid[thebod['Mat']][thebod['Lsize']][samount][thebod['Exc']]:
            #Misc.SendMessage('Fuck yeah keep this one',78)
            move_sorted_to_book(str(thebod['Amount']),"lbods",thebod["bod_serial"])
        else:
            Misc.SendMessage('Crap LBOD',78)
            move_sorted_to_book("bin","book",thebod["bod_serial"])
    else:
        samount = str(thebod['Amount'])
        if thebod['Amount'] == 15:
            samount = "10"
        if thebod['Mat'] in ["spined","barbed","horned"]:
            mats = "hides"
            move_sorted_to_book(str(thebod['Amount']),mats,thebod["bod_serial"]) 
        elif sbod_grid[thebod['Itemstring']][samount][thebod['Exc']]:
            mats = thebod['Mat']
            move_sorted_to_book(str(thebod['Amount']),mats,thebod["bod_serial"])    
        else:
            Misc.SendMessage('Crap SBOD',78)
            move_sorted_to_book("bin","book",thebod["bod_serial"])

def worldSave():
    if (Journal.SearchByType('The world will save in 1 minute.', 'System') or Journal.SearchByType('pause', 'Regular')):
        Misc.Pause(700)
        Misc.SendMessage('Pausing for world save or player-called break.', 33)
        while (not Journal.SearchByType('World save complete.', 'System') and not Journal.SearchByType('play', 'Regular')):
            Misc.Pause(1000)
        Misc.Pause(2500)
        Misc.SendMessage('Continuing run', 33)
        Misc.Pause(700)
    Journal.Clear()  
    
    
def fill_bod(thebod):
    thebod = get_mats(thebod)
    if thebod:
        thebod = make(thebod)
        add_to(thebod)
    
def workTheBod(bod):
    worldSave()
    thebod = ReadBod(bod)
    if thebod["Status"] != "Complete":
        rec_num = check_recycle(thebod)
        if rec_num > 0:
            Misc.SendMessage('Nice, Recycled '+str(rec_num)+" Items",78)
            add_to(thebod)
            thebod = ReadBod(bod)
            Misc.Pause(moveitempause)
        check_tools(thebod)
        while thebod["Status"] not in ["Complete", "Resources","Weight","Type"]:
            Misc.Pause(moveitempause)
            fill_bod(thebod)
            thebod = ReadBod(bod)
        if thebod["Status"] == "Complete":
            Misc.SendMessage('Bod Finished ',100)
            recycle(thebod)
            dump_materials()
    
    if thebod["Status"] == "Weight":
        Misc.SendMessage('Carrying too much weight, Stopping ',100)
        return
    if thebod["Status"] == "Complete":
        if sort_bods == True:
            bod_sorter(thebod)
    
def file_bods():
    for i in Player.Backpack.Contains:
        sortbook = Items.FindByName("Sort", 0x0000, Player.Backpack.Serial, 4)
        if i.ItemID == 0x14EF:
            Items.Move(i,sortbook,1)
            Misc.Pause(1000)    

Journal.Clear()
Misc.Pause(500)    
for i in Player.Backpack.Contains:
    if i.Hue == 0x0483:
        workTheBod(Items.FindBySerial(i.Serial))

file_bods()
Misc.Pause(2000)




