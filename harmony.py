#harmony.py
#Forest Ma
#calculates four-part harmony given a melody from main.py

import sys
import copy
import random
from scale import *

###===========================================
###    STARTING POINT: genHarmonyRecursive
###===========================================
#recursively calculates roman numeral analysis and part writing simultaneously,
#backtracking if their invalidities in either the RN analysis or the part writing
#starting from the cadence (right to left)
def genHarmonyRecursive(melody, tonic, mode, curNumerals, parts, allPossibleVoicings, cadences, lvMaxIntApart, length):
    # print(melody,tonic,mode)
    if melody == []:
        print('done:',parts[::-1])
        return [parts, curNumerals]
    note = melody[-1]

    if curNumerals == []:
        # print(tonic,mode,note)
        prio = getCadenceNumeral(tonic, mode, note, [])

    elif len(curNumerals) == length - 1:

        prio = getCadenceNumeral(tonic, mode, note, getPriorityList(curNumerals[-1], mode))
        # print('cadNum:', prio)
    else:
        prio = getPriorityList(curNumerals[-1], mode)
    originalPrio = copy.deepcopy(prio)
    # print('prio:',prio)

    # i = 0
    # term = len(prio)
    # while i < term:
    #     if not isGoodProgression(curNumerals, prio[i], melody, length):
    #         prio.append(prio.pop(i))
    #         term -= 1
    #     else:
    #         i += 1
    siftPriorityList(tonic, mode, curNumerals, prio, melody, length)
    for i in range(len(prio)):
        originalNumerals = copy.deepcopy(curNumerals)
        originalParts = copy.deepcopy(parts)
        originalVoicings = copy.deepcopy(allPossibleVoicings)
        #check if numeral is possible given note
        if note[:-1] in chordFromNumeral(tonic, mode, prio[i]):
            # print(note[:-1], 'fits in ', prio[i])
            curNumerals.append(prio[i]) #add to cur
            # print('NUMERALS:',curNumerals[::-1])

        else:
            # print('continuing:', note[:-1], 'doesnt fit in ', prio[i])
            continue #go next in priority list if current numeral not possible

        #chord is available/possible at this point, already added to current
        #check for imperfections with isGoodProgression, or just proceed if
        #i is last in the priority list
        #generateVoices generates the other three parts and returns true
        #if there is a solution to the part writing - if false, this
        #call of the function returns None
        if voiceLeadingPossible(tonic, mode, parts, curNumerals, melody, allPossibleVoicings, cadences, lvMaxIntApart, length):
            solution = genHarmonyRecursive(melody[:-1], tonic, mode, curNumerals, parts, allPossibleVoicings, cadences, lvMaxIntApart, length)

            if solution != None:  
                return solution
        else:
            pass#print(allPossibleVoicings[-1],'---',parts)
            # print('vl not possible')


        curNumerals = copy.deepcopy(originalNumerals)
        parts = copy.deepcopy(originalParts)
        prio = copy.deepcopy(originalPrio)
        allPossibleVoicings = copy.deepcopy(originalVoicings)
        
        # print('------------\n','preserve original numerals:', curNumerals[::-1],'\nPARTS:',parts[::-1],'\n------------') 
    return None

#called at the end of generation, returns True if the start and the cadence
#are good progressions
def goodStartEnd(tonic, mode, parts, numerals):
    if numerals[0] == 'I':
        if len(parts) == 1: return True
        if (parts[1][0][:-1] in chordFromNumeral(tonic, mode, 'V7') and
            numerals[1] not in ['V','V7']):
            return False
    return True


# ====================================================#

