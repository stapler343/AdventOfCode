#AdventOfCode 2024 Day 15 Part 1!

from datetime import datetime
from collections import deque

start_time = datetime.now()
running_total = start_time

print('begin')

path = '2024/Day15/example.txt'; tiles_width = 10; tiles_height = 10; x_max = 9; y_max = 9
# path = '2024/Day15/example2.txt'; tiles_width = 8; tiles_height = 8; x_max = 7; y_max = 7
path = '2024/Day15/input.txt'; tiles_width = 100; tiles_height = 100; x_max = 99; y_max = 99
with open(path, mode="r", encoding="utf-8") as f:
    read_data = f.read().strip().split('\n\n') #->list
    map_lines = read_data[0].split('\n')
    dir_lines = read_data[1].splitlines()
    dir_list = []
    for i in range(len(dir_lines)):
        for li in range(len(dir_lines[i])):
            dir_list.append(dir_lines[i][li])


    

#structure:
# dict (x,y): char
# dict (x,y): ?
robot_pos = tuple((int,int))
warehouse = dict()
for y in range(len(map_lines)):
    for x in range(len(map_lines[0])):
        warehouse[(x,y)]=map_lines[y][x]
        if warehouse[(x,y)]=='@':
            robot_pos = (x,y)

# print(warehouse)
# print(dir_list)

def move_robot(robot_pos,dir):
    #if adjacent to other boxes, move all of them the same direction until it hits something
    move_queue = deque()
    move_queue.append(robot_pos)
    moves = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}
    x_move, y_move = moves[dir]

    steps = 0
    box_count = 0
    while move_queue:
        cur_pos = move_queue.popleft()
        cx, cy = cur_pos        
        next_pos = (cx+x_move,cy+y_move)

        if warehouse[next_pos]=='#': #border/obstacle
            continue

        if warehouse[next_pos]=='O':
            move_queue.append(next_pos)
            box_count += 1
            continue
            # ? 
            # actually need to check what comes next after all of the boxes...
            #   need to see if the last one hits a barrier to know if all boxes can move 

        steps += 1 + box_count
    
    cur_pos = robot_pos 
    cx, cy = cur_pos
    cur_val = warehouse[cur_pos] #shuold always start with robot @
    prev_val = '.'
    for i in range(steps):
        #move the robot (x,y) and i # of boxes one space
        next_pos = (cx+x_move,cy+y_move)
        if cur_val=='@':
            robot_pos = next_pos
        next_val = warehouse[next_pos]
        warehouse[(cx,cy)]=prev_val #prev val becomes vacant "."
        # everything else shifts once
        warehouse[next_pos]=cur_val
        prev_val = cur_val
        cur_val = next_val
        cx, cy = next_pos
    
    return robot_pos


for dir in dir_list:
    robot_pos = move_robot(robot_pos, dir)


running_total = datetime.now()
print(f'begin processing: {running_total-start_time}')

running_total = datetime.now()
print(f'begin totaling: {running_total-start_time}')
total = 0
for wk in warehouse:
    if warehouse[wk]=='O':
        x, y = wk
        total += 100 * y + x

for y in range(len(map_lines)):
    line = ""
    for x in range(len(map_lines[0])):
        line += warehouse[(x,y)]
    print(line)

# print(results)
running_total = datetime.now()
print(f"Part 1 total: {total}, duration: {running_total - start_time}")
#1514333 right!
