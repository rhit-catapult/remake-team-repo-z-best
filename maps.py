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
    [1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1],
    
]

map_data_5 = [
    [4,4,4,4,4,4,4,4,4,4,4,4,4],
    [2,2,2,2,2,2,2,2,2,2,2,2,4],
    [2,2,2,2,2,2,2,2,2,2,2,2,4],
    [2,2,2,2,2,2,2,2,2,2,2,2,2],
    [2,2,2,2,2,2,2,2,2,2,2,2,2],
    [2,2,2,2,2,2,2,2,2,2,2,2,4],
    [2,2,2,2,2,2,2,2,2,2,2,2,4],
    [4,4,4,4,4,4,4,4,4,4,4,4,4],

]

map_data_6 = [
    [4,4,4,4,4,4,4,4,4,4,4,4,4],
    [2,2,2,2,2,2,2,2,2,2,2,2,4],
    [2,2,2,2,2,2,2,2,2,2,2,2,4],
    [2,2,2,2,2,2,2,2,2,2,2,2,4],
    [2,2,2,2,2,2,2,2,2,2,2,2,4],
    [2,2,2,2,2,2,2,2,2,2,2,2,4],
    [2,2,2,2,2,2,2,2,2,2,2,2,4],
    [4,4,4,4,2,2,2,2,2,4,4,4,4],

]

# Map 7: Mid-right room attached to map 3.
map_data_7 = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,1,1,1,1,0,0,0,0,0,1,1],
]

# Map 8: Smaller lower-right room that forms the diagonal leg of the "R".
map_data_8 = [
    [1,1,1,1,1,1,1,1,1,1,1],
    [1,1,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,0,0,0],
]

# Open doorways on map 3 and map 2 right walls so new rooms connect naturally.
for doorway_row in (3, 4):
    map_data_3[doorway_row][12] = 0
for doorway_row in (4, 5):
    map_data_2[doorway_row][12] = 0


def _build_section(height, width, fill_tile=1):
    return [[fill_tile for _ in range(width)] for _ in range(height)]


def _stamp_room(section, room, start_row, start_col):
    for r, room_row in enumerate(room):
        section_row = start_row + r
        if section_row < 0 or section_row >= len(section):
            continue
        for c, tile in enumerate(room_row):
            section_col = start_col + c
            if section_col < 0 or section_col >= len(section[section_row]):
                continue
            section[section_row][section_col] = tile


# Keep the top section width as the base world width.
top_section_rows = max(len(map_data_4), len(map_data_5), len(map_data_6))
map4_width = len(map_data_4[0])
map5_width = len(map_data_5[0])
map6_width = len(map_data_6[0])
world_cols = map4_width + map5_width + map6_width

# Top: rooms 4, 5, 6 (top bar of the R)
top_section = _build_section(top_section_rows, world_cols, fill_tile=1)
_stamp_room(top_section, map_data_4, 0, 0)
_stamp_room(top_section, map_data_5, 0, map4_width)
_stamp_room(top_section, map_data_6, 0, map4_width + map5_width)

# Middle: rooms 3 and 7 (middle arm of the R)
middle_section_rows = max(len(map_data_3), len(map_data_7))
middle_section = _build_section(middle_section_rows, world_cols, fill_tile=1)
_stamp_room(middle_section, map_data_3, 0, 0)
_stamp_room(middle_section, map_data_7, 0, map4_width)

# Lower-middle: room 2 plus smaller room 8 shifted right (diagonal leg of the R)
lower_section_rows = max(len(map_data_2), len(map_data_8))
lower_section = _build_section(lower_section_rows, world_cols, fill_tile=1)
_stamp_room(lower_section, map_data_2, 0, 0)
_stamp_room(lower_section, map_data_8, 0, map4_width + 7)

# Bottom: room 1 only (left stem of the R)
bottom_section = _build_section(len(map_data_1), world_cols, fill_tile=1)
_stamp_room(bottom_section, map_data_1, 0, 0)

# Combine sections from top to bottom.
map_data_4_5_6 = top_section
full_world_map = top_section + middle_section + lower_section + bottom_section

map4_rows_count = len(map_data_4_5_6)
map3_rows_count = len(middle_section)
map2_rows_count = len(lower_section)
map1_rows_count = len(map_data_1)

map5_rows_count = top_section_rows
map5_cols_count = map5_width
map5_start_col = map4_width
map5_start_row = 0
map6_rows_count = top_section_rows
map6_cols_count = map6_width
map6_start_col = map4_width + map5_width
map6_start_row = 0

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
    (map1_start_row + 6, 10, 10),
    (map1_start_row + 6, 6, 20)   # Corpse in map1
]
