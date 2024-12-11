#AdventOfCode 2024 Day 5 Part 1!

with open('Day5/input.txt', mode="r", encoding="utf-8") as f:
    read_data = f.read().split("\n\n") #->list[]

page_order_rules = read_data[0].splitlines()
pages = read_data[1].splitlines()

# print(page_order_rules)
order_rules = []
#build coordinates
for y in range(len(page_order_rules)): 
    order_rule = page_order_rules[y].split("|") 
    order_rules.append([order_rule[0],order_rule[1]])
order_rules.sort()

def get_applicable_rules(page_number):
    return [item for item in order_rules if (item[0]==page_number)]
# print(get_applicable_rules('75'))
#current_pages = [75,47,61,53,29]
#applicable rules = 
#75,47
#75,61
#75,53
#75,29
#47,61
#47,53
#47,29
#61,53
#61,29
#29?
def check_page(current_pages):
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

total = 0
for i in range(0,len(pages)):
    #page index
    current_pages = pages[i].split(",")
    # print("current_pages: "+str(current_pages))
    if check_page(current_pages):
        total += int(current_pages[int(len(current_pages) / 2)])

print("Total: "+str(total)) #5208 is right!