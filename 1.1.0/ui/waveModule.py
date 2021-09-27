# print(" This program is developed by Yagiz Arda Cicek / METU Coastal Engineering Department (Sept - 2020) ".center(120,"-"))

from math import (pi, sqrt)
import numpy as np
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import size
from regularWave import Wave
from scipy.optimize import fsolve

class Waves:

      g = 9.81
      # nu = 1.36*10**-6 #float(input("\u03BD (m\u00B2/s): "))
      # ro = 1027 #float(input("\u03C1w (kg/m\u00B3): "))
      # ro_s = 2650 #float(input("\u03C1\u209B (kg/m3): "))

      def __init__(self, H0, T, angle, d50, h, z, nu, ro, ro_s, bedType, fwFormulationInput):
            self.H0 = H0
            self.T = T
            self.angle = angle
            self.d50 = d50*10**-3
            self.h = h
            self.z = z
            self.nu = nu*10**-6
            self.ro = ro
            self.ro_s = ro_s
            self.bedType = bedType
            self.fwFormulationInput = fwFormulationInput

## Wave Characteristics           
      def waveLength(self):
            wave = Wave(self.H0, self.T, self.h, self.angle)
            return wave.waveLength()

      def waveHeight(self):
            wave = Wave(self.H0, self.T, self.h, self.angle)
            return wave.waveHeight()

      def approachAngle(self):
            wave = Wave(self.H0, self.T, self.h, self.angle)
            return wave.approachAngle()

      def regularOrbitalVelocity(self):
            wave = Wave(self.H0, self.T, self.h, self.angle)
            k = 2*pi/wave.waveLength()
            return pi*wave.waveHeight()/(self.T*np.sinh(k*self.h)) # Eqn. 54

      def excursionLength(self):
            wave = Wave(self.H0, self.T, self.h, self.angle)
            return self.regularOrbitalVelocity()*self.T/(2*pi)

      def reynolds(self):
            return self.regularOrbitalVelocity()*self.excursionLength()/self.nu

## z0 wrt. Bottom Types (Table 7)
      def z0Table(self):
            return {"Mud": 0.2*10**-3, "Mud/sand" : 0.7*10**-3, "Silt/sand" : 0.05*10**-3, "Sand (unrippled)" : 0.4*10**-3, \
                  "Sand (rippled)" : 6*10**-3, "Sand/shell" : 0.3*10**-3, "Sand/gravel" : 0.3*10**-3, "Mud/sand/gravel" : 0.3*10**-3, \
                        "Gravel" : 3*10**-3, "Flat" : self.d50/12}


