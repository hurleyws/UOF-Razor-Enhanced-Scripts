from System.Collections.Generic import List
import clr
clr.AddReference("System.Core")
import time
import os
import datetime
import random
import re

debug_mode = True


valid_towns = [
    "Britain", "Crafter's Guild", "Buccaneers Den", "Cove", "Jhelom", "Magencia", "Moonglow", "Nujel'm",
    "Ocllo", "Serpents Hold", "Skara Brae", "Trinsic", "Vesper", "Wind", "Yew", "Minoc", "Destard", "wrong", "Hythloth", "Deceit", "Despise", "Covetous", "Shame"
]




npc_location_options = {
    "Britain": ["BritainOne", "BritainTwo"],
    "Yew": ["YewOne"],
    "Jhelom": ["JhelomOne", "JhelomThree"],
    "Moonglow": ["MoonglowTwo"],
    "Skara Brae": ["Skara BraeOne"],
    "Trinsic": ["TrinsicOne"]
}


def wait_for_lead_on(target, max_attempts=5):
    log_bug("wait_for_lead_on")
    for attempt in range(max_attempts):
        Misc.WaitForContext(target.Serial, 10000)
        Misc.ContextReply(target.Serial, 2)
        Misc.Pause(2000)  # Give time for the NPC to respond

        response = journal_check_for_response(target.Name)
        if response == "lead_on":
            return True
        elif response == "must_rest":
            goHome()
            Misc.ScriptStop("npc_Escorts.py")

        move_near(target)
        Misc.Pause(1000)

    return False

def SafePathFindTo(x, y, z):
    log_bug("SafePathFindTo")
    try:
        Player.PathFindTo(x, y, z)
    except Exception:
        Misc.Pause(5000)
        try:
            Player.PathFindTo(x, y, z)
        except Exception:
            pass

            
def journal_check_for_response(mobile_name):
    log_bug("journal_check_for_response")
    lines = Journal.GetTextByName(mobile_name, False)
    for line in lines:
        lower = line.lower()
        if "lead on!" in lower:
            return "lead_on"
        elif "you must rest" in lower:
            return "must_rest"
    return None


def stockRegs():
    log_bug("stockRegs")
    root = Items.BackpackCount(0x0F86,-1)
    moss = Items.BackpackCount(0x0F7B,-1)
    pearl = Items.BackpackCount(0x0F7A,-1)
    picks = Items.BackpackCount(0x14FC,-1)
    shade = Items.FindByID(0x0F88,-1,Player.Backpack.Serial)
    garlic = Items.FindByID(0x0F84,-1,Player.Backpack.Serial)
    ginseng = Items.FindByID(0x0F85,-1,Player.Backpack.Serial)
    ash = Items.BackpackCount(0x0F8C,-1)
    silk = Items.FindByID(0x0F8D,-1,Player.Backpack.Serial)
    gold = Items.FindByID(0x0EED,-1,Player.Backpack.Serial)
    scrolls = Items.FindByID(0x0EF3,-1,Player.Backpack.Serial)
    logs = Items.FindByID(0x1BDD,-1,Player.Backpack.Serial)
  
    Items.UseItem(0x42E88440)
    Misc.Pause(500)
    Items.UseItem(0x42E87E92)
    Misc.Pause(500)
    
    
    if picks < 30:
        Items.Move(Items.FindByID(0x14FC,-1,0x42E88440),Player.Backpack.Serial,30-picks)
        Misc.Pause(1000)  

    if root < 30:
        Items.Move(Items.FindByID(0x0F86,-1,0x42E88440),Player.Backpack.Serial,30-root)
        Misc.Pause(1000)
    elif root > 30:
        Items.Move(Items.FindByID(0x0F86,-1,Player.Backpack.Serial),0x42E88440,root-30)
        Misc.Pause(1000)
    else:
        Misc.Pause(200)
    
    if moss < 30:
        Items.Move(Items.FindByID(0x0F7B,-1,0x42E88440),Player.Backpack.Serial,30-moss)
        Misc.Pause(1000)
    elif moss > 30:
        Items.Move(Items.FindByID(0x0F7B,-1,Player.Backpack.Serial),0x42E88440,moss-30)
        Misc.Pause(1000)
    else:
        Misc.Pause(200)
        
    if pearl < 30:
        Items.Move(Items.FindByID(0x0F7A,-1,0x42E88440),Player.Backpack.Serial,30-pearl)
        Misc.Pause(1000)
    elif pearl > 30:
        Items.Move(Items.FindByID(0x0F7A,-1,Player.Backpack.Serial),0x42E88440,pearl-30)
        Misc.Pause(1000)
    else:
        Misc.Pause(200)
        
    if ash < 30:
        Items.Move(Items.FindByID(0x0F8C,-1,0x42E88440),Player.Backpack.Serial,30-ash)
        Misc.Pause(1000)
    elif ash > 30:
        Items.Move(Items.FindByID(0x0F8C,-1,Player.Backpack.Serial),0x42E88440,ash-30)
        Misc.Pause(1000)
    else:
        Misc.Pause(200)
        
    if silk:
        Items.Move(silk,0x42E88440,-1)
        Misc.Pause(1000)

    if ginseng:
        Items.Move(ginseng,0x42E88440,-1)
        Misc.Pause(1000)
    if garlic:
        Items.Move(garlic,0x42E88440,-1)
        Misc.Pause(1000)
    if shade:
        Items.Move(shade,0x42E88440,-1)
        Misc.Pause(1000)
    if gold:
        Items.Move(gold,0x42E87E92,-1)
        Misc.Pause(1000)
    if scrolls:
        Items.Move(scrolls,0x42E87E92,-1)
        Misc.Pause(1000)
    if logs:
        for l in Player.Backpack.Contains:
            if l.ItemID == 0x1BDD:
                Items.Move(l,0x41132AE2,-1)
                Misc.Pause(1000)


    

