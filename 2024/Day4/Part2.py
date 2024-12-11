#AdventOfCode 2024 Day 4 Part 2!

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
def search_cross_val(read_data, corner_y_idx, corner_x_idx, corners, search_val):
    for corner in corners:
        cx = corner[0]
        cy = corner[1]
        cval = read_data[cy][cx]
        # search_val = "M"
        if cval == search_val:
                #try both adjacent corners
                #looking for exactly 1 match
            adj_corners = []
            for idx_y in corner_y_idx:
                for idx_x in corner_x_idx:
                    if idx_x==cx and idx_y==cy:
                        continue
                    if abs(idx_x-cx)==2 and abs(idx_y-cy)==2:
                        continue
                    adj_corners.append([idx_x,idx_y])
            # for ac in adj_corners:
            acx = adj_corners[0][0]
            acy = adj_corners[0][1]
            acx2 = adj_corners[1][0]
            acy2 = adj_corners[1][1]
            adjacent_corner_val1 = read_data[acy][acx]
            adjacent_corner_val2 = read_data[acy2][acx2]
            if adjacent_corner_val1==search_val or adjacent_corner_val2==search_val:
                if not (adjacent_corner_val1==search_val and adjacent_corner_val2==search_val):
                    return True

for coord in grid:
    # print(coord)
    x = coord[0]
    y = coord[1]

    # y_val = read_data[y]
    val = read_data[y][x]
    if val == "A":
        #for every "A", check the corner coordinates to find 2 M's and 2 S's in line with each other
        corner_y_idx = []
        if y > 0 and y < len(read_data)-1:
            corner_y_idx.append(y-1)
            corner_y_idx.append(y+1)
        corner_y_idx.sort()
        
        corner_x_idx = []
        if x > 0 and x < len(read_data[y])-1:
            corner_x_idx.append(x-1)
            corner_x_idx.append(x+1)
        corner_x_idx.sort()

        if not(len(corner_y_idx)==2 and len(corner_x_idx)==2):
            continue

        #search for 2 side by side M's at those coords
        #search for 2 side by side S's at those coords
        corners = []
        for idx_y in corner_y_idx:
            for idx_x in corner_x_idx:
                corners.append([idx_x,idx_y])
        # print("corners: ")
        # print(corners)
        blnM = search_cross_val(read_data, corner_y_idx, corner_x_idx, corners, "M")
        blnS = search_cross_val(read_data, corner_y_idx, corner_x_idx, corners, "S")

        if blnM and blnS:
            total += 1

print('Part2 total: '+str(total)) #1952 is right!