###===========================================
###    voiceLeadingPossible + all helpers
###===========================================
#generates VL possibilities, returns false if there is no possible solution
#in which case the algorithm backtracks
#soprano is the melody note
def voiceLeadingPossible(tonic, mode, parts, numerals, melody, allPossibleVoicings, cadences, lvMaxIntApart, length):
    
    numeral = copy.copy(numerals[-1])
    chord = chordFromNumeral(tonic, mode, numeral)
    soprano = copy.copy(melody[-1])
    
    #generate all the possible voicings for each individual chord
    #push them onto a 3D list indexed by chords from right to left (0 is last chord),
    #each element of the list being a list of possible voicings (chordal format)
    #at the end, run a function that chooses one voicing from each list of possible voicings,
    #with attention to voice leading rules as well as conventions and idioms.
    #if no solution exists to satisfy voice leading rules, this function returns false

    allPossibleVoicings.append(getPossibleVoicings(tonic, mode, numerals, soprano, parts))

    #reduce first set of voicings to valid cadences
    if len(allPossibleVoicings) == 1:
        siftVoicings(tonic, mode, allPossibleVoicings[0], chordFromNumeral(tonic,mode,numerals[0]), numerals[0], parts)
        # cadences = getCadences(tonic, mode, allPossibleVoicings[0], numerals[0])
        copyList(cadences, getCadences(tonic, mode, allPossibleVoicings[0], numerals[0]))
        allPossibleVoicings[0] = copy.deepcopy(cadences)
        # print('CADENCES: ', cadences)

        # parts.append(cadences[0])
        # return True
    #checks if the newest set of possible voicings allows for legal voice leading
    if len(allPossibleVoicings) == length and length != 2:
        start = getCadences(tonic, mode, allPossibleVoicings[-1], numeral)
        # print('cad',start)
        allPossibleVoicings[-1] = copy.deepcopy(start)

    originalVoicings = copy.deepcopy(allPossibleVoicings)
    originalParts = copy.deepcopy(parts)
    # print('calling vl path, index',len(parts), allPossibleVoicings[len(parts)])
    solution = getVLPath(tonic, mode, numerals, parts, copy.deepcopy(allPossibleVoicings), originalVoicings, len(parts), lvMaxIntApart, length, 1)
    if solution != None:
        copyList(parts, solution)
        #print('PARTS:', parts[::-1])
        return True
    return False

#returns an array of notes (no register) pertaining to an input chord
#output format: [['A', 0],['C', 0],['E', 0]]
def chordFromNumeral(tonic, mode, numeral):
    scale = getScale(tonic, mode)
    
    #currently assuming input has no accidentals in major
    if mode == "major":
        if numeral == 'I':
            return [scale[1]] + [scale[3]] + [scale[5]]
        # elif numeral == 'i':
        #     return scale[1] + flatten(scale[3], 1) + scale[5]
        elif numeral == 'ii':
            return [scale[2]] + [scale[4]] + [scale[6]]
        elif numeral == 'iii':
            return [scale[3]] + [scale[5]] + [scale[7]]
        elif numeral == 'IV':
            return [scale[4]] + [scale[6]] + [scale[1]]
        elif numeral == 'V':
            return [scale[5]] + [scale[7]] + [scale[2]]
        elif numeral == 'vi':
            return [scale[6]] + [scale[1]] + [scale[3]]

        #7th chords
        elif numeral == 'ii7':
            return [scale[2]] + [scale[4]] + [scale[6]] + [scale[1]]
        elif numeral == 'iio/7':
            return [scale[2]] + [scale[4]] + [flatten(scale[6], 1)] + [scale[1]]
        elif numeral == 'IV7':
            return [scale[4]] + [scale[6]] + [scale[1]] + [scale[3]]
        elif numeral == 'V7':
            return [scale[5]] + [scale[7]] + [scale[2]] + [scale[4]]
        elif numeral == 'viio7':
            return [scale[7]] + [scale[2]] + [scale[4]] + [flatten(scale[6], 1)]
        elif numeral == 'viio/7':
            return [scale[7]] + [scale[2]] + [scale[4]] + [scale[6]]

        #secondary chords
        elif numeral == 'V/V':
            return [scale[2]] + [sharpen(scale[4], 1)] + [scale[6]]
        elif numeral == 'V/vi':
            return [scale[3]] + [sharpen(scale[5], 1)] + [scale[7]]
        elif numeral == 'V/ii':
            return [scale[6]] + [sharpen(scale[1], 1)] + [scale[3]]
        elif numeral == 'V/iii':
            return [scale[7]] + [sharpen(scale[2], 1)] + [sharpen(scale[4], 1)]
        elif numeral == 'V7/IV':
            return [scale[1]] + [scale[3]] + [scale[5]] + [flatten(scale[7], 1)]
        elif numeral == 'V7/V':
            return [scale[2]] + [sharpen(scale[4], 1)] + [scale[6]] + [scale[1]]
        elif numeral == 'V7/vi':
            return [scale[3]] + [sharpen(scale[5], 1)] + [scale[7]] + [scale[2]]
        elif numeral == 'V7/ii':
            return [scale[6]] + [sharpen(scale[1], 1)] + [scale[3]] + [scale[5]]
        elif numeral == 'V7/iii':
            return [scale[7]] + [sharpen(scale[2], 1)] + [sharpen(scale[4], 1)] + [scale[6]]

        #flat 6 chords
        elif numeral == 'iv':
           return [scale[4]] + [flatten(scale[6], 1)] + [scale[1]]
        elif numeral == 'VI':
            return [flatten(scale[6], 1)] + [scale[1]] + [flatten(scale[3], 1)]
        elif numeral == 'Ge':
            return [flatten(scale[6], 1)] + [scale[1]] + [flatten(scale[3], 1)] + [sharpen(scale[4], 1)]
        elif numeral == 'Fr':
            return [flatten(scale[6], 1)] + [scale[1]] + [scale[2]] + [sharpen(scale[4], 1)]
        elif numeral == 'N':
           return [flatten(scale[2], 1)] + [scale[4]] + [flatten(scale[6], 1)]

    else: #minor
        pass
    
