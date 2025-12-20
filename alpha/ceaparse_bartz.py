# For parsing main combustion chamber CEARUN outputs
# Feeds into Bartz correlation integration and suchnot
# (Regenerative cooling and expander cycle capacity, 
#  preliminary materials choices, etc...)
#
# For parsing preburner CEARUN data, see ceaparse_preeb.py
# (in future all this will be rewritten and consolidated
#  down into a single omnibusal ceaparse.py)

import numpy as np

def splitList(lst, chunkSize):
    return (lst[i:i + chunkSize] for i in range(0, len(lst), chunkSize))

def parseLine(lineIn):
    lstA = lineIn.split("  ")
    lstB = [x.strip() for x in lstA]
    lstC = list(filter(None, lstB))
    return lstC

def parseBlock(blockIn):
    parsedBlock = []
    clunk = 0
    for line in blockIn:
        clunk += 1
        lstP = parseLine(line)
        parsedBlock.append(lstP)
    preparedBlock = parsedBlock
    preparedBlock[0].insert(0, "POSITION")
    preparedBlock[-1].insert(1, "INJ")
    preparedBlock[-2].insert(1, "INJ")
    preparedBlock[-3].insert(1, "INJ")
    return preparedBlock

class Position:
    def __init__(self, position, P, T, Cp, gam, SoS, M, mu, Pr, AR, Cstar, Isp):
        try:
            self.position = str(position)
            self.P = float(P)
            self.T = float(T)
            self.Cp = float(Cp)
            self.gam = float(gam)
            self.SoS = float(SoS)
            self.M = float(M)
            self.mu = float(mu)
            self.Pr = float(Pr)
            if (AR == "INJ") or (AR == "Ae/At"):
                self.AR = float(0)
                self.Cstar = float(0)
                self.Isp = float(0)
            else:
                try:
                    self.AR = float(AR)
                    self.Cstar = float(Cstar)
                    self.Isp = float(Isp)
                except:
                    self.AR = "WARNING! Bad input!"
                    self.Cstar = "WARNING! Bad input!"
                    self.Isp = "WARNING! Bad input!"
        except:
            exceptString = str("         position: " + str(self.position) +
                         ", P: " + str(P) +
                         ", T: " + str(T) +
                         ", \n         Cp: " + str(Cp) +
                         ", gam: " + str(gam) +
                         ", SoS: " + str(SoS) +
                         ", M:" + str(M) +
                         ", \n         mu: " + str(mu) +
                         ", Pr: " + str(Pr) +
                         ", AR: " + str(AR) +
                         ", Cstar: " + str(Cstar) +
                         ", Isp: " + str(Isp))
            print()
            print("WARNING! class Position and its methods (__str__, debug) failed to initialise!")
            print("         Bad data input at an unexpected location - AR, Cstar and Isp are OK")
            print("         as their INJECTOR data is expected to be a string. Bad input below:")
            print(exceptString)
            print()

    def __str__(self):
        try:
            stringReturn = str("Position: " + str(self.position) + "\nPressure (bar): " + str(self.P) +
                               "\nTemperature (Kelvin): " + str(self.T) + "\nCp (kJ/kg-K): " + str(self.Cp) +
                               "\ngamma: " + str(self.gam) + "\nSpeed of sound (m/s): " + str(self.SoS) +
                               "\nMach number: " + str(self.M) + "\nViscosity (millipoise): " + str(self.mu) +
                               "\nPrandtl number: " + str(self.Pr) + "\nArea / throatArea: " + str(self.AR) +
                               "\nC* (m/s): " + str(self.Cstar) + "\nIsp/exhaust velocity (m/s): " + str(self.Isp))
            return stringReturn
        except:
            return "ERROR! Position string return not initialised!"

    def summary(self):
        summaryString = str(str(self.position) + ": A/At = " + str(self.AR) +
                            ", T = " + str(self.T) + "K, P = " + str(self.P) +
                            "bar, V = " + str(self.Isp) + "m/s")
        return summaryString

    def debug(self):
        self.position = "Debug"
        self.P = 0
        self.T = 0
        self.Cp = 0
        self.gam = 0
        self.SoS = 0
        self.M = 0
        self.mu = 0
        self.Pr = 0
        self.AR = 0
        self.Cstar = 0
        self.Isp = 0

