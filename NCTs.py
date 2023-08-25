from harmony import *
from scale import *

def genNonChordTones(tonic, mode, parts, numerals):
    
    partsNCT = copy.deepcopy(parts[::-1])
    #First make each voicing a 3D array that can hold up to 2 voicings
    #so we can generate eighth note NCTs

    for i in range(len(partsNCT)):
        partsNCT[i] = [parts[i]]

    genPassingTones(tonic, mode, partsNCT, numerals)
    genAppoggiaturas(tonic, mode, partsNCT)
    #genSuspensions(tonic, mode, partsNCT, numerals, hasPassingTone)
    print('with NCTS:',partsNCT)
    return partsNCT

def genPassingTones(tonic, mode, partsNCT, numerals):

    for i in range(len(partsNCT)):

        
        original = copy.deepcopy(partsNCT[i][0])
        hasPassingTone = False
        hasSuspension = False
        # numerals that we don't want passing tones from
        if i != len(partsNCT) - 1 and numerals[i] not in ['iv','Ge','Fr','N'] and (i == 0 or numerals[i-1] not in ['Ge','Fr','N']) and numerals[i+1] not in ['Ge','Fr','N']:
            nctChord = copy.deepcopy(partsNCT[i][0])
            v1 = copy.deepcopy(partsNCT[i][0]) #current voicing
            v2 = copy.deepcopy(partsNCT[i+1][0]) #adjacent voicing
            for voice in range(1,4):
                if steps(v1[voice], v2[voice]) == 3:
                    nctChord[voice] = getScaleNote(tonic, mode, nctChord[voice], 1)
                    hasPassingTone = True
                elif steps(v1[voice], v2[voice]) == -3:
                    nctChord[voice] = getScaleNote(tonic, mode, nctChord[voice], -1)
                    hasPassingTone = True
        if hasPassingTone:
            partsNCT[i].append(nctChord)
            continue

        #suspensions
        elif i != 0 and i != len(partsNCT) - 1 and numerals[i] not in ['iv','Ge','Fr','N'] and (i == 0 or numerals[i-1] not in ['Ge','Fr','N']) and numerals[i+1] not in ['Ge','Fr','N']:
            nctChord = copy.deepcopy(partsNCT[i][0])
            v1 = copy.deepcopy(partsNCT[i-1][0]) #current voicing
            v2 = copy.deepcopy(partsNCT[i][0]) #adjacent voicing
            
            scale = getScale(tonic, mode)
            nctChord = copy.deepcopy(v2)
            if numerals[i] not in []:
                for voice in range(1,4):
            
                    if steps(v1[voice], v2[voice]) == -2 and v2[voice][:-1] not in [scale[5], scale[1]]:
                        nctChord[voice] = getScaleNote(tonic, mode, nctChord[voice], 1)
                        hasSuspension = True
            if hasSuspension:
                partsNCT[i].insert(0,nctChord)
                continue

        #if no NCTS, just append the copy  
        partsNCT[i].append(original)
                            

def genAppoggiaturas(tonic, mode, partsNCT):
    pass
def genSuspensions(tonic, mode, partsNCT, numerals, hasPassingTone):
    for i in range(1,len(partsNCT)-1):
        v1 = copy.deepcopy(partsNCT[i-1][0]) #current voicing
        v2 = copy.deepcopy(partsNCT[i][0]) #adjacent voicing
        
        scale = getScale(tonic, mode)
        nctChord = copy.deepcopy(v2)

        # numerals that we don't want suspensions from
        if numerals[i] not in []:
            for voice in range(1,4):
                if [i, voice] not in hasPassingTone:
                    if steps(v1[voice], v2[voice]) == -2 and v2[voice][:-1] != scale[5]:
                        nctChord[voice] = getScaleNote(tonic, mode, nctChord[voice], 1)
                        partsNCT[i].insert(0,nctChord)
        
