#harmony.py
#Forest Ma
#calculates four-part harmony given a melody from main.py

import copy
import random
from music import *

###===========================================
###    STARTING POINT: genHarmonyRecursive
###===========================================
#recursively calculates roman numeral analysis and part writing simultaneously,
#backtracking if their invalidities in either the RN analysis or the part writing
#starting from the cadence (right to left)
def genHarmonyRecursive(melody, tonic, mode, curNumerals, parts, allPossibleVoicings, lvMaxIntApart, length):
    
    if melody == []:
        print('done:',parts)
        return parts

    note = melody[-1]

    if curNumerals == []:
        prio = getCadenceNumeral(tonic, mode, note, [])

    elif len(curNumerals) == length - 1:

        prio = getCadenceNumeral(tonic, mode, note, getPriorityList(curNumerals[-1], mode))
        print('cadNum:', prio)
    else:
        prio = getPriorityList(curNumerals[-1], mode)
    originalPrio = copy.deepcopy(prio)

    i = 0
    term = len(prio)
    while i < term:
        if not isGoodProgression(curNumerals, prio[i], melody):
            prio.append(prio.pop(i))
            term -= 1
        else:
            i += 1
    for i in range(len(prio)):
        originalNumerals = copy.deepcopy(curNumerals)
        originalParts = copy.deepcopy(parts)
        originalVoicings = copy.deepcopy(allPossibleVoicings)
        #check if numeral is possible given note
        print(prio[i])
        if note[:-1] in chordFromNumeral(tonic, mode, prio[i]):
            print(note[:-1], 'fits in ', prio[i])
            curNumerals.append(prio[i]) #add to cur
            print('NUMERALS:',curNumerals[::-1])

        else:
            print('continuing:', note[:-1], 'doesnt fit in ', prio[i])
            continue #go next in priority list if current numeral not possible

        #chord is available/possible at this point, already added to current
        #check for imperfections with isGoodProgression, or just proceed if
        #i is last in the priority list
        #generateVoices generates the other three parts and returns true
        #if there is a solution to the part writing - if false, this
        #call of the function returns None
        if voiceLeadingPossible(tonic, mode, parts, curNumerals, melody, allPossibleVoicings, lvMaxIntApart, length):
            solution = genHarmonyRecursive(melody[:-1], tonic, mode, curNumerals, parts, allPossibleVoicings, lvMaxIntApart, length)

            if solution != None:  
                return solution
        else:
            #print(allPossibleVoicings[-1],'---',parts)
            print('vl not possible')


        curNumerals = copy.deepcopy(originalNumerals)
        parts = copy.deepcopy(originalParts)
        prio = copy.deepcopy(originalPrio)
        allPossibleVoicings = copy.deepcopy(originalVoicings)
        
        print('------------\n','preserve original numerals:', curNumerals[::-1],'\nPARTS:',parts[::-1],'\n------------') 
    return None

# ====================================================#

###===========================================
###    voiceLeadingPossible + all helpers
###===========================================
#generates VL possibilities, returns false if there is no possible solution
#in which case the algorithm backtracks
#soprano is the melody note
def voiceLeadingPossible(tonic, mode, parts, numerals, melody, allPossibleVoicings, lvMaxIntApart, length):
    
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
    if len(allPossibleVoicings) < 2:
        siftVoicings(tonic, mode, allPossibleVoicings[0], chord, numeral, parts)
        cadences = getCadences(tonic, mode, allPossibleVoicings[0], numeral)
        print('CADENCES: ', cadences)
        allPossibleVoicings[0] = copy.deepcopy(cadences)
        
        parts.append(cadences[0])
        return True
    #checks if the newest set of possible voicings allows for legal voice leading
    if len(allPossibleVoicings) == length:
        cadences = getCadences(tonic, mode, allPossibleVoicings[-1], numeral)
        print('cad',cadences)
        allPossibleVoicings[-1] = copy.deepcopy(cadences)
    solution = getVLPath(tonic, mode, numerals, copy.deepcopy(parts), copy.deepcopy(allPossibleVoicings), len(parts), lvMaxIntApart)
    if solution == None: return False
    copyList(parts, solution)
    print('PARTS:', parts[::-1])
    return True
    
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
        elif numeral == 'viio':
            return [scale[7]] + [scale[2]] + [scale[4]]
        elif numeral == 'V7':
            return [scale[5]] + [scale[7]] + [scale[2]] + [scale[4]]
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
    else: #minor
        pass
    