def doParseCEARUN(filenameString):
    lines = []
    
    with open(filenameString) as cearun:
        for line in cearun:
            lines.append(line)
    
    lineIndicies = {}
    it = -1
    for line in lines:
        it += 1
        lineCopy = str(line)
        if lineCopy.lstrip().startswith("INJECTOR") == True:
            lineIndicies.update({it: "blockStart"})
        elif lineCopy.lstrip().startswith("Isp, M/SEC") == True:
            lineIndicies.update({it: "blockEnd"})
    
    #creating the blocks
    blockIndiciesList = list(lineIndicies.keys())
    blockIndicies = splitList(blockIndiciesList, 2)
    blocks = []
    for indicies in blockIndicies:
        blockLo = indicies[0]
        blockHi = indicies[1]
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

    #amountOfBlocks = len(blocks)
    #print("Number of blocks =", amountOfBlocks)
    #trim the blocks down
    trimmedBlocks = []
    for block in blocks:
        trimmedBlock = []
        for line in block:
            lineCopy = str(line)
            if lineCopy.lstrip().startswith("INJECTOR") == True:
                trimmedBlock.append(line.rstrip())
            elif lineCopy.lstrip().startswith("P, BAR") == True:
                trimmedBlock.append(line.rstrip())
            elif lineCopy.lstrip().startswith("T, K") == True:
                trimmedBlock.append(line.rstrip())
            elif lineCopy.lstrip().startswith("RHO, KG/CU M") == True:
                pass
                #trimmedBlock.append(line.rstrip())
                #too hard to split into chunks 
            elif lineCopy.lstrip().startswith("Cp, KJ/(KG)(K)") == True:
                trimmedBlock.append(line.rstrip())
            elif lineCopy.lstrip().startswith("GAMMAs") == True:
                trimmedBlock.append(line.rstrip())
            elif lineCopy.lstrip().startswith("SON VEL,M/SEC") == True:
                trimmedBlock.append(line.rstrip())
            elif lineCopy.lstrip().startswith("MACH NUMBER") == True:
                trimmedBlock.append(line.rstrip())
            elif lineCopy.lstrip().startswith("VISC,MILLIPOISE") == True:
                trimmedBlock.append(line.rstrip())
            elif lineCopy.lstrip().startswith("PRANDTL NUMBER") == True:
                trimmedBlock.append(line.rstrip())
            elif lineCopy.lstrip().startswith("WITH FROZEN REACTIONS") == True:
                trimmedBlock.append(line.rstrip())
            elif lineCopy.lstrip().startswith("Ae/At") == True:
                trimmedBlock.append(line.rstrip())
            elif lineCopy.lstrip().startswith("CSTAR, M/SEC") == True:
                trimmedBlock.append(line.rstrip())
            elif lineCopy.lstrip().startswith("Isp, M/SEC") == True:
                trimmedBlock.append(line.rstrip())
            else:
                pass
        trimmedBlocks.append(trimmedBlock)

    #trim stage 2 (removing frozen reactions and unneeded Cp under equilibrium reactions)
    trimtBlocks = trimmedBlocks
    trimmedBlocks = []
    for block in trimtBlocks:
        blockIndices = range(0, len(block), 1)
        trimmedBlock = []
        trimmedBlockIndices = list(blockIndices)
        for index in blockIndices:
            testLine = block[index]
            if testLine.lstrip().startswith("WITH FROZEN REACTIONS") == True:
                unusedCp = index - 2
                frozenCp = index + 1
                frozenPr = index + 2
                trimmedBlockIndices.remove(index)
                trimmedBlockIndices.remove(unusedCp)
                trimmedBlockIndices.remove(frozenCp)
                trimmedBlockIndices.remove(frozenPr)
            else:
                pass
        for index in trimmedBlockIndices:
            passLine = block[index]
            trimmedBlock.append(passLine)
        trimmedBlocks.append(trimmedBlock)

    arrays = []
    #print()
    #print("before transposition:")
    for block in trimmedBlocks:
        preparedBlock = parseBlock(block)
        array = np.asarray(preparedBlock)
        sherpa = np.shape(array)
        #print(sherpa)
        #array.transpose() no idea how the fuck I got away with transposing twice
        arrays.append(array)

    #print("after transposition:")
    arraysT = []
    for array in arrays:
        arrayT = array.transpose()
        sherbert = np.shape(arrayT)
        #print(sherbert)
        arraysT.append(arrayT)
    
    arraysTup = tuple(arraysT)
    stack = np.vstack(arraysTup)
    uniqueStack = np.unique(stack, axis=0)
    
    positions = []
    for line in uniqueStack:
        if (line[1] == "P, BAR"):
            pass
        else:
            pos = Position(line[0], line[1], line[2], line[3],
                           line[4], line[5], line[6], line[7],
                           line[8], line[9], line[10], line[11])
            positions.append(pos)
    
    positions.sort(key=lambda x: x.AR)
    positions[2], positions[1] = positions[1], positions[2]
    return positions

def parseCEARUN(filenameStr):
    try:
        filenameString = str(filenameStr)
        return doParseCEARUN(filenameString)
    except:
        exceptString = str("ERROR! Can't find the following file: " + str(filenameStr))
        print(exceptString)
