import copy
from harmony import *
from NCTs import *



class Piece:
    #Function creates array of entries with minimum denomination of 32nd notes
    def __init__(self, tonic, mode, tstop, tsbottom, bars, parts, melody):
        self.tonic = tonic
        self.mode = mode
        self.tstop = tstop
        self.tsbottom = tsbottom
        self.bars = bars
        self.parts = parts
        self.size = 4*bars*tstop//tsbottom
        self.melody = melody
        self.romanNumerals = []

        #harmony array with all four parts
        self.parts = [[['_', 0, 0] for i in range(self.size)] for i in range(0, 4)]
        self.parts[0] = copy.deepcopy(self.melody)


    def generateHarmony(self):
        #different for major minor?**
        # romanNumerals = getRomanNumeralAnalysis(self.melodyArray, self.tonic, self.mode)
        # for i in range(self.parts):
        #     completePart(self.melodyArray, self.curPart, romanNumerals)
        #     self.result.append(self.curPart.copy())
        #     self.curPart = [['_', 0] for i in range(self.size)]
        lvMaxIntApart = 2
        genHarmonyRecursive(self.melody, self.tonic, self.mode, self.romanNumerals, self.parts, lvMaxIntApart)
    def printResult(self):
        pass
def parseToAbjad(parts):
    res = ["","","",""] #four strings for four different parts, SATB
    for x in range(len(parts)):
        voicing = parts[x]

        
        for i in range(4):
            if len(voicing) == 2 and voicing[0][i] != voicing[1][i]: #no NCTs
                duration = '8'
            else:
                duration = '4'
            if len(voicing) == 2 and voicing[0][i] != voicing[1][i]:
                
                for j in range(2):
                    res[i] += voicing[j][i][0].lower()
                    if voicing[j][i][1] >= 1:
                        accidental = "s"
                    elif voicing[j][i][1] <= -1:
                        accidental = "f"
                    else:
                        accidental = ""
                    accidental *= abs(voicing[j][i][1])
                    res[i] += accidental
                    
                    regDiff = voicing[j][i][2] - 3
                    if regDiff > 0:
            
                        registers = "'"*regDiff

                    elif regDiff < 0:
                        registers = ","*abs(regDiff)

                    else:
                        registers = ""
                    res[i] += registers
                    res[i] += duration
                    res[i] += " "
            else:
                res[i] += voicing[0][i][0].lower()
                if voicing[0][i][1] >= 1:
                    accidental = "s"
                elif voicing[0][i][1] <= -1:
                    accidental = "f"
                else:
                    accidental = ""
                accidental *= abs(voicing[0][i][1])
                res[i] += accidental
                
                regDiff = voicing[0][i][2] - 3
                if regDiff > 0:
        
                    registers = "'"*regDiff

                elif regDiff < 0:
                    registers = ","*abs(regDiff)

                else:
                    registers = ""
                res[i] += registers
                res[i] += duration
                res[i] += " "
    return res


