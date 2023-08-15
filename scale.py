#music.py
#Forest Ma

import copy

#========================================
#collection of basic music notation
#helper functions to harmony.py
#========================================



#returns a list of all the notes in a major or minor scale, first index being None
#to conform to scale degree conventions
def getScale(tonic, mode):
    
    CMajor = [('C', 0), ('D', 2), ('E', 4), ('F', 5), ('G', 7), ('A', 9), ('B', 11)] 
                    #second part of tuple is distance in half step to next note
    CMinor = [('C', 0), ('D', 2), ('E', 3), ('F', 5), ('G', 7), ('A', 8), ('B', 10)]     

    if mode == "major":
        CScale = CMajor
    else:
        CScale = CMinor
    
    #Derive scales based off above scales in C
    scaleArray = [['_',  0],['_',  0],['_',  0],['_',  0],['_',  0],['_',  0],['_',  0]]
    scaleArray[0] = copy.copy(tonic)
    notes = ['C','D','E','F','G','A','B']
    offset = notes.index(tonic[0])

    for i in range(0, 7):
        if i + offset >= 7:
            curNote = notes[(i + offset)%7]
        else:
            curNote = notes[i + offset]

        #first set the note
        scaleArray[i][0] = curNote

        #then set the accidental
        #half steps of the natural note from tonic
        curHalfStepsFromTonic = CMajor[notes.index(curNote)][1] - (CMajor[offset][1] + tonic[1])

        if curHalfStepsFromTonic < 0:
            curHalfStepsFromTonic += 12 

        #half steps from desired note to tonic
        desiredHalfStepsFromTonic = CScale[i][1]
        scaleArray[i][1] = desiredHalfStepsFromTonic - curHalfStepsFromTonic

        #edge cases
        if mode == "major" and scaleArray[i][1] < 0 and (i == 0 or i == 6) and tonic[1] != -1:
            scaleArray[i][1] += 12
        if mode == "minor" and scaleArray[i][1] >=10 and i == 6 and tonic[1] == -1:
            scaleArray[i][1] -= 12
        if mode == "minor" and scaleArray[i][1] < 0 and i == 0 and tonic[1] == 1:
            scaleArray[i][1] += 12

    
    scaleArray.insert(0, None) #offset by 1 index to notation conventions (1 is unison)
    return scaleArray


def degreesToNotes(part, tonic, mode):

    for i in range(len(part)):

        note = getScale(tonic, mode)[part[i][0]]
        note[1] += part[i][1] #accidentals
        part[i] = note
    return part
    

def notesToDegrees(part, tonic, mode):

    notes = ['C','D','E','F','G','A','B']
    scale = getScale(tonic, mode)
    for i in range(len(part)):
        degree = [0,0]
        degree[0] = notes.index(part[i][0]) - notes.index(tonic[0]) + 1
        if degree[0] <= 0:
            degree[0] += 7 

        #accidental
        degree[1] = part[i][1] - scale[degree[0]][1] 
        part[i] = degree
    return part

#returns 1 if n1 < n2, 0 if equal, -1 if n2 > n1
def compareNotes(n1, n2):

    #return none if notes do not have register
    if len(n1) == 2 or len(n2) == 2:
        return None
    #compare register
    if n1[2] > n2[2]:
        return 1
    if n2[2] > n1[2]:
        return -1

    #compare notes
    scale = ['C','D','E','F','G','A','B']
    if scale.index(n1[0]) > scale.index(n2[0]):
        return 1
    if scale.index(n2[0]) > scale.index(n1[0]):
        return -1

    #compare accidental
    if n1[1] > n2[1]:
        return 1
    if n2[1] > n1[1]:
        return -1
    
    return 0
#flatten or sharpen note by count
def flatten(note, count):
    new = note.copy()
    new[1] -= count
    return new
def sharpen(note, count):
    new = note.copy()
    new[1] += count
    return new
#returns the least number of octaves than fit between n1 and n2
def octavesApart(n1, n2):
    #set n2 to be greater than n1
    n1 = copy.copy(n1)
    n2 = copy.copy(n2)
    if compareNotes(n1, n2) == 1:
        x = copy.copy(n1)
        n1 = copy.copy(n2)
        n2 = copy.copy(x)
    octaves = -1
    while compareNotes(n1, n2) <= 0:
        n2[2] -= 1
        octaves += 1
    
    return octaves
    