def log_bug(location_note=""):
    if not debug_mode:
        return  # Skip logging if debug mode is off
        
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    position = Player.Position  # Assumes Razor Enhanced environment
    log_dir = r"C:\Users\Hurley\Documents\GitHub\UOF-Razor-Enhanced-Scripts\Debug_logs"
    log_file = "bug_log.txt"
    log_path = os.path.join(log_dir, log_file)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    try:
        with open(log_path, "a") as log:
            log.write(f"[{timestamp}] Position: {position} | Note: {location_note}\n")
    except:
        Misc.Pause(500)  # Still pausing silently in case of error


def attempt_recall(location):
    try:
        log_bug(f"attempt_recall to {location}")
        Misc.Pause(500)
        Journal.Clear()
        while True:
            worldSave()
            Misc.Pause(500)
            log_bug("Recall cast begin")
            Misc.Pause(500)
            Player.ChatSay(f"[recall {location}")
            Journal.Clear()
            Misc.Pause(100)
            log_bug("Recall command sent")
            try:
                Misc.Pause(5000)
                log_bug("Recall pause complete")
            except Exception as e:
                log_bug(f"CRASH DURING PAUSE: {str(e)}")
            # ... rest of your journal checks

            # Check if the spell was disturbed
            if Journal.SearchByType("Your concentration is disturbed, thus ruining thy spell.", "System"):
                Journal.Clear()
                Misc.Pause(500)
                continue  # Skip the rest of the loop and start over
                
            elif Journal.SearchByType("Insufficient mana for this spell.","System"):
                while Player.Mana < 11:
                    Misc.Pause(1000)
                Misc.Pause(1000)
                Journal.Clear()
                continue
                
            elif Journal.SearchByType("This book needs time to recharge.","System"):
                Misc.Pause(1500)
                Journal.Clear()
                Misc.Pause(500)
                continue            
            else:
                break  # Exit the loop if no disturbance is detected
    except Exception as e:
        log_bug(f"CRASH CAUGHT: {str(e)}")
        raise  # optionally re-raise to halt script