def getPriorityList(numeral, mode): #numerals from right to left from cadence
    if mode == "major":

        if numeral == 'I':
            return ['V','V7','IV','I','ii','vi']#allow ii, vi to precede a cadential 64
        elif numeral == 'ii':
            return ['IV','vi','I','V7/ii','V/ii','ii']
        elif numeral == 'iii':
            return ['vi','I','IV','V7/iii','V/iii']
        elif numeral == 'IV':
            return ['I','vi','V7/IV','IV']
        elif numeral == 'V':
            return ['ii','IV','V7/V','V/V','I','V']
        elif numeral == 'vi':
            return ['V','iii','V7/vi','V/vi','I','vi']

        #     return ['IV','vi','V/vi','V/V','iii']
        # elif numeral == 'IV':
        #     return ['V','ii','I','V/V','IV']
        # elif numeral == 'V':
        #     return ['I','vi','V7','V','V/vi']
        # elif numeral == 'vi':
        #     return ['IV','ii','V/V','V/vi','vi']


        elif numeral == 'viio':
            pass
        elif numeral == 'ii7':
            pass
        elif numeral == 'iii7':
            pass
        elif numeral == 'IV7':
            pass
        elif numeral == 'V7':
            return ['ii','IV','V/V','I','vi','V']
        elif numeral == 'vi7':
            pass
        elif numeral == 'viio7':
            pass
        elif numeral == 'V/ii' or numeral == 'V7/ii':
            return ['I','vi','V','iii','ii','V/ii']
        elif numeral == 'V/V' or numeral == 'V7/V':
            return ['vi','IV','iii','I','V','V/V']
        elif numeral == 'V/vi' or numeral == 'V7/vi':
            return ['V','V7','iii','vi','V/vi']
        elif numeral == 'V/iii' or numeral == 'V7/iii':
            return ['I','iii','vi','IV']
        elif numeral == 'V7/IV':
            return ['I','IV','V']

        return
    if mode == "minor":
        raise Exception("unfinished")
    raise Exception("invalid mode")

#checks for strength of progressions, duplicate sequences, etc
#precondition: numerals is already a valid progression
def isGoodProgression(numerals, next, melody): #right to left, starting from cadence
    
    numerals = copy.copy(numerals)
    numerals.append(next)
    if len(numerals) >= 3:
        for i in range(len(numerals) - 2):
            #allow consecutive numerals but not 3 in a row
            if numerals[i] == numerals[i+1] == numerals[i+2]:
                return False
    
    if len(numerals) >= 4:
        for i in range(len(numerals) - 3):
            #don't allow consecutive progressions
            if numerals[i:i+2] == numerals[i+2:i+4]:
                return False
    
    # for i in range(len(numerals)):
    #     print(melody[len(melody)-i-1], numerals[i])
        #assert(melody[len(melody)-i-1] in chordFromNumeral(['C',0],'major',numerals[i]))

    return True

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
                print('available',available)
                return [numeral]
    
    return []

