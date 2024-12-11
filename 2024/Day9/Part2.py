#AdventOfCode 2024 Day 9 Part 2!

from datetime import datetime
start_time = datetime.now()
running_total = start_time

print('begin')

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
    
    master_dict[id] = [block_count,free_space]
    master_dict_orig[id] = [block_count,free_space]

    id += 1

running_total = datetime.now()
print(f'file read and data structures prepared in {running_total-start_time}')


running_total = datetime.now()
print(f'begin processing: {running_total-start_time}')

moved_ids = dict()
moved_ids_list = []
for id in master_id_list:
    moved_ids[id] = []

reversed_ids = master_id_list.copy()
reversed_ids.reverse()
#try fitting each block from the right only once into any left spot that fits it
for rid in reversed_ids:
    # rbc, rfs = master_dict[rid] #block count and free space
    rbc = master_dict[rid][0] #block count and free space
    rfs = master_dict[rid][1] #block count and free space
    
    moved = False
    for lid in master_id_list:
        if rid<=lid:
            continue    
        # lbc, lfs = master_dict[lid] #block count and free space
        lbc = master_dict[lid][0] #block count and free space
        lfs = master_dict[lid][1] #block count and free space
        if lfs==0:
            continue
        if lfs>=rbc and rbc>0:
            lfs-=rbc
            moved_ids[lid].append([rid,rbc])
            moved_ids_list.append(rid)
            rbc-=lfs
            rfs+=lfs
            master_dict[lid][1] = lfs
            master_dict[rid][0] = rbc
            moved=True
        if moved:
            break


running_total = datetime.now()
print(f'begin organizing: {running_total-start_time}')

total = 0
ordered_blocks = []
for id in moved_ids:    
    lbc = master_dict[id][0]
    lfs = master_dict[id][1]
    lbc_orig = master_dict_orig[id][0]
    lfs_orig = master_dict_orig[id][1]
    
    if id not in moved_ids_list:
        for i in range(0,lbc):
            ordered_blocks.append(id)
    else:
        #append 0's to represent free spaces
        for i in range(0,lbc_orig):
            ordered_blocks.append(0)
    #append 0's to represent free spaces
    #now do the moved spaces

    for rid in moved_ids[id]:        
        for block in range(0,rid[1]):
            ordered_blocks.append(rid[0]) #id
    
    #now fill with free spaces if anything left
    for j in range(0,lfs):
        ordered_blocks.append(0)

running_total = datetime.now()
print(f'begin totaling: {running_total-start_time}')
for i in range(0,len(ordered_blocks)):
    total += int(ordered_blocks[i])*i

running_total = datetime.now()
print(f"Part 2 total: {total}, duration: {running_total - start_time}")
#6478232739671 is right!