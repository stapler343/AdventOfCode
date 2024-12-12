#AdventOfCode 2024 Day 12 Part 1!

from datetime import datetime
from collections import defaultdict
from collections import deque
start_time = datetime.now()
running_total = start_time

print('begin')

# path = '2024/Day12/example.txt'
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

matrix = dict() #{(x,y): plot_type}
plot_types = defaultdict(int) #track unique plot types and the number of occurrences
for y in range(0,len(grid)):
    for x in range(0,len(grid[y])):
        matrix[(x,y)]=(grid[y][x],get_perimeter_count((x,y)))
        plot_types[grid[y][x]]+=1

found_regions = dict() #{plot_type: [(x,y)] plot type with list of lists of areas?
region_coords = dict() #{plot_type: [(x,y)]
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
        for x, y in lst:
            total += len(lst)*matrix[(x,y)][1]


# print(results)
running_total = datetime.now()
print(f"Part 1 total: {total}, duration: {running_total - start_time}")
#1433460 is right!