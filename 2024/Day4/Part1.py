#AdventOfCode 2024 Day 4 Part 1!

with open('Day4/input.txt', mode="r", encoding="utf-8") as f:
    read_data = f.read().splitlines() #->list[]

grid = []

#build coordinates
for y in range(len(read_data)):    
    for x in range(len(read_data[y])):
        grid.append([x,y])

#need to count occurences of "XMAS", forward, backward, vertical, diagonal
#make sure to check each direction from every "X" so we don't miss overlaps
#look for every "X" coordinate as starting point?
total = 0
for coord in grid:
    # print(coord)
    x = coord[0]
    y = coord[1]

    # y_val = read_data[y]
    val = read_data[y][x]
    if val == "X":
        # print("x: "+str(x)+", y: "+str(y)+", val: "+val)
        #check for every possible M around it, starting from the line above if possible
        #check y-1 first for x-1, x, x+1
        #   then for y check x-1 and x+1
        #       then for y+1 check x-1, x, x+1

        #get starting point for search
        #get y indexes to check 
        y_idx_range = [y]
        if y-1 >= 0:
            y_idx_range.append(y-1)
        if y+1 <= len(read_data)-1:
            y_idx_range.append(y+1)
        y_idx_range.sort()
        
        x_idx_range = [x]
        if x-1 >= 0:
            x_idx_range.append(x-1)
        if x+1 <= len(read_data[y])-1:
            x_idx_range.append(x+1)
        x_idx_range.sort()

        for iy in y_idx_range:
            dy = iy-y
            ydir = ""
            if dy==-1:
                ydir = "down"
            elif dy==1:
                ydir = "up"
            #2-1, 2-2, 2-3 == 1, 0, -1
            #1==down, 0==left or right, -1==up
            for ix in x_idx_range:
                dx = ix-x
                xdir = ""
                if dx==1:
                    xdir = "right"
                elif dx==-1:
                    xdir = "left"
                #1-2, 2-2, 3-2 == -1, 0, 1
                #-1==left, 0==up or down, 1==right
                mval = read_data[iy][ix]
                if mval=="M":
                    #continue searching further this direction for "A" and "S"
                    #determine direction? 
                    ay = iy
                    if ydir == "up":
                        ay += 1
                    elif ydir == "down":
                        ay -= 1
                    if ay < 0 or ay > len(read_data)-1:
                        continue

                    ax = ix
                    if xdir == "left":
                        ax -= 1
                    elif xdir == "right":
                        ax += 1  
                    if ax < 0 or ax > len(read_data[ay])-1:
                        continue
                    
                    aval = read_data[ay][ax]
                    if aval=="A":
                        if ydir == "up":
                            ay += 1
                        elif ydir == "down":
                            ay -= 1
                        if ay < 0 or ay > len(read_data)-1:
                            continue
                            
                        if xdir == "left":
                            ax -= 1
                        elif xdir == "right":
                            ax += 1
                        if ax < 0 or ax > len(read_data[ay])-1:
                            continue

                        aval = read_data[ay][ax]
                        if aval == "S":
                            total += 1
                            # print("added total: x: "+str(x)+", y: "+str(y)+", val: "+val+", xdir: "+xdir+", ydir: "+ydir+", ax: "+str(ax)+", ay: "+str(ay)+", aval: "+aval)

                            


        #example:
        #for an X val at 2,2 we want to check all of these xy coords for M
        #1,1 2,1 3,1    dlu du  dru
        #1,2     3,2    dl      dr
        #1,3 2,3 3,3    dld dd  drd


print('Part1 total: '+str(total)) #2644 is right!
