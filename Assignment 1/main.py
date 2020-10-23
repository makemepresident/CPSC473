import sys
import itertools

supp_t = 0
records = 0
lines_arr = []
initial = 0

# Have to parse file a single line at time (cannot store in memory)
# def parseFile(filename):
#     reader = open(filename)
#     lines = reader.readlines()
#     for i in range(0, len(lines)):
#         if i == 0:
#             records = int(stripNL(lines[0]))
#             continue
#         arr = lines[i].split('\t')
#         arr[2] = arr[2].strip()
#         lines_arr.append(arr)

# def parseFile(filename, start, final):
#     with open(filename) as line:
#         for i in enumerate(line):
#             if i < start:
#                 continue


        

# def stripNL(string):
#     string.replace('\n', '')
#     return string

# Implemented from included wiki_algo screenshot
# https://en.wikipedia.org/wiki/Apriori_algorithm
def apriori(db=None, minsup=None):
    db = [['a', 'c', 'd'], ['b', 'c', 'e'], ['a', 'b', 'c', 'e'], ['b', 'e']]
    candidate = init_candidate(db)
    candidate = [['a', 'b'], ['a', 'c'], ['a', 'e'], ['b', 'c'], ['b', 'e'], ['c', 'e']]
    # candidate = []
    # print(candidate)
    temp = gen_level_table(db, candidate, 0.50)
    print(temp)
    gen_candidate(temp)
    return

def init_candidate(db):
    if not isinstance(db, list):
        return None
    unique = []
    for i in db:
        if not isinstance(i, list):
            return None
        for j in i:
            if [j] not in unique:
                unique.append([j])
    return unique

def gen_level_table(db, candidate, minsup, dcl=[]):
    level = {}
    for i in db: #['a', 'c', 'd']
        for j in candidate: # ['a']
            missing = False
            for k in j: # 'a'
                if k not in i:
                    missing = True
                    break
            if not missing:
                if tuple(j) not in level:
                    level[tuple(j)] = 1
                else:
                    level[tuple(j)] += 1
    temp = []
    for i in level:
        if level[i] / len(db) < minsup:
            temp.append(i)
    for j in temp:
        dcl.append(j)
        del level[j]
    return level, dcl

def gen_candidate(level):
    x = level[0]
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
                for i in z:
                    if set(i) == set(t):
                        flag = True
                if not flag:
                    z.append(t)
    h = []
    for i in level[1]:
        for j in z:
            if not set(list(i)).issubset(j):
                h.append(j)
    print(z)
    print(h)

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