def getPriorityList(numeral, mode): #numerals from right to left from cadence
    if mode == "major":

        if numeral == 'I':
            return ['V','V7','IV','IV7','I','ii','iio/7','iv','VI','ii7','vi','viio7','viio/7','N']
            #allow ii, vi to precede a cadential 64
        elif numeral == 'ii':
            return ['IV','IV7','vi','I','iv','V7/ii','V/ii','ii']
        elif numeral == 'iii':
            return ['vi','I','V7/IV','V7/iii','V/iii','viio/7','iii']
        elif numeral == 'IV':
            return ['I','vi','V7/IV','iii','IV7','IV']
        elif numeral == 'V':
            return ['ii','ii7','IV','iv','I','V7/V','V/V','V','iio/7','Fr','Ge','N']
        elif numeral == 'vi':
            return ['V7','iii','V7/vi','V/vi','I','V','vi']

        #7th chords
        elif numeral == 'ii7':
            return ['IV','IV7','vi','I','ii']
        elif numeral == 'iio/7':
            return ['IV','IV7','VI','vi','I','ii']
        elif numeral == 'IV7':
            return ['iii','I','vi','V7/IV','IV','IV7']
        elif numeral == 'V7':
            return ['ii','iio/7','ii7','IV','iv','V/V','V7/V','I','vi','V','V7']
        elif numeral == 'viio7':
            return ['ii','IV','iio/7','ii7','IV','vi']
        elif numeral == 'viio/7':
            return ['ii','IV','iio/7','ii7','IV','vi']


        #secondary chords
        elif numeral == 'V/ii' or numeral == 'V7/ii':
            return ['I','vi','V','iii','ii','V/vi','V7/vi','V/ii']
        elif numeral == 'V/V' or numeral == 'V7/V':
            return ['ii','vi','IV','iii','I','V','V/ii','V7/ii','V/V']
        elif numeral == 'V/vi' or numeral == 'V7/vi':
            return ['V','V7','iii','V/iii','V7/iii','vi','V/vi']
        elif numeral == 'V/iii' or numeral == 'V7/iii':
            return ['I','iii','vi','IV']
        elif numeral == 'V7/IV':
            return ['I','IV','V']

        #flat 6 chords
        elif numeral == 'iv':
            return ['VI','vi','I','IV','V7/IV']
        elif numeral == 'VI':
            return ['I','V']
        elif numeral == 'Ge':
            return ['IV','vi','V','I','VI','iv']
        elif numeral == 'Fr':
            return ['IV','vi','V','I','VI','iv']
        elif numeral == 'N':
            return ['I','VI','V7/IV']
    if mode == "minor":
        raise Exception("unfinished")
    raise Exception("invalid mode")

#checks for strength of progressions, duplicate sequences, etc
#precondition: numerals is already a valid progression
def siftPriorityList(tonic, mode, numerals, prio, melody, length):
    i = 0
    numIndex = len(numerals)
    term = len(prio)
    boolBreak = False
    while i < term:
        numerals.append(prio[i])
        if len(numerals) >= 3:
            #allow consecutive numerals but not 3 in a row
            if numerals[numIndex] == numerals[numIndex-1] == numerals[numIndex-2]:
                prio.append(prio.pop(i))
                numerals.pop()
                term -= 1
                continue


        
        if len(numerals) >= 4:

            #don't allow consecutive progressions
            if numerals[numIndex:numIndex-2] == numerals[numIndex-2:numIndex-4]:
                prio.append(prio.pop(i))
                numerals.pop()
                term -= 1
                continue
                



        i += 1
        numerals.pop()

    if len(numerals) == length - 2:
        if melody[0][:-1] in chordFromNumeral(tonic, mode, 'I'):
            if 'IV' in prio:
                prio.pop(prio.index('IV'))
                prio.insert(0,'IV')
            if 'V' in prio:
                prio.pop(prio.index('V'))
                prio.insert(0,'V')
            if 'vi' in prio:
                prio.append(prio.pop(prio.index('vi')))
            if 'iii' in prio:
                prio.append(prio.pop(prio.index('iii')))
    # print('SIFTED PRIORITY: ',prio)
    # for i in range(len(numerals)):
    #     print(melody[len(melody)-i-1], numerals[i])
        #assert(melody[len(melody)-i-1] in chordFromNumeral(['C',0],'major',numerals[i]))