## Bed Friction Factor
      def fwFormulation(self):
            r = self.excursionLength()/self.ks()
            # Myrhaug (1989)
            func = lambda fwMyr : 0.32/fwMyr-(np.log(6.36*r*fwMyr**0.5)-np.log(1-np.exp(-0.0262*self.reynolds()*fwMyr**0.5/r))+4.71*r/(self.reynolds()*fwMyr**0.5))**2-1.64
            myrhaugInitialGuess = 1.39*(self.excursionLength()/self.z0Total())**-0.52
            fwMyrhaug = fsolve(func, myrhaugInitialGuess)
            
            # Swart's (1974)
            if r <= 1.57:
                  fwrSwart = 0.3
            else:
                  fwrSwart = 0.00251*np.exp(5.21*r**(-0.19))
            
            # Nielsen (1992)
            fwrNielsen = np.exp(5.5*r**(-0.2)-6.3)

            # Soulsby
            fwrSoulsby = 1.39*(self.excursionLength()/self.z0Total())**-0.52
            return {"Swart (1974)": fwrSwart, "Myrhaug (1989)": fwMyrhaug, "Nielsen (1992)" : fwrNielsen, "Soulsby" : fwrSoulsby}      
      
      def fwFormulationTable(self):
            r = self.excursionLength()/self.ksTable()
            func = lambda fwMyr : 0.32/fwMyr-(np.log(6.36*r*fwMyr**0.5)-np.log(1-np.exp(-0.0262*self.reynolds()*fwMyr**0.5/r))+4.71*r/(self.reynolds()*fwMyr**0.5))**2-1.64
            myrhaugInitialGuess = 1.39*(self.excursionLength()/self.z0Table()[self.bedType])**-0.52
            fwMyrhaug = fsolve(func, myrhaugInitialGuess)
            
            if r <= 1.57:
                  fwrSwart = 0.3
            else:
                  fwrSwart = 0.00251*np.exp(5.21*r**(-0.19))
            
            fwrNielsen = np.exp(5.5*r**(-0.2)-6.3)

            fwrSoulsby = 1.39*(self.excursionLength()/self.z0Table()[self.bedType])**-0.52
            return {"Swart (1974)": fwrSwart, "Myrhaug (1989)": fwMyrhaug, "Nielsen (1992)" : fwrNielsen, "Soulsby" : fwrSoulsby}
            
      def fwTable(self): # From Table 7
            if not self.fwFormulationInput == "Myrhaug (1989)":
                  fwr = self.fwFormulationTable()[self.fwFormulationInput]
                  if self.reynolds() <= 5*10**5:
                        B = 2
                        N = 0.5
                        text = "Laminar flow"
                  else:
                        B = 0.0521
                        N = 0.187
                  fws = B*self.reynolds()**(-N)

                  if fws > fwr and self.reynolds() > 5*10**5:
                        text = "Smooth turbulent flow"
                  elif fws <= fwr and self.reynolds() > 5*10**5:
                        text = "Rough turbulent flow"
                  return {"fw" : max(fwr, fws), "Condition" : text}
            elif self.fwFormulationInput == "Myrhaug (1989)": 
                  fw = self.fwFormulationTable()[self.fwFormulationInput]
                  if self.reynolds() <= 5*10**5:
                        B = 2
                        N = 0.5
                        text = "Laminar flow"
                  else:
                        B = 0.0521
                        N = 0.187
                  fws = B*self.reynolds()**(-N)
                  if fws > fw and self.reynolds() > 5*10**5:
                        text = "Smooth turbulent flow"
                  elif fws <= fw and self.reynolds() > 5*10**5:
                        text = "Rough turbulent flow"
                  return {"fw" : fw, "Condition" : text}

      def fwZ0(self): # From z0
            if not self.fwFormulationInput == "Myrhaug (1989)":
                  fwr = self.fwFormulation()[self.fwFormulationInput]
                  if self.reynolds() <= 5*10**5:
                        B = 2
                        N = 0.5
                        text = "Laminar flow"
                  else:
                        B = 0.0521
                        N = 0.187
                  fws = B*self.reynolds()**(-N)

                  if fws > fwr and self.reynolds() > 5*10**5:
                        text = "Smooth turbulent flow"
                  elif fws <= fwr and self.reynolds() > 5*10**5:
                        text = "Rough turbulent flow"
                  return {"fw" : max(fwr, fws), "Condition" : text}
            elif self.fwFormulationInput == "Myrhaug (1989)": 
                  fw = self.fwFormulation()[self.fwFormulationInput]
                  if self.reynolds() <= 5*10**5:
                        B = 2
                        N = 0.5
                        text = "Laminar flow"
                  else:
                        B = 0.0521
                        N = 0.187
                  fws = B*self.reynolds()**(-N)
                  if fws > fw and self.reynolds() > 5*10**5:
                        text = "Smooth turbulent flow"
                  elif fws <= fw and self.reynolds() > 5*10**5:
                        text = "Rough turbulent flow"
                  return {"fw" : fw, "Condition" : text}


## Shear Stress
      def tauSkin(self):
            fwr = 1.39*(self.excursionLength()/self.z0Table()["Flat"])**-0.52 # Eqn. 62a
            
            if self.reynolds() <= 5*10**5: # Eqn. 63
                  B = 2
                  N = 0.5
            else:
                  B = 0.0521
                  N = 0.187
            fws = B*self.reynolds()**(-N)
            fw = max(fwr, fws)
            return 0.5*self.ro*fw*self.regularOrbitalVelocity()**2 # Eqn. 57
            
      def shieldsSkin(self):
            return self.tauSkin()/(self.g*(self.ro_s-self.ro)*self.d50) # Eqn. 2a

      def tauTotalTable(self): # From Table 7
            return 0.5*self.ro*self.fwTable()["fw"]*self.regularOrbitalVelocity()**2 # Eqn. 57

      def tauTotalZ0(self): # From z0
            return 0.5*self.ro*self.fwZ0()["fw"]*self.regularOrbitalVelocity()**2 # Eqn. 57

## Threshold of Motion
      def s(self):
            return self.ro_s/self.ro

      def Dstar(self):
            return (self.g*(self.s()-1)/self.nu**2)**(1/3)*self.d50 # Eqn. 75

      def shieldsCritical (self):
            return 0.3/(1+1.2*self.Dstar())+0.055*(1-np.exp(-0.02*self.Dstar())) # Eqn. 76

      def tauCritical(self):
            return self.shieldsCritical()*self.g*(self.ro_s-self.ro)*self.d50

      def control(self):
            if self.shieldsSkin() < self.shieldsCritical():
                  return "Immobile, Assume Rippled!"
            elif self.shieldsSkin() <= 0.8 and self.shieldsSkin() >= self.shieldsCritical() and self.d50 < 0.8*10**-3:
                  return "Mobile, Rippled!"
            elif self.shieldsSkin() <= 0.8 and self.shieldsSkin() >= self.shieldsCritical() and self.d50 >= 0.8*10**-3:
                  return "Mobile, No Ripple!"
            elif self.shieldsSkin() > 0.8:
                  return "Mobile, Flat Bed, Sheet Flow!"

