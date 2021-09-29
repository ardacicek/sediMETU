# print(" This program is developed by Yagiz Arda Cicek / METU Coastal Engineering Department (Sept - 2020) ".center(120,"-"))

from math import (pi, sqrt)
from numpy import (tanh, sinh, sin, cos, arcsin, arccos)

class Wave:

      g = 9.81

      def __init__(self, height, period, depth, angle):
            self.height = height
            self.period = period
            self.depth = depth
            self.angle = angle

      def deepwaterLength(self):
            return self.period**2*self.g/(2*pi)

      def deepwaterCg0(self):
            celerity = self.deepwaterLength()/self.period
            return 0.5*celerity

      def waveLength(self):
            lengthInit = 0.00001
            error = 1
            while error > 0.0001:
                  k = 2*pi/lengthInit
                  lengthNext = ((self.period**2)*self.g/(2*pi))*tanh(k*self.depth)
                  error = abs(lengthNext-lengthInit)
                  lengthInit = lengthNext
            return lengthInit

      def groupVelocity(self):
            k = 2*pi/self.waveLength()
            n = 0.5*(1+2*k*self.depth/sinh(2*k*self.depth))
            celerity = self.waveLength()/self.period
            return n*celerity

      def shoalingCoefficient(self):
            return sqrt(self.deepwaterCg0()/self.groupVelocity())

      def tanhkd(self):
            return tanh(2*pi*self.depth/self.waveLength())

      def approachAngle(self):
            return 180*arcsin(self.tanhkd()*sin(self.angle*pi/180))/pi

      def refractionCoefficient(self):
            return sqrt(cos(self.angle*pi/180)/cos(pi*self.approachAngle()/180))

      def waveHeight(self):
            return self.height*self.shoalingCoefficient()*self.refractionCoefficient()