#returns the numeral of cadence or first chord, returns I or i if possible
#takes in the melody note of cadence or first note
def getCadenceNumeral(tonic, mode, note, available):

    if available == []: #happens when we call this function for the cadence
        for numeral in ['I','V','IV','V/V','V/ii','V/vi','V/iii','V7/IV']:
            if note[:-1] in chordFromNumeral(tonic, mode, numeral):
                return [numeral]
    else:
        for numeral in ['I','V','IV','V/V','V/ii','V/vi','V/iii','V7/IV']:
            if (note[:-1] in chordFromNumeral(tonic, mode, numeral)
                and numeral in available):
                return [numeral]
    
    return []


#helper to siftVoicings, returns true if n1 is a valid upper adjacent voice to n2
def validAdjacentNotes(n1, n2):
    if compareNotes(n1, n2) >= 0:
        if n1[2] == n2[2]:
           return True
        if n1[2] - n2[2] == 1: 
            scale = ['C','D','E','F','G','A','B']
            if scale.index(n1[0]) - scale.index(n2[0]) <= 0:
                return True
    return False



#destructively modifies the list of possible voicings,
#eliminating illegal chords and prioritizing desirable chords
#takes into account the whole parts
def siftVoicings(tonic, mode, voicings, chord, numeral, parts):

    #least desirable qualities are accounted for last, so they are at the end of the list
    root = chord[0]
    third = chord[1]
    fifth = chord[2]

    if mode == "major":

        i = 0
        term = len(voicings)
        while i < term:
            
            voicing = copy.deepcopy(voicings[i])
            # if voicing == [['G', 0, 4], ['G', 0, 3], ['D', 0, 3], ['B', 0, 1]]:
            #     raise Exception

            if len(parts) >= 1:
                v2 = parts[-1]
            soprano = voicing[0]
            alto = voicing[1]
            tenor = voicing[2]
            bass = voicing[3]
            

            #general rule across all inversions - can't double leading tone
            if isDoubled(voicing, getScale(tonic, "major")[7]):
                if voicing == [['G', 0, 4], ['G', 0, 3], ['D', 0, 3], ['B', 0, 1]]:
                    raise Exception
                voicings.pop(i)
                term -= 1
                continue
                
            #cannot double the third of V/_ chords
            if 'V/' in numeral and isDoubled(voicing, third):
                voicings.pop(i)
                term -= 1
                continue
            
            #first inversion rules
            if bass[:-1] == third:
                #iii6 and vi6 don't exist
                if numeral == 'iii' or numeral == 'vi':
                    voicings.pop(i)
                    term -= 1
                    continue
            
            #second inversion rules
            if bass[:-1] == fifth:
                if numeral == 'iii' or numeral == 'vi':
                    voicings.pop(i)
                    term -= 1
                    continue
            
            #if the tenor is above E4, push to back of the list
            if compareNotes(tenor, ['E',0,4]) == 1:
                voicings.append(voicings.pop(i))
                term -= 1
                continue
            
            #root position preferences
            if bass[:-1] == root:
                if isDoubled(voicing, root):
                    voicings.insert(0, voicings.pop(i))
                    i += 1
                    continue

            #first inversion preferences
            elif bass[:-1] == third:

                #prioritize doubling root, then fifth, then third
                if isDoubled(voicing, root):
                    voicings.insert(0,voicings.pop(i))
                    i += 1
                    continue
                if isDoubled(voicing, third):
                    voicings.append(voicings.pop(i))
                    term -= 1
                    continue

            #second inversion preferences
            elif bass[:-1] == fifth:

                # if isDoubled(voicing, fifth):
                #     voicings.insert(0, voicings.pop(i))
                #     i += 1
                #     continue
                voicings.append(voicings.pop(i))
                term -= 1
            i += 1
        prioritizeInversions(tonic, mode, voicings, numeral)
    if mode == "minor":
        pass

        
        #first inversion chords allowed: I, ii, IV, V



    #bass preferences
    i = 0
    term = len(voicings)
    while i < term:
        voicing = copy.deepcopy(voicings[i])
        #if the bass is a 12th down from tenor (or more), push to back of list
        if int(interval(voicing[2],voicing[3])[1:]) >= 12:
            voicings.append(voicings.pop(i))
            term -= 1
            continue
        
        #don't let the bass deviate too much from the cadential position
        #bass should always move
        if len(parts) >= 1:
            if int(interval(voicing[3], parts[0][3])[1:]) > 6:
                voicings.append(voicings.pop(i))
                term -= 1
                continue
            if compareNotes(voicing[3], parts[-1][3]) == 0:
                voicings.append(voicings.pop(i))
                term -= 1
                continue
        i += 1
    #this loop eliminates badly spaced chords, incomplete chords, and 
    #pushes chords with unisons to the back of the list
    #consistent with either mode
    i = 0
    term = len(voicings)
    while i < term:
        voicing = copy.deepcopy(voicings[i])
        if len(parts) >= 1:
            v2 = parts[-1]
            soprano = voicing[0]
            alto = voicing[1]
            tenor = voicing[2]
            bass = voicing[3]
        boolBreak = False
        
        if not ((validAdjacentNotes(voicing[0], voicing[1]) and
                validAdjacentNotes(voicing[1], voicing[2]) and
                compareNotes(voicing[2], voicing[3]) >= 0)):

            if voicings.pop(i) != voicing:
                raise Exception
            term -= 1
            
            continue
        voicingNoRegister = removeRegister(voicing)
        for j in range(len(chord)):
            if chord[j] not in voicingNoRegister:
                if voicings.pop(i) != voicing:
                    raise Exception
                boolBreak = True
                term -= 1
                break
        if boolBreak: 
            continue

        if unisonVoicing(voicing):
            voicings.append(voicings.pop(i))
            #voicings.pop(i)
            term -= 1
            continue
        soprano = voicing[0]
        alto = voicing[1]
        tenor = voicing[2]
        bass = voicing[3]
        #vocal ranges of SATB
        if compareNotes(soprano, ['B',0,5]) == 1 or compareNotes(soprano, ['C',0,4]) == -1:
            raise Exception('Melody range exceeded')
        if compareNotes(alto, ['D',0,5]) == 1 or compareNotes(alto, ['F',0,3]) == -1:

            # print('alto range', voicing)
            voicings.pop(i)
            term -= 1
            continue
        if compareNotes(tenor, ['A',0,4]) == 1 or compareNotes(tenor, ['C',0,3]) == -1:
            # print('tenor range', voicing, tenor)
            voicings.pop(i)
            term -= 1
            continue
        if compareNotes(bass, ['E',0,4]) == 1:# or compareNotes(bass, ['F',0,2]) == -1:
            # print('bass range', voicing)
            voicings.pop(i)
            term -= 1
            continue
        i += 1
    # print('SIFTED: ', voicings)
    
