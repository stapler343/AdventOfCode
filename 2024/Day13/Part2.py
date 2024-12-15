#AdventOfCode 2024 Day 13 Part 2!
# the same thing but the prizes are 10 trillion higher....

from datetime import datetime
from sympy import symbols, Eq, solve 

start_time = datetime.now()
running_total = start_time

print('begin')

# path = '2024/Day13/example.txt'
path = '2024/Day13/input.txt'
with open(path, mode="r", encoding="utf-8") as f:
    read_data = f.read().strip() #->str
    machines = read_data.strip().split('\n\n') #->list

# claw machine...
# A and B button (i.e. X and Y)
# Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400

# Button A: X+26, Y+66
# Button B: X+67, Y+21
# Prize: X=12748, Y=12176

# Button A: X+17, Y+86
# Button B: X+84, Y+37
# Prize: X=7870, Y=6450

# Button A: X+69, Y+23
# Button B: X+27, Y+71
# Prize: X=18641, Y=10279

#A costs 3, B costs 1

#struct...
def parse_XY(line):
    X = line[line.index('X')+2:line.index(',')]
    Y = line[line.index('Y')+2:]
    return (int(X),int(Y))


claw_machines = [] # (A button, B button, prize location)
for machine in machines:
    lines = machine.split('\n')
    ButtonA_raw = lines[0]
    ButtonB_raw = lines[1]
    Prize_raw = lines[2]

    # ButtonA_comma_split = ButtonA_raw.split(',')
    # ButtonB_comma_split = ButtonB_raw.split(',')
    # Prize_comma_split = Prize_raw.split(',')

    ButtonA = parse_XY(ButtonA_raw)
    ButtonB = parse_XY(ButtonB_raw)
    Prize = parse_XY(Prize_raw)
    Prize = (Prize[0]+10000000000000,Prize[1]+10000000000000)

    claw_machines.append(((ButtonA),(ButtonB),(Prize),0))

print(claw_machines)

running_total = datetime.now()
print(f'begin processing: {running_total-start_time}')

def button_press(x,y,x_inc,y_inc):
    return (x+x_inc,y+y_inc)

total = 0
for i in range(len(claw_machines)):
    ax, ay = claw_machines[i][0]
    bx, by = claw_machines[i][1]
    px, py = claw_machines[i][2]
    fewest_turns=0

    # too high to brute force
    # reddit suggests linear algebra or just solving a system of 2 equations 

    # solve for a and b
    b = (ax * py - ay * px) / (ax * by - ay * bx)
    a = (px - bx * b) / ax

    # Check if a and b are integers
    tokens = 0    
    if a.is_integer() and b.is_integer():
        tokens = int(a * 3 + b)
    
    total += tokens  
    claw_machines[i]=(claw_machines[i][0],claw_machines[i][1],claw_machines[i][2],tokens)

running_total = datetime.now()
print(f'begin totaling: {running_total-start_time}')


# print(results)
running_total = datetime.now()
print(f"Part 1 total: {total}, duration: {running_total - start_time}")
#83232379451012 is right!