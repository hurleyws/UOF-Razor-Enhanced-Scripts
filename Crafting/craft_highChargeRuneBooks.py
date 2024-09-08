
#Set the minimum charges before throwing the book away
keepValue = 30
storeChest = 0x42E8832C

Player.HeadMessage(64,"Let's make some runebooks.")
Misc.Pause(1000)
Player.HeadMessage(64,"First, lets make sure we don't throw any of mine away.")
Misc.Pause(1000)
for i in Player.Backpack.Contains:
    if i.ItemID == 0x22C5:
        Misc.IgnoreObject(i)
        Misc.Pause(500)

book = Items.FindByID(0x22C5,-1,Player.Backpack.Serial,-1,True)

props = Items.GetPropStringByIndex(book,6)
# Split the string to get the part after the "/"
parts = props.split("/")
# Get the value of x, which is the second part after splitting
charges = int(parts[1])
# Print or use the extracted value of x
if charges > keepValue:
    Player.HeadMessage(64,"Ah ha! A keeper! "+charges+" charges on this one!")
    Mobiles.UseMobile(self)
    