import math

def turbineTW(eta, Cp, Ttin, Ptin, Ptout, gamma):
    return eta * Cp * Ttin * (1 - (Ptout / Ptin)**((gamma - 1) / gamma))
