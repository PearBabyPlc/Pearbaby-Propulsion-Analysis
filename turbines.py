import math

def turbineTW(eta, Cp, Ttin, Ptin, Ptout, gamma):
    return eta * Cp * Ttin * (1 - (Ptout / Ptin)**((gamma - 1) / gamma))

class StageVelocityTriangle:
    def __init__(self, U, Ca, alpha2, beta3, Cw2, Cv2, C2, V2, beta2, Cv3, Cw3, C3, V3, alpha3):
        try:
            self.U = float(U)
            self.Ca = float(Ca)
            self.alpha2 = float(alpha2)
            self.beta3 = float(beta3)
            self.Cw2 = float(Cw2)
            self.Cv2 = float(Cv2)
            self.C2 = float(C2)
            self.V2 = float(V2)
            self.beta2 = float(beta2)
            self.Cv3 = float(Cv3)
            self.Cw3 = float(Cw3)
            self.C3 = float(C3)
            self.V3 = float(V3)
            self.alpha3 = float(alpha3)
        except:
            print("WARNING! class StageVelocityTriangle failed to initialise!")
            print("         (Bad input data (missing, wrong type)")

#source: https://himech.wordpress.com/wp-content/uploads/2010/02/dke672_ch7.pdf
def turbineStage(N, R, angleIn, Vin, angleStator, angleRotor):
    U = 2 * math.pi * R * (N / 60)
    print("U =", U)
    radIn = math.radians(angleIn)
    Ca = Vin * math.cos(radIn)
    print("Ca =", Ca)
    alpha2 = math.radians(angleStator)
    print("degStator alpha2 =", angleStator, alpha2)
    beta3 = math.radians(angleRotor)
    print("degRotor beta3 =", angleRotor, beta3)

    Cw2 = Ca * math.tan(alpha2)
    print("Cw2 =", Cw2)
    Cv2 = Cw2 - U
    print("Cv2 =", Cv2)
    C2 = math.sqrt(Ca**2 + Cw2**2)
    print("C2 =", C2)
    V2 = math.sqrt(Ca**2 + Cv2**2)
    print("V2 =", V2)
    beta2 = math.acos(Ca / V2)
    beta2deg = math.degrees(beta2)
    print("beta2deg rad =", beta2deg, beta2)

    rightAngle = math.radians(90)
    Cv3 = Ca * math.tan(rightAngle - beta3)
    print("Cv3 =", Cv3)
    Cw3 = Cv3 - U
    print("Cw3 =", Cw3)
    C3 = math.sqrt(Ca**2 + Cw3**2)
    print("C3 =", C3)
    V3 = math.sqrt(Ca**2 + Cv3**2)
    print("V3 =", V3)
    alpha3 = beta3 - math.atan(Cw3 / Ca)
    alpha3deg = math.degrees(alpha3)
    print("alpha3deg rad =", alpha3deg, alpha3)

    outputVelTri = StageVelocityTriangle(U, Ca, angleStator, angleRotor, Cw2, Cv2, C2, V2, beta2deg, Cv3, Cw3, C3, V3, alpha3deg)
    return outputVelTri
    
