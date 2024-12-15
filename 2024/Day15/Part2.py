#AdventOfCode 2024 Day 15 Part 2!

from datetime import datetime
from collections import deque

start_time = datetime.now()
running_total = start_time

print('begin')

path = '2024/Day15/example.txt'; tiles_width = 10; tiles_height = 10; x_max = 9; y_max = 9
# path = '2024/Day15/example2.txt'; tiles_width = 8; tiles_height = 8; x_max = 7; y_max = 7
# path = '2024/Day15/example3.txt'; tiles_width = 7; tiles_height = 7; x_max = 6; y_max = 6
# path = '2024/Day15/example4.txt'; tiles_width = 7; tiles_height = 7; x_max = 6; y_max = 6
path = '2024/Day15/input.txt'; tiles_width = 100; tiles_height = 100; x_max = 99; y_max = 99
with open(path, mode="r", encoding="utf-8") as f:
    read_data = f.read().strip().split('\n\n') #->list
    orig_map_lines = read_data[0].split('\n')
    # map_lines = read_data[0].split('\n')
    map_lines = []
    for y in range(len(orig_map_lines)):
        line = ""
        #double the map width!
        for x in range(len(orig_map_lines[0])):
            match orig_map_lines[y][x]:
                case '#':
                    line+='##'
                case 'O':
                    line+='[]'
                case '.':
                    line+='..'
                case '@':
                    line+='@.'
        map_lines.append(line)

    dir_lines = read_data[1].splitlines()
    dir_list = []
    for i in range(len(dir_lines)):
        for li in range(len(dir_lines[i])):
            dir_list.append(dir_lines[i][li])


robot_pos = tuple((int,int))
warehouse = dict()
for y in range(len(map_lines)):
    for x in range(len(map_lines[0])):
        warehouse[(x,y)]=map_lines[y][x]
        if warehouse[(x,y)]=='@':
            robot_pos = (x,y)

def print_map():
    for y in range(len(map_lines)):
        line = ""
        for x in range(len(map_lines[0])):
            line += warehouse[(x,y)]
        print(line)

def check_vertical_boxes(pos, dir):
    moves = {"^": (0, -1), "v": (0, 1)}
    x_move, y_move = moves[dir]
    side_flip = {"[": "]", "]": "["}
    other_half_moves = {"[": (1, 0), "]": (-1, 0)}

    end_tiles = set() # track the tile type at the end of every fork. If any are not "." then it is not a possible move
    checked = dict()

    boxes_queue = deque()
    boxes_queue.append(pos)

    #point of this is to extrapolate all of the wide "O's" to check if any in the chain are blocked
    # ...##
    # .....
    # [][].
    # .[]..
    # ..@..
    
    # we start with the ] from the position above the robot
    # we should add the horizontally adjacent [ to the queue
    # we should add the vertically adjacent [ to the queue, and also its horizontally adjacent ]
    # then see that there is a "." above both points
    # count the vertical rows? Nah... just prove it can be moved, then move later..
    while boxes_queue:
        qx, qy = boxes_queue.popleft()
        next_vertical_pos = (qx,qy+y_move)     

        # get other half of box position
        if warehouse[(qx,qy)] in other_half_moves:
            sx_move, sy_move = other_half_moves[warehouse[(qx,qy)]]
            buddy_pos = (qx+sx_move,qy)
            if buddy_pos not in checked:
                boxes_queue.append(buddy_pos)
                # checked.add(buddy_pos)
            
        nx, ny = next_vertical_pos
        if warehouse[next_vertical_pos] not in side_flip:
            # found an end tile
            end_tiles.add(warehouse[next_vertical_pos])
            if "#" in end_tiles:
                return False, checked # not possible move

        if warehouse[next_vertical_pos] in side_flip:
            if next_vertical_pos not in checked:
                boxes_queue.append(next_vertical_pos)     

        checked[(qx,qy)]=warehouse[(qx,qy)]  


    return True, checked

