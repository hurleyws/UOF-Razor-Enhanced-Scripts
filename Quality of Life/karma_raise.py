#########################
# You need a target named NPC
# if the NPC is not located the script will tell you to move closer
# If you have no gold it will tell you to get more gold
# put the amount of gold in your pack and the script will give it one coin
# at a time to NPC to raise karma
#######################################
# By Kamster
######################################

npc = 0x00176F43
#npc = Target.GetTargetFromList('npc')
gold = Items.FindByID(0x0EED,-1, Player.Backpack.Serial)

if gold: 
    if npc:
        Items.Move(Items.FindByID(0x0EED,-1, Player.Backpack.Serial), npc, 1)
        Misc.Pause(600)
    else:
       Player.HeadMessage(33,'Move Closer')
       Misc.Pause(400)
else:
    Player.HeadMessage(33,'Get More Gold')