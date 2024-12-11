#AdventOfCode 2024 Day 1 Part 1!

with open('Day1/input.txt', mode="r", encoding="utf-8") as f:
    read_data = f.read().splitlines()

listA = []
listB = []

for line in read_data:
    line_parts = line.split()
    listA.append(line_parts[0])
    listB.append(line_parts[1])

listA.sort()
listB.sort()

c = len(read_data)
total = 0
for i in range(len(read_data)):
    dif = int(listA[i]) - int(listB[i])
    if dif < 0:
        dif *= -1
    # print('Index '+str(i)+' Line input: '+read_data[i]+' listA '+listA[i]+' listB '+listB[i]+' dif '+str(dif))
    total += dif
print(str(total)) #2164381 is right!