# keep moving left or right until a "." or "#" is found
# return False if # found, otherwise True
# also return the position to move to...
def check_horizontal_boxes(pos, dir):
    moves = {">": (1, 0), "<": (-1, 0)}
    x_move, y_move = moves[dir]
    cx, cy = pos
    next_horizontal_pos = (cx+x_move,cy)

    x_queue = deque()
    x_queue.append(pos)

    while x_queue:
        qx, qy = x_queue.popleft()
        next_horizontal_pos = (qx+x_move,qy)
        if warehouse[next_horizontal_pos]=="#":
            return False, next_horizontal_pos
        elif warehouse[next_horizontal_pos]==".":
            break
        else:
            x_queue.append(next_horizontal_pos)
    
    return True, next_horizontal_pos

def move_x(move_to, dir, robot_pos):
    moves = {"<": (1, 0), ">": (-1, 0)}# note this is REVERSED
    x_move, y_move = moves[dir]
    # mx, my = move_to
    # next_horizontal_pos = (mx+x_move,my)

    x_queue = deque()
    x_queue.append(move_to)

    while x_queue:
        qx, qy = x_queue.popleft()
        next_horizontal_pos = (qx+x_move,qy)
        if warehouse[next_horizontal_pos]=="@":
            robot_pos = (qx, qy)
            warehouse[robot_pos] = "@"
            warehouse[next_horizontal_pos] = "."
            return robot_pos
        else:
            warehouse[(qx, qy)] = warehouse[next_horizontal_pos]
            x_queue.append(next_horizontal_pos)
    
    return robot_pos

def move_y(checked, dir):
    #take in a set of checked positions
    #every [ or ] needs to move 1 space on the y axis
    moves = {"^": (0, -1), "v": (0, 1)}
    x_move, y_move = moves[dir]
    # cx, cy = pos
    for pos in checked:
        warehouse[pos]="."
    for pos in checked:
        cx, cy = pos
        next_vertical_pos = (cx,cy+y_move)
        warehouse[next_vertical_pos]=checked[pos]


def move_robot_part2(robot_pos,dir):
    #if adjacent to other boxes, move all of them the same direction until it hits something
    move_queue = deque()
    move_queue.append(robot_pos)
    moves = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}
    lr_moves = ("<",">")
    box_chars = ("[","]")
    x_move, y_move = moves[dir]

    while move_queue:
        cx, cy = move_queue.popleft()
        next_pos = (cx+x_move,cy+y_move)

        if warehouse[next_pos]=='#': #border/obstacle, no move
            return robot_pos

        if warehouse[next_pos]=='.': #border/obstacle, no move
            #move robot only
            warehouse[next_pos] = "@"
            warehouse[(cx, cy)] = "."
            return next_pos

        if (warehouse[next_pos] in box_chars):
            if (dir in lr_moves):
                chkHoriz, move_to = check_horizontal_boxes(next_pos, dir)
                if chkHoriz:
                    #pull horizontally from destination point?
                    robot_pos = move_x(move_to, dir, robot_pos)
                    return robot_pos
            else: #up or down... recurse through every fork and only return true if ends with "".."?
                chkVert, checked = check_vertical_boxes(next_pos, dir)
                if chkVert:
                    #move all vertically
                    move_y(checked, dir)
                    warehouse[next_pos] = "@"
                    warehouse[(cx, cy)] = "."
                    return next_pos

    return robot_pos


running_total = datetime.now()
print(f'begin processing: {running_total-start_time}')
for dir in dir_list:
    # print_map()
    robot_pos = move_robot_part2(robot_pos, dir)


running_total = datetime.now()
print(f'begin totaling: {running_total-start_time}')
total = 0
for wk in warehouse:
    if warehouse[wk]=='[':
        x, y = wk
        total += 100 * y + x

print_map()

# print(results)
running_total = datetime.now()
print(f"Part 2 total: {total}, duration: {running_total - start_time}")
#1528453 right!