#gets a specified note with register from a chord given a starting note and a diretion/vector
#input note MUST BE IN THE CHORD
def getChordalNote(note, chord, vector):
    chord = copy.deepcopy(chord)
    if note[:-1] not in chord: raise Exception("inputted note not in inputted chord")
    if vector == 0:
        return note

    direction = int(vector/abs(vector))
    resultNote = chord[(chord.index(note[:-1]) + vector)%(len(chord))]
    octaveDiff = (abs(vector) // len(chord)) * direction

    if interval(chord[0], chord[1]) == "M3":    
        scale = toNoteScale(getScale(chord[0], "major"))[1:]
    else:
        scale = toNoteScale(getScale(chord[0], "minor"))[1:]
    
    #loop to see if there is a C in between the two notes, if so, register increments
    if direction == 1:
        i = scale.index(note[0]) + 1
        if i == len(scale): i == 0
        while i != scale.index(resultNote) + 1:
            if scale[i][0] == 'C':
                octaveDiff += direction
                break
            i += direction
            if i == len(scale):
                i = 0
    else:
        #print(note[:-1], '--',scale, '--',chord, vector)
        i = scale.index(note[0])

        if i == -1: i = len(scale) - 1
        #print(resultNote, scale)
        resultNoteIndex = scale.index(resultNote[0]) - 1

        if resultNoteIndex == -1: resultNoteIndex = len(scale) - 1
        while i != resultNoteIndex:
            if scale[i][0] == 'B' and note[0] != 'B':
                octaveDiff += direction
                break
            i += direction
            if i == -1:
                i = len(scale) - 1 
    
    resultNote.append(note[2] + octaveDiff)
    return resultNote

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
            if voicing == [['D', 0, 5], ['D', 0, 4], ['F', 0, 3], ['A', 0, 2]]:
                print('HERE')
            if len(parts) >= 1:
                v2 = parts[-1]
            soprano = voicing[0]
            alto = voicing[1]
            tenor = voicing[2]
            bass = voicing[3]
            

            #general rule across all inversions - can't double leading tone
            if isDoubled(voicing, getScale(tonic, "major")[7]):
                voicings.pop(i)
                term -= 1
                continue
                
            #cannot double the third of V/_ chords
            if 'V/' in numeral and isDoubled(voicing, third):
                voicings.pop(i)
                term -= 1
                continue

            #don't want tenor to be too high
            if (compareNotes(tenor, ['G',0,4]) > 0 and 
                compareNotes(soprano, ['G',0,5]) <= 0):
                voicings.pop(i)
                term -= 1
                print('hi')
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

            #if the bass is 2 octaves down from tenor (or more), push to back of list
            if int(interval(voicing[2],voicing[3])[1:]) > 10:
                voicings.append(voicings.pop(i))
                term -= 1
                continue
            
            #if the tenor is above E4, push to back of the list
            if compareNotes(tenor, ['E',0,4]) == 1:
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
    if mode == "minor":
        pass

        
        #first inversion chords allowed: I, ii, IV, V


        
    #this loop eliminates badly spaced chords, incomplete chords, and 
    #pushes chords with unisons to the back of the list
    #consistent with either mode
    i = 0
    term = len(voicings)
    while i < term:
        boolBreak = False
        voicing = copy.deepcopy(voicings[i])
        
        if not ((validAdjacentNotes(voicing[0], voicing[1]) and
                validAdjacentNotes(voicing[1], voicing[2]) and
                compareNotes(voicing[2], voicing[3]) >= 0)):
            voicings.pop(i)
            term -= 1
            
            continue
        voicingNoRegister = removeRegister(voicing)
        for j in range(len(chord)):
            if chord[j] not in voicingNoRegister:
                voicings.pop(i)
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
        i += 1
    print('SIFTED: ', voicings)
    
#gets all the possible voicings for a single chord given melody note
def getPossibleVoicings(tonic, mode, numerals, soprano, parts):
    possibleVoicings = []
    numeral = copy.copy(numerals[-1])
    chord = chordFromNumeral(tonic, mode, numeral)
    if numeral == 'V7' or '/' in numeral:
        for bassStepsBelowSoprano in [8,9,7,10,6,11,12]:

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
        print(voicings)
        return voicings[0]
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
            if int(interval(v1[innerVoice], v2[innerVoice])[1]) > lvMaxIntApart:
                print(interval(v1[innerVoice], v2[innerVoice]),'MAX LEAPS',innerVoice)

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
            print('bass leap')
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
                            print('7th resolve')
                            break
            if boolBreak: continue
        #leading tone must resolve if in outer voices
        for j in [0,3]:
            if (v1[j][:-1] == leadingTone and (not(v2[j][:-1] == tonic
                and compareNotes(v1[j], v2[j]) == - 1))):
                if j == 0:
                    raise Exception('Leading tone in melody not resolved')
                voicings.pop(i)
                term -= 1
                boolBreak = True
                print('leading tone resolve')
                break
        if boolBreak: continue        

        #check for illegal 5ths and octaves
        for m in range(3, 0, -1):
            for n in range(m-1, -1, -1):
                        
                if (interval(v1[m], v1[n]) == 'P8' and interval(v2[m], v2[n]) == 'P8'
                    and compareNotes(v1[m], v2[m]) != 0):
                    print('parallel octaves',m,n, v1)
                    voicings.pop(i)
                    term -= 1
                    boolBreak = True
                    break
                if (interval(v1[m], v1[n]) in ['P5','d5'] and interval(v2[m], v2[n]) == 'P5'
                    and compareNotes(v1[m], v2[m]) != 0):
                    print('parallel fifths',m,n)
                    voicings.pop(i)
                    term -= 1
                    boolBreak = True
                    break
                if m == 3 and n == 0:

                    if ((interval(v2[m], v2[n]) == 'P12' or interval(v2[m], v2[n]) == 'P19' or interval(v2[m], v2[n]) == 'P24' or interval(v2[m], v2[n]) == 'P5')
                        and (compareNotes(v1[m], v2[m]) == compareNotes(v1[n], v2[n])) and
                        compareNotes(v1[m], v2[m]) != 0 and int(interval(v1[n], v2[n])[1:]) >= 3):
                        print('direct fifths', v1, v2)
                        voicings.pop(i)
                        term -= 1
                        boolBreak = True
                        break
                    if ((interval(v2[m], v2[n]) == 'P8' or interval(v2[m], v2[n]) == 'P15' or interval(v2[m], v2[n]) == 'P22')
                        and (compareNotes(v1[m], v2[m]) == compareNotes(v1[n], v2[n])) and
                        compareNotes(v1[m], v2[m]) != 0 and int(interval(v1[n], v2[n])[1:]) >= 3):
                        print('direct octaves', v1, v2)
                        voicings.pop(i)
                        term -= 1
                        boolBreak = True
                        break
            if boolBreak: break
        if boolBreak: continue
        #cadencing convention, root position V - I PAC
        if len(parts) == 1:
            if n1 == 'V':
                if (not(rootPosition(tonic, mode, parts[0], numerals[0]) 
                    and rootPosition(tonic, mode, v1, numerals[1]))):
                    voicings.pop(i)
                    term -= 1
                    print('cadencing convention')
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
                        print('invalid second inversion', v1)
                        continue

            # elif len(parts) >= 1:
            #     if not (n1 == 'I' and n2 == 'V' and
            #             v2[3][:-1] == chordFromNumeral(tonic, mode, n2)[0]):
            #             voicings.pop(i)
            #             term -= 1
            #             print('invalid second inversion')
            #             continue
        
        #cadential 64
        if len(parts) >= 2 and n2 == 'I' and n1 in ['ii','vi']:
            if not (n3 in ['V','V7'] and v2[3][:-1] == v3[3][:-1] and 
                v3[3][:-1] != chordFromNumeral(tonic, mode, n3)[2]):
                voicings.pop(i)
                term -= 1
                print('invalid cadential 64')
                continue
      
        #7th chord rules
        if len(parts) >= 1 and '7' in n1:
            if v1[3][:-1] == c1[3]:
                if not (int(interval(v1[3], v2[3])[1:]) == 2 
                    and compareNotes(v1[3],v2[3]) == -1):
                    voicings.pop(i)
                    term -= 1
                    continue
            
        i += 1
    print('sifted VL: ',voicings)

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
    cadences = []
    soprano = voicings[0][0]
    chord = chordFromNumeral(tonic, mode, numeral)
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
    for i in range(len(voicings)):
        #best case is root to be doubled, root position (PAC or IAC)
        #if soprano is the root
        scale = ['C','D','E','F','G','A','B']
        if scale.index(soprano[0]) - scale.index(chord[0][0]) >= 0:
            if (root == removeRegister(voicings[i])[3] and isDoubled(voicings[i], root)
                and voicings[i][3][2] == voicings[i][0][2] - 2):
                cadences.append(copy.deepcopy(voicings[i]))
        else:
            if (root == removeRegister(voicings[i])[3] and isDoubled(voicings[i], root)
                and voicings[i][3][2] == voicings[i][0][2] - 3):
                cadences.append(copy.deepcopy(voicings[i]))

    return cadences

#called when the current path is not a solution, starts from cadence
#to find a new solution
def getVLPath(tonic, mode, numerals, parts, allPossibleVoicings, index, lvMaxIntApart):
    if len(parts) == len(allPossibleVoicings[:index+1]):
        return parts
    originalVoicings = copy.deepcopy(allPossibleVoicings[index])
    numeral = numerals[index]
    siftVoicings(tonic, mode, allPossibleVoicings[index], chordFromNumeral(tonic, mode, numeral), numerals, parts[:index])
    print(index)
    if allPossibleVoicings[0] == []: return None
    siftVoiceLeading(tonic, mode, allPossibleVoicings[index], numerals, parts[:index], lvMaxIntApart)
    for i in range(len(allPossibleVoicings[index])):
        parts.append(copy.deepcopy(allPossibleVoicings[index][i]))
        print('PASSED: ', parts[-1], i, len(allPossibleVoicings[index]))
        return getVLPath(tonic, mode, numerals, parts, allPossibleVoicings, index + 1, lvMaxIntApart)

    popped = parts.pop(-1)
    print('POPPED: ', popped, 'PARTS:', parts[::-1])
    allPossibleVoicings[index-1].pop(allPossibleVoicings[index-1].index(popped))
    allPossibleVoicings[index] = originalVoicings
    return getVLPath(tonic, mode, numerals, parts, allPossibleVoicings, index - 1, lvMaxIntApart)



#melody = [['G', 0, 5], ['B', 0, 5], ['C', 0, 6], ['A', 0, 5], ['B', 0, 5], ['G', 0, 5], ['A', 0, 5], ['F', 1, 5], ['G', 0, 5]]

#melody = [['E', 0, 5], ['F', 0, 5], ['G', 0, 5], ['B', 0, 4], ['C', 0, 5], ['D', 0, 5], ['C', 0, 5], ['B', 0, 4], ['C', 0, 5]]
# melody = [['B', 0, 4], ['C', 0, 5], ['D', 0, 5], ['E', 0, 5], ['D', 0, 5], ['C', 0, 5], ['B', 0, 4], ['A', 0, 4], ['G', 0, 4]]
# melody = [['E', 0, 4], ['F', 0, 4], ['G', 0, 4], ['A', 0, 4], ['G', 0, 4], ['F', 0, 4], ['E', 0, 4], ['D', 0, 4], ['C', 0, 4]]


#melody = [['C', 1, 5], ['D', 0, 5], ['F', 0, 5], ['E', 0, 5], ['A', 0, 5],['G', 0, 5], ['F', 0, 5], ['E', 0, 5], ['D', 1, 5], ['E', 0, 5], ['C', 1, 5], ['D', 0, 5], ['C', 0, 5], ['B', 0, 4], ['C', 0, 5]]
# #CDFEAGFED#EC#DCBC
# melody = [['E', 0, 5], ['D', 0, 5], ['C', 1, 5], ['D', 0, 5], ['E', 0, 5],['E', 0, 5], ['E', 0, 5], ['D', 0, 5], ['D', 0, 5], ['D', 0, 5], ['E', 0, 5], ['A', 0, 5], ['A', 0, 5]]
#melody = [['C', 0, 5], ['G', 0, 5], ['C', 0, 5], ['G', 0, 5], ['C', 0, 5], ['G', 0, 5], ['C', 0, 5], ['G', 0, 5], ['C', 0, 5]]

# melody = [['G', 0, 5], ['C', 0, 5], ['D', 0, 5], ['E',0,0],['G', 0, 5], ['E', 0, 5],['D', 0, 5], ['G', 0, 5]]
# melody = [['G', 0, 5], ['C', 0, 5], ['D', 0, 5], ['E', 0, 5], ['D', 0, 5],['E', 0, 5],['A', 0, 5], ['G', 0, 5], ['E', 0, 5], ['D', 0, 5], ['C', 0, 5],['A', 0, 5]]
# melody = [['G', 0, 5], ['C', 0, 5], ['D', 0, 5], ['E', 0, 5], ['D', 0, 5],['E', 0, 5],['A', 0, 5], ['G', 0, 5], ['E', 0, 5], ['D', 0, 5], ['C', 0, 5],['A', 0, 5]]
# melody = [['G', 0, 5], ['C', 0, 5], ['D', 0, 5], ['E', 0, 5], ['D', 0, 5],['E', 0, 5],['A', 0, 5], ['G', 0, 5], ['E', 0, 5], ['D', 0, 5], ['C', 0, 5],['A', 0, 5]]
# melody = [['G', 0, 5], ['C', 0, 5], ['D', 0, 5], ['E', 0, 5], ['G', 0, 5],['E', 0, 5],['D', 0, 5], ['C', 0, 5], ['A', 0, 5], ['C', 0, 5], ['A', 0, 5],['C', 0, 5]
#           ,['A', 0, 5], ['G', 0, 5], ['C', 0, 5], ['D', 0, 5], ['E', 0, 5],['G', 0, 5],['A', 0, 5], ['G', 0, 5], ['E', 0, 5], ['D', 0, 5], ['C', 0, 5],['A', 0, 5],['G',0,0],['C',0,0]]
# melody = [['C', 0, 5], ['G', 0, 5], ['F', 1, 5], ['A', 0, 5], ['G', 0, 5],['B', 0, 5], ['C', 0, 5]]

#CDFEAGFEGG#AF#Gdown to BC
#melody = [['D', -1, 4], ['D', -1, 5], ['C',0,5], ['D', -1, 5], ['G', -1, 4], ['G', 0, 4], ['A', -1, 4], ['G', -1, 4], ['F', 0, 4], ['E', -1, 4], ['A', -1, 4], ['A', 0, 4], ['B', -1, 4], ['G', 0, 4], ['A', -1, 4], ['C', 0, 4], ['D', -1, 4]]
#melody = [['D', 0, 5], ['A', 0, 5], ['F', 1, 5], ['D', 0, 5], ['C', 1, 5], ['D', 0, 5], ['E', 0, 5], ['F', 1, 5], ['G', 0, 5],['F', 1, 5],['E', 0, 5],['D', 0, 5]]
#melody = [['C', 0, 5],['D', 0, 5],['E', 0, 5],['C', 0, 5],['C', 0, 5],['D', 0, 5],['E', 0, 5],['C', 0, 5],['E', 0, 5],['F', 0, 5],['G', 0, 5],['E', 0, 5],['F', 0, 5],['G', 0, 5]]
#Dflat4 Dflat5 C 
# parts = []
#genHarmonyRecursive(melody, ['C', 0], "major", [], [], [], 4, 15)
# parts = parts[::-1]
# print(parseToLilypond(parts))
#siftVoicings(['C', 0], "major", [[['D', 0, 5], ['D', 0, 4], ['F', 0, 3], ['A', 0, 2]]],[['D', 0], ['F', 0], ['A', 0]], 'ii', [])
#[['D', 0, 5], ['D', 0, 4], ['F', 0, 3], ['A', 0, 2]]



