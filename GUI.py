import abjad
from harmony import *

def parseToLilypond(parts):
    res = ["","","",""] #four strings for four different parts, SATB
    for voicing in parts:
        for i in range(4):
            res[i] += voicing[i][0].lower()
            if voicing[i][1] >= 1:
                accidental = "s"
            elif voicing[i][1] <= -1:
                print('here')
                accidental = "f"
            else:
                accidental = ""
            accidental *= abs(voicing[i][1])
            res[i] += accidental
            
            regDiff = voicing[i][2] - 3
            if regDiff > 0:
      
                registers = "'"*regDiff

            elif regDiff < 0:
                registers = ","*abs(regDiff)

            else:
                registers = ""
            res[i] += registers
            res[i] += " "
    return res

#adapted from Abjad Documentation https://abjad.github.io/
rh_voice_1 = abjad.Voice(name="RH_Voice1")
rh_voice_2 = abjad.Voice(name="RH_Voice2")
rh_staff = abjad.Staff([rh_voice_1], name="RH_Staff", simultaneous=True)
rh_staff.extend([rh_voice_1, rh_voice_2])
lh_voice_1 = abjad.Voice(name="LH_Voice_1")
lh_voice_2 = abjad.Voice(name="LH_Voice_2")
lh_staff = abjad.Staff(name="LH_Staff", simultaneous=True)
lh_staff.extend([lh_voice_1, lh_voice_2])
piano_staff = abjad.StaffGroup(lilypond_type="PianoStaff", name="Piano_Staff")
piano_staff.extend([rh_staff, lh_staff])
score = abjad.Score([piano_staff], name="Score")


# parts = []
# melody = [['C', 1, 5], ['D', 0, 5], ['F', 0, 5], ['E', 0, 5], ['A', 0, 5],['G', 0, 5], ['F', 0, 5], ['E', 0, 5], ['D', 1, 5], ['E', 0, 5], ['C', 1, 5], ['D', 0, 5], ['C', 0, 5], ['B', 0, 4], ['C', 0, 5]]
parts = []
#melody = [['C', 1, 5], ['D', 0, 5], ['F', 0, 5], ['E', 0, 5], ['A', 0, 5],['G', 0, 5], ['F', 0, 5], ['E', 0, 5], ['D', 1, 5], ['E', 0, 5], ['C', 1, 5], ['D', 0, 5], ['C', 0, 5], ['B', 0, 4],['C', 0, 5]]
melody = [['D', 0, 4], ['A', 0, 4], ['F', 1, 4], ['E', 0, 4], ['F', 1, 4], ['G',1,4],['A', 0, 4], ['C', 1, 5],['D',0,5],['E',0,5]]
melody = [['D', 0, 5],['G',1,5],['E',0,5]]
parts = genHarmonyRecursive(melody, ['D', 0], "major", [], parts, [], 3, 3)
parts = parts[::-1]
print('asdf',parts)
#fix parallel unisons
parts = parseToLilypond(parts)
print(parts)
rh1 = r"\voiceOne " + parts[0]
rh2 = r"\voiceTwo " + parts[1]

lh1 = r"\voiceOne " + parts[2]
lh2 = r"\voiceTwo " + parts[3]




rh_voice_1.extend(rh1)
rh_voice_2.extend(rh2)
lh_voice_1.extend(lh1)
lh_voice_2.extend(lh2)
clef = abjad.Clef("bass")
note1 = abjad.select.note(lh_voice_1, 0)
abjad.attach(clef, note1)
note2 = abjad.select.note(lh_voice_2, 0)
abjad.attach(clef, note2)
abjad.show(score)