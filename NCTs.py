from harmony import *
from scale import *

def genNonChordTones(tonic, mode, parts):
    
    partsNCT = copy.deepcopy(parts[::-1])
    #First make each voicing a 3D array that can hold up to 2 voicings
    #so we can generate eighth note NCTs

    for i in range(len(partsNCT)):
        partsNCT[i] = [parts[i]]

    genPassingTones(tonic, mode, partsNCT)
    genAppoggiaturas(tonic, mode, partsNCT)
    genSuspensions(tonic, mode, partsNCT)
    print('with NCTS:',partsNCT)
    return partsNCT

def genPassingTones(tonic, mode, partsNCT):

    for i in range(len(partsNCT)-1):
        v1 = copy.deepcopy(partsNCT[i][0]) #current voicing
        v2 = copy.deepcopy(partsNCT[i+1][0]) #adjacent voicing
        
        nctChord = copy.deepcopy(v1)
        for voice in range(1,4):
            if steps(v1[voice], v2[voice]) == 3:
                nctChord[voice] = getScaleNote(tonic, mode, nctChord[voice], 1)
            elif steps(v1[voice], v2[voice]) == -3:
                nctChord[voice] = getScaleNote(tonic, mode, nctChord[voice], -1)
        partsNCT[i].append(nctChord)
def genAppoggiaturas(tonic, mode, partsNCT):
    pass
def genSuspensions(tonic, mode, partsNCT):
    pass
print(genNonChordTones(['C',0],"major",[[['C', 0, 5], ['G', 0, 4], ['E', 0, 4], ['C', 0, 3]], [['A', 0, 4], ['F', 0, 4], ['C', 0, 4], ['F', 0, 3]], [['B', 0, 4], ['D', 0, 4], ['G', 0, 3], ['G', 0, 2]], [['C', 0, 5], ['E', 0, 4], ['G', 0, 3], ['C', 0, 3]]]
))
    
print(steps(['C',0,5],['E',0,5]))