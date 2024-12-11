#AdventOfCode 2024 Day 1 Part 2!

with open('Day1/input.txt', mode="r", encoding="utf-8") as f:
    read_data = f.read().splitlines()

listA = []
listB = []
dictA = dict()

for line in read_data:
    line_parts = line.split()
    listA.append(line_parts[0])
    listB.append(line_parts[1])
    
    if line_parts[1] in dictA:
        dictA[line_parts[1]] += 1
    else:
        dictA[line_parts[1]] = 1

total = 0
for i in range(len(read_data)):
    multiplier = 0
    if listA[i] in dictA:
        multiplier = dictA[listA[i]]
    
    similarity_score = int(listA[i]) * multiplier
    total += similarity_score

print(str(total)) #20719933 is right!
