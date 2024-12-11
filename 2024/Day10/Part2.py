#AdventOfCode 2024 Day 10 Part 1!

from datetime import datetime
start_time = datetime.now()
running_total = start_time

print('begin')

with open('Day10/input.txt', mode="r", encoding="utf-8") as f:
    read_data = f.read().strip() #->str
    grid = read_data.strip().splitlines() #->list

#things to track
# puzzle input is topographic map
    # indicates height between 0 and 9

# fill in missing GOOD hiking trails
    # good hiking trail is as long as possible and has an even, gradual, uphill slope
        # only up, down, left, or right (not diagonal)
#trailhead is any position that starts one or more hiking trails, always height 0
    #trailhead score is how many 9's can be reached from it
        #how many UNIQUE 9's from that 0

matrix = set() #{(x,y): [(x,y)]} tracks locations of all 9's
trailends = set() #{(x,y)} tracks locations of all 9's
trailheads = dict() #{(x,y): [(x,y)]} tracks locations of successful 9. order does not matter as we just need to sum the count of results
for y in range(0,len(grid)):
    for x in range(0,len(grid[y])):
        matrix.add((x,y))
        if grid[y][x] == "9":
            trailends.add((x,y))
        if grid[y][x] == "0":
            trailheads[(x,y)] = set()

print(matrix)
print(trailends)
print(trailheads)

running_total = datetime.now()
print(f'file read and data structures prepared in {running_total-start_time}')


running_total = datetime.now()
print(f'begin processing: {running_total-start_time}')

def in_bounds(x,y):
    cols = len(grid)
    rows = len(grid[0])
    return (y >= 0 and y < rows) and (x >= 0 and x < cols)

def get_coordinates_inbounds(xyset):
    x, y = xyset
    # moves = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}
    moves = {(0, 1), (0, -1), (-1, 0), (1, 0)}
    next_coords = set()
    for move in moves:
        #try moving every direction except backwards to where we came from? 
        #   ...maybe it doesn't actually matter since it would be quickly disqualified anyway
        x_move, y_move = move
        if not(in_bounds(x + x_move, y + y_move)):
            continue
        #check value of next location in grid
        if int(grid[y][x])==int(grid[y + y_move][x + x_move])-1:
            next_coords.add((x + x_move, y + y_move))
            continue

    return next_coords

def check_path(ptrailhead, xyset, path, psuccess):
    if psuccess:
        return psuccess
    
    next_safe_coordinates = get_coordinates_inbounds(xyset)

    # moves = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}
    # px, py = xyset

    for x, y in next_safe_coordinates:
        success=False
        path_branch = path.copy()
        if len(path_branch)==9 and grid[y][x]=="9":
            success = True
            path_branch.append((x,y))
            trailstring = ''
            for bx,by in path_branch[0:len(path_branch)-1]:
                trailstring+=f"({bx},{by})|"
            trailstring+=f"({x},{y})"
            trailheads[ptrailhead].add(trailstring)
        elif len(path_branch) < 9:
            path_branch.append((x,y))
            psuccess = check_path(ptrailhead,(x,y),path_branch,success)
            # continue

    return psuccess

#for every adjacent square, continue if the value is next in sequence
#exit conditions:
#   out of bounds
#   found coordinate of a 9 in trailends with a length of 10

#loop through every trailhead to try to find sequential digits until 9
for th in trailheads:
    #have to calculate the score of this trailhead by finding all of the possible unique 9's it can hit
    #recursively continue down each fork?
    x, y = th
    check_path(th,th,[(x,y)],None)

running_total = datetime.now()
print(f'begin organizing: {running_total-start_time}')

running_total = datetime.now()
print(f'begin totaling: {running_total-start_time}')
total = 0
for x,y in trailheads:
    successes = set()
    for path in trailheads[(x,y)]:
        # path_list = path.split('|')
        successes.add(path)
    total+=len(successes)
    # print(successes)
running_total = datetime.now()
print(f"Part 2 total: {total}, duration: {running_total - start_time}")
#1324