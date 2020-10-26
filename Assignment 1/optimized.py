import sys
from itertools import product

db_len = 0
minsup = 0.01
level = []
candidate = []
level_union = []
dcl = []

# filen = 'data'
filen = '1k5L'
inputf = sys.path[0] + '\\' + filen + '.txt'

# Implemented from included wiki_algo screenshot
# https://en.wikipedia.org/wiki/Apriori_algorithm
def apriori():
    global minsup
    global candidate
    global level_union
    candidate = init_candidate() # Initial candidate table containing singletons
    while len(candidate) != 0:
        gen_level_table()
        gen_candidate()

def parseEle(string):
    parsed = string.split('\t')
    elements = parsed[2].split(' ')
    parsed = None
    elements[len(elements) - 1] = elements[len(elements) - 1][:-1]
    return elements

def init_candidate():
    global db_len
    db = open(inputf)
    unique = []
    for index, value in enumerate(db):
        if index == 0:
            continue
        db_len += 1
        elements = parseEle(value)
        for i in elements:
            if {i} not in unique and i != '':
                unique.append({i})
    return unique

def gen_level_table():
    global level
    level = [0] * len(candidate)
    db = open(inputf)
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

        # for item in candidate:
        #     temp_hash = 0
        #     for val in item:
        #         if val in elements:
        #             temp_hash += hash(val)
        #         else:
        #             break
        #         if temp_hash in level:
        #             level[temp_hash] += 1
        #         else:
        #             level[temp_hash] = 1

def gen_candidate():
    global db_len
    global candidate
    global dcl
    global level_union
    min_count = db_len * minsup
    temp_candidate = []
    for index, item in enumerate(candidate):
        if level[index] < min_count:
            dcl.append(item)
            continue
        level_union.append(item)
        for i in range(index + 1, len(candidate)):
            if level[i] < min_count:
                continue
            x = item.copy()
            for j in candidate[i]:
                x.add(j)
            if x not in temp_candidate:
                temp_candidate.append(x)
    candidate = temp_candidate

    # x = level[0] # Points to infrequent subsets
    # y = []
    # for i in x:
    #     y.append(list(i))
    # z = []
    # for i in range(len(y)): # ['a', 'c']
    #     for j in range(i + 1, len(y)): # ['b', 'e']
    #         t = list.copy(y[i])
    #         for k in y[j]: # 'b'
    #             if k in y[i]:
    #                 continue
    #             t.append(k)
    #         if len(z) == 0:
    #             z.append(t)
    #         else:
    #             flag = False
    #             for l in range(len(z)):
    #                 if set(z[l]) == set(t):
    #                     flag = True
    #             if not flag:
    #                 z.append(t)
    # h = []
    # for j in z:
    #     flag = False
    #     for i in level[1]:
    #         if set(list(i)).issubset(j):
    #             flag = True
    #     if not flag:
    #         h.append(j)
    # # print(z)
    # # print(h)
    # return h

    # z = itertools.product(y, y[0])
    # print(list(z))

# Check if arguments exist, if they do not, cancel or set to default
# if len(sys.argv) == 1 or len(sys.argv) > 3:
#     print("Unable to find or improper system arguments, check input carefully")
# elif len(sys.argv) == 2:
#     supp_t = 50
#     parseFile(sys.argv[1])
# else:
#     supp_t = int(sys.argv[2])
#     parseFile(sys.argv[1])

apriori()
print(level_union)