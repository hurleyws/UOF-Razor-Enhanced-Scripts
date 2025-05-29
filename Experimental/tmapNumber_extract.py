import re

tmap = Items.FindByID(0x14EC,-1,Player.Backpack.Serial)
print("DEBUG: tmap =", tmap)

coordString = Items.GetPropStringByIndex(tmap,4)
propString = Items.GetPropStringByIndex(tmap,4)
print("DEBUG: propString =", repr(propString))


print("DEBUG: coordString =", repr(coordString))  # Print the raw string




import re

def extract_coordinates(coordString):
    """Extracts (x, y) coordinates from a string like 'Location: (2359, 2506)'."""
    if not isinstance(coordString, str):
        coordString = str(coordString)  # Ensure it's a string

    print("DEBUG: coordString after conversion =", repr(coordString))  # Debugging

    # Try to extract coordinates
    match = re.search(r'[-]?\d+,\s*[-]?\d+', coordString)  # Matches numbers inside ()
    if match:
        x, y = map(int, match.group().split(","))
        print("DEBUG: Extracted coordinates =", (x, y))  # Debugging
        return x, y
    
    print("DEBUG: No match found")
    return None  # Return None if no valid coordinates found


def create_coordinate_lookup():
    """Creates a dictionary mapping coordinate tuples to their corresponding numbers."""
    data = """
    961,506 1
    1162,189 2
    1314,317 3
    1470,229 4
    1504,366 5
    2672,392 6
    2740,435 7
    2770,345 8
    2781,289 9
    2836,233 10
    3014,250 11
    3082,202 12
    1027,1180 13
    1319,889 14
    1414,771 15
    1529,753 16
    1555,806 17
    1511,967 18
    1562,1058 19
    1510,1071 20
    2340,645 21
    2350,688 22
    2395,723 23
    2433,767 24
    2643,851 25
    2458,1042 26
    2517,1066 27
    2337,1159 28
    2392,1154 29
    3246,245 30
    3404,238 31
    3375,458 32
    3369,637 33
    199,1461 34
    208,1444 35
    358,1337 36
    581,1455 37
    348,1565 38
    620,1706 39
    962,1858 40
    980,1849 41
    969,1893 42
    968,1884 43
    977,1879 44
    1018,1859 45
    1034,1877 46
    1042,1903 47
    1042,1960 48
    1037,1975 49
    1024,1990 50
    974,1992 51
    989,1992 52
    451,2053 53
    477,2044 54
    492,2027 55
    468,2087 56
    465,2100 57
    1658,2030 58
    1689,1993 59
    1709,1964 60
    1726,1998 61
    1731,2016 62
    1743,2028 63
    1754,2020 64
    2033,1942 65
    2054,1962 66
    2066,1979 67
    2058,1992 68
    2071,2007 69
    2062,1962 70
    2097,1975 71
    2089,1987 72
    2093,2006 73
    2187,1991 74
    1427,2405 75
    1433,2381 76
    1471,2340 77
    1450,2301 78
    1437,2294 79
    1439,2217 80
    1466,2181 81
    1464,2245 82
    1478,2273 83
    1562,2312 84
    1546,2221 85
    1519,2214 86
    1534,2189 87
    1523,2150 88
    1541,2115 89
    1595,2193 90
    1619,2236 91
    1654,2268 92
    1724,2288 93
    1772,2321 94
    1758,2333 95
    1765,2430 96
    1703,2318 97
    1655,2304 98
    2062,2144 99
    2104,2123 100
    2098,2101 101
    2130,2108 102
    2153,2120 103
    2186,2144 104
    2178,2151 105
    2162,2148 106
    2129,2132 107
    2123,2120 108
    2648,2167 109
    2629,2221 110
    2642,2289 111
    2682,2290 112
    2727,2309 113
    2782,2293 114
    2804,2255 115
    2850,2252 116
    2957,2150 117
    2968,2170 118
    2951,2177 119
    2956,2200 120
    2932,2240 121
    958,2504  122
    1025,2702 123
    1290,2735 124
    1383,2840 125
    1388,2984 126
    1415,3059 127
    1647,2641 128
    1562,2705 129
    1670,2808 130
    1602,3012 131
    1664,3062 132
    1068,3182 133
    1076,3156 134
    1073,3133 135
    1090,3110 136
    1094,3131 137
    1096,3178 138
    1129,3403 139
    1162,3469 140
    1128,3500 141
    1135,3445 142
    2013,3269 143
    2039,3427 144
    2097,3384 145
    2149,3362 146
    2370,3428 147
    2341,3482 148
    2360,3507 149
    2387,3505 150
    2467,3581 151
    2482,3624 152
    2527,3585 153
    2535,3608 154
    2797,3452 155
    2803,3488 156
    2793,3519 157
    2831,3511 158
    2989,3606 159
    3035,3603 160
    2154,3983 161
    2143,3986 162
    2140,3940 163
    2157,3924 164
    2152,3950 165
    2162,3988 166
    2453,3942 167
    2422,3928 168
    2415,3920 169
    2421,3902 170
    2480,3908 171
    2513,3901 172
    2512,3918 173
    2513,3962 174
    2528,3982 175
    2516,3999 176
    4477,3282 177
    4477,3230 178
    4466,3209 179
    4424,3152 180
    4419,3117 181
    4448,3130 182
    4453,3148 183
    4500,3108 184
    4513,3103 185
    4471,3188 186
    4507,3227 187
    4496,3241 188
    4642,3369 189
    4694,3485 190
    3476,2761 191
    3425,2723 192
    3417,2675 193
    3533,2471 194
    3511,2421 195
    3568,2402 196
    3702,2825 197
    3594,2825 198
    3558,2819 199
    3541,2784 200
    """
    
    coordinate_dict = {}
    for line in data.strip().split("\n"):
        parts = line.split()
        coord = tuple(map(int, parts[0].split(",")))
        coordinate_dict[coord] = int(parts[1])
    
    return coordinate_dict

def get_map_number(coordString):
    """Extract coordinates from a location string and return the map number."""
    coordinates = extract_coordinates(coordString)
    
    if coordinates is None:
        return "Invalid location format."

    lookup = create_coordinate_lookup()
    
    # Debugging output
    print("DEBUG: Checking lookup for", coordinates)
    
    return lookup.get(coordinates, "Coordinates not found in map.")


# Example usage in your script:
coordString = Items.GetPropStringByIndex(tmap,4)
print(get_map_number(coordString))

