import math

import formulaegg as egg
import ceaparse_mcc as ceaMCC
import ceaparse_pb as ceaPB

print("==========COMBUSTOR CEAPARSE DEMO==========")

testMCCpositions = ceaMCC.parseCEARUN("mccTest.txt")
for pos in testMCCpositions:
    print()
    pos.summary()

print()
print("==========PREBURNER CEAPARSE DEMO==========")

testPBconfigs = ceaPB.parseCEARUN("pbTest.txt")
for pb in testPBconfigs:
    print()
    pb.summary()
