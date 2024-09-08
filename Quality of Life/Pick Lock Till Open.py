#lockpics chest till open
lockpick = 0x14FC

def pickbox(box):

    Journal.Clear()
    while not ( Journal.SearchByName( 'The lock quickly yields to your skill.', '' ) or Journal.SearchByType( 'This does not appear to be locked.', 'System' ) ):
        if Items.FindByID(lockpick, -1, Player.Backpack.Serial):
            targetitem = Items.FindByID(lockpick, -1, Player.Backpack.Serial)
        else:
            Player.HeadMessage(54, "Forget LPs")    
        Items.UseItem(targetitem)
        Target.WaitForTarget(10000, False)
        Target.TargetExecute(box)
        Misc.Pause( 4000 )
        if Journal.SearchByName( 'lock can be manipulated', '' ):
            Player.HeadMessage(54, 'you dumb')
            return
        if lockpick == None:
            Player.HeadMessage( colors[ 'red' ], 'Ran out of lockpicks!' )
            Player.HeadMessage(54, 'Out of lockpicks')
            return

            
chest1 = Target.PromptTarget( 'Target the treasure chest' )
chest = Items.FindBySerial(chest1)  
pickbox(chest)

Player.ChatSay(26,'Unlocked, now I will untrap.')
