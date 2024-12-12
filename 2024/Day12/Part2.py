#AdventOfCode 2024 Day 12 Part 2!

from datetime import datetime
from collections import defaultdict
from collections import deque
start_time = datetime.now()
running_total = start_time

print('begin')

# path = '2024/Day12/example3.txt'
path = '2024/Day12/input.txt'
with open(path, mode="r", encoding="utf-8") as f:
    read_data = f.read().strip() #->str
    grid = read_data.strip().splitlines() #->list

#summary of problem
#help determine cost of fence around a single region

#input:
#grid of garden plots
#adjacent plots are 'regions'
#   need area and perimeter
#   area is number of plots in region
#   
#return
#price of fence
#multiply area by perimeter for each region to get total price of all regions


def in_bounds(x,y):
    cols = len(grid)
    rows = len(grid[0])
    return (y >= 0 and y < rows) and (x >= 0 and x < cols)

def get_perimeter_count(a):
    x, y = a
    perimeter = 0
    moves = {(0, 1), (0, -1), (-1, 0), (1, 0)}
    for move in moves:
        x_move, y_move = move
        if not in_bounds(x + x_move, y + y_move):
            perimeter += 1
            continue
        #check value of next location in grid
        #if not same value, increment perimeter
        if grid[y][x]!=grid[y + y_move][x + x_move]:
            perimeter += 1
    return perimeter

def get_corner_count(a): #should be the same as the number of sides in an area
    x, y = a
    corner = 0
    #e.g. for the 1st C in this
    # AAAA
    # BBCD
    # BBCC
    # EEEC
    # top left corner are A and B, top right corner is A and D
    # this is y-1 and x-1, and then y-1 and x+1
    corner_checks = {((0, -1),(-1, 0)), ((0, -1),(1, 0)), ((0, 1),(1, 0)), ((0, 1),(-1, 0))}
    for side1, side2 in corner_checks:
        x_move1, y_move1 = side1
        x_move2, y_move2 = side2
        side1_in_bounds = in_bounds(x + x_move1, y + y_move1)
        side2_in_bounds = in_bounds(x + x_move2, y + y_move2)
        if not side1_in_bounds or (side1_in_bounds and grid[y][x]!=grid[y + y_move1][x + x_move1]):
            if not side2_in_bounds or (side2_in_bounds and grid[y][x]!=grid[y + y_move2][x + x_move2]):
                corner += 1
    # edge case, the middle B needs to detect 4 diagonal corners too
    # ABA
    # BBB
    # ABA
    diagonal_corner_checks = {(-1, -1),(1, 1),(1, -1),(-1, 1)}
    for dx, dy in diagonal_corner_checks:
        is_in_bounds = in_bounds(x+dx, y+dy)
        if not is_in_bounds:
            continue #already counted in prev loop... not an edge case
        if grid[y][x]==grid[y+dy][x+dx]:
            continue #matches, so it's not a corner
        # if grid[y][x]!=grid[y+dy][x+dx]:
        #if the 2 sides next to the original position and the new position match the original plot type
        if dx==-1 and dy==-1:
            matching_side_checks = {((0, 1),(1, 0))}
        elif dx==1 and dy==1:
            matching_side_checks = {((0, -1),(-1, 0))}
        elif dx==-1 and dy==1:
            matching_side_checks = {((0, -1),(1, 0))}
        elif dx==1 and dy==-1:
            matching_side_checks = {((-1, 0),(0, 1))}
            
        for side1, side2 in matching_side_checks:
            x_move1, y_move1 = side1
            x_move2, y_move2 = side2
            side1_in_bounds = in_bounds(x+dx + x_move1, y+dy + y_move1)
            side2_in_bounds = in_bounds(x+dx + x_move2, y+dy + y_move2)
            if side1_in_bounds and grid[y][x]==grid[y+dy + y_move1][x+dx + x_move1]:
                if side2_in_bounds and grid[y][x]==grid[y+dy + y_move2][x+dx + x_move2]:
                    corner += 1

    return corner

matrix = dict() #{(x,y): plot_type}
plot_types = defaultdict(int) #track unique plot types and the number of occurrences
for y in range(0,len(grid)):
    for x in range(0,len(grid[y])):
        matrix[(x,y)]=(grid[y][x],get_corner_count((x,y)))
        plot_types[grid[y][x]]+=1


found_regions = dict() #{plot_type: [(x,y)]}  plot type with list of lists of areas?
region_coords = dict() #{plot_type: [(x,y)], blnChecked} 
for p in plot_types:
    found_regions[p] = []
    region_coords[p] = []
for a in matrix:
    region_coords[matrix[a][0]].append(a) #

checked_grids = set() #{(x,y)}  only mark as checked when we actually add this to a region (i.e. not for just a bounds or perimeter check)

#can we just cheat and say for every "A" plot (even if in multiple regions), we don't count the regions at all?
#   i.e. only count the area of every "A"? add number of "sides" not adjacent to another "A"?
#   i think this would factor in the other plots in the middle.... 
#   right... but we also need the area of each plot


def get_matching_plots_inbounds(xyset):
    x, y = xyset
    # moves = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}
    moves = {(0, 1), (0, -1), (-1, 0), (1, 0)}
    next_coords = set()
    for move in moves:
        #try moving every direction except backwards to where we came from? 
        x_move, y_move = move
        if not(in_bounds(x + x_move, y + y_move)):
            continue
        if (x + x_move, y + y_move) in checked_grids:
            continue
        #check value of next location in grid
        if matrix[(x,y)][0]==matrix[(x + x_move, y + y_move)][0]:
            next_coords.add((x + x_move, y + y_move))

    return next_coords

def get_region(p, px, py):
    region_queue = deque()
    region_queue.append((px,py))
    checked_grids.add((px,py))
    region = set()
    region.add((px,py))

    while region_queue:
        x, y = region_queue.popleft()

        get_adjacent_matches = get_matching_plots_inbounds((x,y))
        for nextx, nexty in get_adjacent_matches:
            region_queue.append((nextx,nexty))
            checked_grids.add((nextx,nexty))
            region.add((nextx,nexty))
    
    found_regions[p].append(region)

    return len(region)

def build_regions(p):
    plot_count = plot_types[p]
    startx, starty = region_coords[p][0]
    # area = [(startx,starty)]
    # grid_size = len(grid[0])*len(grid)
    while plot_count > 0:
        plot_count-=get_region(p,startx,starty)
        #get next coordinate not already allocated to a region
               
        startx=-1
        starty=-1
        for a in region_coords[p][1:]:                
            if a not in checked_grids:
                startx, starty = a
                break #for
            if startx>=0 and starty>=0:
                break #for


running_total = datetime.now()
print(f'begin processing: {running_total-start_time}')
for plot_type in plot_types:
    build_regions(plot_type)


running_total = datetime.now()
print(f'begin totaling: {running_total-start_time}')

total = 0
for r in found_regions:
    for lst in found_regions[r]:
        corner_count = 0
        area_size = len(lst)
        for x, y in lst:
            corner_count+=matrix[(x,y)][1]
        
        total += area_size*corner_count


# print(results)
running_total = datetime.now()
print(f"Part 2 total: {total}, duration: {running_total - start_time}")
#855082 is right!