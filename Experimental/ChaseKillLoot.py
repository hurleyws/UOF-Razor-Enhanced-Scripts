from System import Int32 as int
from System.Collections.Generic import List
import random
import clr
import time

CORPSE_GRAPHICS = [0x2006]  # Example graphics for corpses
RANGE_MAX = 10
MAX_RETRY = 5
TIMEOUT = 10


def findTargets(graphics, range_max):
    """
    Finds targets (e.g., chests or corpses) based on specified graphics and range.
    """
    targetFilter = Items.Filter()
    targetFilter.Enabled = True
    targetFilter.Movable = False
    targetFilter.OnGround = True
    targetFilter.Graphics = List[int](graphics)
    targetFilter.RangeMax = range_max
    return Items.ApplyFilter(targetFilter)

def moveToTarget(target, max_retry, timeout):
    """
    Moves to a target (e.g., chest or corpse) while checking for danger.
    """
    targetPosition = target.Position
    Misc.SendMessage("Original target position: {}".format(targetPosition))

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Directions to try: Down, Up, Right, Left
    for dx, dy in directions:
        targetCoords = PathFinding.Route()
        targetCoords.MaxRetry = max_retry
        targetCoords.StopIfStuck = False
        targetCoords.X = targetPosition.X + dx
        targetCoords.Y = targetPosition.Y + dy
        PathFinding.Go(targetCoords)
        
        startTime = time.time()
        while Player.DistanceTo(target) > 1:
            currentTime = time.time()
            if currentTime - startTime > timeout:
                Misc.SendMessage("Timed out, trying next position")
                break
            Misc.Pause(500)
        
        # Check if the player has successfully moved close enough
        if Player.DistanceTo(target) <= 1:
            break

    
def followMobile(mobile):
    """
    Follows a mobile until the player is within 1 tile of it.
    """
    while mobile:
        if Player.DistanceTo(mobile) > 1:
            mobilePosition = mobile.Position
            route = PathFinding.Route()
            route.MaxRetry = 5
            route.StopIfStuck = False
            route.X = mobilePosition.X
            route.Y = mobilePosition.Y - 1  # Adjust the target position as needed
            PathFinding.Go(route)
            Misc.Pause(250)
            Misc.SendMessage("Pathfinding")  # Short pause to allow smooth following
            Misc.Pause(250)
        else:
            Misc.SendMessage("Distance check OK")  # Short pause to allow smooth following
            Misc.Pause(2000)
            break
    
#    
#mobile = Mobiles.FindBySerial(0x001ED03A)
#
#while True:
#    followMobile(mobile)
#    
    

corpses = findTargets(CORPSE_GRAPHICS, RANGE_MAX)
for corpse in corpses:
    moveToTarget(corpse, MAX_RETRY, TIMEOUT)



