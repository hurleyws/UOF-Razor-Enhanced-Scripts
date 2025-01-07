def checkPositionAndRetry(expectedX, expectedY, maxWait=10000):
    """
    Check if the player is at the expected position. If not, move to the expected position
    using pathfinding, wait 3 seconds, and check the position again.

    :param expectedX: Expected X coordinate of the player.
    :param expectedY: Expected Y coordinate of the player.
    :param maxWait: Maximum wait time in milliseconds to retry position check.
    """
    Misc.SendMessage(f"Checking position: Expected ({expectedX}, {expectedY}), Current ({Player.Position.X}, {Player.Position.Y})", 77)
    Misc.Pause(500)
    if Player.IsGhost:
        return
    
    elapsedTime = 0
    retryInterval = 2000  # Retry every 2 seconds

    while elapsedTime < maxWait:
        # Check if the player is in the correct position
        if Player.Position.X == expectedX and Player.Position.Y == expectedY:
            Misc.SendMessage("Pass: Player is at the correct position.", 77)
            return  # Exit the function when in the correct position

        # If player is not in the correct position, use pathfinding to move there
        Misc.SendMessage("Position check failed. Moving to the expected position.", 33)
        Player.PathFindTo(expectedX, expectedY)  # Move player to the expected position
        Misc.Pause(3000)  # Wait 3 seconds before rechecking position
        
        elapsedTime += retryInterval

    # If the player is still not at the correct position after maxWait, return
    Misc.SendMessage("Fail: Player did not reach the expected position within the allowed time.", 33)