def attempt_gate(location):
    log_bug("attempt_gate")
    while True:
        worldSave()
        Player.ChatSay(f"[gate {location}")
        Misc.Pause(3000)  # Wait for the spell to cast

        # Check if the spell was disturbed
        if Journal.SearchByType("Your concentration is disturbed, thus ruining thy spell.", "System"):
            Journal.Clear()
            Misc.Pause(500)
            continue  # Skip the rest of the loop and start over
            
        elif Journal.SearchByType("Insufficient mana for this spell.","System"):
            while Player.Mana < 40:
                Misc.Pause(1000)
            Misc.Pause(1000)
            Journal.Clear()
            continue
            
        elif Journal.SearchByType("This book needs time to recharge.","System"):
            Misc.Pause(1500)
            Journal.Clear()
            Misc.Pause(500)
            continue            
        else:
            break  # Exit the loop if no disturbance is detected
            
def worldSave():
    log_bug("worldSave")
    if (Journal.SearchByType('The world will save in 1 minute.', 'System') or Journal.SearchByType('pause', 'Regular')):
        Misc.Pause(700)
        log_bug("Pausing for world save or player-called break.")
        Misc.Pause(500)
        while (not Journal.SearchByType('World save complete.', 'System') and not Journal.SearchByType('play', 'Regular')):
            Misc.Pause(1000)
        Misc.Pause(2500)
        log_bug("Continuing run")
        Misc.Pause(700)
    Journal.Clear()  
    
def move_near(target):
    log_bug("move_near")
    if 4431 <= target.Position.X <= 4457 and 1102 <= target.Position.Y <= 1145:
        return False  # Skip escorts in hedge maze

    max_total_duration = 30  # seconds
    start_time = time.time()

    if Player.DistanceTo(target) > 3:
        Misc.Pause(500)

        offsets = [(dx, dy) for dx in range(-1, 2) for dy in range(-1, 2) if not (dx == 0 and dy == 0)]
        random.shuffle(offsets)

        for dx, dy in offsets:
            if time.time() - start_time > max_total_duration:
                Misc.Pause(500)
                return False

            tx = target.Position.X + dx
            ty = target.Position.Y + dy
            tz = target.Position.Z

            Misc.Pause(500)

            path = PathFinding.GetPath(tx, ty, True)
            log_bug("path calculated")

            if path is None or path.Count == 0:
                Misc.Pause(500)
                log_bug("No path found")
                continue

            Misc.Pause(500)

            try:
                SafePathFindTo(tx, ty, tz)
                Misc.Pause(500)
                log_bug("Path find attempted")

                move_start = time.time()
                while Player.DistanceTo(target) > 3 and (time.time() - move_start) < 3:
                    if time.time() - start_time > max_total_duration:
                        return False
                    Misc.Pause(500)

                if Player.DistanceTo(target) <= 3:
                    return True
                else:
                    return False  # <- previously missing

            except Exception as e:
                Misc.Pause(500)  # or add logging if needed

        return False
    else:
        return True








def escortService():

    log_bug("escortService")
    
    while True:
        # Filter for valid human NPCs nearby
        mobiles_filter = Mobiles.Filter()
        mobiles_filter.Enabled = True
        mobiles_filter.IsHuman = True
        mobiles_filter.RangeMax = 15
        mobiles_filter.CheckLineOfSight = True
        mobiles_filter.CheckIgnoreObject = True
        
        

        targets = list(Mobiles.ApplyFilter(mobiles_filter))
        
        if not targets:
            Misc.Pause(1000)
            return False  # Nothing to do

        # Filter out vendors with "Buy"
        valid_targets = []
        for target in targets:
            try:
                if Mobiles.ContextExist(target.Serial, "Buy") < 0:
                    valid_targets.append(target)
                else:
#                    Misc.IgnoreObject(target.Serial)
                    continue

            except:
                continue  # Skip if error

        if not valid_targets:
            Misc.Pause(1000)
            return False  # Nothing to do


        # Attempt to escort each one
        for target in valid_targets:
            if not target or target.Serial == Player.Serial:
                continue

            if not move_near(target):
                continue

            Journal.Clear()
            Misc.WaitForContext(target.Serial, 10000)
            Misc.ContextReply(target.Serial, 1)
            Misc.Pause(3000)

            lines = Journal.GetTextByName(target.Name, False)
            match_found = False
            matched_town = None

            for line in lines:
                lower_line = line.lower()
                for town in sorted(valid_towns, key=len, reverse=True):
                    pattern = rf'\b{re.escape(town.lower())}\s*,'
                    if re.search(pattern, lower_line):
                        matched_town = town
                        match_found = True
                        break

                if match_found:
                    break

            if match_found:
                if wait_for_lead_on(target):
                    attempt_gate(matched_town)
                    Misc.Pause(1000)
                    gate = Items.FindByID(0x0F6C, 0x0000, -1, 3, False)
                    Misc.Pause(500)
                    Items.UseItem(gate)
                    Misc.Pause(4000)
                    Journal.Clear()
                    attempt_recall("Moonglow Bank")
