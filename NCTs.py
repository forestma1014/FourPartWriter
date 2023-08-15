from harmony import *
from scale import *

def genNonChordTones(tonic, mode, parts):
    
    partsNCT = copy.deepcopy(parts)
    #First make each voicing a 3D array that can hold up to 2 voicings
    #so we can generate eighth note NCTs

    for i in range(len(partsNCT)):
        partsNCT[i] = [parts[i]]

    
    return partsNCT


print(genNonChordTones(['C',0],"major",[[['E', -1, 4], ['B', -1, 3], ['G', 0, 3], ['E', -1, 3]], [['F', 0, 4], ['B', -1, 3], ['F', 0, 3], ['D', 0, 3]], [['F', 0, 4], ['E', -1, 4], ['A', 0, 3], ['C', -1, 3]], [['G', -1, 4], ['C', -1, 4], ['E', -1, 3], ['C', -1, 3]], [['E', -1, 4], ['B', -1, 3], ['G', 0, 3], ['G', 0, 2]], [['D', 0, 4], ['B', -1, 3], ['F', 0, 3], ['A', -1, 2]], [['B', -1, 4], ['B', -1, 3], ['E', -1, 3], ['G', 0, 2]], [['C', -1, 5], ['E', -1, 4], ['A', -1, 3], ['A', -1, 2]], [['B', -1, 4], ['E', -1, 4], ['G', 0, 3], ['E', -1, 3]]]
))
    
