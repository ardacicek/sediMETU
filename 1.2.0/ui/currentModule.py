# print(" This program is developed by Yagiz Arda Cicek / METU Coastal Engineering Department (Sept - 2020) ".center(120,"-"))

from math import (nan, pi, sqrt)
import numpy as np
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import size

class Current:

      g = 9.81
      # nu = 1.36*10**-6 #float(input("\u03BD (m\u00B2/s): "))
      # ro = 1027 #float(input("\u03C1w (kg/m\u00B3): "))
      # ro_s = 2650 #float(input("\u03C1\u209B (kg/m3): "))

      def __init__(self, U_bar, d50, h, z, nu, ro, ro_s):
            self.U_bar = U_bar
            self.d50 = d50*10**-3
            self.h = h
            self.z = z
            self.nu = nu*10**-6
            self.ro = ro
            self.ro_s = ro_s

## Threshold of Motion
      def s(self):
            return self.ro_s/self.ro

      def Dstar(self):
            return (self.g*(self.s()-1)/self.nu**2)**(1/3)*self.d50 # Eqn. 75

      def shieldsCritical (self):
            return 0.3/(1+1.2*self.Dstar())+0.055*(1-np.exp(-0.02*self.Dstar())) # EQN NO???

      def tauCritical(self):
            return self.shieldsCritical()*self.g*(self.ro_s-self.ro)*self.d50

## Ripples
      def ripples(self):
            if self.d50 <= 0.8*10**-3 and self.shieldsSkin()<=0.8 and self.shieldsSkin()>self.shieldsCritical(): # Eqns. 81a & 81b
                  return {'rippleHeight' : 1000*self.d50/7, 'rippleLength' : 1000*self.d50}
            else:
                  return {'rippleHeight' : 0, 'rippleLength' : 1000000}

## Bed Roughness Length
      def uStar(self):
            return self.U_bar*(1/7)*(self.d50/self.h)**(1/7) # Eqn. 34
            

      def ks(self):
            return 2.5*self.d50 # Eqn. 24

      def z0s(self):
            return self.ks()/30*(1-np.exp(-self.uStar()*self.ks()/(27*self.nu)))+self.nu/(9*self.uStar()) # Eqn. 23a

      def z0f(self):
            return 1.0*self.ripples()['rippleHeight']**2/self.ripples()['rippleLength'] # Eqn. 90

      def z0t(self):
            if self.shieldsSkin() > 0.8:
                  return 5*self.tauSkin()/(30*self.g*(self.ro_s-self.ro)) # Eqn.  42
            else:
                  return 0

      def z0(self):
            return self.z0s() + self.z0f() + self.z0t() # Eqn. 43

## Total Shear Stress
      def tauSkin(self):
            return self.ro*self.uStar()**2 # Eqn. 32

      def CD(self):
            return (0.4/(1+np.log(self.z0()/self.h)))**2 # Eqn. 37

      def tauTotal(self):
            return self.ro*self.CD()*self.U_bar**2 # Eqn. 30

      def shieldsSkin(self):
            return self.tauSkin()/(self.g*(self.ro_s-self.ro)*self.d50) # Eqn. 2a

      def control(self):
            if self.shieldsSkin() < self.shieldsCritical():
                  return "Immobile, Assume Rippled!"
            elif self.shieldsSkin() <= 0.8 and self.shieldsSkin() >= self.shieldsCritical() and self.d50 < 0.8*10**-3:
                  return "Mobile, Rippled!"
            elif self.shieldsSkin() <= 0.8 and self.shieldsSkin() >= self.shieldsCritical() and self.d50 >= 0.8*10**-3:
                  return "Mobile, No Ripple!"
            elif self.shieldsSkin() > 0.8:
                  return "Mobile, Flat Bed, Sheet Flow!"

## Sand Waves
      def sandWaveYalin(self):
            if self.tauSkin() < self.tauCritical(): # Eqn. 82a
                  return {'sandWaveYalinHeight': 0, 'sandWaveYalinLength': 0 }
            elif self.tauSkin() < 17.6*self.tauCritical() and self.tauSkin() >= self.tauCritical(): # Eqn. 82b
                  return {'sandWaveYalinHeight': self.h/6*(1-self.tauCritical()/self.tauSkin()), 'sandWaveYalinLength': 2*pi*self.h }
            elif self.tauSkin() >= 17.6*self.tauCritical(): # Eqn. 82c
                  return {'sandWaveYalinHeight': 0, 'sandWaveYalinLength': 0 }

      def vanRijnTs(self):
            return (self.tauSkin()-self.tauCritical())/self.tauCritical()

      def sandWaveVanRijn(self):
            if self.tauSkin() < self.tauCritical(): # Eqn. 83a
                  return {'sandWaveVanRijnHeight': 0, 'sandWaveVanRijnLength': 0 }
            elif self.tauSkin() < 26*self.tauCritical() and self.tauSkin() >= self.tauCritical(): # Eqn. 83b
                  return {'sandWaveVanRijnHeight': 0.11*self.h*(self.d50/self.h)**0.3*(1-np.exp(-0.5*self.vanRijnTs()))*(25-self.vanRijnTs()), 'sandWaveVanRijnLength': 7.3*self.h }
            elif self.tauSkin() >= 26*self.tauCritical(): # Eqn. 83c
                  return {'sandWaveVanRijnHeight': 0, 'sandWaveVanRijnLength': 0 }