#                    Player.ChatSay("Bank")
#                    Misc.Pause(500)
#                    gold = Items.FindByID(0x0EED,-1,Player.Backpack.Serial)
#                    if gold:
#                        Items.Move(gold, Player.Bank, -1)
#                        Misc.Pause(1000)
#                        Player.ChatSay("Deposit")
#                        Misc.Pause(500)
                    Misc.Pause(300000)
                    worldSave()
                    return True  # ESCORT SUCCESSFUL
                else:
                    log_bug("No 'Lead on!' response after attempts")
            else:
                return False
#                Misc.IgnoreObject(target.Serial)
                log_bug("No town match found")

        # No valid escort was completed
        return False



def waitForRightOfWay(max_attempts=10):
    log_bug("waitForRightOfWay")
    priority_order = ["Realtree", "Alyer Base", "Tool Time", "ToolmanTailor", "ImaTool"]
    me = Player.Name
    my_priority = priority_order.index(me)

    excluded_coords = [(6804, 3897), (6800, 3898), (6800, 3892), (6805, 3892), (6803, 3892)]

    attempt = 0
    while attempt < max_attempts:
        blocking = False
        
        mobilesFilter = Mobiles.Filter()
        mobilesFilter.IsHuman = True
        allNearby = Mobiles.ApplyFilter(mobilesFilter)
        
        for mob in allNearby:
            if not mob or not mob.Name or mob.Serial == Player.Serial:
                continue

            if (mob.Position.X, mob.Position.Y) in excluded_coords:
                continue

            if mob.Name in priority_order:
                their_priority = priority_order.index(mob.Name)
                if their_priority < my_priority:
                    blocking = True
                    break

        if not blocking:
            return True

        wait_time = random.randint(10000, 20000)  # milliseconds
        Misc.Pause(wait_time)  # pause the full time before retrying

        attempt += 1

    return False

def checkPlayerAtPosition(target_x, target_y, target_z):
    log_bug("checkPlayerAtPosition")
    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        current_pos = Player.Position
        if (current_pos.X == target_x and 
            current_pos.Y == target_y and 
            current_pos.Z == target_z):
            return  # Already at target


        SafePathFindTo(target_x, target_y, target_z)
        Misc.Pause(3000)  # Wait for movement (you can adjust based on expected travel time)

        current_pos = Player.Position
        if (current_pos.X == target_x and 
            current_pos.Y == target_y and 
            current_pos.Z == target_z):

            return  # Success

        attempts += 1

    
def buyRegs():
    log_bug("buyRegs")
    attempt_recall("Buy Regs")
    BuyAgent.Enable()        
    Misc.WaitForContext(0x0026D40E, 10000)
    Misc.ContextReply(0x0026D40E, 1)
    Misc.Pause(500)
   
def goHome():
    log_bug("goHome")
    attempt_recall("Winter Lodge")
    waitForRightOfWay()
    SafePathFindTo(6802, 3901, 12)
    Misc.Pause(2000)
    checkPlayerAtPosition(6802, 3901, 12)
    door = Items.FindBySerial(0x42F89EDC)
    if door and door.ItemID == 0x0677:
        Items.UseItem(door)
        Misc.Pause(500)
    waitForRightOfWay()
    SafePathFindTo(6803, 3899, 17)
    Misc.Pause(2000)  
    checkPlayerAtPosition(6803, 3899, 17)   
    Items.UseItem(0x42E88440) #Open box by door
    Misc.Pause(1500)
    stockRegs()
    SafePathFindTo(6800, 3898, 17)
    Misc.Pause(2000)
    Player.Run("West")

