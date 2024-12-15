#AdventOfCode 2024 Day 13 Part 1!

from datetime import datetime
from collections import defaultdict
from collections import deque
start_time = datetime.now()
running_total = start_time

print('begin')

path = '2024/Day13/example.txt'
# path = '2024/Day13/input.txt'
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

    claw_machines.append(((ButtonA),(ButtonB),(Prize),0))

print(claw_machines)

running_total = datetime.now()
print(f'begin processing: {running_total-start_time}')

def button_press(x,y,x_inc,y_inc):
    return (x+x_inc,y+y_inc)

total = 0
for i in range(len(claw_machines)):
    AX, AY = claw_machines[i][0]
    BX, BY = claw_machines[i][1]
    PX, PY = claw_machines[i][2]
    fewest_turns=0
    #build list of multiples of AX and AY that are less than PX and PY?

    #what would be the best brute force way...
    # start with just A and recurse until either X or Y exceeds the prize?
    #   then press B once and repeat?
    # maybe start from the prize value and do this in reverse..? 
    #   could iterate PX-(PX/AX) times?
    X_value = 0
    Y_value = 0
    list_turns = []
    A_presses = 0
    B_presses = 0
    while X_value<PX and Y_value<PY:
        A_presses += 1
        X_value, Y_value = button_press(X_value,Y_value,AX,AY) #A
        if X_value==PX and Y_value==PY:
            list_turns.append((A_presses, B_presses))
            continue #success
        X_value_B = X_value
        Y_value_B = Y_value
        while X_value_B<PX and Y_value_B<PY:
            B_presses += 1
            X_value_B, Y_value_B = button_press(X_value_B,Y_value_B,BX,BY) #B
            if X_value_B==PX and Y_value_B==PY:
                list_turns.append((A_presses, B_presses))
                continue #success
            if X_value_B>PX or Y_value_B>PY:
                #reset B presses
                B_presses = 0
    X_value = 0
    Y_value = 0
    B_presses = 0
    A_presses = 0
    while X_value<PX and Y_value<PY:
        B_presses += 1
        X_value, Y_value = button_press(X_value,Y_value,BX,BY) #B
        if X_value==PX and Y_value==PY:
            list_turns.append((A_presses, B_presses))
            continue #success
        X_value_B = X_value
        Y_value_B = Y_value
        while X_value_B<PX and Y_value_B<PY:
            A_presses += 1
            X_value_B, Y_value_B = button_press(X_value_B,Y_value_B,AX,AY) #A
            if X_value_B==PX and Y_value_B==PY:
                list_turns.append((A_presses, B_presses))
                continue #success
            if X_value_B>PX or Y_value_B>PY:
                #reset B presses
                A_presses = 0

    # fewest_turns = list_turns[0][0]+list_turns[0][1]
    # tokens = list_turns[0][0]*3+list_turns[0][1]
    tokens = 0
    for A, B in list_turns:
        if tokens==0:
            tokens=A*3+B
            continue
        if A*3+B < tokens:
            tokens = A*3+B
    total += tokens  
    claw_machines[i]=(claw_machines[i][0],claw_machines[i][1],claw_machines[i][2],tokens)




running_total = datetime.now()
print(f'begin totaling: {running_total-start_time}')


# print(results)
running_total = datetime.now()
print(f"Part 1 total: {total}, duration: {running_total - start_time}")
#50215 too high!