#gets all the possible voicings for a single chord given melody note
def getPossibleVoicings(tonic, mode, numerals, soprano, parts):
    possibleVoicings = []
    numeral = copy.copy(numerals[-1])
    chord = chordFromNumeral(tonic, mode, numeral)
    if '7' in numeral:
        for bassStepsBelowSoprano in [8,9,7,10,6,11,5,4,12]:

            voicing = [soprano, None, None, None]
            bass = getChordalNote(soprano, chord, -bassStepsBelowSoprano)
            voicing[3] = bass
            for altoStepsBelowSoprano in range(4):
                alto = getChordalNote(soprano, chord, -altoStepsBelowSoprano)
                voicing[1] = alto
                for tenorStepsBelowAlto in range(4):
                    tenor = getChordalNote(alto, chord, -tenorStepsBelowAlto)
                    voicing[2] = tenor
                    possibleVoicings.append(copy.deepcopy(voicing))
                    
            alto = copy.copy(soprano)
            tenor = getChordalNote(alto, chord, -1)
    else:
        for bassStepsBelowSoprano in [6,7,5,4,8,3]:

            voicing = [soprano, None, None, None]
            bass = getChordalNote(soprano, chord, -bassStepsBelowSoprano)
            voicing[3] = bass
            for altoStepsBelowSoprano in range(4):
                alto = getChordalNote(soprano, chord, -altoStepsBelowSoprano)
                voicing[1] = alto
                for tenorStepsBelowAlto in range(4):
                    tenor = getChordalNote(alto, chord, -tenorStepsBelowAlto)
                    voicing[2] = tenor
                    possibleVoicings.append(copy.deepcopy(voicing))
                    
            alto = copy.copy(soprano)
            tenor = getChordalNote(alto, chord, -1)
    #siftVoicings(tonic, mode, possibleVoicings, chord, numeral, parts)
    return possibleVoicings
def unisonVoicing(voicing):
    for i in range(len(voicing)):
        for j in range(len(voicing)):
            if i != j and voicing[i] == voicing[j]:
                return True
    return False

