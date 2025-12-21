import math

def turbineTW(eta, Cp, Ttin, Ptin, Ptout, gamma):
    return eta * Cp * Ttin * (1 - (Ptout / Ptin)**((gamma - 1) / gamma))

#TODO reaction turbine specific speed stuff, probably a lookup function
#also the beginnings of defining geometry and performance
