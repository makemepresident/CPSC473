import sys
from itertools import product

db_len = 0
minsup = 0.5
level = []
candidate = []
level_union = []
level_union_count = []
dcl = []
current_level = 2

filepath = None

# Implemented from included wiki_algo screenshot
# https://en.wikipedia.org/wiki/Apriori_algorithm
def apriori():
    global level
    global minsup
    global candidate
    global level_union
    global current_level
    candidate = init_candidate() # Initial candidate table containing singletons
    while len(candidate) != 0:
        gen_level_table()
        gen_candidate()
        current_level += 1

def parseEle(string):
    parsed = string.split('\t')
    elements = parsed[2].split(' ')
    parsed = None
    elements[len(elements) - 1] = elements[len(elements) - 1][:-1]
    return elements

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
    db.close()
    return unique

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
    db.close()

def gen_candidate():
    global db_len
    global candidate
    global dcl
    global level_union
    global current_level
    min_count = db_len * minsup
    temp_candidate = []
    for index, item in enumerate(candidate):
        if level[index] < min_count:
            dcl.append(item)
            continue
        level_union.append(item)
        level_union_count.append(level[index])
        for i in range(index + 1, len(candidate)):
            if level[i] < min_count:
                continue
            x = item.copy()
            for j in candidate[i]:
                x.add(j)
            for neg in dcl:
                if neg.issubset(x):
                    continue
            if len(x) != current_level:
                continue
            if x not in temp_candidate:
                temp_candidate.append(x)
    candidate = temp_candidate

def main():
    # Check if arguments exist, if they do not, cancel or set to default
    global minsup
    global filepath
    if len(sys.argv) == 1 or len(sys.argv) > 3:
        print("Unable to find or improper system arguments, check input carefully")
        return
    elif len(sys.argv) == 2:
        minsup = 0.50
        filepath = sys.path[0] + "\\" + sys.argv[1]
    else:
        x = float(sys.argv[2])
        if x >= 1:
            x /= 100
        filepath = sys.path[0] + "\\" + sys.argv[1]
        minsup = x
    apriori()

main()
print('|FPs| = ' + str(len(level_union)))
for i, j in enumerate(level_union):
    print(str(j) + ' : ' + str(level_union_count[i]))