import sys

large_db = [
    {'a', 'c', 'd', 'f', 'g', 'i', 'm', 'p'},
    {'a', 'b', 'c', 'f', 'l', 'm', 'o'},
    {'b', 'f', 'h', 'j', 'o', 'w'},
    {'b', 'c', 'k', 's', 'p'},
    {'a', 'f', 'c', 'e', 'l', 'p', 'm', 'n'}
]

minsup = 0.60
filepath = None
candidate = []
leves = []
db_len = 0

# scan db once
# generate level table for singletons
# use minsup to remove all unnecessary singletons
# sort singletons from high to low (header table)
# build tree based on sorted, pruned singletons
# as tree is being built, increment count of node for each transaction present
# store pointers from items in header table to respective nodes (candidateay of pointers?)

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

def swap(first, second)
    global candidate
    global level
    c_temp = candidate[first]
    l_temp = level[first]
    candidate[first] = candidate[second]
    level[first] = level[second]
    candidate[second] = c_temp
    level[second] = l_temp

# candidate = [10, 80, 30, 90, 40, 50, 70]
# level = [1, 8, 3, 9, 4, 5, 7]
# db_len = 4
# print(candidate)
# print(level)
# print()
# two_quickSort(0, len(candidate) - 1, False)
# print(candidate)
# print(level)
# print()
# prune()
# print(candidate)
# print(level)
# print()