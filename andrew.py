import PySide6
import copy

class Piece:
    #Function creates array of entries with minimum denomination of 32nd notes
    def __init__(self, tonic, mode, tstop, tsbottom, bars, parts):
        self.tonic = tonic
        self.mode = mode
        self.tstop = tstop
        self.tsbottom = tsbottom
        self.bars = bars
        self.parts = parts
        self.size = 4*bars*tstop//tsbottom
        newMArray = [[None for i in range(self.size)] for j in range(3)]
        newHArray = [[None for i in range(self.size)] for j in range(3*parts-1)]
        self.melodyArray = newMArray
        self.harmonyArray = newHArray

    #def arraytoNotation(self, array, size, tstop, tsbottom, bars):

    def melodyArrayInput(self, location, length, note, register):
        for i in range(length):
            self.Marray[0][location + i] = note[0] #char ABCDEFG
            self.Marray[1][location + i] = note[1] #int 0 for natural +1 for sharp amount, -1 for flat amount
            self.Marray[2][location + i] = register #int according to note naming rules

    # def harmonyGeneration(self):
    #     scaleArray = scaleParse()
    #     for i in range(self.size):
    #         #


def getInterval(quality, size, startingNote):
#returns new note triple
    numHalfSteps = halfSteps(quality, abs(size))
    if (size < 0):
        numHalfSteps *= -1
    mathSize = size - 1
    if (size < 0):
        mathSize += 2
    
    numHalfSteps += halfStepsFromC(startingNote)
    mathSize += (ord(startingNote[0]) - 60)%7
    note = ['C', 0, startingNote[2]]

    while (mathSize < 0):
        numHalfSteps += 12
        mathSize += 7
        note[2] -= 1
    while (mathSize > 6):
        numHalfSteps -= 12
        mathSize -= 7
        note[2] += 1
    
    note[0] = chr((mathSize + 2)%7+65)
    note[1] = numHalfSteps - halfStepsFromC(note)
    return note



def halfStepsFromC(startingNote):
#returns int of half steps from lower C (if Cb then negative number)
    if (startingNote[0] == 'C'):
        return startingNote[1]
    elif (startingNote[0] == 'D'):
        return startingNote[1] + 2
    elif (startingNote[0] == 'E'):
        return startingNote[1] + 4
    elif (startingNote[0] == 'F'):
        return startingNote[1] + 5
    elif (startingNote[0] == 'G'):
        return startingNote[1] + 7
    elif (startingNote[0] == 'A'):
        return startingNote[1] + 9
    elif (startingNote[0] == 'B'):
        return startingNote[1] + 11
    else:
        return 0

def halfSteps(quality, size):
#returns int of half steps of interval, size positive
    adjust = 0
    if (quality == 'd'):
        if (size == 1 | size == 4 | size == 5 | size == 8):
            adjust = -1
        else:
            adjust = -2
    elif (quality == 'm'):
        adjust = -1
    elif (quality == 'A'):
        adjust = 1
    if (size == 1):
        return adjust
    elif (size == 2):
        return adjust + 2
    elif (size == 3):
        return adjust + 4
    elif (size == 4):
        return adjust + 5
    elif (size == 5):
        return adjust + 7
    elif (size == 6):
        return adjust + 9
    elif (size == 7):
        return adjust + 11  
    elif (size == 8):
        return adjust + 12  
    else:
        return 0

def getMajTriads(note):
    A = [note[0:2]]
    A.append(getInterval('M', -3, note)[0:2])
    A.append(getInterval('P', -5, note)[0:2])
    return A

def getMinTriads(note):
    
    A = [note[0:2]]
    A.append((getInterval('m', -3, note))[0:2])
    A.append((getInterval('P', -5, note))[0:2])
    return A

def getDimTriads(note):
    A = [note[0:2]]
    A.append((getInterval('m', -3, note))[0:2])
    A.append((getInterval('d', -5, note))[0:2])
    return A

def getDim7(note):
    A = getDimTriads(note)
    A.append((getInterval('d', -7, note))[0:2])
    return A

def getDom7(note):
    A = getMajTriads(note)
    A.append((getInterval('m', -7, note))[0:2])
    return A
def getMin7(note):
    A = getMinTriads(note)
    A.append((getInterval('m', -7, note))[0:2])
    return A
def getMaj7(note):
    A = getMajTriads(note)
    A.append((getInterval('M', -7, note))[0:2])
    return A
def getHalfD(note):
    A = getDimTriads(note)
    A.append((getInterval('m', -7, note))[0:2])
    return A


print(getMin7(['C', 1, 2]))

#graphics class
   #def displayKeySignature(self):

   #def displayTimeSignature(self):

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

    

    return scaleArray
    
def degreesToNotes(part, tonic, mode):

    for i in range(len(part)):

        note = getScale(tonic, mode)[part[i][0] - 1]
        print(part[i][0], note)
        note[1] += part[i][1] #accidentals
        part[i] = note
    return part
    

def notesToDegrees(part, tonic, mode):

    notes = ['C','D','E','F','G','A','B']
    scale = getScale(tonic, mode)
    for i in range(len(part)):
        degree = [0,0]
        degree[0] = notes.index(part[i][0]) - notes.index(tonic[0])
        if degree[0] < 0:
            degree[0] += 7 

        #accidental
        degree[1] = part[i][1] - scale[degree[0]][1] 
        part[i] = degree
    return part