def run(tonic, mode, melody):
    #adapted from Abjad Documentation https://abjad.github.io/
    # rh_voice_1 = abjad.Voice(name="RH_Voice1")
    # rh_voice_2 = abjad.Voice(name="RH_Voice2")
    # rh_staff = abjad.Staff([rh_voice_1], name="RH_Staff", simultaneous=True)
    # rh_staff.extend([rh_voice_1, rh_voice_2])
    # lh_voice_1 = abjad.Voice(name="LH_Voice_1")
    # lh_voice_2 = abjad.Voice(name="LH_Voice_2")
    # lh_staff = abjad.Staff(name="LH_Staff", simultaneous=True)
    # lh_staff.extend([lh_voice_1, lh_voice_2])
    # piano_staff = abjad.StaffGroup(lilypond_type="PianoStaff", name="Piano_Staff")
    # piano_staff.extend([rh_staff, lh_staff])
    # score = abjad.Score([piano_staff], name="Score")


    #generations that aren't desirable but still work
    savedParts = []
    parts = []
    foundGoodProg = False
    for i in range(5,6):
        harmony = genHarmonyRecursive(melody, tonic, mode, [], parts, [], [], i, len(melody))
        if harmony == None:
            if i == 5:
                raise Exception('harmony generation failed')
            else:
                parts = []
                continue
        else:
            
            parts = harmony[0]
            parts = parts[::-1]
            numerals = harmony[1]
            numerals = numerals[::-1]
            if goodStartEnd(tonic, mode, parts, numerals):
                foundGoodProg = True
                print('good',numerals)
                break
            else:
                savedParts.append(copy.deepcopy(parts))
                parts = []
                continue

    if not foundGoodProg:
        parts = savedParts[0]

    parts = genNonChordTones(tonic, mode, parts)
    return parts
    parsedParts = parseToAbjad(parts)
    # parsedParts = ["c8'' c8'' a' b' c'' ", "g' f8' f8' d' e' ", "e8' e8' c' g g ", 'c f g, c ']
    # parsedParts = ["c''8 a'4 b' c'' ", "g' f' d' e' ", "e' c' g g ", 'c f g, c ']
    print(parsedParts)

    rh1 = r"\voiceOne " + parsedParts[0]
    rh2 = r"\voiceTwo " + parsedParts[1]
    lh1 = r"\voiceOne " + parsedParts[2]
    lh2 = r"\voiceTwo " + parsedParts[3]

    # rh_voice_1.extend(rh1)
    # rh_voice_2.extend(rh2)
    # lh_voice_1.extend(lh1)
    # lh_voice_2.extend(lh2)
    # clef = abjad.Clef("bass")
    # note1 = abjad.select.note(lh_voice_1, 0)
    # abjad.attach(clef, note1)
    # note2 = abjad.select.note(lh_voice_2, 0)
    # abjad.attach(clef, note2)
    # abjad.show(score)
    # playback(parts)


# def playback(parts):
#     s = Session()
#     soprano = s.new_part("piano")
#     alto = s.new_part("piano")
#     tenor = s.new_part("piano")
#     bass = s.new_part("piano")
#     SATB = {soprano: 0, alto: 1, tenor: 2, bass: 3}
#     # soprano = s.new_part("violin")
#     # alto = s.new_part("violin")
#     # tenor = s.new_part("viola")
#     # bass = s.new_part("cello")
#     # soprano = s.new_part("organ")
#     # alto = s.new_part("organ")
#     # tenor = s.new_part("organ")
#     # bass = s.new_part("organ")
#     # soprano = s.new_part("voice")
#     # alto = s.new_part("voice")
#     # tenor = s.new_part("voice")
#     # bass = s.new_part("voice")
#     for i in range(len(parts)):
#         voicing = parts[i]
#         # for voice in [soprano, alto, tenor, bass]:
#         #     if len(voicing) == 2 and voicing[0][i] != voicing[1][i]:
#         #         voice.play_note(60 + halfSteps(['C',0,4],parts[i][0][SATB.get(voice)]),1.0,1,blocking=False)
#         #         if voice == bass:
#         #             voice.play_note(60 + halfSteps(['C',0,4],parts[i][1][SATB.get(voice)]),1.0,1)
#         #         else:
#         #             voice.play_note(60 + halfSteps(['C',0,4],parts[i][1][SATB.get(voice)]),1.0,1,blocking=False)

#         #     else:
#         #         if voice == bass:
#         #             voice.play_note(60 + halfSteps(['C',0,4],parts[i][0][SATB.get(voice)]),1.0,2)
#         #         else:
#         #             voice.play_note(60 + halfSteps(['C',0,4],parts[i][0][SATB.get(voice)]),1.0,2,blocking=False)
#         # for voice in [soprano, alto, tenor, bass]:
#         #     if len(voicing) == 2 and voicing[0][i] != voicing[1][i]:
#         #         voice.play_note(60 + halfSteps(['C',0,4],parts[i][0][SATB.get(voice)]),1.0,1,blocking=True)
#         #         voice.play_note(60 + halfSteps(['C',0,4],parts[i][1][SATB.get(voice)]),1.0,1,)
#         #         continue
#         #     if voice == bass:
#         #         voice.play_note(60 + halfSteps(['C',0,4],parts[i][0][SATB.get(voice)]),1.0,2)
#         #     else:
#         #         voice.play_note(60 + halfSteps(['C',0,4],parts[i][0][SATB.get(voice)]),1.0,2,blocking=False)
#         if len(voicing) == 2 and voicing[0][i] != voicing[1][i]:
#             alto.play_note(60 + halfSteps(['C',0,4],parts[i][0][SATB.get(alto)]),1.0,1,blocking=False)
#             alto.play_note(60 + halfSteps(['C',0,4],parts[i][1][SATB.get(alto)]),1.0,1)
#         else:
#             alto.play_note(60 + halfSteps(['C',0,4],parts[i][0][SATB.get(alto)]),1.0,2,blocking=False)
#         # #if 0 1 not the same, play half duration each
#         # soprano.play_note(60 + halfSteps(['C',0,4],parts[i][0]),1.0,2,blocking=False)
#         # alto.play_note(60 + halfSteps(['C',0,4],parts[i][1]),1.0,2,blocking=False)
#         # tenor.play_note(60 + halfSteps(['C',0,4],parts[i][2]),1.0,2,blocking=False)
#         # bass.play_note(60 + halfSteps(['C',0,4],parts[i][3]),1.0,2)
def validMelody(melody):
    return True

