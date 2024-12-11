#AdventOfCode 2024 Day 2 Part 2!

with open('Day2/input.txt', mode="r", encoding="utf-8") as f:
    read_data = f.read().splitlines() #->list[]

total = 0
#how many reports are safe because they are all increasing or all decreasing
#a single unsafe report is tolerable
for line in read_data:
    line_parts = line.split()

    current_row_idx = 0
    row_count = len(line_parts)
    blnFirstIter = True
    blnSuccess = False
    while current_row_idx < row_count + 1:
        #try part 1 solution for every row, but skipping 1 of the chars, until entire list is parsed or a success is found
        
        #build a list of indexes to check
        idx_list = []
        for i in range(len(line_parts)):
            if blnFirstIter:
                idx_list.append(i)
                blnFirstIter = False
            else:
                #skip rows one by one
                if i == current_row_idx - 1:
                    continue
                else:
                    idx_list.append(i)

        r = len(idx_list)
        count_inc = 0
        count_dec = 0
        prev_val = ""
        for i in idx_list:            
            if prev_val == "":
                prev_val = line_parts[i]
                continue
            
            if (int(prev_val) < int(line_parts[i])) and (int(line_parts[i]) - int(prev_val) <= 3):
                count_inc += 1
            elif int(prev_val) > int(line_parts[i]) and (int(prev_val) - int(line_parts[i]) <= 3):
                count_dec += 1
            else: #same val is unsafe
                break
            
            if count_dec != 0 and count_inc != 0:
                break
            
            if (count_inc == r-1) or (count_dec == r-1):
                total += 1
                blnSuccess = True
                break
            
            prev_val = line_parts[i]
        
        if blnSuccess:
            break
        current_row_idx += 1

print(str(total)) 
#566 too high!
#551? too low!
#561? yep!
