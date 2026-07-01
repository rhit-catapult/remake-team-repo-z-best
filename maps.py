"""Map data and configuration"""

# Map 1: Bottom map with wall boundary
map_data_1 = [
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1],
]

# Map 2: Top map (accessible after unlock)
map_data_2 = [
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,1,1,0,0,0,0,0,1,1,1,1],
]

map_data_3 = [
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,1,1,0,0,0,0,0,1,1,1,1],

]

map_data_4 = [
    [1,1,1,1,0,0,0,0,0,1,1,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1],
    
]

map_data_5 = [
    [4,4,4,4,4,4,4,4,4,4,4,4,4],
    [2,2,2,2,2,2,2,2,2,2,2,2,4],
    [2,2,2,2,2,2,2,2,2,2,2,2,4],
    [2,2,2,2,2,2,2,2,2,2,2,2,4],
    [2,2,2,2,2,2,2,2,2,2,2,2,4],
    [2,2,2,2,2,2,2,2,2,2,2,2,4],
    [2,2,2,2,2,2,2,2,2,2,2,2,4],
    [2,2,2,2,2,2,2,2,2,2,2,2,4],
    [4,4,4,4,4,2,2,2,2,4,4,4,4],

]

# Attach map 5 to the right side of map 4.
top_section_rows = max(len(map_data_4), len(map_data_5))
map4_width = len(map_data_4[0])
map5_width = len(map_data_5[0])

map4_padded = [row[:] for row in map_data_4]
map5_padded = [row[:] for row in map_data_5]

while len(map4_padded) < top_section_rows:
    map4_padded.append([1] * map4_width)

while len(map5_padded) < top_section_rows:
    map5_padded.append([4] * map5_width)

map_data_4_5 = [left_row + right_row for left_row, right_row in zip(map4_padded, map5_padded)]

# Combine maps from top to bottom: (4+5), 3, 2, 1.
# This keeps map 1 as the bottom-most section of the world.
full_world_map = map_data_4_5 + map_data_3 + map_data_2 + map_data_1

map4_rows_count = len(map_data_4_5)
map3_rows_count = len(map_data_3)
map2_rows_count = len(map_data_2)
map1_rows_count = len(map_data_1)

map5_rows_count = len(map5_padded)
map5_cols_count = map5_width
map5_start_col = map4_width
map5_start_row = 0

map4_start_row = 0
map3_start_row = map4_rows_count
map2_start_row = map4_rows_count + map3_rows_count
map1_start_row = map4_rows_count + map3_rows_count + map2_rows_count

# Rows above map 1 (maps 2-4) are considered locked until unlock.
locked_rows_count = map1_start_row

# Items: (row, column, item_type)
# 10=box, 20=corpse
items = [
    (map1_start_row + 6, 9, 10),  # Box in map1
    (map1_start_row + 6, 6, 20)   # Corpse in map1
]
