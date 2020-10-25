import sys
import itertools

minsup = 0.0
union_level = []
levels = {}

filen = 'data'
inputf = sys.path[0] + '\\' + filen + '.txt'

# Implemented from included wiki_algo screenshot
# https://en.wikipedia.org/wiki/Apriori_algorithm
def apriori():
    candidate = init_candidate() # Initial candidate table containing singletons
    while len(candidate) != 0:
        level_table = gen_level_table(db, candidate, minsup)
        candidate = gen_candidate(level_table)
    print(union_level)
    return

def parseEle(string):
    parsed = string.split('\t')
    elements = parsed[2].split(' ')
    parsed = None
    elements[len(elements) - 1] = elements[len(elements) - 1][:-1]
    return elements


def init_candidate():
    db = open(inputf)
    unique = []
    for index, value in enumerate(db):
        if index == 0:
            continue
        elements = parseEle(value)
        for i in elements:
            if {i} not in unique:
                unique.append({i})
    return unique

def gen_level_table(candidate, dcl=[]):
    db = open(inputf)
    for index, value in enumerate(db):
        if index == 0:
            continue
        elements = set(parseEle(value))
        for item in candidate:
            for val in item:
                if val in elements:
                    if val in levels:
                        levels[val] += 1
                    else:
                        levels[val] = 1

def gen_candidate(level):
    x = level[0] # Points to infrequent subsets
    y = []
    for i in x:
        y.append(list(i))
    z = []
    for i in range(len(y)): # ['a', 'c']
        for j in range(i + 1, len(y)): # ['b', 'e']
            t = list.copy(y[i])
            for k in y[j]: # 'b'
                if k in y[i]:
                    continue
                t.append(k)
            if len(z) == 0:
                z.append(t)
            else:
                flag = False
                for l in range(len(z)):
                    if set(z[l]) == set(t):
                        flag = True
                if not flag:
                    z.append(t)
    h = []
    for j in z:
        flag = False
        for i in level[1]:
            if set(list(i)).issubset(j):
                flag = True
        if not flag:
            h.append(j)
    # print(z)
    # print(h)
    return h

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


db = open(inputf)

l = init_candidate()
db = open(inputf)
gen_level_table(l)
print(l)
print(len(l))