# melody = [['C', 1, 5], ['D', 0, 5], ['F', 0, 5], ['E', 0, 5], ['A', 0, 5],['G', 0, 5], ['F', 0, 5], ['E', 0, 5], ['D', 1, 5], ['E', 0, 5], ['C', 1, 5], ['D', 0, 5], ['C', 0, 5], ['B', 0, 4], ['C', 0, 5],['C', 0, 5], ['G', 0, 4], ['F', 1, 4], ['A', 0, 4], ['G', 0, 4],['B', 0, 4], ['C', 0, 5]]
#melody = [['C', 1, 5], ['D', 0, 5] ,['D', 1, 5], ['E', 0, 5], ['C', 1, 5], ['D', 0, 5], ['C', 0, 5], ['B', 0, 4], ['C', 0, 5]]#melody = [['C',1,5],['D',0,5],['F',1,4],['G',0,4],['D',0,5],['C',0,5]]
#melody = [['E',0,5],['A',0,5],['D',0,5],['G',0,5],['E',0,5],['D',1,5],['E',0,5],['C',0,5],['D',0,5],['E',0,5]]
#melody = [['C', 1, 5], ['D', 0, 5], ['F', 0,# 5], ['E', 0, 5], ['A', 0, 5],['G', 0, 5], ['F', 0, 5], ['E', 0, 5], ['D', 1, 5], ['E', 0, 5], ['C', 1, 5], ['D', 0, 5], ['C', 0, 5], ['B', 0, 4],['C', 0, 5]]
#melody = [['D', 0, 4], ['E', 0, 4], ['F', 1, 4], ['G', 0, 4], ['A',0, 4], ['B',0,4],['C', 1, 5], ['D', 0, 5]]
#melody = [['C', 0, 4],['E', 0, 4],['G', 0, 4],['F', 0, 4],['E', 0, 4],['F', 0, 4],['D', 0, 4],['E', 0, 4],['C', 0, 4],['D',0,4],['C',0,4]]
# melody = [['B',-1,4],['C',-1,5],['B',-1,4],['D',0,4],['E',-1,4],['G',-1,4],['F',0,4],['F',0,4],['E',-1,4]]
#melody = [['E',-1,5],['D',-1,5],['C',-1,5],['A',0,4],['B',-1,4],['D',0,5],['E',-1,5]]
#melody = [['G',0,4],['B',0,4],['C',0,5]]
#melody = [['C', 0, 5], ['E', 0, 5], ['D', 0, 5],['C', 0, 5], ['D', 0, 5],['C',0,5]]
#melody = [['C', 0, 5], ['G', 0, 4], ['F', 1, 4], ['A', 0, 4], ['G', 0, 4],['B', 0, 4], ['C', 0, 5]]
#melody = [['D', 0, 5],['G',0,4],['Eb,0,4],['B',0,4]]
# melody = [['C',0,5],['A',0,4],['B',0,4],['C',0,5]]
# #melody = [['C',0,5]]
#run(['C',0],"major",melody)
# s = Session()
# soprano = s.new_part("piano")
# for i in range(60,100):
#     soprano.play_note(i,1,.25)
#print(trueInterval(interval(['G',0,2],['D',0,5])))