## Ripples (Nielsen, 1992)
      def ripples(self):
            waveMobilityNumber = self.regularOrbitalVelocity()**2/(self.g*(self.s()-1)*self.d50)
            # return self.shieldsSkin()
            if self.shieldsSkin() < self.shieldsCritical(): # Eqn. 89a
                  return {'rippleHeight' : 0, 'rippleLength' : 100000}
            elif waveMobilityNumber < 156 and self.shieldsSkin() < 0.831 and self.d50 < 0.8*10**-3: # Eqn. 89b and pg. 115
                  return {'rippleHeight' : (0.275-0.022*waveMobilityNumber**0.5)*self.excursionLength(), 'rippleLength' : (0.275-0.022*waveMobilityNumber**0.5)*self.excursionLength()/(0.182-0.24*self.shieldsSkin()**1.5)}
            elif waveMobilityNumber < 156 and self.shieldsSkin() < 0.831 and self.d50 > 0.8*10**-3: # Eqn. 89b and pg. 115
                  return {'rippleHeight' : 0, 'rippleLength' : 100000}
            elif waveMobilityNumber >= 156 or self.shieldsSkin() >= 0.831: # Eqn. 89c
                  return {'rippleHeight' : 0, 'rippleLength' : 100000}

## Bed Roughness Length, Table 7 can also be used
      def ks(self):
            return self.z0Total()*30

      def ksTable(self):
            return self.z0Table()[self.bedType]*30

      def z0s(self):
            return self.z0Table()["Flat"]

      def z0f(self): # Nielsen, 1992
            return 0.267*self.ripples()['rippleHeight']**2/self.ripples()['rippleLength'] # Eqn. 90

      def z0t(self): # Nielsen, 1992
            if self.shieldsSkin() > 0.8:
                  return 5.67*(self.shieldsSkin()-0.05)**0.5*self.d50 # Eqn. 92
            else:
                  return 0

      def z0Total(self):
            return self.z0s()+self.z0f()+self.z0t()

## Settling Velocity
      def settlingVelocity(self):
            return self.nu/self.d50*((10.36**2+1.049*self.Dstar()**3)**0.5-10.36) # Eqn. 102

## Suspension Profile
      def concentration(self):
            if self.shieldsSkin() <= 0.8: # Aşağıdaki formüller rippled bed için
                  r = self.regularOrbitalVelocity()*self.T/(5*pi*self.d50)
                  fwr = 0.00251*np.exp(5.21*r**-0.19) # Eqn. 60b
                  teta_r = fwr*self.regularOrbitalVelocity()**2/(2*(self.s()-1)*self.g*self.d50*(1-pi*self.ripples()["rippleHeight"]/self.ripples()["rippleLength"])**2) # Eqn. 113d
                  C0 = 0.005*teta_r**3 # Eqn. 113c
                  uStar = (self.tauTotalZ0()*self.ro)**0.5 ## total or skin?
                  Rouse = self.settlingVelocity()/(0.4*uStar)
                  if self.regularOrbitalVelocity()/self.settlingVelocity() < 18: # Eqn. 113a
                        l = 0.075*self.regularOrbitalVelocity()/self.settlingVelocity()*self.ripples()["rippleHeight"]
                  else: # Eqn. 113b
                        l = 1.4*self.ripples()["rippleHeight"]

                  zArray = np.linspace(0, self.h, 250)
                  C = []
                  for i in zArray: # Eqn. 112
                        C.append(C0*np.exp(-i/l))
            elif self.shieldsSkin() > 0.8:
                  za = 2*self.d50
                  Ca = 0.331*(self.shieldsSkin()-0.045)**1.75/(1+0.72*(self.shieldsSkin()-0.045)**1.75)
                  uStar = (self.tauTotalZ0()*self.ro)**0.5 ## total or skin?
                  Rouse = self.settlingVelocity()/(0.4*uStar)
                  zArray = np.linspace(0, self.h, 250)
                  C = []
                  for i in zArray: # Eqn. 114
                        C.append(Ca*(i/za)**-Rouse)

            return {"C" : np.asarray(C).reshape(len(C),1), "zArray" : zArray, "Rouse": Rouse}

      def concentrationAtZ(self):
            if self.shieldsSkin() <= 0.8: # Aşağıdaki formüller rippled bed için
                  r = self.regularOrbitalVelocity()*self.T/(5*pi*self.d50)
                  fwr = 0.00251*np.exp(5.21*r**-0.19) # Eqn. 60b
                  teta_r = fwr*self.regularOrbitalVelocity()**2/(2*(self.s()-1)*self.g*self.d50*(1-pi*self.ripples()["rippleHeight"]/self.ripples()["rippleLength"])**2) # Eqn. 113d
                  C0 = 0.005*teta_r**3 # Eqn. 113c

                  if self.regularOrbitalVelocity()/self.settlingVelocity() < 18: # Eqn. 113a
                        l = 0.075*self.regularOrbitalVelocity()/self.settlingVelocity()*self.ripples()["rippleHeight"]
                  else: # Eqn. 113b
                        l = 1.4*self.ripples()["rippleHeight"]

                  concentrationZ = C0*np.exp(-self.z/l)

            elif self.shieldsSkin() > 0.8:
                  za = 2*self.d50
                  Ca = 0.331*(self.shieldsSkin()-0.045)**1.75/(1+0.72*(self.shieldsSkin()-0.045)**1.75)
                  uStar = (self.tauTotalZ0()*self.ro)**0.5 ## total or skin?
                  Rouse = self.settlingVelocity()/(0.4*uStar)
                  concentrationZ = Ca*(self.z/za)**-Rouse

            return concentrationZ

      def concentrationPlot(self):
            
            C = self.concentration()["C"]
            zArray = self.concentration()["zArray"]
            
            fig, (ax1) = plt.subplots(1, 1, figsize=(7, 16))
            # fig.canvas.manager.full_screen_toggle()
            fig.suptitle('Suspension', fontsize = 20)
            
            ax1.plot(C,zArray, linewidth = 2.5)
            ax1.set_xlabel("C ($m^3$/$m^3$)", fontsize = 16)
            ax1.set_ylabel("z from bottom (m)", fontsize = 16)
            ax1.set_title("Concentration Profile", fontsize = 16)
            ax1.grid()
            
            plt.show()

            return "Graphs are plotted!"
            
