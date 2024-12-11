#AdventOfCode 2024 Day 6 Part 2!

from datetime import datetime
start_time = datetime.now()

with open('Day6/input.txt', mode="r", encoding="utf-8") as f:
    read_data = f.read().splitlines() #->list[]

#build coordinates
map = [] #
starting_pos = []
for y in range(len(read_data)):    
    for x in range(len(read_data[y])):
        val = read_data[y][x]
        if val == "^":
            starting_pos = [x,y]
        elif val != "#":
            map.append([x,y])

read_data_copy = read_data[:]

def check_bounds(pos):
    x = pos[0]
    y = pos[1]
    x_max = len(read_data[1]) - 1
    y_max = len(read_data[0]) - 1
    in_bounds = x >= 0 and x < x_max and y >= 0 and y < y_max
    return in_bounds

def check_bounds_next(pos, dir):
    match dir:
        case 'up': pos[1] -= 1
        case 'down': pos[1] += 1
        case 'left': pos[0] -= 1
        case 'right': pos[0] += 1 
    x = pos[0]
    y = pos[1]
    x_max = len(read_data[1]) - 1
    y_max = len(read_data[0]) - 1
    in_bounds = x >= 0 and x <= x_max and y >= 0 and y <= y_max
    if not in_bounds:
        return False
    return in_bounds

def can_move_forward(pos, dir):
    match dir:
        case 'up': pos[1] -= 1
        case 'down': pos[1] += 1
        case 'left': pos[0] -= 1
        case 'right': pos[0] += 1 
    # in_bounds = pos[0] >= 0 and pos[1] >= 0
    if check_bounds(pos):
        if check_obstacle(pos):
            return False
        # return not(check_obstacle(pos))
        return True
    return False

def check_obstacle(pos):
    return read_data[pos[1]][pos[0]] == "#"

def check_obstacle_next(pos, dir):
    match dir:
        case 'up': pos[1] -= 1
        case 'down': pos[1] += 1
        case 'left': pos[0] -= 1
        case 'right': pos[0] += 1 
    return read_data[pos[1]][pos[0]] == "#"

def move_next(pos, dir):
    #pos is just the current [x,y]
    try_pos = [pos[0],pos[1]]
    if not can_move_forward(pos=try_pos, dir=dir[0]): #does not modify params
        if check_obstacle(try_pos):
            #rule says try turning right
            if not try_turn(pos, dir): #modifies direction only
                return False
        else:
            pos[0] = try_pos[0]
            pos[1] = try_pos[1]
            return False        

    match dir[0]:
        case 'up': pos[1] -= 1
        case 'down': pos[1] += 1
        case 'left': pos[0] -= 1
        case 'right': pos[0] += 1    
    
    #check boundary?
    # out_of_bound = y < 0 or x < 0
    return check_bounds(pos)

def try_turn(pos, dir):
    #could have to try this up to 3 times for a 180 degree turn
    pos2 = [pos[0],pos[1]]
    dir2 = [dir[0]]
    # for i in range(1,2):
    match dir2[0]:
        case "up": dir2[0] = "right"
        case "down": dir2[0] = "left"
        case "left": dir2[0] = "up"
        case "right": dir2[0] = "down" 
    
    if can_move_forward(pos2, dir2[0]): #does not modify params
        # pos = pos2
        dir[0] = dir2[0]
        return True
    
    if check_obstacle(pos2):
        #try turning again
        match dir2[0]:
            case "up": dir2[0] = "right"
            case "down": dir2[0] = "left"
            case "left": dir2[0] = "up"
            case "right": dir2[0] = "down" 

        if can_move_forward(pos2, dir2[0]): #does not modify params
            # pos = pos2
            dir[0] = dir2[0]
            return True

    return False #probably shouldn't happen...

def try_move_next(pos, dir):
    if not move_next(pos, dir):
        return False

    return check_bounds(pos)
    

direction = ["up"] #starting
onpath = True
x = starting_pos[0]
y = starting_pos[1]
pos = [x,y]
val = read_data[y][x]
starting_path = (x,y)
pathed = [(x,y)]
# print("start")
# print(pos)
while onpath:
    onpath = try_move_next(pos, direction)
    # print("position ("+str(pos[0])+", "+str(pos[1])+") direction: "+direction[0]+" char: "+read_data[pos[1]][pos[0]])
    if (pos[0],pos[1]) not in pathed:
        pathed.append((pos[0],pos[1]))

