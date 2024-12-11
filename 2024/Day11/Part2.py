#AdventOfCode 2024 Day 11 Part 2!
#had performance issues for 75 blinks from part 1 solution......

from datetime import datetime
from collections import defaultdict
start_time = datetime.now()
running_total = start_time

print('begin')

with open('Day11/input.txt', mode="r", encoding="utf-8") as f:
    read_data = f.read().strip().split(' ') #->str
    # stones_list = [int(x) for x in read_data] #->list
    stones_list = [x for x in read_data] #->list

print(stones_list)
#trick is tracking order doesn't matter!
stones_dict = defaultdict(int)
for stone in stones_list:
    stones_dict[int(stone)] += 1

running_total = datetime.now()
print(f'file read and data structures prepared in {running_total-start_time}')

#things to track
#stones
    # arranged in straight line
    # engraved number
    # stones change when you blink?
        # could be the engraved num, or the stone could be split in two?!
            # splitting in two shifts other stones
        # ALL stones change simultaneously
            # rules (only apply 1st):
                #1 engraved 0, replaced with 1
                #2 even number, replaced by 2 stones
                    # left half of digits in 1, right half in 2
                        #(do not keep leading or trailing 0's)
                #3 multiply engraving by 2024
        # preserve original order of straight line
#example: 0 1 10 99 999
    # 5 stones
    # after 1 blink, there are 7 stones
#example2: 1 2024 1 0 9 9 2021976
    # 7 stones
    # after 6 blinks there are 22 stones
    # after 25, 55312 stones
#answer: number of stones after 25 blinks!
#beware: number can get HUGE

def step_forward(stone_string):
    if stone_string=='0':
        return (int(1),)
    elif len(stone_string)%2==0: #even, split into two, remove ALL leading 0's
        midpoint = int(len(stone_string)/2)
        left_half = int(stone_string[0:midpoint])
        right_half = int(stone_string[(midpoint*-1):])
        return (left_half, right_half)
    else:
        return (int(int(stone_string)*2024), )

running_total = datetime.now()
print(f'begin processing: {running_total-start_time}')


#build a new dict each iteration with only the new stone numbers produced from the previous dict after applying new rules for splitting
#includes a running total of how many new stones spawned from the original stone this cycle
#   e.g. 22, 1 stone 
#       -> 2, 1 stone and 2, 1 stone == 2, 2 stones (doubled number of stones)
#       -> 2*2024 == 4048, 2 stones (no change in number of stones)
#       -> split into 40 and 48 with 2 stones each (doubled stones to 4)
#       -> split into 4 (twice), 0 (once), and 48 (once), with 2 stones each (doubled stoned to 8)
#       -> 4*2024==8096, 1==1, 48 is split into 4 and 8 each with 2 stones (added 2 stones) 
#       -> each of those are single digits and would not create new stones, but be multiplied by 2024 or switched to 1... etc 
#e.g. if we are on iteration 5 and we had seen the number 2 four times in prior iterations, 
#   the number 22 would be split into 2,2 and we add the number of times 22 was seen to new dict 2 (twice), so new dict[2]==8
def calc_next_stones(current_stones):
    prev_stones = current_stones.copy()
    current_stones.clear()
    for stone in prev_stones:
        for next_val in step_forward(str(stone)): #one or two stones, each gets added tracked with its previous stone count
            current_stones[next_val]+=prev_stones[stone]

blinks = 75
for b in range(blinks):
    calc_next_stones(stones_dict)


running_total = datetime.now()
print(f'begin totaling: {running_total-start_time}')
total = 0
for val in stones_dict:
    total += stones_dict[val]
# print(results)
running_total = datetime.now()
print(f"Part 2 total: {total}, duration: {running_total - start_time}")
#223894720281135 is right!
