import PySide6
import copy
from harmony import *


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

melody = [['C', 0, 5], ['D', 0, 5], ['E', 0, 5], ['F', 0, 5], ['C', 0, 6]]
piece = Piece(['C', 0], "major", 4, 4, 4, 2, melody)
piece.generateHarmony()
piece.printResult()