# For parsing preburner CEARUN outputs, informing
# turbomachinery design and cycle choices
#
# For parsing main combustor CEARUN data, see cearun_mcc.py
# (in future all this will be rewritten and consolidated
#  down into a single omnibusal ceaparse.py)
#
# GUIDELINES FOR INPUT:
# Wide variety of chamber pressures and mixture ratios allowed
# No area ratios, infinite area combustor means no contraction
# Include transport properties, and consider ionised species

from ceaparse_mcc import splitList
from ceaparse_mcc import parseLine
from turbines import turbineTW

class Preburner:
    def __init__(self, OF, percentFuel, P, Pch, T, rho, Cp, gamma, SoS, mu, Pr, massFractions):
        try:
            self.OF = float(OF)
            self.percentFuel = float(percentFuel)
            self.P = float(P)
            self.Pch = float(Pch)
            self.T = float(T)
            self.rho = float(rho)
            self.Cp = float(Cp)
            self.gamma = float(gamma)
            self.SoS = float(SoS)
            self.mu = float(mu)
            self.Pr = float(Pr)
            self.massFractions = dict(massFractions)
        except:
            print("WARNING! class Preburner failed to initialise!")
            print("         (Bad input data (missing, wrong type)")

    def __str__(self):
        try:
            massFracList = self.massFractions.items()
            massFracStrings = []
            for x in massFracList:
                appendMassFrac = str("\n" + str(x[0]) + ": " + str(x[1]))
                massFracStrings.append(appendMassFrac)
            massFractionString = "".join(map(str, massFracStrings))
            stringReturn = str("O/F ratio: " + str(self.OF) +
                               "\n % fuel:" + str(self.percentFuel) +
                               "\nPressure (bar): " + str(self.P) +
                               "\nCritical pressure (bar)" + str(self.Pch) +
                               "\nTemperature (Kelvin): " + str(self.T) +
                               "\nDensity (kg/m3): " + str(self.rho) +
                               "\nCp (kJ/kg-K): " + str(self.Cp) +
                               "\ngamma: " + str(self.gamma) +
                               "\nSpeed of sound (m/s): " + str(self.SoS) +
                               "\nViscosity (millipoise): " + str(self.mu) +
                               "\nPrandtl number: " + str(self.Pr) +
                               "\nMass fractions listed below:" + massFractionString)
            return stringReturn
        except:
            return "ERROR! Preburner string return not initialised!"

    def summary(self):
        print("O/F ratio =", self.OF, "| % fuel =", self.percentFuel)
        print("P (bar) =", self.P, "| T (K) =", self.T)
        TPRoundme = self.P / self.Pch
        TPR = round(TPRoundme, 3)
        print("Best TPR =", TPR, "| rho (kg/m3) =", self.rho)
        CpJoules = self.Cp * 1000
        TWest = turbineTW(0.8, CpJoules, self.T, self.P, self.Pch, self.gamma)
        TWestkW = TWest / 1000
        print("Max TW estimate:", TWestkW, "kW/kg of preburner mass flow")
        print("(constant Tt, Cp, gamma, efficiency=80%)")

    def debug(self):
        self.OF = 4.0
        self.P = 450.0
        self.Pch = 180.0
        self.T = 1300.0
        self.rho = 45.0
        self.Cp = 10000.0
        self.gamma = 1.15
        self.SoS = 1200.0
        self.mu = 1.22
        self.Pr = 0.98
        self.massFractions = {"H2": 0.4, "O2": 0.6}