#returns the interval from n1 to n2, n1 IS THE FIRST NOTE
def interval(n1, n2):

    if n1 == n2:
        return 'P1'

    if compareNotes(n1, n2) != None and compareNotes(n1, n2) == 1:
        x = copy.copy(n1)
        n1 = copy.copy(n2)
        n2 = copy.copy(x)

    if len(n1) == 2 or len(n2) == 2:
        octs = 0
    else:
        octs = octavesApart(n1 ,n2)
    #if compareNotes(n1, n2) == None or compareNotes(n1, n2) <= 0:
    scale = getScale(n1, "major")
    for i in range(1, len(scale)):
        if n2[0] == scale[i][0]:
            if n2[1] == scale[i][1]:
                if i == 4 or i == 5:
                    return "P" + str(i + 7*octs)
                if i == 1:
                    return "P" + str(8 + 7*(octs-1))
                
                return "M" + str(i + 7*octs)
            elif n2[1] == scale[i][1] - 1:
                if i == 2 or i == 3 or i == 6 or i == 7:
                    return "m" + str(i + 7*octs)
                else:
                    return "d" + str(i + 7*octs)
            elif n2[1] == scale[i][1] - 2:

                return "d" + str(i + 7*octs)
            elif n2[1] == scale[i][1] + 1:
                return "A" + str(i + 7*octs)

print(interval(['F',0,2],['B',0,2]))
#returns the input scale without accidental or register
def toNoteScale(scale):
    res = [None]
    for i in range(1, len(scale)):
        res.append(scale[i][0])
    return res
#returns a list of the same notes with register removed, or a single note
def removeRegister(notes):
    if isinstance(notes[0], list):
        res = []
        for i in range(len(notes)):
            res.append(notes[i][:-1])
        return res
    if isinstance(notes, list):
        return notes[:-1]

#copies L2 to L1
def copyList(L1, L2):
    for i in range(len(L2)):
        if len(L1) < i + 1: L1.append(None)
        L1[i] = copy.deepcopy(L2[i])
    while len(L1) > len(L2):
        L1.pop()

# L1 = [a, b, c]
# L2 = [f, g, h, i, j, k, l]

# copyListFromIndex(L1, L2, 3)

#copies L2 to L1 starting from given index
# def copyListFromIndex(L1, L2, index):
#     newList = []
#     # New list is size of L2 always
#     for i in range(0, len(L2)):
#         # If index less than starting index, pull from L1
#         if i < index:
#             newList.append(L1[i])
#         else:
#             newList.append(L2[i])
#     L1 = newList

def copyListFromIndex(L1, L2, index):
    for i in range(index, len(L2)):
        if len(L1) < i + 1: L1.append(None)
        L1[i] = copy.deepcopy(L2[i])
    while len(L1) > len(L2):
        L1.pop()

#returns the number of note steps from n1 to n2, negative if n2 < n1
def steps(n1, n2):

    cmp = compareNotes(n1, n2)
    if cmp == 0: return 0
    steps = int(interval(n1, n2)[1:])
    if cmp == 1: 
        return -steps
    else:
        return steps

def enharmonicSimplify(note):
    if note[:-1] == ['E', 1]:
        note[0] = 'F'
        note[1] = 0
        return note
    if note[:-1] == ['B', 1]:
        note[0] = 'C'
        note[1] = 0
        return note
    return note
#returns the number of half steps from n1 to n2, negative if n2 < n1
def halfSteps(n1, n2):
    if compareNotes(n1, n2) == 0:
        return 0
    
    n2 = enharmonicSimplify(n2)
    #make n2 greater than n1, flip if need to and set vector to negative
    if compareNotes(n1, n2) == 1: 
        original = copy.copy(n2)
        n2 = copy.copy(n1)
        n1 = original
        vector = -1

    else: vector = 1
    halfSteps = 0

    
    #create scale from n1
    scale = getScale(n1[:2], "major")[1:]
    n2InScale = copy.copy(n2)
    for i in range(len(scale)):
        if scale[i][0] == n2InScale[0]:
            n2InScale[1] = scale[i][1]
            break

    if n1[0] == 'C':
        startingC = True
    else:
        startingC = False
    i = 0
    while compareNotes(n1, n2) < 0:
        original = copy.copy(n1)
        if i == len(scale): 
            i = 0
        if scale[i][0] == 'C':
            if startingC == False:
                n1[2] += 1
            else:
                startingC = False
        n1[0] = scale[i][0]
        n1[1] = scale[i][1]
        if interval(original, n1) == 'M2':
            halfSteps += 2
        elif interval(original, n1) == 'm2':
            halfSteps += 1
        elif interval(original, n1) == 'A2':
            halfSteps += 3
  
        i += 1

    remainder = interval(n1, n2)

    if remainder == 'm2':
        halfSteps -= 1
    elif remainder == 'M2':
        halfSteps -= 2
    elif remainder == 'A2':
        halfSteps -= 3
    elif remainder == 'A1':
        halfSteps -= 1
    return halfSteps*vector

#given interval, returns single octave equivalent (ie. P12 - > P5)
def trueInterval(interval):
    steps = interval[1:]
    if int(steps) < 8: return interval
    steps = (int(steps)-1)%7 + 1
    return interval[0] + str(steps)

print(trueInterval(interval(['A', 0, 4],['D', 0, 3])))

if (trueInterval(interval(['D',0,3], ['A',0,4])) in ['P5','d5'] 
    and trueInterval(interval(['E',0,3], ['B',0,4])) == 'P5'
    and compareNotes(['D',0,3], ['A',0,4]) != 0):
    print('br')