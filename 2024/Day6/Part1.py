#AdventOfCode 2024 Day 6 Part 1!

with open('Day6/input.txt', mode="r", encoding="utf-8") as f:
    read_data = f.read().splitlines() #->list[]

#build coordinates
map = [] #x,y,value,onpath
starting_pos = []
for y in range(len(read_data)):    
    for x in range(len(read_data[y])):
        val = read_data[y][x]
        if val == "^":
            starting_pos = [x,y]
        map.append([x,y])


def check_bounds(pos):
    x = pos[0]
    y = pos[1]
    x_max = len(read_data[x]) - 1
    y_max = len(read_data[y]) - 1
    in_bounds = x >= 0 and x < x_max and y >= 0 and y < y_max
    return in_bounds

# def can_move_forward(pos, dir):
#     x = pos[0]
#     y = pos[1]
#     match dir:
#         case 'up':
#             y -= 1
#         case 'down':
#             y += 1
#         case 'left':
#             x -= 1
#         case 'right':
#             x += 1 
#     # in_bounds = x >= 0 and y >= 0
#     if check_bounds([x,y]):
#         return not(check_obstacle(pos))
#     return False

def can_move_forward(pos, dir):
    match dir:
        case 'up':
            pos[1] -= 1
        case 'down':
            pos[1] += 1
        case 'left':
            pos[0] -= 1
        case 'right':
            pos[0] += 1 
    # in_bounds = pos[0] >= 0 and pos[1] >= 0
    if check_bounds(pos):
        if check_obstacle(pos):
            return False
        # return not(check_obstacle(pos))
        return True
    return False

def check_obstacle(pos):
    next_val = read_data[pos[1]][pos[0]] #y,x
    if next_val == "#":
        #obstacle
        return True        

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
        case 'up':
            pos[1] -= 1
        case 'down':
            pos[1] += 1
        case 'left':
            pos[0] -= 1
        case 'right':
            pos[0] += 1    
    
    #check boundary?
    # out_of_bound = y < 0 or x < 0
    in_bounds = pos[1] >= 0 and pos[0] >= 0
    return in_bounds

def flip_dir(dir):
    match dir[0]:
        case 'up':
            return 'down'
        case 'down':
            return 'up'
        case 'right':
            return 'left'
        case 'left':
            return 'right'


def try_turn(pos, dir):
    #could have to try this up to 3 times for a 180 degree turn
    pos2 = [pos[0],pos[1]]
    dir2 = [dir[0]]
    # for i in range(1,2):
    match dir2[0]:
        case "up":
            dir2[0] = "right"
        case "down":
            dir2[0] = "left"
        case "left":
            dir2[0] = "up"
        case "right":
            dir2[0] = "down" 
    
    for i in range(1,3):
        if can_move_forward(pos2, dir2[0]): #does not modify params
            # pos = pos2
            dir[0] = dir2[0]
            return True
        try_turn(pos,dir2)

    # #flip left/right or up/down
    # dir2[0] = flip_dir(dir2)
    # if can_move_forward(pos2, dir2[0]):
    #     # pos = pos2
    #     dir[0] = dir2[0]
    #     return True

    return False #probably shouldn't happen...

def try_move_next(pos, dir):
    if not move_next(pos, dir):
        return False

    return check_bounds(pos)
    
    


total = 0
# direction = "up" #starting
direction = ["up"] #starting
onpath = True
x = starting_pos[0]
y = starting_pos[1]
pos = [x,y]
val = read_data[y][x]
pathed = [(x,y)]
# pathed = [[starting_pos[0]],[starting_pos[1]]]
#try to move in current direction
# print("start")
# print(pos)
total = 1
while onpath:
    # print(pos)
    # val = read_data[pos[1]][pos[0]]
    # if pos[1] >=62 and pos[1] <= 65 and pos[0] < 10:
    onpath = try_move_next(pos, direction)
    # print("position ("+str(pos[0])+", "+str(pos[1])+") direction: "+direction[0]+" char: "+read_data[pos[1]][pos[0]])
    if (pos[0],pos[1]) not in pathed:
        total += 1
        pathed.append((pos[0],pos[1]))
        # print("position added ("+str(pos[0])+", "+str(pos[1])+") direction: "+direction[0])
    # print(pathed)
    
    #sanity check that we cannot pass the starting position in the same direction again
    if pos[0] == starting_pos[0] and pos[1] == starting_pos[1] and direction[0] == "up":
        break
        # Exception("passed same starting position in same direction")

    # onpath = try_move_next(pos, direction)
    # if onpath:
    #     onpath = False

total = len(pathed)

print("Total: "+str(total)) #4432 too low
#4433 is right!