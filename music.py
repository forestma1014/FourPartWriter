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
    scaleArray[0] = tonic.copy()
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
                if i == 3 or i == 6 or i == 7:
                    return "m" + str(i + 7*octs)
                else:
                    return "d" + str(i + 7*octs)
            elif n2[1] == scale[i][1] + 1:
                return "A" + str(i + 7*octs)

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
