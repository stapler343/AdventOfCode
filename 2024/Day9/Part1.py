#AdventOfCode 2024 Day 9 Part 1!

from datetime import datetime
start_time = datetime.now()

with open('Day9/input.txt', mode="r", encoding="utf-8") as f:
    read_data = f.read().strip() #->str
    # grid = read_data.strip().splitlines() #->list

#things to track
#disk map [id,block_count,free_space]
    #ID number (just a sequence number of files before re-arranging)
    #file blocks (every other num, starting with the 1st)
    #free space (every other num, starting with the 2nd)
#process
    #start from rightmost ID, try moving to leftmost freespace
    #requirements:
        # loop input from left to build:
        #   ID (seq)
        #   block_count
        #   free_space
        # loop from right IDs trying to fill available freespace from the left with blocks
        #   
#return sum of checksums
    #seq(left to right) * (ID_current)
    #e.g. 0099811188827773336446555566
    # 0 * 0 = 0, 1 * 0 = 0, 2 * 9 = 18, 3 * 9 = 27, 4 * 8 = 32, and so on
    # ==1928

master_id_list = []
master_freespace_list = [] #(id,free)
master_dict = dict()
master_dict_orig = dict()

char_count = len(read_data)
id = 0
block_count = 0
free_space = 0
for i in range(0,char_count,2):
    master_id_list.append(id)
    block_count = int(read_data[i])
    free_space = 0
    if i+1<=char_count-1:
        free_space = int(read_data[i+1])
    
    master_dict[id] = (block_count,free_space)
    master_dict_orig[id] = (block_count,free_space)

    id += 1

# print(master_id_list)
# print(master_dict)
#build new list of ID numbers

#loop ID dictionary left to right, in order!
ordered_blocks = []
for id in master_id_list:
    bc, fs = master_dict[id] #block count and free space
    for b in range(0,bc):
        ordered_blocks.append(id)
    
    #loop IDs from right to left
    exit = False
    while fs>0 and not exit:
        #for each free space available in left, try adding one block from right to left
        for right_id in range(len(master_id_list)-1,0,-1):
            if id == master_id_list[right_id]:
                exit = True
                break #exit because we reached the midpoint?
            rbc, rfs = master_dict[master_id_list[right_id]]
            while rbc>0 and fs>0:
                rbc-=1
                fs -= 1
                master_dict[master_id_list[right_id]] = (rbc, rfs+1)
                ordered_blocks.append(right_id)

            if fs == 0:
                break
    master_dict[id] = (bc,fs)

total = 0
for i in range(0,len(ordered_blocks)):
    total += int(ordered_blocks[i])*i

print(f"Part 1 total: {total}, duration: {datetime.now() - start_time}")