#returns if given voicing is in root position with doubled root
def rootPosition(tonic, mode, voicing, numeral):
    chord = chordFromNumeral(tonic, mode, numeral)
    if voicing[3][:-1] != chord[0]: return False
    if not isDoubled(voicing, chord[0]): return False
    return True
def siftVoiceLeading(tonic, mode, voicings, numerals, parts, lvMaxIntApart):
    if len(parts) == 0:
        return voicings
    n1 = numerals[len(parts)]
    c1 = chordFromNumeral(tonic, mode, n1)
    if len(parts) >= 1:
        v2 = parts[-1]
        n2 = numerals[len(parts)-1]
        c2 = chordFromNumeral(tonic, mode, n2)
    if len(parts) >= 2:
        v3 = parts[-2]
        n3 = numerals[len(parts)-2]
        c3 =  chordFromNumeral(tonic, mode, n3)
    leadingTone = getScale(tonic, mode)[7]
    
    #first organize by middle voice movement (less is best)
    i = 0
    term = len(voicings)
    smallestDist = 8
    while i < term:
        v1 = copy.deepcopy(voicings[i])
        
        #pop voicings that violate max interval apart
        boolBreak = False
        for innerVoice in range(1,3):
            #check if any leaps in inner voices above lvMaxIntApart
            if int(interval(v1[innerVoice], v2[innerVoice])[1:]) > lvMaxIntApart:
                #(v1[innerVoice], v2[innerVoice]),'MAX LEAPS',innerVoice)
                #print('inner voices leap')
                voicings.pop(i)
                term -= 1
                boolBreak = True
                break
        if boolBreak: 
            continue
        
        averageDist = (int(interval(v1[1], v2[1])[1:]) + int(interval(v1[2], v2[2])[1:]))/2
        if averageDist < smallestDist:
            smallestDist = averageDist
            voicings.insert(0, voicings.pop(i))
            i += 1
            continue
        i += 1
    i = 0
    term = len(voicings)
    while i < term:
        v1 = copy.deepcopy(voicings[i])
        boolBreak = False

        #don't allow the bass to leap above an octave
        if int(interval(v1[3], v2[3])[1:]) > 8:
            voicings.pop(i)
            term -= 1
            #print('bass leap')
            continue

        #7th of a chord must resolve down
        if '7' in n1:
            for j in range(4): 
                if v1[j][:-1] == chordFromNumeral(tonic, mode, n1)[3]:
                    if not (int(interval(v1[j], v2[j])[1:]) == 2 and 
                            compareNotes(v1[j], v2[j]) == 1):
                            voicings.pop(i)
                            term -= 1
                            boolBreak = True
                            #print('7th resolve')
                            break
            if boolBreak: continue
        #leading tone must resolve if in outer voices
        for j in [3]:
            if (v1[j][:-1] == leadingTone and (not(v2[j][:-1] == tonic
                and compareNotes(v1[j], v2[j]) == - 1))):
                if j == 0:
                    raise Exception('Leading tone in melody not resolved')
                voicings.pop(i)
                term -= 1
                boolBreak = True
                #print('leading tone resolve')
                break
        if boolBreak: continue   

        #do the same for secondary dominant chords    
        if ('V/' in n1 and n1 != n2) or ('V7/' in n1 and n1 != n2): 
            third = chordFromNumeral(tonic, mode, n1)[1]
            for j in [0,3]:
                if (v1[j][:-1] == third and steps(v1[j], v2[j]) != 2):
                    voicings.pop(i)
                    term -= 1
                    boolBreak = True
                    #print('leading tone resolve')
                    break
            if boolBreak: continue        



        #voice overlap
        for voice in range(4):
            if voice != 0:
                if compareNotes(v1[voice], v2[voice-1]) != compareNotes(v1[voice], v1[voice-1]):
                    voicings.pop(i)
                    term -= 1
                    boolBreak = True
                    break
            if voice != 3:
                if compareNotes(v1[voice], v2[voice+1]) != compareNotes(v1[voice], v1[voice+1]):
                    voicings.pop(i)
                    term -= 1
                    boolBreak = True
                    break
        if boolBreak: continue

        #cadencing convention, root position V - I PAC
        if len(parts) == 1:
            if n1 == 'V':
                if (not(rootPosition(tonic, mode, parts[0], numerals[0]) 
                    and rootPosition(tonic, mode, v1, numerals[1]))):
                    voicings.append(voicings.pop(i))
                    term -= 1
                    #('cadencing convention')
                    continue
        #first inversion rules
        if len(parts) >= 1:
            if v2[3][:-1] == chordFromNumeral(tonic, mode, n2)[1]:
                if abs(steps(v1[3],v2[3])) != 2:
                    voicings.pop(i)
                    term -= 1
                    continue
        #second inversion rules - passing, neighboring, cadential
        if v2[3][:-1] == chordFromNumeral(tonic, mode, n2)[2]:
            if len(parts) >= 2:
                bass1 = v1[3]
                bass2 = v2[3]
                bass3 = v3[3]
                if not (n2 == 'I' and n1 in ['ii','vi']):
                    if ((not (bass1 == bass2 and bass2 == bass3)) and
                        (not ((int(interval(bass1, bass2)[1:])) == 2 and 
                            (int(interval(bass2, bass3)[1:])) == 2 and
                            compareNotes(bass1, bass2) == compareNotes(bass2, bass3)))):
                        voicings.pop(i)
                        term -= 1
                        #print('invalid second inversion', v1)
                        continue

            # elif len(parts) >= 1:
            #     if not (n1 == 'I' and n2 == 'V' and
            #             v2[3][:-1] == chordFromNumeral(tonic, mode, n2)[0]):
            #             voicings.pop(i)
            #             term -= 1
            #             print('invalid second inversion')
            #             continue
        
        #cadential 64
        if n2 == 'I' and n1 in ['ii','iio/7','VI','ii7','vi']:
            if not len(parts) >= 2:
                voicings.pop(i)
                term -= 1
                continue
                #print('invalid cadential 64')
            if (not (n3 in ['V','V7'] and v2[3][:-1] == v3[3][:-1] and 
                v3[3][:-1] != chordFromNumeral(tonic, mode, n3)[2]) or
                len(parts) <= 2):
                voicings.pop(i)
                term -= 1
                #print('invalid cadential 64')
                continue
      
        #7th chord rules
        if len(parts) >= 1 and '7' in n1:
            if v1[3][:-1] == c1[3]: #V42
                if steps(v1[3], v2[3]) != -2:
                    voicings.pop(i)
                    term -= 1
                    continue

            



        i += 1

    #Bass motion preferences
    i = 0
    term = len(voicings)
    boolBreak = False
    # don't allow the bass to repeat if it doesn't have to
    while i < term:
        v1 = copy.deepcopy(voicings[i])
        if len(parts) >= 1:
            if v1[3] == v2[3]:
                voicings.append(voicings.pop(i))
                term -= 1
                continue

        i += 1

    i = 0
    term = len(voicings)
    while i < term:  
    
        v1 = copy.deepcopy(voicings[i])
        boolBreak = False    
        #no augmented leaps
        if len(parts) >= 1:
            for voice in range(1,4):
                if interval(v1[voice],v2[voice])[0] == 'A':
                    voicings.pop(i)
                    term =- 1
                    boolBreak = True
                    break
        if boolBreak: continue
        i += 1
    i = 0
    term = len(voicings)
    while i < term:  
    
        v1 = copy.deepcopy(voicings[i])
        boolBreak = False    
        #check for illegal 5ths and octaves
        for m in range(3, 0, -1):
            for n in range(m-1, -1, -1):
                if (trueInterval(interval(v1[m], v1[n])) == 'P1' 
                    and trueInterval(interval(v2[m], v2[n])) == 'P1'
                    and compareNotes(v1[m], v2[m]) != 0):
                    # print('parallel octaves',m,n, v1)
                    voicings.pop(i)
                    term -= 1
                    boolBreak = True
                    break
                if (trueInterval(interval(v1[m], v1[n])) in ['P5','d5'] 
                    and trueInterval(interval(v2[m], v2[n])) == 'P5'
                    and compareNotes(v1[m], v2[m]) != 0):
                    # print('parallel fifths',v1,v2,m,n)
                    voicings.pop(i)
                    term -= 1
                    boolBreak = True
                    break
                if m == 3 and n == 0:

                    if (trueInterval(interval(v2[m], v2[n])) == 'P5' 
                        and (compareNotes(v1[m], v2[m]) == compareNotes(v1[n], v2[n])) and
                        compareNotes(v1[m], v2[m]) != 0 and int(interval(v1[n], v2[n])[1:]) >= 3):
                        #print('direct fifths', v1, v2)
                        voicings.pop(i)
                        term -= 1
                        boolBreak = True
                        break
                    if (trueInterval(interval(v2[m], v2[n])) == 'P1'
                        and (compareNotes(v1[m], v2[m]) == compareNotes(v1[n], v2[n])) and
                        compareNotes(v1[m], v2[m]) != 0 and int(interval(v1[n], v2[n])[1:]) >= 3):
                        #print('direct octaves', v1, v2)
                        voicings.pop(i)
                        term -= 1
                        boolBreak = True
                        break
            if boolBreak: break
        if boolBreak: continue
        i += 1

    # i = 0
    # term = len(voicings)
    # while i < term:  
    
    #     v1 = copy.deepcopy(voicings[i])
    #     boolBreak = False    
    #     #no augmented leaps
    #     if len(parts) >= 1:
    #         for voice in range(1,4):
    #             if interval(v1[voice],v2[voice])[0] == 'A':
    #                 print(v1,v2,voice)
    #                 voicings.pop(i)
    #                 term =- 1
    #                 boolBreak = True
    #                 break
    #     if boolBreak: continue

    # print('sifted VL: ',voicings)
