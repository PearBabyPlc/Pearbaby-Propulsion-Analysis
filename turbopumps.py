import math

g = 9.80665
m3s_gpm = 15850.3
m_ft = 3.28084
ft_m = 0.3048
m_in = 39.3701
in_m = 0.0254

class Turbopump:
    def __init__(self, Q, H, Ns, Ds, psi, N, R1, R2, b1, b2, beta1, beta2, eta, U1, U2, Cm1, NPSHr, powerIdeal, powerReal, rho):
        try:
            self.Q = float(Q)
            self.H = float(H)
            self.Ns = float(Ns)
            self.Ds = float(Ds)
            self.psi = float(psi)
            self.N = float(N)
            self.R1 = float(R1)
            self.R2 = float(R2)
            self.b1 = float(b1)
            self.b2 = float(b2)
            self.beta1 = float(beta1)
            self.beta2 = float(beta2)
            self.eta = float(eta)
            self.U1 = float(U1)
            self.U2 = float(U2)
            self.Cm1 = float(Cm1)
            self.NPSHr = float(NPSHr)
            #self.Ss = float(Ss)
            self.powerIdeal = float(powerIdeal)
            self.powerReal = float(powerReal)
            self.rho = float(rho)
        except:
            print("WARNING! class Turbopump failed to initialise!")
            print("         (Bad input data (missing, wrong type)")

    def summary(self):
        print("m3/s =", self.Q)
        print("Head =", self.H)
        print("rpm =", self.N)
        print("Ns =", self.Ns)
        print("Ds =", self.Ds)
        print("psi =", self.psi)
        print("R1 R2 =", self.R1, self.R2)
        print("b1 b2 =", self.b1, self.b2)
        print("beta1 beta2 =", self.beta1, self.beta2)
        print("efficiency =", self.eta)
        print("U1 U2 =", self.U1, self.U2)
        print("Cm1 NPSHr =", self.Cm1, self.NPSHr)
        #print("Suction specific speed (US) =", self.Ss)
        print("powerIdeal =", self.powerIdeal)
        print("powerReal =", self.powerReal)
        print("working fluid rho =", self.rho)

#developed from NASA SP-8109 I curve fit and smoothed in Desmos
#link: https://www.desmos.com/calculator/euixobhrat
def lookupPumpEta(Ns, psi):
    #curve fits
    def f2(x):
        a = (1.26949 * 10**-14) * x**4
        b = (2.05646 * 10**-10) * x**3
        c = 0.00000115809 * x**2
        d = 0.0230073 * x
        output = a - b - c + d + 13.44883
        #print("f2 =", output)
        return output
    def f4(x):
        a = (3.08992 * 10**-15) * x**4
        b = (3.63925 * 10**-10) * x**3
        c = 0.00000718233 * x**2
        d = 0.036644 * x
        output = -a + b - c + d + 30.90883
        #print("f4 =", output)
        return output
    def f6a(x):
        a = (3.52657 * 10**-9) * x**3
        b = 0.0000255838 * x**2
        c = 0.101172 * x
        output = -a -b + c + 0
        #print("f6a =", output)
        return output
    def f6b(x):
        a = (0.00121064 * x) - 1.95137
        b = 1.43253 * math.sin(a)
        output = b + 80.57608
        #print("f6b =", output)
        return output
    def f6c(x):
        a = (-0.00111024 * x) + 6.2494
        b = 1 + math.e**-a
        output = 86.89636 / b
        #print("f6c =", output)
        return output
    def f6(x):
        if x < 1270:
            output = f6a(x)
        elif x > 3095.87185:
            output = f6c(x)
        else:
            output = f6b(x)
        #print("f6 =", output)
        return output
    def f8(x):
        a = (1.1833 * 10**-13) * x**4
        b = (2.10513 * 10**-9) * x**3
        c = 0.0000175735 * x**2
        d = 0.0503068 * x
        output = -a + b - c + d + 34.31181
        #print("f8 =", output)
        return output

    #modulating how much of each curve is in the final
    def c2(x):
        if x < 0.2:
            output = 1
        elif x > 0.4:
            output = 0
        else:
            output = (-5 * (x - 0.2)) + 1
        #print("c2 =", output)
        if output < 0:
            #print("c8 corrected to 0")
            output = 0
        return output
    def c4(x):
        if (x < 0.2) or (x > 0.6):
            output = 0
        elif x < 0.4:
            output = (5 * (x - 0.4)) + 1
        else:
            output = (-5 * (x - 0.4)) + 1
        #print("c4 =", output)
        if output < 0:
            #print("c8 corrected to 0")
            output = 0
        return output
    def c6(x):
        if (x < 0.4) or (x > 0.8):
            output = 0
        elif x < 0.6:
            output = (5 * (x - 0.6)) + 1
        else:
            output = (-5 * (x - 0.6)) + 1
        #print("c6 =", output)
        if output < 0:
            #print("c8 corrected to 0")
            output = 0
        return output
    def c8(x):
        if x < 0.6:
            output = 0
        elif x > 0.8:
            output = 1
        else:
            output = (5 * (x - 0.8)) + 1
        #print("c8 =", output)
        if output < 0:
            #print("c8 corrected to 0")
            output = 0
        return output

    #looking up the efficiency value
    c2psi = c2(psi)
    c4psi = c4(psi)
    c6psi = c6(psi)
    c8psi = c8(psi)
    #csum = c2psi + c4psi + c6psi + c8psi
    fc2 = f2(Ns) * c2psi
    fc4 = f4(Ns) * c4psi
    fc6 = f6(Ns) * c6psi
    fc8 = f8(Ns) * c8psi
    percent = fc2 + fc4 + fc6 + fc8
    eta = percent / 100
    return eta

