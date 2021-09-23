# print(" This program is developed by Yagiz Arda Cicek / METU Coastal Engineering Department (Sept - 2020) ".center(120,"-"))

from math import (pi, sqrt)
import numpy as np
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import size
from regularWave import Wave
from scipy.optimize import fsolve

class WavePlusCurrent:

      g = 9.81
      # nu = 1.36*10**-6 #float(input("\u03BD (m\u00B2/s): "))
      # ro = 1027 #float(input("\u03C1w (kg/m\u00B3): "))
      # ro_s = 2650 #float(input("\u03C1\u209B (kg/m3): "))

      def __init__(self, H0, T, angle, U_bar, d50, h, z, nu, ro, ro_s, fi):
            
            self.H0 = H0
            self.T = T
            self.angle = angle
            self.U_bar = U_bar
            self.d50 = d50
            self.h = h
            self.z = z
            self.nu = nu
            self.ro = ro
            self.ro_s = ro_s
            self.fi = fi

## Wave Characteristics Under Current
      def waveLength(self): # Eqn. 68
            # Defining Function
            omega = 2*pi/self.T
            func = lambda k : (omega-self.U_bar*k*np.cos(np.deg2rad(self.fi)))**2-(self.g*k*np.tanh(k*self.h))

            # k = np.linspace(-1, 5, 1000)
            # plt.plot(k, func(k))
            # plt.grid()
            # plt.show()

            initialGuess = 2*pi/(1.56*self.T**2)
            return 2*pi/fsolve(func, initialGuess)

      def orbitalVelocity(self):
            k = 2*pi/self.waveLength()
            wave = Wave(self.H0, self.T, self.h, self.angle)
            return pi*wave.waveHeight()/(self.T*np.sinh(k*self.h))

      def excursionLength(self):
            return self.orbitalVelocity()*self.T/(2*pi)

      def waveHeight(self):
            wave = Wave(self.H0, self.T, self.h, self.angle)  
            return wave.waveHeight()  

      def approachAngle(self):
            wave = Wave(self.H0, self.T, self.h, self.angle) 
            return wave.approachAngle()

## Threshold of Motion
      def s(self):
            return self.ro_s/self.ro

      def Dstar(self):
            return (self.g*(self.s()-1)/self.nu**2)**(1/3)*self.d50 # Eqn. 75

      def shieldsCritical (self):
            return 0.3/(1+1.2*self.Dstar())+0.055*(1-np.exp(-0.02*self.Dstar())) # Eqn. 76

      def tauCritical(self):
            return self.shieldsCritical()*self.g*(self.ro_s-self.ro)*self.d50

