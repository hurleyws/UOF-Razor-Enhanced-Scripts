import time
import random

def repairCheck():
    repairPouch = Items.FindBySerial(0x41547DA9)
    
    if repairPouch:
        prop_list = Items.GetPropStringByIndex(repairPouch,4)
        prop_list_split = prop_list.split()
        items = prop_list_split[0]
        items = int(items)
    
        if items > 0 :
            Player.ChatSay("Looks like repairs are in order.")
            Misc.Pause(1500)
            Player.PathFindTo(6801, 3898, 17)
            Misc.Pause(2000)
            Items.UseItem(repairPouch)
            Misc.Pause(500)
            staff = Items.FindByID(0x0E89,-1,repairPouch.Serial)
            Misc.Pause(200)
            if staff:
                Items.Move(staff,Player.Backpack.Serial,1)
                Misc.Pause(1000)
            staff = Items.FindByID(0x0E89,-1,Player.Backpack.Serial)
            if staff:
                Misc.Pause(200)
                Items.UseItemByID(0x1034,-1)
                Misc.Pause(500)
                Gumps.WaitForGump(949095101, 10000)
                Gumps.SendAction(949095101, 42)
                Misc.Pause(500)
                Target.TargetExecute(staff)
                Misc.Pause(500)
                Gumps.WaitForGump(949095101, 10000)
                Gumps.SendAction(949095101, 0)
                Misc.Pause(500)
                Items.Move(staff,0x42EA55BA,1)
                Misc.Pause(1000)
                Player.ChatSay("This looks good as new.")
                Misc.Pause(1000)
            Player.PathFindTo(6804, 3897, 17)
            Misc.Pause(2000)

def trashCheck():
    for item in Player.Backpack.Contains:
        prop_list = Items.GetPropStringList(item)

        # Keywords for weapons
        weapon_keywords = ["mace", "axe", "katana", "halberd", "kryss"]

        # Check for "bone" keyword
#        if "bone" in str(prop_list):
#            Player.HeadMessage(64, "Bone item! Tossing...")
#            Misc.Pause(1000)
#            Items.MoveOnGround(item, 1, Player.Position.X - 1, Player.Position.Y, Player.Position.Z)
#            Misc.Pause(1000)

        # Check if property list length is >= 9 and contains a weapon keyword
        if len(prop_list) >= 9 and any(keyword in prop.lower() for prop in prop_list for keyword in weapon_keywords) and item.ItemID == 0x14EF:
            Player.HeadMessage(64, "Large weapon BOD! Tossing...")
            Misc.Pause(1000)
            Items.MoveOnGround(item, 1, Player.Position.X - 1, Player.Position.Y, Player.Position.Z)


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

def stockRegs():
    root = Items.BackpackCount(0x0F7A,-1)
    moss = Items.BackpackCount(0x0F7B,-1)
    pearl = Items.BackpackCount(0x0F86,-1)
  
    
    if root < 15:
        Items.Move(Items.FindByID(0x0F7A,-1,0x42E88440),Player.Backpack.Serial,15-root)
        Misc.Pause(1000)
    
    if moss < 15:
        Items.Move(Items.FindByID(0x0F7B,-1,0x42E88440),Player.Backpack.Serial,15-moss)
        Misc.Pause(1000)
        
    if pearl < 15:
        Items.Move(Items.FindByID(0x0F86,-1,0x42E88440),Player.Backpack.Serial,15-pearl)
        Misc.Pause(1000)
        
    else:
        Player.HeadMessage(64,"Regs look good")
        Misc.Pause(500)
    
