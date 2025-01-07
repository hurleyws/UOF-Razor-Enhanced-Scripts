import clr
import random

# List of 12 forest-type locations
forest_locations = [
    "Whispering Woods", "Emerald Forest", "Shadow Glen",
    "Misty Grove", "Elderwood", "Bramblewood",
    "Verdant Hollow", "Silverleaf Grove", "Willow Copse",
    "Oakshade Glade", "Twilight Thicket", "Moonlit Glade"
]

# List to track unused locations
unused_locations = []

# Function to recall to a random location
def recall_to_random_forest():
    global unused_locations

    # Reset unused_locations if all locations have been used
    if not unused_locations:
        unused_locations = forest_locations.copy()
        random.shuffle(unused_locations)  # Shuffle for randomness

    # Select the next location
    next_location = unused_locations.pop()

    # Send recall command
    Player.ChatSay(f"[recall ({next_location})")
    Misc.Pause(2000)  # Pause for 2 seconds

    # Log the recall for debugging
    Misc.SendMessage(f"Recalled to: {next_location}")

# Example usage: Call the function
recall_to_random_forest()
