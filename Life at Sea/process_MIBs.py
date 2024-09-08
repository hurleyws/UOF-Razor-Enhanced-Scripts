MibFileName = 'C:/Program Files (x86)/UOForever/UO/Forever/Data/Client/userMarkers.USR'    
#MibFileName = 'C:\Program Files (x86)\UOForever\UO\Forever\Data\Client\userMarkers.usr'
 
rawmibid= 0x099F
openedmibid = 0x14EE
rawmibstorage =0x42BE72DE
catalogedstorage = 0x42557C9C
MibContainer = Player.Backpack.Serial
TargetName = "SOS"
#
LordBritishThrone=[1624, 1323]    
WorldSize = [4096, 5120]
TilesPerDegree= [ WorldSize[0]/360.0, WorldSize[1]/360.0 ] 
#
 
def worldSave():
    if Journal.SearchByType('The world will save in 1 minute.', 'Regular' ):
        Misc.SendMessage('Pausing for world save', 33)
        while not Journal.SearchByType('World save complete.', 'Regular'):
            Misc.Pause(500)
        Misc.Pause(2500)
        Misc.SendMessage('Continuing run', 33)
        Journal.Clear()   
 
 
def splitToPieces(location):
    degree, secTemp= location.split('\xb0')
    seconds, direction = secTemp.split('\x27')
    return int(degree), int(seconds), direction
 
def convertDegreesToDecimal(degree, seconds, direction):
    result = 0
    if direction.lower() == 'w': 
        result = (LordBritishThrone[1]-(seconds/60.0)* TilesPerDegree[1]-degree*TilesPerDegree[1])%WorldSize[1]
    #    
    if direction.lower() == 'e': 
        result = (LordBritishThrone[1]+(seconds/60.0)* TilesPerDegree[1]+degree*TilesPerDegree[1])%WorldSize[1]
    #    
    if direction.lower() == 'n': 
        result = (LordBritishThrone[0]-(seconds/60.0)* TilesPerDegree[0]-degree*TilesPerDegree[0])%WorldSize[0]
    #    
    if direction.lower() == 's': 
        result = (LordBritishThrone[0]+(seconds/60.0)* TilesPerDegree[0]+degree*TilesPerDegree[0])%WorldSize[0]
    #    
    return int(result)+1
 
def GetDecimalCoordinates(mib):
    x = -1
    y = -1
    Items.UseItem(mib)
    Gumps.WaitForGump(0, 3000)
    if Gumps.HasGump():
        texts = Gumps.LastGumpGetLineList()
        location = texts[len(texts)-1]
        z = location.split(',')
        Player.HeadMessage(54, str(z[1]))
        NSloc, EWloc = location.split(',')
        deg1, sec1, dir1 = splitToPieces(NSloc) 
        deg2, sec2, dir2 = splitToPieces(EWloc)
        Gumps.CloseGump(0)
        #
        Misc.SendMessage("deg: {} sec: {} dir: {}".format(deg1, sec1, dir1))
        Misc.SendMessage("deg: {} sec: {} dir: {}".format(deg2, sec2, dir2))
        x = convertDegreesToDecimal(deg2, sec2, dir2)
        y = convertDegreesToDecimal(deg1, sec1, dir1)
        return x, y
    else:
        Misc.SendMessage("Gump did not Open for mib 0x{:x}".format(mib.Serial))
    return x, y
 
def examplemain():
    if MibContainer != None:
        for maybeMIB in MibContainer.Contains:
            if maybeMIB.ItemID == 0x099F and maybeMIB.Hue == 0x0:
                mib = maybeMIB
                Items.UseItem(mib.Serial)
                Misc.Pause(1000)
        Items.WaitForContents(MibContainer, 3000)        
        #
        with open(MibFileName, 'w') as file:
            file.write("3\n")
        #        
            for maybeMIB in MibContainer.Contains:
                if maybeMIB.ItemID == 0x14EE and maybeMIB.Hue == 0x0:
                    mib = maybeMIB
                    x, y = GetDecimalCoordinates(mib)
                    Misc.SendMessage("X: {}".format(x))
                    Misc.SendMessage("Y: {}".format(y))
                    file.write("+treasure: {} {} 0 {}\n".format(x, y, TargetName))
                if maybeMIB.ItemID == 0x14EE and maybeMIB.Hue == 0x0481:
                    mib = maybeMIB
                    x, y = GetDecimalCoordinates(mib)
                    Misc.SendMessage("X: {}".format(x))
                    Misc.SendMessage("Y: {}".format(y))
                    file.write("+treasure: {} {} 0 {}\n".format(x, y, "Ancient "+TargetName))                
 
 
def noxmain(mib):
    Items.UseItem(mib)
    Misc.Pause(800)
    f = open(MibFileName, 'a')    
    x, y = GetDecimalCoordinates(mib)
    Player.HeadMessage(54, str(x))
    Player.HeadMessage(54, str(y))
    Misc.SendMessage("X: {}".format(x))
    Misc.SendMessage("Y: {}".format(y))
    z = str(x) + ',' + str(y) + ',0,'+  str(x) + ' ' + str(y) +',,' + 'red' + ',3'
    Misc.Pause(100)
    f.write(z)
    Misc.Pause(100)
    f.write("\n")
    Gumps.SendAction(1426736667, 0)
    Misc.Pause(800)
    f.close()     
 
 
 
 
Items.UseItem(rawmibstorage)
Misc.Pause(800)
Items.UseItem(catalogedstorage)
 
Player.HeadMessage(54, 'starting to process mibs')
Misc.Pause(800)
 
chest = Target.PromptTarget("select chest with mibs to catalog")   
Items.UseItem(chest)  
Misc.Pause(800) 
targetchest = Items.FindBySerial(chest)
for i in targetchest.Contains:
    worldSave()
    Items.Move(i, Player.Backpack.Serial, -1)
    Misc.Pause(800)
    if Items.FindByID(rawmibid, -1, Player.Backpack.Serial):
        Player.HeadMessage(54,'Cracking Mibs')        
        Items.UseItem(i)
        Misc.Pause(800)
 
    if Items.FindByID(openedmibid, -1, Player.Backpack.Serial):
        ii = Items.FindByID(openedmibid, -1, Player.Backpack.Serial)
        noxmain(ii)
        Misc.Pause(800)
        Items.Move(ii, chest, -1)
        Misc.Pause(800)
 

 