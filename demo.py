import math

import ceaparse_mcc as ceaMCC
import ceaparse_pb as ceaPB
#import turbopumps as tp
import turbines as tu
from turbopumps import roughTP_demo

print("==========ROUGH TURBINE DEMO==========")
N = 10000
R = 0.1
angleIn = 0
Vin = 200
angleStator = 40
angleRotor = 60
turbineDemo = tu.turbineStage(N, R, angleIn, Vin, angleStator, angleRotor)
quit()

print("==========ROUGH TURBOPUMP DEMO==========")
#link: https://www.nuclear-power.com/nuclear-engineering/fluid-dynamics/centrifugal-pumps/eulers-turbomachine-equations/
tpDemo_NuclearPowerDotCom = roughTP_demo(0.1, 0.2, 0.04, 0.04, 1500, 30, 20, 1000)
print("nuclear-power.com example")
tpDemo_NuclearPowerDotCom.summary()
print()

#the rest are early versions of pumps for a personal engine design project
tpDemo_HMX_HTP = roughTP_demo(0.05, 0.07, 0.02, 0.02, 60000, 10, 25, 70.85)
print("HMX HTP")
tpDemo_HMX_HTP.summary()
print()

tpDemo_HMX_OTP = roughTP_demo(0.06, 0.075, 0.025, 0.015, 36000, 6, 10, 1141)
print("HMX OTP")
tpDemo_HMX_OTP.summary()
print()

tpDemo_HMX_MTP = roughTP_demo(0.045, 0.06, 0.016, 0.012, 36000, 8, 30, 422.8)
print("HMX MTP")
tpDemo_HMX_MTP.summary()
print()

tpDemo_HMX_HBP = roughTP_demo(0.03, 0.04, 0.007, 0.005, 100000, 8, 30, 70.85)
print("HMX HBP")
tpDemo_HMX_HBP.summary()
print()

tpDemo_HMX_OBP = roughTP_demo(0.02, 0.022, 0.006, 0.005, 100000, 5, 10, 1141)
print("HMX OBP")
tpDemo_HMX_OBP.summary()
print()
quit()
print()
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