def doParseCEARUN(filenameString):
    print("ingest file")
    lines = []
    with open(filenameString) as cearun:
        for line in cearun:
            lines.append(line)

    #get block start and end indices
    lineIndices = {}
    it = -1
    for line in lines:
        it += 1
        lineCopy = str(line)
        if lineCopy.lstrip().startswith("O/F=") == True:
            lineIndices.update({it: "blockStart"})
        elif lineCopy.lstrip().startswith("NOTE. WEIGHT FRACTION") == True:
            blockEndIt = it - 4
            lineIndices.update({blockEndIt: "blockEnd"})

    #split into blocks
    blockIndicesList = list(lineIndices.keys())
    blockIndices = splitList(blockIndicesList, 2)
    blocks = []
    for indices in blockIndices:
        blockLo = indices[0]
        blockHi = indices[1]
        blockHii = blockHi + 1
        blockRange = range(blockLo, blockHii)
        blockLines = []
        for index in blockRange:
            line = lines[index]
            lineCopy = str(line)
            if lineCopy.isspace() == True:
                pass
            else:
                blockLines.append(line)
        blocks.append(blockLines)
    
    strippedBlocks = []
    for block in blocks:
        strippedBlock = []
        for line in block:
            lineStripped = line.strip()
            strippedBlock.append(lineStripped)
        strippedBlocks.append(strippedBlock)

    #just for debugging
    #print("blocks stripped down")    
    #for x in strippedBlocks:
        #print()
        #it = -1
        #for y in x:
            #it += 1
            #print("strip index", it, "|", y)

    preburners = []
    #in this case, blocks are actually the configs practically speaking, so may as well just initialise the objects here
    for block in strippedBlocks:
        it = -1
        splitIndex = int()
        for line in block:
            it += 1
            if line.startswith("O/F=") == True:
                OFline = parseLine(line)
                OF = OFline[1]
                percentFuel = OFline[2].split(" ")[-1]
            elif line.startswith("P, BAR") == True:
                Pline = parseLine(line)
                P = Pline[1]
                Pch = Pline[2]
            elif line.startswith("T, K") == True:
                Tline = parseLine(line)
                T = Tline[1]
            elif line.startswith("RHO, KG/CU M") == True:
                rhoLine = parseLine(line)
                rhoLineSplit = rhoLine[1].split(" ")
                rho = float(rhoLineSplit[0]) * (10**float(rhoLineSplit[1]))
            elif (line.startswith("Cp, KJ/(KG)(K)") == True) and (it < 14):
                CpLine = parseLine(line)
                Cp = CpLine[1]
            elif line.startswith("GAMMAs") == True:
                gammaLine = parseLine(line)
                gamma = gammaLine[1]
            elif line.startswith("SON VEL,M/SEC") == True:
                SoSline = parseLine(line)
                SoS = SoSline[1]
            #elif line.startswith("MACH NUMBER") == True:
                #Mline = parseLine(line)
                #print(Mline)
            elif line.startswith("VISC,MILLIPOISE") == True:
                muLine = parseLine(line)
                mu = muLine[1]
            elif (line.startswith("PRANDTL NUMBER") == True) and (it < 24):
                PrLine = parseLine(line)
                Pr = PrLine[1]
            #elif line.startswith("CSTAR, M/SEC") == True:
                #CstarLine = parseLine(line)
                #print(CstarLine)
            elif line.startswith("MASS FRACTIONS") == True:
                splitIndex = it
        it = -1
        massFractions = {}
        #this is a really shockingly bad bit of code but it gets the job done
        for line in block:
            it += 1
            if it > splitIndex:
                splitLineA = line.split(" ")
                massFracCompound = splitLineA[0]
                splitLineA.pop(0)
                splitLineB = []
                for x in splitLineA:
                    try:
                        y = float(x)
                        splitLineB.append(y)
                    except:
                        pass
                massFracAmount = splitLineB[0]
                massFractions.update({massFracCompound: massFracAmount})
        preburner = Preburner(OF, percentFuel, P, Pch, T, rho, Cp, gamma, SoS, mu, Pr, massFractions)
        preburners.append(preburner)

    return preburners

def parseCEARUN(filenameStr):
    try:
        filenameString = str(filenameStr)
        return doParseCEARUN(filenameString)
    except:
        exceptString = str("ERROR! Can't find the following file: " + str(filenameStr))
        print(exceptString)
