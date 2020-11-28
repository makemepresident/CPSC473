import sys

class Node:

    def __init__(self, value: int) -> None:
        self.value = value
        self.children = []

large_db = [
    '1  3   4',
    '2  3   5',
    '1  2   3   5',
    '2  5'
]

minsup = 0.60
filepath = None
candidate = []
level = []
pointers = []
db_len = 0

# scan db once
# generate level table for singletons
# use minsup to remove all unnecessary singletons
# sort singletons from high to low (header table)
# build tree based on sorted, pruned singletons
# as tree is being built, increment count of node for each transaction present
# store pointers from items in header table to respective nodes (candidateay of pointers?)

def fp_growth():
    gen_level_table() # generate candidate with levels
    two_quickSort(0, len(candidate) - 1, True) # sorts candidates
    prune() # uses minsup to prune
    

def init_candidate():
    global db_len
    global filepath
    try:
        db = open(filepath)
    except:
        print("Problem finding filepath, try again - ensure the format \"____.txt\"")
        sys.exit()
    unique = []
    for index, value in enumerate(db):
        if index == 0:
            value = value[:-1]
            db_len = int(value)
            continue
        elements = parseEle(value)
        for i in elements:
            if {i} not in unique and i != '':
                unique.append({i})
    return unique

def parseEle(string):
    parsed = string.split('\t')
    elements = parsed[2].split(' ')
    parsed = None
    elements[len(elements) - 1] = elements[len(elements) - 1][:-1]
    return elements

def gen_level_table():
    init_candidate()
    global level
    global filepath
    level = [0] * len(candidate)
    db = open(filepath)
    for index, value in enumerate(db):
        if index == 0:
            continue
        elements = set(parseEle(value))
        for index2, item in enumerate(candidate):
            flag = True
            for val in item:
                if val in elements:
                    continue
                else:
                    flag = False
                    break
            if flag:
                level[index2] += 1

def prune():
    global candidate
    global level
    global db_len
    for index, value in enumerate(level):
        if value < minsup * db_len:
            temp_candidate = candidate[:index - 1]
            temp_level = level[:index - 1]
            candidate = temp_candidate
            level = temp_level

def two_quickSort(low, high, low_high=True):
    if low < high:
        pi = partition(low, high, low_high)
        two_quickSort(low, pi - 1, low_high)
        two_quickSort(pi + 1, high, low_high)

#use [2, 5, 6, 9, 8]
def partition(low, high, low_high):
    pivot = candidate[high] # last element
    se = low - 1 # -1
    for index in range(low, high):
        if low_high:
            if candidate[index] < pivot:
                se += 1
                swap(se, index)
        else:
            if candidate[index] > pivot:
                se += 1
                swap(se, index)
    swap(se + 1, high)
    return se + 1

def swap(first, second):
    global candidate
    global level
    c_temp = candidate[first]
    l_temp = level[first]
    candidate[first] = candidate[second]
    level[first] = level[second]
    candidate[second] = c_temp
    level[second] = l_temp

def gen_tree():
    # look at each transaction in database
    # for each transaction, iterate through candidate IN ORDER
    # if candidate in transaction, add child to root node
    # change current node to NODE JUST ADDED
    # repeat
    # for next transaction, go back to root node
    # for first candidate in transaction, check if child of current node
    # if so, change pointer to child node
    # if not, add to child of current node, change pointer to NODE JUST ADDED
    # repeat
    global filepath
    db = open(filepath)
    for index, value in enumerate(db):
        if index == 0:
            continue