## Logarithmic Velocity Profile
      def logVeloProfile(self):
            za = max(0.01*self.h,self.sandWaveVanRijn()['sandWaveVanRijnHeight']/2) # Eqn. 110
            zArray = np.linspace(za, self.h, 100)
            zArrayPlot = np.linspace(0.00001, self.h, 150) # for plotting
            Ulog = []
            UlogPlot = []
            zPlot = [] # for suspended load calculations
            for i in zArray: 
                  if za < i and i < self.h/2:
                        Ulog.append(self.uStar()/0.4*np.log(i/self.z0())) # Eqn. 22
                        zPlot.append(i)
                  elif self.h/2 < i  and i < self.h:
                        Ulog.append(self.uStar()/0.4*np.log(i/self.z0())) # Eqn. 22
                        zPlot.append(i)

            for j in zArrayPlot:
                  if self.uStar()/0.4*np.log(j/self.z0()) < 0:
                        UlogPlot.append(0)
                  else:
                        UlogPlot.append(self.uStar()/0.4*np.log(j/self.z0()))   

            return {"Ulog": np.asarray(Ulog).reshape(len(Ulog),1), "zPlot": np.asarray(zPlot).reshape(len(zPlot),1), "UlogPlot":np.asarray(UlogPlot).reshape(len(UlogPlot),1), "zArrayPlot" : np.asarray(zArrayPlot).reshape(len(zArrayPlot),1)}

## Settling Velocity
      def settlingVelocity(self):
            return self.nu/self.d50*((10.36**2+1.049*self.Dstar()**3)**0.5-10.36) # Eqn. 102

