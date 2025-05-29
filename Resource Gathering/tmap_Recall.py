# Define rune books with their corresponding number ranges
rune_books = {
    (1, 16): 0x402B008A,
    (17, 32): 0x402B06DE,
    (33, 48): 0x402B0AC6,
    (49, 64): 0x402B0D08,
    (65, 80): 0x402B0E9B,
    (81, 96): 0x402B10CD,
    (97, 112): 0x402B123F,
    (113, 128): 0x402B1419,
    (129, 144): 0x402B18F0,
    (145, 160): 0x402B1BB0,
    (161, 176): 0x402B5185,
    (177, 192): 0x402B4D18,
    (193, 200): 0x402B4905
}

# Clear Journal and prompt for T-Map location
Journal.Clear()
recall = Items.FindByID(0x1F4C, -1, Player.Backpack.Serial)
Player.HeadMessage(75, 'Which T-Map location are we headed to?')
Journal.WaitByName(Player.Name, 10000)
tmap_location = Journal.GetTextByName(Player.Name)

# Validate input
if not tmap_location or not tmap_location[0].isdigit():
    Misc.SendMessage("Invalid input. Please enter a number.", 33)
    Misc.ScriptStop("tmap_Recall.py")

location = int(tmap_location[0])  # Convert input to an integer

Misc.Pause(1000)
Player.ChatSay(75, f'See you at T-Map: {location}')
Misc.Pause(1000)

# Find the correct rune book and rune index
for (start, end), book_serial in rune_books.items():
    if start <= location <= end:
        rune = location - start  # Get correct rune index
        Items.UseItem(book_serial)
        Gumps.WaitForGump(1431013363, 10000)
        Gumps.SendAction(1431013363, 2 + (6 * rune))
        break

Misc.Pause(3000)
