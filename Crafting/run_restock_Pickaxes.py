Player.PathFindTo(2134, 346, 7)
Misc.Pause(8000)
Player.PathFindTo(2117, 359, 7)
Misc.Pause(9500)
if Player.Position.X == 2117 and Player.Position.Y == 359 or Player.Position.Y == 357:
    Player.ChatSay(64,"On location")
else:
    Player.ChatSay(64,"Adjusting")
    Player.PathFindTo(2117, 359, 7)
    Misc.Pause(5000)
    Player.ChatSay(64,"On location")
Player.PathFindTo(2120, 355, 7)
Misc.Pause(3000)
Items.UseItem(0x40CFB51E) #open patio door
Misc.Pause(400)
Player.PathFindTo(2127, 354, 7) #approach forge
Misc.Pause(6000)

Misc.ScriptRun("restock_Pickaxes.py")

while Misc.ScriptStatus("restock_Pickaxes.py"):
    Misc.Pause(5000)

Player.PathFindTo(2134, 348, 7)
Misc.Pause(6500)
Player.PathFindTo(2138, 341, 7)
Misc.Pause(5000)
Player.PathFindTo(2138, 338, 7)
Misc.Pause(3000)
Player.Run("West")
Misc.Pause(500)
Player.HeadMessage(64,"Organizing")
Misc.ScriptRun("master_Organizer.py")
    



