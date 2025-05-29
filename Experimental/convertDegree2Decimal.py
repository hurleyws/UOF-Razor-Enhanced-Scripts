LordBritishThrone=[1624, 1323]    
WorldSize = [4096, 5120]
TilesPerDegree= [ WorldSize[0]/360.0, WorldSize[1]/360.0 ] 

def convertDecimalToDegrees(x_decimal, y_decimal):
    """
    Converts decimal coordinates (X, Y) into degrees, minutes, and direction.
    :param x_decimal: The decimal X coordinate (longitude)
    :param y_decimal: The decimal Y coordinate (latitude)
    :return: ((lon_degrees, lon_minutes, lon_direction), (lat_degrees, lat_minutes, lat_direction))
    """

    def calculateDegrees(decimal, center, tiles_per_degree, world_size, east_west):
        """
        Internal function to calculate degrees, minutes, and direction.
        :param decimal: The decimal coordinate (converted to int)
        :param center: The reference point (LordBritishThrone)
        :param tiles_per_degree: Conversion factor
        :param world_size: World wrap-around size
        :param east_west: True if longitude (E/W), False if latitude (N/S)
        :return: (degrees, minutes, direction)
        """
        decimal = float(decimal)  # Convert to float to avoid type errors
        center = float(center)
        tiles_per_degree = float(tiles_per_degree)
        world_size = float(world_size)

        adjusted_decimal = (decimal - center) % world_size  # Ensure subtraction is valid

        # Determine direction
        direction = 'E' if east_west else 'S' if adjusted_decimal >= 0 else 'W' if east_west else 'N'

        # Convert to absolute value
        adjusted_decimal = abs(adjusted_decimal)

        # Calculate degrees and minutes
        degrees = int(adjusted_decimal / tiles_per_degree)
        remaining_tiles = adjusted_decimal % tiles_per_degree
        minutes = int((remaining_tiles / tiles_per_degree) * 60)

        return degrees, minutes, direction

    # Calculate longitude (X-axis)
    lon_degrees, lon_minutes, lon_direction = calculateDegrees(
        x_decimal, LordBritishThrone[1], TilesPerDegree[1], WorldSize[1], True)

    # Calculate latitude (Y-axis)
    lat_degrees, lat_minutes, lat_direction = calculateDegrees(
        y_decimal, LordBritishThrone[0], TilesPerDegree[0], WorldSize[0], False)

    return (lon_degrees, lon_minutes, lon_direction), (lat_degrees, lat_minutes, lat_direction)



    
Misc.SendMessage(convertDecimalToDegrees(2359,3506))