def check_Traps():
    log_bug("check_Traps")

    # Map integers to word-based names
    trap_locations = [
        "TrapOne", "TrapTwo", "TrapThree", "TrapFour",
        "TrapFive", "TrapSix", "TrapSeven", "TrapEight"
    ]

    location = random.choice(trap_locations)
    log_bug(f"Selected trap location: {location}")

    attempt_recall(location)
    Misc.Pause(2000)
    escortService()

                
                
for location_key, location_choices in npc_location_options.items():
    log_bug(f"Begin location iteration: {location_key}")
    location = random.choice(location_choices)
    attempt_recall(location)
    
    if escortService():
        Misc.Pause(500)
        worldSave()
        Misc.Pause(500)
        continue  # Skip further pathfinding steps in this location

    if location == "BritainOne":
        britain_steps = [
            (1503, 1686, 6000),
            (1512, 1668, 6000),
            (1512, 1651, 5000),
            (1490, 1651, 6000),
            (1467, 1651, 6000),
            (1467, 1660, 4000),
            (1484, 1660, 4000)
        ]
        for x, y, pause in britain_steps:
            SafePathFindTo(x, y, 20)
            Misc.Pause(pause)
            worldSave()
            if escortService():
                break  # Stop doing more steps, but continue the outer loop

    elif location == "MoonglowTwo":
        moonglow_steps = [
            (4499, 1093, 4000),
            (4497, 1093, 2000),
            (4473, 1108, 4000),
            (4458, 1099, 6000),
            (4449, 1099, 3000),
            (4438, 1099, 3000),
            (4426, 1099, 4000),
            (4429, 1118, 4000),
            (4426, 1099, 4000),
            (4426, 1082, 6000),
            (4437, 1073, 4000),
            (4455, 1073, 4000),
            (4471, 1074, 4000),
            (4485, 1074, 4000),
        ]
        for x, y, pause in moonglow_steps:
            SafePathFindTo(x, y, 0)
            Misc.Pause(pause)
            worldSave()
            if escortService():
                break
                
    elif location == "YewOne":
        yew_steps = [
            (524, 941, 6000),
            (497, 966, 6000),
            (503, 1004, 6000),
            (523, 1034, 6000),
            (551, 1046, 6000),
            (579, 1024, 5000),
            (601, 1004, 5000),
            (594, 979, 5000),
            (569, 936, 5000),
            (546, 932, 5000)
            
        ]
        for x, y, pause in yew_steps:
            SafePathFindTo(x, y, 0)
            Misc.Pause(pause)
            worldSave()
            if escortService():
                break
    elif location == "JhelomOne":
        jhelom1_steps = [
            (1420, 3719, 3000),
            (1420, 3735, 3000),
            (1420, 3756, 3000)

        ]
        for x, y, pause in jhelom1_steps:
            SafePathFindTo(x, y, -21)
            Misc.Pause(pause)
            worldSave()
            if escortService():
                break
                
    elif location == "JhelomThree":
        jhelom3_steps = [
            (1428, 3723, 5000),
            (1409, 3723, 4000),
            (1386, 3723, 4000)

        ]
        for x, y, pause in jhelom3_steps:
            SafePathFindTo(x, y, 0)
            Misc.Pause(pause)
            worldSave()
            if escortService():
                break

    elif location == "TrinsicOne":
        trin1_steps = [
            (1955, 2793, 4000),
            (1955, 2779, 3000),
            (1977, 2779, 4000),
            (1977, 2795, 4000),

        ]
        for x, y, pause in trin1_steps:
            SafePathFindTo(x, y, 0)
            Misc.Pause(pause)
            worldSave()
            if escortService():
                break
                
    elif location == "BritainTwo":
        brit2_steps = [
            (1431, 1572, 4000),
            (1431, 1566, 3000),

        ]
        for x, y, pause in brit2_steps:
            SafePathFindTo(x, y, 30)
            Misc.Pause(pause)
            worldSave()
            if escortService():
                break
                
                
                
check_Traps()                
buyRegs()                
goHome()
Misc.Pause(2000)
log_bug("Script end.")


        
   
        
        