total = len(pathed) 
print(f"Part 1 total: {total}, duration: {datetime.now() - start_time}") #4433 is right!

def try_turn_p2(pos, dir):
    #could have to try this up to 2 times for a 180 degree turn
    dir_copy = [dir[0]]
    match dir_copy[0]:
        case "up": dir_copy[0] = "right"
        case "down": dir_copy[0] = "left"
        case "left": dir_copy[0] = "up"
        case "right": dir_copy[0] = "down" 
    
    if not check_bounds_next([pos[0],pos[1]], dir_copy[0]):
        return False        
    
    dir[0] = dir_copy[0]
    
    if check_obstacle_next([pos[0],pos[1]], dir_copy[0]):
        return False
    
    # pos[0] = pos_copy[0]
    # pos[1] = pos_copy[1]
    # dir[0] = dir_copy[0]

    return True

def move_next_p2(pos, dir):
    #pos is just the current [x,y]
    match dir[0]:
        case 'up': pos[1] -= 1
        case 'down': pos[1] += 1
        case 'left': pos[0] -= 1
        case 'right': pos[0] += 1    
    
    #check boundary?
    # out_of_bound = y < 0 or x < 0
    val = read_data[pos[1]][pos[0]]
    return val == "." or val == "^"

def start_part2_loop(pos, dir, turn_from):
    # if next space out of bounds, return False
    # if next space is obstable, return True
    pos_copy = [pos[0],pos[1]]
    dir_copy = [dir[0]]
    if not check_bounds_next(pos_copy, dir_copy[0]):
        return False        
    pos_copy = [pos[0],pos[1]]
    dir_copy = [dir[0]]
    if check_obstacle_next(pos_copy, dir_copy[0]):
        #try turn
        if try_turn_p2(pos, dir):
            turn_from[0] = ((pos[0],pos[1]), direction[0])
            return True
        else:
            if try_turn_p2(pos, dir):         
                turn_from[0] = ((pos[0],pos[1]), direction[0])
                return True
            else:
                return False
    
    return move_next_p2(pos, dir)



# pathed = [(7,7)] #known obstruction from example
# example obstructions:
# (3,8)
# (7,7)
# (7,9)
# (6,7)
# (1,8)
# (3,6)
successful_obstructions = []
pathed.sort()
# with open('d6p2_output_pathed_p1.txt', 'w') as f:
#     for line in pathed:
#         f.write("("+str(line[0])+","+str(line[1])+")")
#         f.write('\n')

for pathed_pos in pathed:
    if pathed_pos == starting_path:
        continue
    pos = [x,y] #starting position
    direction = ["up"]
    new_map = read_data_copy[:]
    add_obstruction = new_map[pathed_pos[1]]
    x_index = pathed_pos[0]
    add_obstruction = add_obstruction[:x_index] + '#' + add_obstruction[x_index + 1:]
    new_map[pathed_pos[1]] = add_obstruction
    read_data = new_map
    onpath = True
    turns = []
    while onpath:
        turn_from = [0]
        onpath = start_part2_loop(pos, direction, turn_from)
        # print("position ("+str(pos[0])+", "+str(pos[1])+") direction: "+direction[0]+" char: "+read_data[pos[1]][pos[0]])
        if len(turn_from) > 0 and turn_from[0]!=0:
            if turn_from in turns:            
                onpath = False
                successful_obstructions.append(pathed_pos)
                # print("successful obstruction in path: ("+str(pathed_pos[0])+","+str(pathed_pos[1])+") at "+str(datetime.now()))
                break        
            else:
                turns.append(turn_from)
                # print("position added ("+str(pos[0])+", "+str(pos[1])+") direction: "+direction[0])

# print("successful_obstructions: "+str(len(successful_obstructions)))
total = len(successful_obstructions)

# successful_obstructions.sort()
# with open('d6p2_output.txt', 'w') as f:
#     for line in successful_obstructions:
#         f.write("("+str(line[0])+","+str(line[1])+")")
#         f.write('\n')


print(f"Part 2 total: {total}, duration: {datetime.now() - start_time}") #1511 too low
#1516 is right!