#AdventOfCode 2024 Day 8 Part 1!

from datetime import datetime
start_time = datetime.now()

with open('Day8/input.txt', mode="r", encoding="utf-8") as f:
    read_data = f.read().strip() #->str
    str_all = read_data.strip().replace('\n','') #->str
    grid = read_data.strip().splitlines() #->list
    # print(str_all)
# print(read_data)

matrix = dict()
frequency_locations = dict() #e.g. {'0': [(x,y), (x,y)], 'A': [(x,y)]}
count = 0
for y in range(0,len(grid)):
    for x in range(0,len(grid[y])):
        matrix[(x,y)] = [grid[y][x],count]
        count+=1
        if grid[y][x] != ".":
            if frequency_locations.get(grid[y][x]) is None:
                frequency_locations[grid[y][x]] = [(x,y)]
            else:
                frequency_locations[grid[y][x]].append((x,y))

antinodes = set()
dctANodes = dict()
for f in frequency_locations.keys():
    #get each next matching frequency location
    # print(f"current frequency: {f}")
    frequency_location_count = len(frequency_locations[f])
    for fli in range(0,frequency_location_count-1):
        # print(f"current frequency location value: {frequency_locations[f][fli]} and loc:{fli}")
        left_frequency_location = frequency_locations[f][fli]
        right_frequency_locations = frequency_locations[f][fli+1:]
        for rfl in right_frequency_locations:
            right_frequency_location = rfl
            # print(f"other_frequency_location_index: {ofli}, other_frequency_location: {other_frequency_location}")
            lx = left_frequency_location[0]
            ly = left_frequency_location[1]
            rx = right_frequency_location[0]
            ry = right_frequency_location[1]

            #check left
            xdiff = rx-lx
            ydiff = ry-ly
            xanode = lx-xdiff
            yanode = ly-ydiff
            if (xanode>=0 and xanode<len(grid[0])) and (yanode>=0 and yanode<len(grid)):
                left_anode = (xanode,yanode)
                if matrix[left_anode]!=f:
                    antinodes.add(left_anode)

            #check right
            xdiff = lx-rx #eg. - num tells left, + num tells right
            ydiff = ly-ry #eg. - num for up, + num for down
            xanode = rx-xdiff
            yanode = ry-ydiff
            if (xanode>=0 and xanode<len(grid[0])) and (yanode>=0 and yanode<len(grid)):
                right_anode = (xanode,yanode)
                if matrix[right_anode]!=f:
                    antinodes.add(right_anode)

# for key in dctANodes:
#     print(f"frequency: '{key}' has {len(frequency_locations[key])} locations: {frequency_locations[key]}")    
#     print(f"frequency: '{key}' has {len(dctANodes[key])} antinodes: {sorted(dctANodes[key])}")

total = len(antinodes)
print(f"Part 1 total: {total}, duration: {datetime.now() - start_time}")
#274 too high!
#273? right!