## Friction Factor & CD (Example 5.1)
      def fw(self): # Table 10 - GM79
            z0 = 0.001 # Assumption: hydrodynamically rough bed (usual case)
            A = self.excursionLength()
            ratio = A/z0
            if ratio<10**2:
                  return 0.1057
            elif ratio >= 100 and ratio < 1000:
                  return 0.1057+(0.0316-0.1057)*(ratio-100)/900
            elif ratio >= 1000 and ratio < 10000:
                  return 0.0316+(0.0135-0.0316)*(ratio-1000)/9000
            elif ratio >= 10000 and ratio < 100000:
                  return 0.0135+(0.00690-0.0135)*(ratio-10000)/90000
            else:
                  return 0.00690

      def fwSkin(self): # Table 10 - GM79
            z0 = self.d50/12 # Assumption: hydrodynamically rough bed (usual case) 
            A = self.excursionLength()
            ratio = A/z0
            if ratio<10**2:
                  return 0.1057
            elif ratio >= 100 and ratio < 1000:
                  return 0.1057+(0.0316-0.1057)*(ratio-100)/900
            elif ratio >= 1000 and ratio < 10000:
                  return 0.0316+(0.0135-0.0316)*(ratio-1000)/9000
            elif ratio >= 10000 and ratio < 100000:
                  return 0.0135+(0.00690-0.0135)*(ratio-10000)/90000
            else:
                  return 0.00690  ## Shear stress (Grant & Madsen, 1979 and Soulsby Parametrization)

      def CD(self):
            z0 = 0.001 # Assumption: hydrodynamically rough bed (usual case)
            h = self.h
            ratio = z0/h
            if ratio>10**-2:
                  return 0.01231
            elif ratio <= 10**-2 and ratio > 10**-3:
                  return 0.01231-(0.01231-0.00458)*(10**-2-ratio)/(10**-2-10**-3)
            elif ratio <= 10**-3 and ratio > 10**-4:
                  return 0.00458-(0.00458-0.00237)*(10**-3-ratio)/(10**-3-10**-4)
            elif ratio <= 10**-4 and ratio > 10**-5:
                  return 0.00237-(0.00237-0.00145)*(10**-4-ratio)/(10**-4-10**-5)
                  
            else:
                  return 0.00145


      def CDSkin(self):
            z0 = self.d50/12 # Assumption: hydrodynamically rough bed (usual case)
            h = self.h
            ratio = z0/h
            if ratio>10**-2:
                  return 0.01231
            elif ratio <= 10**-2 and ratio > 10**-3:
                  return 0.01231-(0.01231-0.00458)*(10**-2-ratio)/(10**-2-10**-3)
            elif ratio <= 10**-3 and ratio > 10**-4:
                  return 0.00458-(0.00458-0.00237)*(10**-3-ratio)/(10**-3-10**-4)
            elif ratio <= 10**-4 and ratio > 10**-5:
                  return 0.00237-(0.00237-0.00145)*(10**-4-ratio)/(10**-4-10**-5)
                  
            else:
                  return 0.00145

      def tauCurrent(self):
            return self.ro*self.CD()*self.U_bar**2

      def tauCurrentSkin(self):
            return self.ro*self.CDSkin()*self.U_bar**2

      def shieldsCurrent(self):
            return self.tauCurrent()/(self.g*(self.ro_s-self.ro)*self.d50) # Eqn. 2a

      def shieldsCurrentSkin(self):
            return self.tauCurrentSkin()/(self.g*(self.ro_s-self.ro)*self.d50) # Eqn. 2a

      def tauWave(self):
            return 0.5*self.ro*self.fw()*self.orbitalVelocity()**2

      def tauWaveSkin(self):
            return 0.5*self.ro*self.fwSkin()*self.orbitalVelocity()**2

      def shieldsWave(self):
            return self.tauWave()/(self.g*(self.ro_s-self.ro)*self.d50) # Eqn. 2a

      def shieldsWaveSkin(self):
            return self.tauWaveSkin()/(self.g*(self.ro_s-self.ro)*self.d50) # Eqn. 2a

      def tauMeanMax(self): # Total
            a1, a2, a3, a4 = 0.11, 1.95, -0.49, -0.28 # Coefficients from Table 9 (GM79)
            m1, m2, m3, m4 = 0.65, -0.22, 0.15, 0.06
            n1, n2, n3, n4 = 0.71, -0.19, 0.17, -0.15
            I, J = 0.67, 0.5
            b1, b2, b3, b4 = 0.73, 0.4, -0.23, -0.24
            p1, p2, p3, p4 = -0.68, 0.13, 0.24, -0.07
            q1, q2, q3, q4 = 1.04, -0.56, 0.34, -0.27
            
            a = (a1+a2*abs(np.cos(np.deg2rad(self.fi)))**I)+(a3+a4*abs(np.cos(np.deg2rad(self.fi)))**I)*np.log10(self.fw()/self.CD())
            m = (m1+m2*abs(np.cos(np.deg2rad(self.fi)))**I)+(m3+m4*abs(np.cos(np.deg2rad(self.fi)))**I)*np.log10(self.fw()/self.CD())
            n = (n1+n2*abs(np.cos(np.deg2rad(self.fi)))**I)+(n3+n4*abs(np.cos(np.deg2rad(self.fi)))**I)*np.log10(self.fw()/self.CD())
            b = (b1+b2*abs(np.cos(np.deg2rad(self.fi)))**J)+(b3+b4*abs(np.cos(np.deg2rad(self.fi)))**J)*np.log10(self.fw()/self.CD())
            p = (p1+p2*abs(np.cos(np.deg2rad(self.fi)))**J)+(p3+p4*abs(np.cos(np.deg2rad(self.fi)))**J)*np.log10(self.fw()/self.CD())
            q = (q1+q2*abs(np.cos(np.deg2rad(self.fi)))**J)+(q3+q4*abs(np.cos(np.deg2rad(self.fi)))**J)*np.log10(self.fw()/self.CD())

            X = self.tauCurrent()/(self.tauCurrent()+self.tauWave())
            Z = 1+a*X**m*(1-X)**n
            Y = X*(1+b*X**p*(1-X)**q)

            tauMean = Y*(self.tauCurrent()+self.tauWave())
            tauMax = Z*(self.tauCurrent()+self.tauWave())
            
            return {"tauMean" : tauMean, "tauMax" : tauMax}

      def tauMeanMaxSkin(self): # Page 149
            a1, a2, a3, a4 = 0.11, 1.95, -0.49, -0.28 # Coefficients from Table 9 (GM79)
            m1, m2, m3, m4 = 0.65, -0.22, 0.15, 0.06
            n1, n2, n3, n4 = 0.71, -0.19, 0.17, -0.15
            I, J = 0.67, 0.5
            b1, b2, b3, b4 = 0.73, 0.4, -0.23, -0.24
            p1, p2, p3, p4 = -0.68, 0.13, 0.24, -0.07
            q1, q2, q3, q4 = 1.04, -0.56, 0.34, -0.27
            
            a = (a1+a2*abs(np.cos(np.deg2rad(self.fi)))**I)+(a3+a4*abs(np.cos(np.deg2rad(self.fi)))**I)*np.log10(self.fw()/self.CD())
            m = (m1+m2*abs(np.cos(np.deg2rad(self.fi)))**I)+(m3+m4*abs(np.cos(np.deg2rad(self.fi)))**I)*np.log10(self.fw()/self.CD())
            n = (n1+n2*abs(np.cos(np.deg2rad(self.fi)))**I)+(n3+n4*abs(np.cos(np.deg2rad(self.fi)))**I)*np.log10(self.fw()/self.CD())
            b = (b1+b2*abs(np.cos(np.deg2rad(self.fi)))**J)+(b3+b4*abs(np.cos(np.deg2rad(self.fi)))**J)*np.log10(self.fw()/self.CD())
            p = (p1+p2*abs(np.cos(np.deg2rad(self.fi)))**J)+(p3+p4*abs(np.cos(np.deg2rad(self.fi)))**J)*np.log10(self.fw()/self.CD())
            q = (q1+q2*abs(np.cos(np.deg2rad(self.fi)))**J)+(q3+q4*abs(np.cos(np.deg2rad(self.fi)))**J)*np.log10(self.fw()/self.CD())

            X = self.tauCurrentSkin()/(self.tauCurrentSkin()+self.tauWaveSkin())
            Z = 1+a*X**m*(1-X)**n
            Y = X*(1+b*X**p*(1-X)**q)

            tauMeanSkin = Y*(self.tauCurrentSkin()+self.tauWaveSkin())
            tauMaxSkin = Z*(self.tauCurrentSkin()+self.tauWaveSkin())
            
            return {"tauMeanSkin" : tauMeanSkin, "tauMaxSkin" : tauMaxSkin}
            
      def shieldsMeanMax(self):
            return {"shieldsMean" : self.tauMeanMax()["tauMean"]/(self.g*(self.ro_s-self.ro)*self.d50), "shieldsMax" : self.tauMeanMax()["tauMax"]/(self.g*(self.ro_s-self.ro)*self.d50)}

      def shieldsMeanMaxSkin(self):
            return {"shieldsMeanSkin" : self.tauMeanMaxSkin()["tauMeanSkin"]/(self.g*(self.ro_s-self.ro)*self.d50), "shieldsMaxSkin" : self.tauMeanMaxSkin()["tauMaxSkin"]/(self.g*(self.ro_s-self.ro)*self.d50)}

