from System.Collections.Generic import List
from System import Byte
from System import Int32 as int

def attempt_recall(location):
    while True:
        Player.ChatSay(f"[recall {location}")
        Misc.Pause(2500)  # Wait for the spell to cast

        # Check if the spell was disturbed
        if Journal.SearchByType("Your concentration is disturbed, thus ruining thy spell.", "System"):
            Misc.SendMessage("Spell was disturbed. Recasting...")
            Journal.Clear()
            Misc.Pause(500)
            killGame()
            Misc.Pause(500)
            continue  # Skip the rest of the loop and start over
            
        elif Journal.SearchByType("Insufficient mana for this spell.","System"):
            while Player.Mana < 11:
                Misc.Pause(1000)
            Misc.Pause(1000)
            killGame()
            Journal.Clear()
            continue
            
        elif Journal.SearchByType("Insufficient mana for this spell.","System"):
            while Player.Mana < 11:
                Misc.Pause(1000)
            Misc.Pause(1000)
            killGame()
            Journal.Clear()
            continue
            
        elif Journal.SearchByType("This book needs time to recharge.","System"):
            Misc.Pause(500)
            killGame()
            Misc.Pause(1500)
            Journal.Clear()
            Misc.Pause(500)
            continue            
            
        else:
            break  # Exit the loop if no disturbance is detected


mobileFilter = Mobiles.Filter()
mobileFilter.Enabled = True
mobileFilter.IsHuman = True
mobileFilter.Notorieties = List[Byte](bytes([3,4,5,6]))

while True:
    Misc.Pause(100);
    foundMobiles = Mobiles.ApplyFilter(mobileFilter)

    if foundMobiles:
        attempt_recall("Winter Lodge")
        Misc.ScriptStop("auto__lumberjack.py")
        Player.HeadMessage(44,"Murderer detected!")
        

       