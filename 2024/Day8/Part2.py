#AdventOfCode 2024 Day 8 Part 2!

from datetime import datetime
start_time = datetime.now()

with open('Day8/input.txt', mode="r", encoding="utf-8") as f:
    read_data = f.read().strip() #->str
    grid = read_data.strip().splitlines() #->list

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

def add_antinodes_part1(antinodes, lx, ly, rx, ry):    
    xdiff = lx-rx #eg. - num tells left, + num tells right
    ydiff = ly-ry #eg. - num for up, + num for down

    #check left
    left_anode = (lx+xdiff,ly+ydiff)
    if left_anode in matrix and matrix[left_anode]!=f:
        antinodes.add(left_anode)

    #check right
    right_anode = (rx-xdiff,ry-ydiff)
    if right_anode in matrix and matrix[right_anode]!=f:
        antinodes.add(right_anode)

def add_antinodes_part2(antinodes2, lx, ly, rx, ry):    
    xdiff = lx-rx #eg. - num tells left, + num tells right
    ydiff = ly-ry #eg. - num for up, + num for down
    left_anode = (lx-xdiff,ly-ydiff)
    right_anode = (rx-xdiff,ry-ydiff)

    while left_anode in matrix: #loop from left node back in the direction of the right node so it also gets added
        antinodes2.add(left_anode)
        x, y = left_anode
        left_anode = (x+xdiff, y+ydiff) 
    
    while right_anode in matrix: #loop from right node back in the direction of the left node so it also gets added
        antinodes2.add(right_anode)
        x, y = right_anode
        right_anode = (x-xdiff, y-ydiff) 

antinodes = set() #simplifies things because it cannot add duplicates
antinodes2 = set()
for f in frequency_locations.keys():
    for fli in range(0,len(frequency_locations[f])-1): #no need to check the last frequency in the list
        lx, ly = frequency_locations[f][fli]        
        for rx, ry in frequency_locations[f][fli+1:]: #get each subsequent matching frequency location
            add_antinodes_part1(antinodes, lx, ly, rx, ry)
            add_antinodes_part2(antinodes2, lx, ly, rx, ry)

# total = len(antinodes)
print(f"Part 1 total: {len(antinodes)}, duration: {datetime.now() - start_time}")
#274 too high!
#273? right!
print(f"Part 2 total: {len(antinodes2)}, duration: {datetime.now() - start_time}")
#1007 too low!
#1017 is right!