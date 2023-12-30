if Player.Name == "Alyer Base" or Player.Name == "Snuke in Sniz":
    Player.ChatSay(64,"All follow me")
    Player.ChatSay(75,"[recall HVL")
    Misc.Pause(2000)
    gold_found = Items.FindByID(0x0EED,-1,Player.Backpack.Serial)
    if gold_found:
           Items.Move(gold_found,0x00092B55,-1)
           Misc.Pause(800)
           
if Player.Name == "Realtree" or Player.Name == "ToolTime" or Player.Name == "ToolmanTailor":
    Player.ChatSay(75,"[recall HVL")
    Misc.Pause(2000)
    
else:
    Player.ChatSay(75,"[recall HVL")
    Misc.Pause(2000)
    gold_found = Items.FindByID(0x0EED,-1,Player.Backpack.Serial)
    if gold_found:
           Items.Move(gold_found,0x405A1E11,-1)
           Misc.Pause(800)