## Settling Velocity
      def settlingVelocity(self):
            return self.nu/self.d50*((10.36**2+1.049*self.Dstar()**3)**0.5-10.36) # Eqn. 102

## Suspension Profile (Van Rijn, 1984)
      def concentration(self):

            za = 2*self.d50
            if self.shieldsMeanMaxSkin()["shieldsMaxSkin"] >= 0.8:
                  Ca = 0.331*(self.shieldsMeanMaxSkin()["shieldsMaxSkin"]-0.045)**1.75/(1+0.72*(self.shieldsMeanMaxSkin()["shieldsMaxSkin"]-0.045)**1.75) # Eqn. 111
                  
                  uStarMax = (self.tauMeanMaxSkin()["tauMaxSkin"]/self.ro)**0.5
                  ustarMean = (self.tauMeanMaxSkin()["tauMeanSkin"]/self.ro)**0.5

                  bmax = self.settlingVelocity()/(0.4*uStarMax)  # Eqn. 115c
                  bmean = self.settlingVelocity()/(0.4*ustarMean)  # Eqn. 115d

                  zw = uStarMax*self.T/(2*pi) # Eqn. 115e

                  zArray = np.linspace(za, self.h, 1000)
                  C = []
                  zPlot = []
                  for i in zArray: 
                        if za < i and i <= zw:
                              C.append(Ca*(i/za)**(-bmax)) # Eqn. 115a
                              zPlot.append(i)
                        elif zw < i  and i <= self.h:
                              C.append(Ca*(zw/za)**(-bmax)*(i/zw)**(-bmean)) # Eqn. 115b
                              zPlot.append(i)

                  return {"zPlot": np.asarray(zPlot).reshape(len(zPlot),1), "C": np.asarray(C).reshape(len(C),1)}

            else:
                  Ca = 0.331*(self.shieldsMeanMaxSkin()["shieldsMaxSkin"]-0.045)**1.75/(1+0.72*(self.shieldsMeanMaxSkin()["shieldsMaxSkin"]-0.045)**1.75) # Eqn. 111
                  
                  uStarMax = (self.tauMeanMax()["tauMax"]/self.ro)**0.5
                  ustarMean = (self.tauMeanMax()["tauMean"]/self.ro)**0.5

                  bmax = self.settlingVelocity()/(0.4*uStarMax)  # Eqn. 115c
                  bmean = self.settlingVelocity()/(0.4*ustarMean)  # Eqn. 115d

                  zw = uStarMax*self.T/(2*pi) # Eqn. 115e

                  zArray = np.linspace(za, self.h, 1000)
                  C = []
                  zPlot = []
                  for i in zArray: 
                        if za < i and i <= zw:
                              C.append(Ca*(i/za)**(-bmax)) # Eqn. 115a
                              zPlot.append(i)
                        elif zw < i  and i <= self.h:
                              C.append(Ca*(zw/za)**(-bmax)*(i/zw)**(-bmean)) # Eqn. 115b
                              zPlot.append(i)

                  return {"zPlot": np.asarray(zPlot).reshape(len(zPlot),1), "C": np.asarray(C).reshape(len(C),1)}


            ## EXAMPLE'A BAK
      


      def concentrationAtZ(self):
            za = 2*self.d50
            if self.shieldsMeanMaxSkin()["shieldsMaxSkin"] >= 0.8:
                  Ca = 0.331*(self.shieldsMeanMaxSkin()["shieldsMaxSkin"]-0.045)**1.75/(1+0.72*(self.shieldsMeanMaxSkin()["shieldsMaxSkin"]-0.045)**1.75) # Eqn. 111
                  
                  uStarMax = (self.tauMeanMaxSkin()["tauMaxSkin"]/self.ro)**0.5
                  ustarMean = (self.tauMeanMaxSkin()["tauMeanSkin"]/self.ro)**0.5

                  bmax = self.settlingVelocity()/(0.4*uStarMax)  # Eqn. 115c
                  bmean = self.settlingVelocity()/(0.4*ustarMean)  # Eqn. 115d

                  zw = uStarMax*self.T/(2*pi) # Eqn. 115e

 
                  if za < self.z and self.z <= zw:
                        concentrationZ = (Ca*(self.z/za)**(-bmax)) # Eqn. 115a

                  elif zw < self.z  and self.z <= self.h:
                        concentrationZ = (Ca*(zw/za)**(-bmax)*(self.z/zw)**(-bmean)) # Eqn. 115b


                  return concentrationZ

            else:
                  Ca = 0.331*(self.shieldsMeanMaxSkin()["shieldsMaxSkin"]-0.045)**1.75/(1+0.72*(self.shieldsMeanMaxSkin()["shieldsMaxSkin"]-0.045)**1.75) # Eqn. 111
                  
                  uStarMax = (self.tauMeanMax()["tauMax"]/self.ro)**0.5
                  ustarMean = (self.tauMeanMax()["tauMean"]/self.ro)**0.5

                  bmax = self.settlingVelocity()/(0.4*uStarMax)  # Eqn. 115c
                  bmean = self.settlingVelocity()/(0.4*ustarMean)  # Eqn. 115d

                  zw = uStarMax*self.T/(2*pi) # Eqn. 115e


                  if za < self.z and self.z <= zw:
                        concentrationZ = (Ca*(self.z/za)**(-bmax)) # Eqn. 115a
                  elif zw < self.z  and self.z <= self.h:
                        concentrationZ = (Ca*(zw/za)**(-bmax)*(self.z/zw)**(-bmean)) # Eqn. 115b

                  return concentrationZ

      def concentrationPlot(self):
            zPlot = self.concentration()["zPlot"]
            C = self.concentration()["C"]

            fig, (ax1) = plt.subplots(1, 1, figsize=(7, 16))
            # fig.canvas.manager.full_screen_toggle()
            fig.suptitle('Suspension', fontsize = 20)
            
            ax1.plot(C,zPlot, linewidth = 2.5)
            ax1.set_xlabel("C ($m^3$/$m^3$)", fontsize = 16)
            ax1.set_ylabel("z from bottom (m)", fontsize = 16)
            ax1.set_title("Concentration Profile", fontsize = 16)
            ax1.grid()
            
            plt.show()
            

            return "Graphs are plotted!"
            