def findNPSHr(Rinlet, b1, N, U1, Cm1, beta1):
    Rhub = Rinlet - b1
    AnozzleInlet = math.pi * Rinlet**2
    Ahub = math.pi * Rhub**2
    ApumpInlet = AnozzleInlet - Ahub
    areaPercent = (AnozzleInlet / ApumpInlet) * 100

    def lookupK1(x):
        a = 0.0000232901 * x**2
        b = 0.0042306 * x
        return a - b + 1.38757

    def lookupK2(x):
        a = -0.0000559072 * x**4
        b = 0.0010761 * x**3
        c = 0.00122983 * x**2
        d = 0.00361627 * x
        return -a + b + c + d + 0.301049

    Uhub = 2 * math.pi * Rhub * (N / 60)
    Uavg = (U1 + Uhub) / 2
    theta = math.atan(Cm1 / Uavg)
    alpha = abs(beta1 - theta)
    
    K1 = lookupK1(areaPercent)
    K2 = lookupK2(alpha)
    
    w = math.sqrt(Cm1**2 + U1**2)
    Cb = 1.0
    NPSHr = (((K1 * Cm1**2) / (2 * g)) + ((K2 * w**2) / (2 * g))) * Cb
    return NPSHr

#TODO add more functions that allow mass flow/head/rpm to be set in stone
#at the moment all geometry and the rotational speed must be supplied
#can be difficult to obtain decent efficiencies in some cases
def roughTP_demo(R1, R2, b1, b2, N, beta1deg, beta2deg, rho):
    beta1 = math.radians(beta1deg)
    beta2 = math.radians(beta2deg)
    U1 = 2 * math.pi * R1 * (N / 60)
    Vr1 = U1 * math.tan(beta1)
    Q = 2 * math.pi * R1 * b1 * Vr1
    Vr2 = Q / (2 * math.pi * R2 * b2)
    U2 = 2 * math.pi * R2 * (N / 60)
    Vt2 = U2 - (Vr2 * (1 / math.tan(beta2)))
    powerIdeal = rho * Q * U2 * Vt2
    H = powerIdeal / (rho * g * Q)
    Ns = (N * math.sqrt(Q * m3s_gpm)) / (H * m_ft)**0.75
    Ds = (2 * R2 * m_ft * (H * m_ft)**0.25) / math.sqrt(Q * m3s_gpm)
    psi = (g * H) / U2**2
    eta = lookupPumpEta(Ns, psi)
    powerReal = powerIdeal / eta
    Cm1 = U1 * math.tan(beta1)
    NPSHr = findNPSHr(R1, b1, N, U1, Cm1, beta1)
    output = Turbopump(Q, H, Ns, Ds, psi, N, R1, R2, b1, b2, beta1deg, beta2deg, eta, U1, U2, Cm1, NPSHr, powerIdeal, powerReal, rho)
    return output
