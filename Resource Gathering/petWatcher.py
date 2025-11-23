primaryPet = 0x00136CD2 #drago 0x00136CD2
secondaryPet = 0x00000A14 #steed 0x00000A14

from System import Byte
import time

# Loop constantly to keep pets near the player
while True:
    pet1 = Mobiles.FindBySerial(primaryPet)
    pet2 = Mobiles.FindBySerial(secondaryPet)
    pets = [pet1, pet2]

    if Player.IsGhost:
        Misc.Pause(1000)
        continue

    # Check distance and issue guard command if needed
    if any(pet and Player.DistanceTo(pet) > 7 for pet in pets if pet):
        Player.ChatSay("All guard me")
        Misc.Pause(500)

    Misc.Pause(1000)  # Check every 2 seconds
