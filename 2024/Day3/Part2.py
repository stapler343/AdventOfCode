#AdventOfCode 2024 Day 3 Part 2!

with open('Day3/input.txt', mode="r", encoding="utf-8") as f:
    read_data = f.read() #->string

import re
pattern1 = re.compile(r'(mul\(\d+,\d+\)|do\(\)|don\'t\(\))')
pattern2 = re.compile(r'(\d+)')

matches = list(re.finditer(pattern1, read_data))
blnDo = True
total = 0
for i in range(len(matches)):
    if matches[i].group() == "do()":
        blnDo = True
        continue
    elif matches[i].group() == "don't()":
        blnDo = False
        continue
    if not blnDo:
        continue

    num_matches = list(re.finditer(pattern2, matches[i].group()))
    num1 = num_matches[0].group()
    num2 = num_matches[1].group()
    prod = int(num1) * int(num2)
    total += prod

print('Part2 total: '+str(total)) #62098619 is right!