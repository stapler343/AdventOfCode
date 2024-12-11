#AdventOfCode 2024 Day 5 Part 2!

with open('Day5/input.txt', mode="r", encoding="utf-8") as f:
    read_data = f.read().split("\n\n") #->list[]

page_order_rules = read_data[0].splitlines()
pages = read_data[1].splitlines()

order_rules = []
#build coordinates
for y in range(len(page_order_rules)): 
    order_rule = page_order_rules[y].split("|") 
    order_rules.append([order_rule[0],order_rule[1]])
order_rules.sort()

def get_applicable_rules(page_number):
    return [item for item in order_rules if (item[0]==page_number)]

def check_page(current_pages):
    if current_pages is None:
        return False
    for pn in range(0,len(current_pages)):
        #page numbers index
        current_page = current_pages[pn]
        applicable_rules = get_applicable_rules(current_page)
        # print(applicable_rules)
        # print("current_page: "+str(current_page))
        for next_page in current_pages[pn+1:]:
            #check the rule for current_page and next_page
            if not ([current_page, next_page] in applicable_rules):
                return False

    return True

def is_possible_starting_node(num, other_pages):
    applicable_rules = get_applicable_rules(num)
    for other_page in other_pages:
        #check the rule for current_page and next_page
        if not ([num, other_page] in applicable_rules):
            return False
    return True

def get_starting_nodes(current_pages):
    possible_starting_nodes = []
    for i_num in range(0,len(current_pages)):
        #check if every subsequent num has a rule
        #there should be a num with a rule for every other number, and that should be ther starting node
        #perhaps there could be two possible starting nodes?
        other_nums = current_pages[:i_num] + current_pages[i_num+1:]
        if is_possible_starting_node(current_pages[i_num], other_nums):
            # print('possible starting node: '+ current_pages[i_num])
            possible_starting_nodes.append(current_pages[i_num])
            # print(possible_starting_nodes)
        # print(other_nums)
    return possible_starting_nodes

def check_next_nodes(remaining_pages, current_node_list, page_length):
    # print(current_node_list)
    starting_nodes = get_starting_nodes(remaining_pages)
    #starting_nodes=29
    #remaining_pages=13,29
    for p in range(0,len(starting_nodes)):
        current_node_list.append(starting_nodes[p])
        other_nodes = [page for page in remaining_pages if (page not in current_node_list)]
        # print(other_nodes)
        if len(other_nodes)==1:
            #starting from [29], only [13] is remaining 
            # print(current_node_list)
            current_node_list.append(other_nodes[0])
        if len(current_node_list)==page_length:
            return
        check_next_nodes(other_nodes, current_node_list, page_length)

fixed_pages = []
total = 0
incorrect_pages = [page for page in pages if (not check_page(page.split(",")))]
for i in range(0,len(incorrect_pages)):
    current_pages = incorrect_pages[i].split(",")
    # print("pages_to_sort")
    # print(current_pages)
    # pages_reversed = current_pages.reverse()
    #e.g. 61,13,29 becomes 61,29,13

    starting_nodes = get_starting_nodes(current_pages)
    #starting_nodes=61
    #current_pages=61,13,29
    blnSorted = False
    for p in range(0,len(starting_nodes)):
        if blnSorted:
            break
        page_length = len(current_pages)
        current_node_list = [starting_nodes[p]]

        #get all other nodes
        other_nodes = [page for page in current_pages if (page not in current_node_list)]
        # print("build_sorted_list")
        check_next_nodes(other_nodes, current_node_list, page_length)
        if check_page(current_node_list):
            blnSorted = True
            # print("final_sorted_list")
            # print(current_node_list)
            # print()
            total += int(current_node_list[int(page_length / 2)])
        
print("Total: "+str(total)) #6732 is right!