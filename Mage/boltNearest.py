from System.Collections.Generic import List
from System import Byte

def cast_energy_bolt():
    def get_mana_cost():
        initial_mana = Player.Mana
        Spells.CastMagery('Energy Bolt')
        Target.WaitForTarget(2000, False)
        Target.TargetExecute(target)
        Misc.Pause(500)  # Short delay to ensure the spell has been cast
        final_mana = Player.Mana
        return initial_mana - final_mana

    filterExample = Mobiles.Filter()
    filterExample.Enabled = True
    filterExample.RangeMin = 0
    filterExample.RangeMax = 12  # Define a maximum range if necessary
    filterExample.Notorieties = List[Byte](bytes([3, 4, 6]))  # Filter based on notoriety

    while True:
        Journal.Clear()
        # Check for the "Targeting canceled" message in the journal
        if Journal.SearchByType("Targeting canceled", "System"):
            Misc.SendMessage("Targeting canceled. Stopping cast.")
            Journal.Clear()
            break  # Exit the casting loop if the message is found

        filterExampleList = Mobiles.ApplyFilter(filterExample)  # Get the filtered list of mobiles

        if not filterExampleList:  # Exit if no valid targets are found
            Misc.SendMessage("No more valid targets.")
            break

        # Sort by distance or use another method to choose a target
        for target in filterExampleList:
            if target and target.Hits > 0:  # Ensure the target is alive and valid
                mana_cost = get_mana_cost()  # Cast spell and determine mana cost

                # Determine cooldown based on mana cost
                if mana_cost == 20:
                    Misc.Pause(1000)  # No buff, longer cooldown
                else:
                    Misc.Pause(500)  # Buff active, shorter cooldown

                if target.Hits <= 0:  # If target is dead, ignore it
                    Misc.IgnoreObject(target)
                    Misc.Pause(500)
                    break  # Break the loop if target dies to refresh target list

        Misc.Pause(500)  # Slight delay before checking the next target

cast_energy_bolt()
