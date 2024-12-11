#AdventOfCode 2024 Day 3 Part 1!

with open('Day3/input.txt', mode="r", encoding="utf-8") as f:
    read_data = f.read() #->string

import re
pattern1 = re.compile(r'(mul\(\d+,\d+\))')
pattern2 = re.compile(r'(\d+)')

matches = list(re.finditer(pattern1, read_data))
total = 0
for i in range(len(matches)):
    #mul(num,num), e.g. mul(3,4)
    num_matches = list(re.finditer(pattern2, matches[i].group()))
    num1 = num_matches[0].group()
    num2 = num_matches[1].group()
    prod = int(num1) * int(num2)
    total += prod

print('Part1 total: '+str(total)) #183788984 is right!