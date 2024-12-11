#AdventOfCode 2024 Day 11 Part 1!

from datetime import datetime
from collections import deque
start_time = datetime.now()
running_total = start_time

print('begin')

with open('Day11/input.txt', mode="r", encoding="utf-8") as f:
    read_data = f.read().strip().split(' ') #->str
    # stones_list = [int(x) for x in read_data] #->list
    stones_list = [x for x in read_data] #->list

print(stones_list)
queue = deque()
for stone in stones_list:
    queue.append(stone)

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


#structures:
# original stones list to maintain order?
# original stones dict? (sequence_num, original stone)
# original stones dict? (sequence_num, original stone)
# loop for number of blinks (25)
    # new queue = function(queue)
        # use a FIFO queue
        #   popleft each number, apply logic, add to new FIFO queue 
        # build 
from functools import cache
@cache
def build_next_queue(queue_string):
    queue = deque(queue_string.split(' '))
    new_queue = deque()

    #popleft until done
    while queue:
        value = queue.popleft()
        
        if value=='0':
            new_queue.append('1')
        elif len(value)%2==0: #even, split into two, remove ALL leading 0's
            midpoint = int(len(value)/2)
            left_half = str(int(value[0:midpoint]))
            #remove 0's from left... convert to int and back to string?
            new_queue.append(left_half) #left half
            right_half = str(int(value[(midpoint*-1):]))

            new_queue.append(right_half) #right half
        else:
            new_queue.append(str(int(value)*2024))

    return new_queue

running_total = datetime.now()
print(f'begin processing: {running_total-start_time}')

blinks = 25
for b in range(0,blinks):
    queue_string = queue.popleft()
    while queue:
        queue_string+=(f' {queue.popleft()}')
    queue = build_next_queue(queue_string)

results = []
while queue:
    results.append(queue.popleft())



running_total = datetime.now()
print(f'begin totaling: {running_total-start_time}')
# print(results)
total = len(results)
running_total = datetime.now()
print(f"Part 1 total: {total}, duration: {running_total - start_time}")
#196614 too high
#188902 is right! 2 seconds....
