#AdventOfCode 2024 Day 14 Part 1!

from datetime import datetime

start_time = datetime.now()
running_total = start_time

print('begin')

path = '2024/Day14/example.txt'; tiles_width = 11; tiles_height = 7
# path = '2024/Day14/example2.txt'; tiles_width = 11; tiles_height = 7
path = '2024/Day14/input.txt'; tiles_width = 101; tiles_height = 103
with open(path, mode="r", encoding="utf-8") as f:
    read_data = f.read().strip().split('\n') #->list
    
#get list of robot's positions and velocities
# e.g.
# p=0,4 v=3,-3
# p=6,3 v=-1,-3

robots = []
for i in range(len(read_data)):
    line = read_data[i].split(' ')
    position_raw = line[0].split('=')
    position_nums_split = position_raw[1].split(',')
    posx = int(position_nums_split[0])
    posy = int(position_nums_split[1])

    velocity_raw = line[1].split('=')
    velocity_nums_split = velocity_raw[1].split(',')
    velx = int(velocity_nums_split[0])
    vely = int(velocity_nums_split[1])

    robots.append(((posx,posy),(velx,vely)))

#robots move once per second
#how what is each robots position after 100 seconds...?
#ans: count the number of robots in each quadrant
#   robots in the center row or column are excluded
#   multiply all 4 quadrant counts together for the answer

#tile space is 101 wide and 103 tall

quadrants = dict()
quadrants[1]=0
quadrants[2]=0
quadrants[3]=0
quadrants[4]=0

def check_x_bound(x,vx):
    new_x = x + vx
    w = tiles_width-1
    if new_x > w: #wrap right back to 0
        new_x = 0 + (new_x-1-w)
        # new_x = ((tiles_width-1-x)*-1)-1 #moving right... wrap back to start
    elif new_x < 0: #wrap left (0) back to right (w)
        new_x = w+1 + new_x
        # new_x = (tiles_width+x) #moving left... adding a negative... wrap around right
    if new_x < 0 or new_x > w:
        Exception('x too high')
    return new_x

def check_y_bound(y,vy):
    new_y = y + vy
    h = tiles_height-1
    if new_y > h:
        new_y = 0 + (new_y-1-h)
        # new_y = ((tiles_height-1-y)*-1)-1 #moving down... wrap back to top
    elif new_y < 0:
        new_y = h+1 + new_y
        # new_y = (tiles_height+y) #moving up... adding a negative... wrap around end
    if new_y < 0 or new_y > h:
        Exception('y too high')
    return new_y

#for each robot...
seconds = 100
for ri in range(len(robots)):
    #advance once per second...
    px, py = robots[ri][0]
    vx, vy = robots[ri][1]
    for sec in range(seconds):
        #if new x in bounds
        px = check_x_bound(px, vx)
        py = check_y_bound(py, vy)
    
    #determine quadrant of final pos
    middle_x = int(tiles_width/2)
    middle_y = int(tiles_height/2)
    if px < middle_x and py < middle_y: #q1
        quadrants[1]+=1
    elif px > middle_x and py < middle_y: #q2
        quadrants[2]+=1
    elif px < middle_x and py > middle_y: #q3
        quadrants[3]+=1
    elif px > middle_x and py > middle_y: #q4
        quadrants[4]+=1

running_total = datetime.now()
print(f'begin processing: {running_total-start_time}')

running_total = datetime.now()
print(f'begin totaling: {running_total-start_time}')
total = 1
for q in quadrants:
    total *= quadrants[q]

# print(results)
running_total = datetime.now()
print(f"Part 1 total: {total}, duration: {running_total - start_time}")
#222901875 right!
