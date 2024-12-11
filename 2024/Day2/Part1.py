#AdventOfCode 2024 Day 2 Part 1!

with open('Day2/input.txt', mode="r", encoding="utf-8") as f:
    read_data = f.read().splitlines()

total = 0
#how many reports are safe because they are all increasing or all decreasing
for line in read_data:
    line_parts = line.split()

    count_inc = 0
    count_dec = 0
    prev_val = ""
    for part in line_parts:
        if prev_val == "":
            prev_val = part
            continue

        
        if count_dec != 0 and count_inc != 0:
            break
        
        if (int(prev_val) < int(part)) and (int(part) - int(prev_val) <= 3):
            count_inc += 1
        elif int(prev_val) > int(part) and (int(prev_val) - int(part) <= 3):
            count_dec += 1
        else: #reset
            break
        
        if (count_inc == len(line_parts)-1) or (count_dec == len(line_parts)-1):
            total += 1
        
        prev_val = part

print(str(total)) # 516 is right!