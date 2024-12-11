#AdventOfCode 2024 Day 7 Part 2!

with open('Day7/input.txt', mode="r", encoding="utf-8") as f:
    read_data = f.read().splitlines() #->list[]
# print(read_data)

def try_next_nums(answer, current, next_nums):
    # for j in range(0,len(next_nums)):
        #try applying a + or * operator
        #if tried operation, break
        #apply operation
    # operators = ['+','*']
    next_num = int(next_nums[0])
    # prev_total = current

    added = current + next_num
    multiplied = current * next_num
    concatenated = int(str(current)+str(next_num))

    #try additions
    total_found = 0
    if added==answer and len(next_nums)==1: #found success on the last test value... return it back
        return answer    
    elif added <= answer and len(next_nums)>1:
        total_found=try_next_nums(answer, added, next_nums[1:])
        if total_found is not None and total_found!=0:
            return total_found
    #try multiplications
    if multiplied==answer and len(next_nums)==1: #found success on the last test value... return it back
        return answer
    elif multiplied <= answer and len(next_nums)>1:
        total_found=try_next_nums(answer, multiplied, next_nums[1:])
        if total_found is not None and total_found!=0:
            return total_found
    #try concatenated
    if concatenated==answer and len(next_nums)==1: #found success on the last test value... return it back
        return answer
    elif concatenated <= answer and len(next_nums)>1:
        total_found=try_next_nums(answer, concatenated, next_nums[1:])
        if total_found is not None and total_found!=0:
            return total_found

#for starting num 
#try next operation on next number until we run out of numbers
#   if < answer: keep going
#   if end of list: break
#   else: break
#check if answer = calculated answer


answers = []
for i in range(0,len(read_data)):
    line_split = read_data[i].split(':')
    answer = int(line_split[0])
    test_values = line_split[1].strip().split(' ')
    starting_num = int(test_values[0])
    current = starting_num
    next_values = test_values[1:]
    result = try_next_nums(answer, starting_num, next_values)
    if result == answer:
        answers.append(result)

print("Part 2 total: "+str(sum(answers))) #59002246504791 is right!

#attempt 2 = 6082467277734 too low
#it was the darn list ending with just a 1!
#attempt 3 = 6083020304036