#prioritizes root position for I, IV, V chords after sift
#pushes second inversion chords to the back
def prioritizeInversions(tonic, mode, voicings, numeral):

    if mode == "major":
        i = 0
        term = len(voicings)
        while i < term:
            v = copy.deepcopy(voicings[i])
            if rootPosition(tonic, mode, v, numeral) and numeral in ['I','IV','V']:
                voicings.insert(0,voicings.pop(i))
                i += 1
                continue
            i += 1

#returns whether or not a note is doubled in voicing
def isDoubled(voicing, note):
    count = 0
    for i in range(len(voicing)):
        if removeRegister(voicing[i]) == note:
            count += 1
        if count == 2:
            return True
    return False
#returns a list of valid cadences, indexed by strength from left to right
def getCadences(tonic, mode, voicings, numeral):
    cadences = copy.deepcopy(voicings)
    soprano = voicings[0][0]
    chord = chordFromNumeral(tonic, mode, numeral)
    root = chord[0]
    third = chord[1]
    fifth = chord[2]
    if numeral == 'I':
        root = copy.copy(tonic)
    elif numeral == 'V':
        root = getScale(tonic, mode)[5]
    elif numeral == 'IV':
        root = getScale(tonic, mode)[4]
    elif numeral == 'V/V':
        root = getScale(tonic, mode)[2]
    elif numeral == 'V/ii':
        root = getScale(tonic, mode)[6]
    elif numeral == 'V/vi':
        root = getScale(tonic, mode)[3]
    elif numeral == 'V/iii':
        root = getScale(tonic, mode)[7]
    elif numeral == 'V7/IV':
        root = getScale(tonic, mode)[1]

    i = 0
    term = len(cadences)
    while i < term:
        v = copy.deepcopy(cadences[i])
        #cannot cadence on a 64 chord
        if not rootPosition(tonic, mode, v, numeral):
            cadences.pop(i)
            term -= 1
            continue
        i += 1
    i = 0

    term = len(cadences)
    while i < term:
        v = copy.deepcopy(cadences[i])
        if int(interval(v[3],v[2])[1:]) == 10:
            cadences.insert(0, cadences.pop(i))
            i += 1
            continue
        i += 1
    i = 0
    term = len(cadences)
    while i < term:
        v = copy.deepcopy(cadences[i])
        if int(interval(v[3],v[2])[1:]) == 5:
            cadences.insert(0,cadences.pop(i))
            i += 1
            continue
        i += 1
    
    #prioritize PAC
    i = 0
    term = len(cadences)
    while i < term:
        v = copy.deepcopy(cadences[i])
        if not isDoubled(v, root):
            cadences.append(cadences.pop(i))
            term -= 1
            continue
        i += 1
    
    return cadences