def bod_run():
    Journal.Clear()
    # Randomly select a wait time between 90 and 120 seconds
    wait_time = random.randint(75, 300)
    # Inform the player about the wait time
    Player.ChatSay(64, f"Making a run in {wait_time} seconds.")
    # Convert wait time to milliseconds and pause
    Misc.Pause(wait_time * 1000)
    Misc.ScriptStopAll(True)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, 0)
    worldSave()
    Player.ChatSay(64,'[recall Britain Crafting')
    Misc.Pause(3000)
    Misc.WaitForContext(0x00029397, 10000)
    Misc.ContextReply(0x00029397, 1)
    Misc.Pause(1000)
    while Gumps.HasGump():
        Gumps.WaitForGump(2611865322, 1000)
        Misc.Pause(1200)
        Gumps.SendAction(2611865322, 1)
        Misc.Pause(500)
        Gumps.WaitForGump(3188567326, 1000)
        Gumps.SendAction(3188567326, 1)
        Misc.Pause(500)
    Player.ChatSay(64,'[recall Britain Crafting 2')
    Misc.Pause(3000)
    Misc.WaitForContext(0x0024A965, 10000)
    Misc.ContextReply(0x0024A965, 1)
    Misc.Pause(1000)
    while Gumps.HasGump():
        Gumps.WaitForGump(2611865322, 1000)
        Misc.Pause(1200)
        Gumps.SendAction(2611865322, 1)
        Misc.Pause(500)
        Gumps.WaitForGump(3188567326, 1000)
        Gumps.SendAction(3188567326, 1)
        Misc.Pause(500)
    Misc.Pause(2000)
    while Player.Mana < 11:
        Misc.Pause(1000)
    Player.ChatSay(64,'[recall Winter Lodge')
    Misc.Pause(3000)
    trashCheck()
    Player.PathFindTo(6802, 3901, 12)
    Misc.Pause(1500)
    door = Items.FindBySerial(0x42F89EDC)
    if door.ItemID == 0x0677:
        Items.UseItem(door)
        Misc.Pause(500)
    Player.PathFindTo(6802, 3900, 17)
    Misc.Pause(1500)      
    Items.UseItem(0x42E88440) #Open box by door
    Misc.Pause(1000)
    stockRegs()
    for i in Player.Backpack.Contains: #Sort/store tailor BODS
        if i.ItemID == 0x14EF and i.Hue == 1155:
            Items.Move(i,0x4194BF9C,-1)
            Misc.Pause(1000)
        
    for i in Player.Backpack.Contains: #Sort/store blacksmith BODS
        list = Items.GetPropStringList(i)
        len_det = len(list)
        keywords = ["mace", "axe", "katana", "halberd"]
        if i.ItemID == 0x14EF and len_det > 9:
            Items.Move(i,0x40C8592D,-1)
            Misc.Pause(1000)
        if i.ItemID == 0x14EF and len_det == 9:
            Items.Move(i,0x42369679,-1)
            Misc.Pause(1000)
        if i.ItemID == 0x14EF and len_det == 7:
            Items.Move(i,0x4236967B,-1)
            Misc.Pause(1000)
        if i.ItemID == 0x14EF and len_det == 8 and "exceptional." in str(list):
            Items.Move(i,0x49A27509,-1)
            Misc.Pause(1000)
        if i.ItemID == 0x14EF and len_det == 8 and not "exceptional." in str(list):
            Items.Move(i,0x4236967A,-1)
            Misc.Pause(1000)
    
    if Player.Name == 'ToolmanTailor':
        Player.PathFindTo(6800, 3898, 17)
        Misc.Pause(2000)
        Player.Run("West")
    elif Player.Name == 'Realtree':
        Player.PathFindTo(6804, 3897, 17)
        Misc.Pause(3000)
        Player.Run("North")
    elif Player.Name == 'Tool Time':
        Player.PathFindTo(6800, 3892, 17)
        Misc.Pause(5000)
        Player.Run("North")
    elif Player.Name == 'ImaTool':
        Player.PathFindTo(6805, 3892, 17)
        Misc.Pause(5000)
        Player.Run("North")          
            
    Player.ChatSay(64, 'Bod run complete')
    Misc.Pause(1000)
    if Journal.Search('You can ask for a bulk order deed in'):
        string = Journal.GetLineText('You can',False)
        string = string.split("in")
        string = string[1]
        string = string.split("h")
        string = string[0]
        hour = int(string)
        mstring = Journal.GetLineText('You can',False)
        mstring = mstring.split("in")
        mstring = mstring[1]
        mstring = mstring.split("m")
        mstring = mstring[0]
        mstring = mstring.split("h ")
        mstring = mstring[1]
        min = int(mstring)
        sleepTime = (hour*60) + min + 2
        Misc.Pause(500)
        Player.ChatSay(64,"I was too early. Will return in " + str(hour) + " hours and " + str(min) + " minutes.")
        Misc.Pause(1000)
        if Player.Name == 'ToolmanTailor':
            for x in range(hour):
                Player.ChatSay("I have more than an hour to wait, making a farm run.")
                Misc.Pause(1000)
                Misc.ScriptRun("FarmGod.py")
                time.sleep(60*60)
            time.sleep(60*min)
            Journal.Clear()
        elif Player.Name == "ImaTool":
            Player.ChatSay("I will make "+str(hour)+" treasure runs in the meantime.")
            Misc.Pause(1000)
            for x in range(0,hour):
                Misc.ScriptRun("treasure_God.py")
                time.sleep(1*60*60)
            Player.ChatSay("Now just waiting the final "+str(min)+" minutes.")
            Misc.Pause(1000)
            time.sleep(60*(min+2))
            Journal.Clear()
        elif Player.Name == "Tool Time":
            Misc.ScriptRun("trashPanda.py")
            time.sleep(60*sleepTime)
            Journal.Clear()
        elif Player.Name == "Realtree":