## Bed Load
      def stokesUCrest(self): # Eqn. 55a
            wave = Wave(self.H0, self.T, self.h, self.angle)
            k = 2*pi/wave.waveLength()
            return self.regularOrbitalVelocity()*(1+3*k*self.h/(8*(np.sinh(k*self.h))**3)*wave.waveHeight()/self.h)

      def stokesUTrough(self): # Eqn. 55b
            wave = Wave(self.H0, self.T, self.h, self.angle)
            k = 2*pi/wave.waveLength()
            return self.regularOrbitalVelocity()*(1-3*k*self.h/(8*(np.sinh(k*self.h))**3)*wave.waveHeight()/self.h)

      def bedLoad(self): # Example 9.2
            # fw = self.fwZ0()["fw"]
            ks = 2.5*self.d50

            # Crest
            excursionCrest = self.stokesUCrest()*self.T/(2*pi)
            rCrest = excursionCrest/ks
            fwrCrest = 0.237*rCrest**-0.52
            tauSkinCrest = 0.5*self.ro*fwrCrest*self.stokesUCrest()**2
            shieldsSkinCrest = tauSkinCrest/(self.ro*self.g*self.d50*(self.s()-1))
            qbCrest = 5.1*(self.g*(self.s()-1)*self.d50**3)**0.5*(shieldsSkinCrest-self.shieldsCritical())**1.5
            
            # Trough
            excursionTrough = self.stokesUTrough()*self.T/(2*pi)
            rTrough = excursionTrough/ks
            fwrTrough = 0.237*rTrough**-0.52
            tauSkinTrough = 0.5*self.ro*fwrTrough*self.stokesUTrough()**2
            shieldsSkinTrough = tauSkinTrough/(self.ro*self.g*self.d50*(self.s()-1))
            qbTrough = 5.1*(self.g*(self.s()-1)*self.d50**3)**0.5*(shieldsSkinTrough-self.shieldsCritical())**1.5
            return {"qbc" : qbCrest, "qbt" : qbTrough, "qbnet" : qbCrest-qbTrough}


# wav = Waves(1,6,0,1,5,0.1,1.36,1027,2650,"Sand (rippled)","Soulsby")

# print(wav.fwFormulation())

# print(curren.CD())
# print(curren.ripples())
# print(curren.shieldsSkin())
# print(curren.shieldsCritical())
# print(curren.z0f())
# print(curren.z0s())
# print(curren.z0t())
# print(curren.concentrationPlot())
# print(curren.settlingVelocity())
# print(np.size(curren.logVeloProfile()["Ulog"]))

# print(curren.tauSkin())
# print(curren.CD())
# print(curren.uStar())
# print(curren.vanRijnTs())

