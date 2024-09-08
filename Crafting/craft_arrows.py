#DEFAULT WILL BE TO MAKE OAK ARROWS

woodchest = 0x42E87E92
woodpouch = 0x41132AE2
wood_ID = 0x1BDD
feather_ID = 0x1BD1

#hues
oak = 0x07da
ash = 0x04a7
yew = 0x04a8
heartwood = 0x04a9
blood = 0x04aa
frost = 0x047f

Player.ChatSay(64, "How lethal should I make these arrows?")

# Wait a moment for the player to respond
Misc.Pause(5000)  # Adjust the time as needed

# Check the players response in the journal
if Journal.SearchByName("oak", "Realtree"):
    # Run the script for boats nearby
    woodtype = oak
    Journal.Clear()
elif Journal.SearchByName("ash", "Realtree"):
    # Run the script for boats nearby
    woodtype = ash
    Journal.Clear()
elif Journal.SearchByName("yew", "Realtree"):
    # Run the script for boats nearby
    woodtype = yew
    Journal.Clear()
elif Journal.SearchByName("heartwood", "Realtree"):
    # Run the script for boats nearby
    woodtype = heartwood
    Journal.Clear()
elif Journal.SearchByName("blood", "Realtree"):
    # Run the script for boats nearby
    woodtype = blood
    Journal.Clear()
elif Journal.SearchByName("frost", "Realtree"):
    # Run the script for boats nearby
    woodtype = frost
    Journal.Clear()
else:
    # Handle cases where no valid response was detected
    Player.ChatSay(64, "I cant make up my mind.")
    

Player.HeadMessage(64, "How many thousands of arrows?")
Journal.Clear()

# Wait a moment for the player to respond
Misc.Pause(5000)  # Adjust the time as needed

# Check the players response in the journal
Journal.WaitByName('Realtree',10000)
amount = Journal.GetTextByName('Realtree')
iterations = int(str(amount[0]))  

def craftArrows():
    for i in range(iterations):
        wood = Items.FindByID(wood_ID,woodtype,woodpouch)
        feathers = Items.FindByID(feather_ID,-1,woodchest)
        Items.Move(wood,Player.Backpack.Serial,1000)
        Misc.Pause(1000)
        Items.Move(feathers,Player.Backpack.Serial,1000)
        Misc.Pause(1000)
        Items.UseItemByID(0x1022,-1)
        Misc.Pause(500)
        #wood type menu
        Gumps.WaitForGump(949095101, 10000)
        Gumps.SendAction(949095101, 7)
        if woodtype == oak:
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, 13)
        elif woodtype == ash:
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, 20)
        elif woodtype == yew:
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, 27)
        elif woodtype == heartwood:
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, 34)
        elif woodtype == blood:
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, 41)
        elif woodtype == frost:
            Gumps.WaitForGump(949095101, 10000)
            Gumps.SendAction(949095101, 48)
        Misc.Pause(500)
        #make shafts
        Gumps.WaitForGump(949095101, 10000)
        Gumps.SendAction(949095101, 1)
        Gumps.WaitForGump(949095101, 10000)
        Gumps.SendAction(949095101, 9)
        Misc.Pause(3000)
        #make arrows
        Items.UseItemByID(0x1022,-1)
        Misc.Pause(500)
        Gumps.SendAction(949095101, 8)
        Gumps.WaitForGump(949095101, 10000)
        Gumps.SendAction(949095101, 2)
        Misc.Pause(3000)
        #store arrows
        arrows = Items.FindByID(0x0F3F,-1,Player.Backpack.Serial)
        if arrows:
            Items.Move(arrows,0x42E88440,-1)
            Misc.Pause(1000)
        
tools = Items.FindByID(0x1022,-1,Player.Backpack.Serial)


if tools:
    craftArrows()
else:
    Items.UseItemByID(0x1EB8,-1)
    Misc.Pause(500)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, 8)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, 149)
    Misc.Pause(2000)
    craftArrows()