## Bed Load (Soulsby)
      def bedLoad(self):
            if self.shieldsMeanMaxSkin()["shieldsMaxSkin"] >= 0.8: # Rippled bed (see pg. 168)
                  fi_x1 = 12*self.shieldsMeanMaxSkin()["shieldsMeanSkin"]**0.5*(self.shieldsMeanMaxSkin()["shieldsMeanSkin"]-self.shieldsCritical())
                  fi_x2 = 12*(0.95+0.19*np.cos(np.deg2rad(2*self.fi)))*self.shieldsWaveSkin()**0.5*self.shieldsMeanMaxSkin()["shieldsMeanSkin"]
                  fi_x = max(fi_x1, fi_x2)

                  fi_y = 12*(0.19*self.shieldsMeanMaxSkin()["shieldsMeanSkin"]*self.shieldsWaveSkin()**2*np.sin(np.deg2rad(2*self.fi)))/(self.shieldsWaveSkin()**1.5+1.5*self.shieldsMeanMaxSkin()["shieldsMeanSkin"]**1.5)

                  return {"qbx" : fi_x*(self.g*(self.s()-1)*self.d50**3)**0.5, "qby" : fi_y*(self.g*(self.s()-1)*self.d50**3)**0.5}

            else: # Un-rippled bed (see pg. 168)
                  fi_x1 = 12*self.shieldsMeanMax()["shieldsMean"]**0.5*(self.shieldsMeanMax()["shieldsMean"]-self.shieldsCritical())
                  fi_x2 = 12*(0.95+0.19*np.cos(np.deg2rad(2*self.fi)))*self.shieldsWave()**0.5*self.shieldsMeanMax()["shieldsMean"]
                  fi_x = max(fi_x1, fi_x2)

                  fi_y = 12*(0.19*self.shieldsMeanMax()["shieldsMean"]*self.shieldsWave()**2*np.sin(np.deg2rad(2*self.fi)))/(self.shieldsWave()**1.5+1.5*self.shieldsMeanMax()["shieldsMean"]**1.5)

                  return {"qbx" : fi_x*(self.g*(self.s()-1)*self.d50**3)**0.5, "qby" : fi_y*(self.g*(self.s()-1)*self.d50**3)**0.5}

# wpc = WavePlusCurrent(1,6,0,1,0.2*10**-3,5,0.1,1.36*10**-6,1017,2650,45)

# print(wpc.bedLoad())
# print(curren.tauCritical())
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