def getVLPath(tonic, mode, numerals, parts, allPossibleVoicings, originalVoicings, index, lvMaxIntApart, length, depth):
    
    if depth == 100: return None
    if len(parts) == len(originalVoicings):
        return parts

    numeral = numerals[index]
    siftVoicings(tonic, mode, allPossibleVoicings[index], chordFromNumeral(tonic, mode, numeral), numeral, parts[:index])
    siftVoiceLeading(tonic, mode, allPossibleVoicings[index], numerals, parts[:index], lvMaxIntApart)
  
    if len(allPossibleVoicings[index]) > 0:
        parts.append(copy.deepcopy(allPossibleVoicings[index][0]))
        return getVLPath(tonic, mode, numerals, parts, allPossibleVoicings, originalVoicings, index + 1, lvMaxIntApart, length, depth+1)
    if len(parts) == 0:
        return None
    popped = parts.pop()

    allPossibleVoicings[index-1].pop(allPossibleVoicings[index-1].index(popped))

    copyListFromIndex(allPossibleVoicings, copy.deepcopy(originalVoicings), index)
    assert(allPossibleVoicings[index:] == originalVoicings[index:])
    return getVLPath(tonic, mode, numerals, parts, allPossibleVoicings, originalVoicings, index - 1, lvMaxIntApart, length, depth+1)


