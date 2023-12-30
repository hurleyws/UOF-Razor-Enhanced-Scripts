book1_16 = 0x402B008A
book17_32 = 0x402B06DE
book33_48 = 0x402B0AC6
book49_64 = 0x402B0D08
book65_80 = 0x402B0E9B
book81_96 = 0x402B10CD
book97_112 = 0x402B123F
book113_128 = 0x402B1419
book129_144 = 0x402B18F0
book145_160 = 0x402B1BB0
book161_176 = 0x402B5185
book177_192 = 0x402B4D18
book193_200 = 0x402B4905

Journal.Clear()
Player.HeadMessage(75,'Which T-Map location are we headed to?')
Journal.WaitByName('Alyer Base',10000)
tmap_location = Journal.GetTextByName('Alyer Base')
location = int(tmap_location[0])
Misc.Pause(1000)
Player.ChatSay(75,'See you at T-Map: ' + tmap_location[0])
Misc.Pause(1000)

if location <= 16:
    rune = location - 1
    Items.UseItem(book1_16)
    Gumps.WaitForGump(1431013363, 10000)
    Gumps.SendAction(1431013363, 5 + (6 * rune))
elif location <= 32:
    rune = location - 17
    Items.UseItem(book17_32)
    Gumps.WaitForGump(1431013363, 10000)
    Gumps.SendAction(1431013363, 5 + (6 * rune))
elif location <= 48:
    rune = location - 33
    Items.UseItem(book33_48)
    Gumps.WaitForGump(1431013363, 10000)
    Gumps.SendAction(1431013363, 5 + (6 * rune))
elif location <= 64:
    rune = location - 49
    Items.UseItem(book49_64)
    Gumps.WaitForGump(1431013363, 10000)
    Gumps.SendAction(1431013363, 5 + (6 * rune))
elif location <= 80:
    rune = location - 65
    Items.UseItem(book65_80)
    Gumps.WaitForGump(1431013363, 10000)
    Gumps.SendAction(1431013363, 5 + (6 * rune))
elif location <= 96:
    rune = location - 81
    Items.UseItem(book81_96)
    Gumps.WaitForGump(1431013363, 10000)
    Gumps.SendAction(1431013363, 5 + (6 * rune))
elif location <= 112:
    rune = location - 97
    Items.UseItem(book97_112)
    Gumps.WaitForGump(1431013363, 10000)
    Gumps.SendAction(1431013363, 5 + (6 * rune))
elif location <= 128:
    rune = location - 113
    Items.UseItem(book113_128)
    Gumps.WaitForGump(1431013363, 10000)
    Gumps.SendAction(1431013363, 5 + (6 * rune))
elif location <= 144:
    rune = location - 129
    Items.UseItem(book129_144)
    Gumps.WaitForGump(1431013363, 10000)
    Gumps.SendAction(1431013363, 5 + (6 * rune))
elif location <= 160:
    rune = location - 145
    Items.UseItem(book145_160)
    Gumps.WaitForGump(1431013363, 10000)
    Gumps.SendAction(1431013363, 5 + (6 * rune))
elif location <= 176:
    rune = location - 161
    Items.UseItem(book161_176)
    Gumps.WaitForGump(1431013363, 10000)
    Gumps.SendAction(1431013363, 5 + (6 * rune))
elif location <= 192:
    rune = location - 177
    Items.UseItem(book177_192)
    Gumps.WaitForGump(1431013363, 10000)
    Gumps.SendAction(1431013363, 5 + (6 * rune))
else:
    rune = location - 193
    Items.UseItem(book193_200)
    Gumps.WaitForGump(1431013363, 10000)
    Gumps.SendAction(1431013363, 5 + (6 * rune))