#            Items.UseItem(0x42E87E92)
#            Misc.Pause(500)
#            Items.UseItem(0x41132AE2)
#            Misc.Pause(500)
#            logs = Items.ContainerCount(0x41132AE2,0x1BDD,0x0000)
#            if logs > 30000:
#                packingots = Items.BackpackCount(0x1BF2,0x0000)
#                ingotstorage = Items.FindByID(0x1BF2,0x0000,0x42E87E92)
#                if packingots < 50:
#                    Items.Move(ingotstorage,Player.Backpack.Serial,200-packingots)
#                    Misc.Pause(1000)
#                packlogs = Items.BackpackCount(0x1BDD,0x0000)
#                logstorage = Items.FindByID(0x1BDD,0x0000,0x41132AE2)
#                if packlogs < 1000:
#                    Items.Move(logstorage,Player.Backpack.Serial,1000-packlogs)
#                    Misc.Pause(1000)
#                Player.ChatSay("[recall Trainer")
#                Misc.Pause(3000)
#                Misc.ScriptRun("trainArtisan.py")
#            Misc.ScriptRun("train_Empower.py")
            time.sleep(60*sleepTime)
            Journal.Clear()
        
        else:
            time.sleep(60*sleepTime)
            Journal.Clear()
        bod_run()
 


    
while True:
    bod_run()
    Misc.Pause(500)
    if Player.Name == 'Realtree':
        Items.UseItem(0x42E87E92)
        Misc.Pause(1000)
        Items.UseItem(0x49A27509)
        Misc.Pause(1000)
        ironExcept = Items.ContainerCount(0x49A27509,0x14EF,0x044e)
        Misc.Pause(500)
        Misc.SendMessage("Iron Exceptional "+str(ironExcept))
        Misc.Pause(1000)
        if ironExcept > 9:
            Misc.ScriptRun("BOD_runIronExcept.py")
        Misc.Pause(1000)
        while Misc.ScriptStatus("BOD_runIronExcept.py"):
            Misc.Pause(10000)
        Misc.Pause(1000)
        Items.UseItem(0x42369679)
        Misc.Pause(1000)
        PreshExcept = Items.ContainerCount(0x42369679,0x14EF,0x044e)
        Misc.Pause(1000)
        Misc.SendMessage("Precious Exceptionals "+str(PreshExcept))
        if PreshExcept > 9:
            Misc.ScriptRun("BOD_runPreshExcept.py")
        Misc.Pause(1000)
        while Misc.ScriptStatus("BOD_runPreshExcept.py"):
            Misc.Pause(10000)   
        Misc.Pause(1000)
        Items.UseItem(0x4194BF9C)
        Misc.Pause(1000)
        Tailor = Items.ContainerCount(0x4194BF9C,0x14EF,0x0483)
        Misc.Pause(1000)
        Misc.SendMessage("Tailor BODs "+str(Tailor))
        if Tailor > 9:
            Misc.ScriptRun("BOD_runTailor.py")
        Misc.Pause(1000)
        while Misc.ScriptStatus("BOD_runTailor.py"):
            Misc.Pause(10000) 
        Misc.Pause(1000)
        Player.ChatSay(64,"I will acquire additional BODs in 5 hours.")
        repairCheck()
#        Misc.ScriptRun("train_Empower.py")
        time.sleep(5*60*60)
#        Items.UseItem(0x42E87E92)
#        Misc.Pause(500)
#        Items.UseItem(0x41132AE2)
#        Misc.Pause(500)
#        logs = Items.ContainerCount(0x41132AE2,0x1BDD,0x0000)
#        if logs > 30000:
#            packingots = Items.BackpackCount(0x1BF2,0x0000)
#            ingotstorage = Items.FindByID(0x1BF2,0x0000,0x42E87E92)
#            if packingots < 50:
#                Items.Move(ingotstorage,Player.Backpack.Serial,200-packingots)
#                Misc.Pause(1000)
#            packlogs = Items.BackpackCount(0x1BDD,0x0000)
#            logstorage = Items.FindByID(0x1BDD,0x0000,0x41132AE2)
#            if packlogs < 1000:
#                Items.Move(logstorage,Player.Backpack.Serial,1000-packlogs)
#                Misc.Pause(1000)
#            Player.ChatSay("[recall Trainer")
#            Misc.Pause(3000)
#            Misc.ScriptRun("trainArtisan.py")
#            time.sleep(5*60*60)
#        else:
#            time.sleep(5*60*60) 

    elif Player.Name == 'ToolmanTailor':
        Misc.Pause(2000)
        for x in range(5):
            Misc.ScriptRun("FarmGod.py")
            time.sleep(60*60) 
    elif Player.Name == 'ImaTool':
        Misc.Pause(5000)
        for x in range(0,5):
            Misc.ScriptRun("treasure_God.py")
            time.sleep(60*60)
    elif Player.Name == 'Tool Time':
        Misc.ScriptRun("trashPanda.py")
        time.sleep((5 * 3600) + (5 * 60))#5 hours and 5 minutes
    else:
        Player.ChatSay(64,"I will acquire additional BODs in 5 hours.")
        time.sleep(5*60*60)


        


