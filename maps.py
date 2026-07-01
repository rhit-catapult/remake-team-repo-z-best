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
    [0,0,0,0,1,1,1,1,1,1,1],
    [1,1,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,1,1],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,0,0,0],
]

# Open doorway on map 2 right wall so it connects to the lower-right branch.
for doorway_row in (4, 5):
    map_data_2[doorway_row][11] = 0
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
map7_start_col = map4_width
_stamp_room(middle_section, map_data_7, 0, map7_start_col)

# Direct connector from room 6 (top section) down into room 7.
connector_col_start = map4_width + map5_width + 4
connector_col_end = connector_col_start + 2
for connector_row in range(0, 5):
    for connector_col in range(connector_col_start, connector_col_end):
        middle_section[connector_row][connector_col] = 0
for connector_col in range(map4_width + 12, connector_col_end):
    middle_section[4][connector_col] = 0

# Lower-middle: room 2 plus smaller room 8 shifted right (diagonal leg of the R)
lower_section_rows = max(len(map_data_2), len(map_data_8))
lower_section = _build_section(lower_section_rows, world_cols, fill_tile=1)
_stamp_room(lower_section, map_data_2, 0, 0)
map8_start_col = map4_width + 7
_stamp_room(lower_section, map_data_8, 0, map8_start_col)

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
map8_start_row = map2_start_row

map3_start_col = 0
map3_room_rows_count = len(map_data_3)
map3_room_cols_count = len(map_data_3[0])

map7_start_row = map3_start_row
map7_rows_count = len(map_data_7)
map7_cols_count = len(map_data_7[0])

map8_rows_count = len(map_data_8)
map8_cols_count = len(map_data_8[0])

# Passage zone connecting room 6 into the middle branch.
room6_passage_start_row = map3_start_row
room6_passage_end_row = map3_start_row + 4
room6_passage_start_col = map4_width + 12
room6_passage_end_col = map4_width + map5_width + 5

# Rows above map 1 (maps 2-4) are considered locked until unlock.
locked_rows_count = map1_start_row

# Items: (row, column, item_type)
# 10=box, 20=corpse
items = [
    (map1_start_row + 6, 9, 10),  # Box in map1
    (map1_start_row + 6, 10, 10),
    (map1_start_row + 6, 6, 20)   # Corpse in map1
]
