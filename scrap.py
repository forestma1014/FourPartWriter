import copy
from scale import *
parts = []
l = [['a','b','c'],['aa','aaa','bb','cc'],['bbb','ccc','ddd'],['aaa','ccc']]
# ,['aaa','b','ccc'],['aaa','bb','ccc'],['aaa','aaaa','bbb','ccc','ddd'],['aaa','ccc']
# ,['aaa','b','ccc'],['aaa','bb','ccc'],['aaa','aaaa','bbb','ccc','ddd'],['aaa','ccc']
# ,['aaa','b','ccc'],['aaa','bb','ccc'],['aaa','aaaa','bbb','ccc','ddd'],['aa','ccc']]


def sift(parts, possible):

    if parts == []:
        return possible
    
    i = 0
    term = len(possible)
    while i < term:
    
        if parts[-1] not in possible[i]:
            possible.pop(i)
            
            term -= 1
            continue
        i += 1

def asdf(parts,possible,length):

    if len(parts) == length:
        return parts


    print('parts:',parts)

    curPossible = copy.deepcopy(possible[len(parts)])
    #print('here',parts,possible,curPossible)
    sift(parts, curPossible)
    print('sifted:',curPossible)

    #asdf = copy.deepcopy(curPossible)
    for i in range(len(curPossible)):
        #assert(curPossible == asdf)
        originalPossible = copy.deepcopy(possible)
        originalParts = copy.deepcopy(parts)
        parts.append(curPossible[i])
        print('added:',curPossible[i])

        solution = asdf(parts, possible, length)
        if solution != None:
            return solution
        
        parts = originalParts
        print('original',parts)
        possible = originalPossible


# def asdf(parts, possible, original, index):
#     print('parts:',parts)
#     if len(parts) == len(original): return parts

#     sift(parts, possible[index])
#     print('sifted:',possible)
#     print('curIndex:',index)
#     if possible[index] != []:
#         parts.append(copy.copy(possible[index][0]))
#         print('added ',possible[index][0])
#         print('parts:',parts)
#         print('^^^^^^^^^^^^^^^^^^')


#         return asdf(parts, possible, original, index+1)


#     print('popped:',parts[-1])

#     popped = parts.pop(-1)
#     print('parts:',parts)

#     possible[index-1].pop(possible[index-1].index(popped))
#     if possible[0] == []:
#         return None

#     print('-----------')
#     copyListFromIndex(possible,copy.deepcopy(original), index)
#     assert(possible[index:] == copy.deepcopy(original[index:]))
#     return asdf(parts, possible, original, index-1)

#print(asdf(parts, l, copy.deepcopy(l),len(parts)))
print(asdf(parts, l, len(l)))
import sys
print(sys.getrecursionlimit())