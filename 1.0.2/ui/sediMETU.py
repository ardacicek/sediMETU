from PyQt5 import QtWidgets, QtCore, QtGui #pyqt stuff
import sys
from MainWindow import Ui_MainWindow
from currentModule import Current
from waveModule import Waves
from wavePlusCurrentModule import WavePlusCurrent
import ctypes  # An included library with Python install.   

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp,self).__init__()
        self.ui = Ui_MainWindow() #self.ui'ı main window classına bağladık
        self.ui.setupUi(self) #ui elemanına main window içindeki elemanları bağladık

        self.ui.calculateCurrent_btn.clicked.connect(self.calculateCurrent) #burada butonlara tıklandığında çalıştıralacak fonksiyonları bağlıyoruz. her buton için bir satır.
        self.ui.calculateWave_btn.clicked.connect(self.calculateWave) #burada butonlara tıklandığında çalıştıralacak fonksiyonları bağlıyoruz. her buton için bir satır.
        self.ui.calculateWPC_btn.clicked.connect(self.calculateWPC) #burada butonlara tıklandığında çalıştıralacak fonksiyonları bağlıyoruz. her buton için bir satır.

    def calculateCurrent(self):
        
        ## Input Error Check
        inputController = 0
        while inputController == 0:
            inputController = 1
            U_bar = self.ui.Ubar_txt.text()
            d50 = self.ui.d50_txt.text()
            h = self.ui.h_txt.text()
            z = self.ui.z_txt.text()
            nu = self.ui.nu_txt.text()
            ro = self.ui.ro_txt.text()
            ro_s = self.ui.ro_s_txt.text()
            
            if not (U_bar.isnumeric() or (U_bar.replace(".","",1)).isnumeric()): #noktalar işi bozuyor
                self.ui.Ubar_txt.setText("Enter a number")
                inputController = 0
                return None
            elif (U_bar.replace(".","")).isnumeric() or U_bar.isnumeric():
                U_bar = float(self.ui.Ubar_txt.text())

            if not (d50.isnumeric() or (d50.replace(".","",1)).isnumeric()):
                self.ui.d50_txt.setText("Enter a number")
                inputController == 0
                return None
            elif (d50.replace(".","")).isnumeric() or d50.isnumeric():
                d50 = float(self.ui.d50_txt.text())

            if not (h.isnumeric() or (h.replace(".","",1)).isnumeric()):
                self.ui.h_txt.setText("Enter a number")
                inputController == 0
                return None
            elif (h.replace(".","")).isnumeric() or h.isnumeric():
                h = float(self.ui.h_txt.text())

            if not (z.isnumeric() or (z.replace(".","",1)).isnumeric()):
                self.ui.z_txt.setText("Enter a number")
                inputController == 0
                return None
            elif (z.replace(".","")).isnumeric() or z.isnumeric():
                z = float(self.ui.z_txt.text())

            if not (nu.isnumeric() or (nu.replace(".","",1)).isnumeric()):
                self.ui.nu_txt.setText("Enter a number")
                inputController == 0
                return None
            elif (nu.replace(".","")).isnumeric() or nu.isnumeric():
                nu = float(self.ui.nu_txt.text())

            if not (ro.isnumeric() or (ro.replace(".","",1)).isnumeric()):
                self.ui.ro_txt.setText("Enter a number")
                inputController == 0
                return None
            elif (ro.replace(".","")).isnumeric() or ro.isnumeric():
                ro = float(self.ui.ro_txt.text())

            if not (ro_s.isnumeric() or (ro_s.replace(".","",1)).isnumeric()):
                self.ui.ro_s_txt.setText("Enter a number")
                inputController == 0
                return None
            elif (ro_s.replace(".","")).isnumeric() or ro_s.isnumeric():
                ro_s = float(self.ui.ro_s_txt.text())

            if float(nu) > 1.6 or float(nu) < 0.9:
                self.ui.nu_txt.setText("Check value")
                inputController = 0
                return None

            if float(ro) > 1300 or float(ro) < 900:
                self.ui.ro_txt.setText("Check value")
                inputController = 0
                return None

            if float(ro_s) > 3000 or float(ro_s) < 2000:
                self.ui.ro_s_txt.setText("Check value")
                inputController = 0
                return None
            

        # U_bar = 1
        # d50 = 6*10**-3
        # h = 10
        # z = 1
        # nu = 1.36*10**-6 
        # ro = 1027
        # ro_s = 2650
        
        currentRes = Current(U_bar, d50, h, z, nu, ro, ro_s)

        self.ui.condition_txt.setText(currentRes.control())

        ## Material Properties
        self.ui.Dstar_txt.setText('%.8f'%currentRes.Dstar())
        self.ui.crShields_txt.setText('%.8f'%currentRes.shieldsCritical())
        self.ui.crShear_txt.setText('%.8f'%currentRes.tauCritical())
        self.ui.fallVelocity_txt.setText('%.8f'%currentRes.settlingVelocity())
        self.ui.crShields_txt.setText('%.8f'%currentRes.shieldsCritical())

        ## Roughness Parameters
        self.ui.ks_txt.setText('%.8f'%currentRes.ks())
        self.ui.z0s_txt.setText('%.8f'%currentRes.z0s())
        self.ui.z0f_txt.setText('%.8f'%currentRes.z0f())
        self.ui.z0t_txt.setText('%.8f'%currentRes.z0t())
        self.ui.z0_txt.setText('%.8f'%currentRes.z0())

        ## Ripple Characteristics
        self.ui.rippleHeight_txt.setText('%.8f'%currentRes.ripples()["rippleHeight"])
        self.ui.rippleLength_txt.setText('%.8f'%currentRes.ripples()["rippleLength"])

        ## Suspension & Bed Load
        self.ui.za_txt.setText('%.8f'%currentRes.concentration()["za"])
        self.ui.rouse_txt.setText('%.8f'%currentRes.concentration()["Rouse"])
        if currentRes.concentrationAtZ()["za"]>z:
            self.ui.concentration_txt.setText(currentRes.concentrationAtZ()["concentrationZ"])
        else:
            self.ui.concentration_txt.setText('%.8f'%currentRes.concentrationAtZ()["concentrationZ"])
        self.ui.qb_txt.setText('%.8f'%currentRes.z0f())

        ## Sandwave Characteristics
        self.ui.swHeightYalin_txt.setText('%.8f'%currentRes.sandWaveYalin()["sandWaveYalinHeight"])
        self.ui.swLengthYalin_txt.setText('%.8f'%currentRes.sandWaveYalin()["sandWaveYalinLength"])
        self.ui.swHeightvanRijn_txt.setText('%.8f'%currentRes.sandWaveVanRijn()["sandWaveVanRijnHeight"])
        self.ui.swLengthvanRijn_txt.setText('%.8f'%currentRes.sandWaveVanRijn()["sandWaveVanRijnLength"])

        ## Shear Stress
        self.ui.uStar_txt.setText('%.8f'%currentRes.uStar())
        self.ui.CD_txt.setText('%.8f'%currentRes.CD())
        self.ui.skinShear_txt.setText('%.8f'%currentRes.tauSkin())
        self.ui.skinShields_txt.setText('%.8f'%currentRes.shieldsSkin())
        self.ui.totalShear_txt.setText('%.8f'%currentRes.tauTotal())

        ## Plotting
        currentRes.concentrationPlot()

    def calculateWave(self):
        bedType = self.ui.bedType_txt.text()
        
        ## Input Error Check
        inputController = 0
        while inputController == 0:
            inputController = 1
            H0 = self.ui.H0_txt.text()
            T = self.ui.T_txt.text()
            angle = self.ui.alpha0_txt.text()
            d50 = self.ui.d50_Wave_txt.text()
            h = self.ui.h_Wave_txt.text()
            z = self.ui.z_Wave_txt.text()
            nu = self.ui.nu_Wave_txt.text()
            ro = self.ui.ro_Wave_txt.text()
            ro_s = self.ui.ro_s_Wave_txt.text()
            
            if not (H0.isnumeric() or (H0.replace(".","",1)).isnumeric()):
                self.ui.H0_txt.setText("Enter a number")
                inputController = 0
                return None
            elif (H0.replace(".","")).isnumeric() or H0.isnumeric():
                H0 = float(self.ui.H0_txt.text())

            if not (T.isnumeric() or (T.replace(".","",1)).isnumeric()):
                self.ui.T_txt.setText("Enter a number")
                inputController = 0
                return None
            elif (T.replace(".","")).isnumeric() or T.isnumeric():
                T = float(self.ui.T_txt.text())

            if not (angle.isnumeric() or (angle.replace(".","",1)).isnumeric()):
                self.ui.alpha0_txt.setText("Enter a number")
                inputController = 0
                return None
            elif (angle.replace(".","")).isnumeric() or angle.isnumeric():
                angle = float(self.ui.alpha0_txt.text())

            if not (d50.isnumeric() or (d50.replace(".","",1)).isnumeric()):
                self.ui.d50_Wave_txt.setText("Enter a number")
                inputController == 0
                return None
            elif (d50.replace(".","")).isnumeric() or d50.isnumeric():
                d50 = float(self.ui.d50_Wave_txt.text())

            if not (h.isnumeric() or (h.replace(".","",1)).isnumeric()):
                self.ui.h_Wave_txt.setText("Enter a number")
                inputController == 0
                return None
            elif (h.replace(".","")).isnumeric() or h.isnumeric():
                h = float(self.ui.h_Wave_txt.text())

            if not (z.isnumeric() or (z.replace(".","",1)).isnumeric()):
                self.ui.z_Wave_txt.setText("Enter a number")
                inputController == 0
                return None
            elif (z.replace(".","")).isnumeric() or z.isnumeric():
                z = float(self.ui.z_Wave_txt.text())

            if not (nu.isnumeric() or (nu.replace(".","",1)).isnumeric()):
                self.ui.nu_Wave_txt.setText("Enter a number")
                inputController == 0
                return None
            elif (nu.replace(".","")).isnumeric() or nu.isnumeric():
                nu = float(self.ui.nu_Wave_txt.text())

            if not (ro.isnumeric() or (ro.replace(".","",1)).isnumeric()):
                self.ui.ro_Wave_txt.setText("Enter a number")
                inputController == 0
                return None
            elif (ro.replace(".","")).isnumeric() or ro.isnumeric():
                ro = float(self.ui.ro_Wave_txt.text())

            if not (ro_s.isnumeric() or (ro_s.replace(".","",1)).isnumeric()):
                self.ui.ro_s_Wave_txt.setText("Enter a number")
                inputController == 0
                return None
            elif (ro_s.replace(".","")).isnumeric() or ro_s.isnumeric():
                ro_s = float(self.ui.ro_s_Wave_txt.text())

            if float(nu) > 1.6 or float(nu) < 0.9:
                self.ui.nu_Wave_txt.setText("Check value")
                inputController = 0
                return None

            if float(ro) > 1300 or float(ro) < 900:
                self.ui.ro_Wave_txt.setText("Check value")
                inputController = 0
                return None

            if float(ro_s) > 3000 or float(ro_s) < 2000:
                self.ui.ro_s_Wave_txt.setText("Check value")
                inputController = 0
                return None

        # H0 = 1
        # T = 6
        # angle = 20
        # d50 = 0.2*10**-3
        # h = 10
        # z = 0.1
        # nu = 1.36*10**-6
        # ro = 1027
        # ro_s = 2650
        waveRes = Waves(H0,T,angle,d50,h,z,nu,ro,ro_s,bedType)
        self.ui.condition_Wave_txt.setText(waveRes.control())

        ## Wave Characteristics
        self.ui.regularOrbitalVelocity_txt.setText('%.8f'%waveRes.regularOrbitalVelocity())
        self.ui.excursionLength_txt.setText('%.8f'%waveRes.excursionLength())
        self.ui.reynolds_txt.setText('%.8f'%waveRes.reynolds())
        self.ui.waveLength_txt.setText('%.8f'%waveRes.waveLength())
        self.ui.waveHeight_txt.setText('%.8f'%waveRes.waveHeight())
        self.ui.approachAngle_txt.setText('%.8f'%waveRes.approachAngle())

        ## Material Properties
        self.ui.Dstar_Wave_txt.setText('%.8f'%waveRes.Dstar())
        self.ui.crShields_Wave_txt.setText('%.8f'%waveRes.shieldsCritical())
        self.ui.crShear_Wave_txt.setText('%.8f'%waveRes.tauCritical())
        self.ui.fallVelocity_Wave_txt.setText('%.8f'%waveRes.settlingVelocity())

        ## Ripple Characteristics
        self.ui.rippleHeight_Wave_txt.setText('%.8f'%waveRes.ripples()["rippleHeight"])
        self.ui.rippleLength_Wave_txt.setText('%.8f'%waveRes.ripples()["rippleLength"])

        ## Suspension & Bed Load
        self.ui.rouse_Wave_txt.setText('%.8f'%waveRes.concentration()["Rouse"])
        self.ui.concentration_Wave_txt.setText('%.8f'%waveRes.concentrationAtZ())
        self.ui.qbC_Wave_txt.setText('%.10f'%waveRes.bedLoad()["qbc"])
        self.ui.qbT_Wave_txt.setText('%.10f'%waveRes.bedLoad()["qbt"])
        self.ui.qb_Wave_txt.setText('%.10f'%waveRes.bedLoad()["qbnet"])

        ## Plotting
        waveRes.concentrationPlot()

        ## Shear Stress
        self.ui.skinShear_Wave_txt.setText('%.8f'%waveRes.tauSkin())
        self.ui.skinShields_Wave_txt.setText('%.8f'%waveRes.shieldsSkin())
        self.ui.fwZ0_txt.setText('%.8f'%waveRes.fwZ0()["fw"])
        self.ui.tauTotalZ0_txt.setText('%.8f'%waveRes.tauTotalZ0())
        self.ui.fwTable_txt.setText('%.8f'%waveRes.fwTable()["fw"])
        self.ui.tauTotalTable_txt.setText('%.8f'%waveRes.tauTotalTable())




        ## Roughness Parameters
        self.ui.z0s_Wave_txt.setText('%.8f'%waveRes.z0s())
        self.ui.z0f_Wave_txt.setText('%.8f'%waveRes.z0f())
        self.ui.z0t_Wave_txt.setText('%.8f'%waveRes.z0t())
        self.ui.flowConditionZ0_txt.setText(waveRes.fwZ0()["Condition"])

        self.ui.z0Table_Wave_txt.setText('%.4f'%waveRes.z0Table()[bedType])
        self.ui.z0Total_Wave_txt.setText('%.8f'%waveRes.z0Total())
        self.ui.flowConditionTable_txt.setText(waveRes.fwTable()["Condition"])

    def calculateWPC(self):

        ## Input Error Check
        inputController = 0
        while inputController == 0:
            inputController = 1
            H0 = self.ui.H0_wpc_txt.text()
            T = self.ui.T_wpc_txt.text()
            angle = self.ui.alpha0_wpc_txt.text()
            U_bar = self.ui.Ubar_wpc_txt.text()
            fi = self.ui.fi_wpc_txt.text()
            d50 = self.ui.d50_wpc_txt.text()
            h = self.ui.h_wpc_txt.text()
            z = self.ui.z_wpc_txt.text()
            nu = self.ui.nu_wpc_txt.text()
            ro = self.ui.ro_wpc_txt.text()
            ro_s = self.ui.ro_s_wpc_txt.text()
            
            if not (H0.isnumeric() or (H0.replace(".","",1)).isnumeric()):
                self.ui.H0_wpc_txt.setText("Enter a number")
                inputController = 0
                return None
            elif (H0.replace(".","")).isnumeric() or H0.isnumeric():
                H0 = float(self.ui.H0_wpc_txt.text())

            if not (T.isnumeric() or (T.replace(".","",1)).isnumeric()):
                self.ui.T_wpc_txt.setText("Enter a number")
                inputController = 0
                return None
            elif (T.replace(".","")).isnumeric() or T.isnumeric():
                T = float(self.ui.T_wpc_txt.text())

            if not (angle.isnumeric() or (angle.replace(".","",1)).isnumeric()):
                self.ui.alpha0_wpc_txt.setText("Enter a number")
                inputController = 0
                return None
            elif (angle.replace(".","")).isnumeric() or angle.isnumeric():
                angle = float(self.ui.alpha0_wpc_txt.text())

            if not (U_bar.isnumeric() or (U_bar.replace(".","",1)).isnumeric()):
                self.ui.Ubar_wpc_txt.setText("Enter a number")
                inputController = 0
                return None
            elif (U_bar.replace(".","")).isnumeric() or U_bar.isnumeric():
                U_bar = float(self.ui.Ubar_wpc_txt.text())

            if not (fi.isnumeric() or (fi.replace(".","",1)).isnumeric()):
                self.ui.fi_wpc_txt.setText("Enter a number")
                inputController = 0
                return None
            elif (fi.replace(".","")).isnumeric() or fi.isnumeric():
                fi = float(self.ui.fi_wpc_txt.text())

            if not (d50.isnumeric() or (d50.replace(".","",1)).isnumeric()):
                self.ui.d50_wpc_txt.setText("Enter a number")
                inputController == 0
                return None
            elif (d50.replace(".","")).isnumeric() or d50.isnumeric():
                d50 = float(self.ui.d50_wpc_txt.text())

            if not (h.isnumeric() or (h.replace(".","",1)).isnumeric()):
                self.ui.h_wpc_txt.setText("Enter a number")
                inputController == 0
                return None
            elif (h.replace(".","")).isnumeric() or h.isnumeric():
                h = float(self.ui.h_wpc_txt.text())

            if not (z.isnumeric() or (z.replace(".","",1)).isnumeric()):
                self.ui.z_wpc_txt.setText("Enter a number")
                inputController == 0
                return None
            elif (z.replace(".","")).isnumeric() or z.isnumeric():
                z = float(self.ui.z_wpc_txt.text())

            if not (nu.isnumeric() or (nu.replace(".","",1)).isnumeric()):
                self.ui.nu_wpc_txt.setText("Enter a number")
                inputController == 0
                return None
            elif (nu.replace(".","")).isnumeric() or nu.isnumeric():
                nu = float(self.ui.nu_wpc_txt.text())

            if not (ro.isnumeric() or (ro.replace(".","",1)).isnumeric()):
                self.ui.ro_wpc_txt.setText("Enter a number")
                inputController == 0
                return None
            elif (ro.replace(".","")).isnumeric() or ro.isnumeric():
                ro = float(self.ui.ro_wpc_txt.text())

            if not (ro_s.isnumeric() or (ro_s.replace(".","",1)).isnumeric()):
                self.ui.ro_s_wpc_txt.setText("Enter a number")
                inputController == 0
                return None
            elif (ro_s.replace(".","")).isnumeric() or ro_s.isnumeric():
                ro_s = float(self.ui.ro_s_wpc_txt.text())

            if float(nu) > 1.6 or float(nu) < 0.9:
                self.ui.nu_wpc_txt.setText("Check value")
                inputController = 0
                return None

            if float(ro) > 1300 or float(ro) < 900:
                self.ui.ro_wpc_txt.setText("Check value")
                inputController = 0
                return None

            if float(ro_s) > 3000 or float(ro_s) < 2000:
                self.ui.ro_s_wpc_txt.setText("Check value")
                inputController = 0
                return None
        # H0 = 1
        # T = 6
        # angle = 20
        # d50 = 0.2*10**-3
        # h = 10
        # z = 0.1
        # nu = 1.36*10**-6
        # ro = 1027
        # ro_s = 2650
        # U_bar = 1
        # fi = 0

        wpcRes = WavePlusCurrent(H0, T, angle, U_bar, d50, h, z, nu, ro, ro_s, fi)

        ## Wave Characteristics Under Current
        self.ui.regularOrbitalVelocity_wpc_txt.setText('%.8f'%wpcRes.orbitalVelocity())
        self.ui.excursionLength_wpc_txt.setText('%.8f'%wpcRes.excursionLength())
        self.ui.waveLength_wpc_txt.setText('%.8f'%wpcRes.waveLength())
        self.ui.waveHeight_wpc_txt.setText('%.8f'%wpcRes.waveHeight())
        self.ui.approachAngle_wpc_txt.setText('%.8f'%wpcRes.approachAngle())

        ## Material Properties
        self.ui.Dstar_wpc_txt.setText('%.8f'%wpcRes.Dstar())
        self.ui.crShields_wpc_txt.setText('%.8f'%wpcRes.shieldsCritical())
        self.ui.crShear_wpc_txt.setText('%.8f'%wpcRes.tauCritical())
        self.ui.fallVelocity_wpc_txt.setText('%.8f'%wpcRes.settlingVelocity())

        ## Suspension & Bed Load
        self.ui.concentration_wpc_txt.setText('%.8f'%wpcRes.concentrationAtZ())
        self.ui.qbx_txt.setText('%.8f'%wpcRes.bedLoad()["qbx"])
        self.ui.qby_txt.setText('%.8f'%wpcRes.bedLoad()["qby"])

        ## Friction Factors
        self.ui.fwSkin_wpc_txt.setText('%.8f'%wpcRes.fwSkin())
        self.ui.CDSkin_wpc_txt.setText('%.8f'%wpcRes.CDSkin())
        self.ui.fw_wpc_txt.setText('%.8f'%wpcRes.fw())
        self.ui.CD_wpc_txt.setText('%.8f'%wpcRes.CD())

        ## Shear Stress
        self.ui.skinShearCurrent_wpc_txt.setText('%.8f'%wpcRes.tauCurrentSkin())
        self.ui.totalShearCurrent_wpc_txt.setText('%.8f'%wpcRes.tauCurrent())
        self.ui.skinShieldsCurrent_wpc_txt.setText('%.8f'%wpcRes.shieldsCurrentSkin())
        self.ui.totalShieldsCurrent_wpc_txt.setText('%.8f'%wpcRes.shieldsCurrent())

        self.ui.skinShearWave_wpc_txt.setText('%.8f'%wpcRes.tauWaveSkin())
        self.ui.totalShearWave_wpc_txt.setText('%.8f'%wpcRes.tauWave())
        self.ui.skinShieldsWave_wpc_txt.setText('%.8f'%wpcRes.shieldsWaveSkin())
        self.ui.totalShieldsWave_wpc_txt.setText('%.8f'%wpcRes.shieldsWave())

        self.ui.meanSkinShear_wpc_txt.setText('%.8f'%wpcRes.tauMeanMaxSkin()["tauMeanSkin"])
        self.ui.maxSkinShear_wpc_txt.setText('%.8f'%wpcRes.tauMeanMaxSkin()["tauMaxSkin"])
        self.ui.meanTotalShear_wpc_txt.setText('%.8f'%wpcRes.tauMeanMax()["tauMean"])
        self.ui.maxTotalShear_wpc_txt.setText('%.8f'%wpcRes.tauMeanMax()["tauMax"])
        self.ui.meanSkinShields_wpc_txt.setText('%.8f'%wpcRes.shieldsMeanMaxSkin()["shieldsMeanSkin"])
        self.ui.maxSkinShields_wpc_txt.setText('%.8f'%wpcRes.shieldsMeanMaxSkin()["shieldsMaxSkin"])
        self.ui.meanTotalShields_wpc_txt.setText('%.8f'%wpcRes.shieldsMeanMax()["shieldsMean"])
        self.ui.maxTotalShields_wpc_txt.setText('%.8f'%wpcRes.shieldsMeanMax()["shieldsMax"])

        ## Plotting
        wpcRes.concentrationPlot()




def app():
    app = QtWidgets.QApplication(sys.argv)
    win = MyApp()
    win.show()
    sys.exit(app.exec_())

app()