## Suspension Profile (Van Rijn, 1984)
      def concentration(self):

            za = max(0.01*self.h,self.sandWaveVanRijn()['sandWaveVanRijnHeight']/2) # Eqn. 110
            Ca = 0.015*self.d50*self.vanRijnTs()**1.5/(za*self.Dstar()**0.3) # Eqn. 110
            uStarFromCD = self.CD()**0.5*self.U_bar # Example 8.2
            Rouse = self.settlingVelocity()/(0.4*uStarFromCD) # Eqn. 105

            if self.settlingVelocity()/self.uStar() > 0.1 and self.settlingVelocity()/self.uStar() < 1:
                  B1 = 1+2*(self.settlingVelocity()/self.uStar())**2 # Eqn. 108d
            elif self.settlingVelocity()/self.uStar()>=1:
                  B1 = 2 # Eqn. 108d
            else:
                  B1 = nan

            if self.settlingVelocity()/self.uStar() >= 0.01 and self.settlingVelocity()/self.uStar() <= 1:
                  B2 = 2.5*(self.settlingVelocity()/self.uStar())**0.8*(Ca/0.65)**0.4 # Eqn. 108e
            elif self.settlingVelocity()/self.uStar()>1:
                  B2 = 0 # Eqn. 108e
            else:
                  B2 = nan

            bprime = Rouse/B1+B2 # Eqn. 108c

            zArray = np.linspace(za, self.h, 100)
            C = []
            zPlot = []
            for i in zArray: 
                  if za < i and i < self.h/2:
                        C.append(Ca*((i/za)*(self.h-za)/(self.h-i))**(-bprime)) # Eqn. 108a
                        
                        zPlot.append(i)
                  elif self.h/2 <= i  and i < self.h:
                        C.append((Ca*(za/(self.h-za))**(bprime))*np.exp(-4*bprime*(i/self.h-0.5))) # Eqn. 108b
                        zPlot.append(i)

            return {"za": za, "Rouse": Rouse, "C": np.asarray(C).reshape(len(C),1)}
      
      def suspendedLoad(self):
            
            conLoad = np.multiply(self.concentration()["C"], self.logVeloProfile()["Ulog"])
            
            za = max(0.01*self.h,self.sandWaveVanRijn()['sandWaveVanRijnHeight']/2) # Eqn. 110
            zArray = np.linspace(za, self.h, 100)
            zPlot = []
            for i in zArray: 
                  if za < i and i < self.h/2:
                        zPlot.append(i)
                  elif self.h/2 <= i  and i < self.h:
                        zPlot.append(i)


            return np.asarray(conLoad).reshape(len(conLoad),1)

      def concentrationAtZ(self):
            za = max(0.01*self.h,self.sandWaveVanRijn()['sandWaveVanRijnHeight']/2) # Eqn. 110
            Ca = 0.015*self.d50*self.vanRijnTs()**1.5/(za*self.Dstar()**0.3) # Eqn. 110
            uStarFromCD = self.CD()**0.5*self.U_bar # Example 8.2
            Rouse = self.settlingVelocity()/(0.4*uStarFromCD) # Eqn. 105

            if self.settlingVelocity()/self.uStar() > 0.1 and self.settlingVelocity()/self.uStar() < 1:
                  B1 = 1+2*(self.settlingVelocity()/self.uStar())**2 # Eqn. 108d
            elif self.settlingVelocity()/self.uStar()>=1:
                  B1 = 2 # Eqn. 108d
            else:
                  B1 = nan

            if self.settlingVelocity()/self.uStar() >= 0.01 and self.settlingVelocity()/self.uStar() <= 1:
                  B2 = 2.5*(self.settlingVelocity()/self.uStar())**0.8*(Ca/0.65)**0.4 # Eqn. 108e
            elif self.settlingVelocity()/self.uStar()>1:
                  B2 = 0 # Eqn. 108e
            else:
                  B2 = nan

            bprime = Rouse/B1+B2 # Eqn. 108c

            if za < self.z and self.z < self.h/2:
                  concentrationZ = (Ca*((self.z/za)*(self.h-za)/(self.h-self.z))**(-bprime)) # Eqn. 108a

            elif self.h/2 <= self.z  and self.z < self.h:
                  concentrationZ = (Ca*(za/(self.h-za))**(bprime))*np.exp(-4*bprime*(self.z/self.h-0.5)) # Eqn. 108b

            else:
                  concentrationZ = "Input z is less than z\u2090 value."

            return {"concentrationZ" : concentrationZ, "za":za}

      def concentrationPlot(self):
            zPlot = self.logVeloProfile()["zPlot"]
            

            fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20,15))
            # fig.canvas.manager.full_screen_toggle()
            fig.suptitle('Suspension', fontsize = 20)
            
            ax1.plot(self.logVeloProfile()["UlogPlot"], self.logVeloProfile()["zArrayPlot"])
            ax1.set_xlabel("U (m/s)", fontsize = 14)
            ax1.set_ylabel("z from bottom (m)", fontsize = 14)
            ax1.set_title("Logarithmic Velocity Profile", fontsize = 14)
            ax1.grid()

            
            ax2.plot(self.concentration()["C"], self.logVeloProfile()["zPlot"])
            ax2.set_xlabel("C ($m^3$/$m^3$)", fontsize = 14)
            ax2.set_title("Concentration Profile (van Rijn, 1984)", fontsize = 14)
            ax2.grid()

            ax3.plot(self.suspendedLoad(), self.logVeloProfile()["zPlot"])
            ax3.set_xlabel("Suspended Load (m/s*$m^3$/$m^3$)", fontsize = 14)
            ax3.set_title("Suspended Load Profile (van Rijn, 1984)", fontsize = 14)
            ax3.grid()
            
            plt.show()

            return "Graphs are plotted!"
            
## Bed Load (Nielsen, 1992)
      def bedLoad(self):
            if self.shieldsSkin() < self.shieldsCritical():
                  fi = 0
            elif self.shieldsSkin() >= self.shieldsCritical():
                  fi = 12*self.shieldsSkin()**0.5*(self.shieldsSkin()-self.shieldsCritical())
            
            return fi*(self.g*(self.s()-1)*self.d50**3)**0.5


# curren = Current(1,0.2,2,1,1.36,1027,2650)
# print(curren.concentrationAtZ())


# print(curren.tauCritical())
# print(curren.CD())
# # print(curren.ripples())
# # print(curren.shieldsSkin())
# # print(curren.shieldsCritical())
# # print(curren.z0f())
# # print(curren.z0s())
# # print(curren.z0t())
# # print(curren.concentrationPlot())
# print(curren.concentrationAtZ())
# print(np.size(curren.logVeloProfile()["Ulog"]))

# print(curren.tauSkin())
# print(curren.CD())
# print(curren.uStar())
# print(curren.vanRijnTs())

