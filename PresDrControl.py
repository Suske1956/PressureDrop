import sys
import math
from PyQt5 import QtWidgets
from scipy.optimize import brentq
from PresDr import Ui_MainWindow


class Calculate:
    # class variables
    def __init__(self):
        self.length = None
        self.length_ok = False
        self.diameter = None
        self.diameter_ok = False
        self.roughness = None
        self.roughness_ok = False
        self.density = None
        self.density_ok = False
        self.dynamic_viscosity = None
        self.dynamic_viscosity_ok = False
        self.kinematic_viscosity = None
        self.kinematic_viscosity = False
        self.velocity = None
        self.velocity_ok = False
        self.flow_rate = None
        self.flow_rate_ok = False
        self.volume = None
        self.volume_ok = False
        self.reynolds_number = None
        self.reynolds_number_ok = False
        self.flow_regime = 'Unknown'
        self.velocity_active = True
        self.dynamic_viscosity_active = True
        self.type_of_conduit = 'Unknown'
        self.line_smooth = False
        self.friction_factor = None
        self.friction_factor_ok = False
        self.pressure_drop = None
        self.pressure_drop_ok = False
        self.method = 'Unknown'

    def calculate_start(self):
        # convert velocity and flow rate triggered by radio buttons
        if self.snelheid_actief:
            if self.diameter_ok and self.snelheid_ok:
                self.debiet = math.pow(self.diameter / 2, 2) * math.pi * self.snelheid
                self.debiet_ok = True
            else:
                self.debiet_ok = False
        else:
            if self.diameter_ok and self.debiet_ok:
                self.snelheid = self.debiet / (math.pow(self.diameter / 2, 2) * math.pi)
                self.snelheid_ok = True
            else:
                self.snelheid_ok = False

        # omrekenen kinematische en dynamische viscositeit, afhankelijk stand radiobuttons
        if self.dynvisc_actief:
            if self.densiteit_ok and self.dyn_visc_ok:
                self.kin_visc = self.dyn_visc / self.densiteit
                self.kin_visc_ok = True
            else:
                self.kin_visc_ok = False
        else:
            if self.densiteit_ok and self.kin_visc_ok:
                self.dyn_visc = self.kin_visc * self.densiteit
                self.dyn_visc_ok = True
            else:
                self.dyn_visc_ok = False

        # bereken leiding inhoud
        if self.lengte_ok and self.diameter_ok:
            self.inhoud = self.lengte * (self.diameter/2)**2*math.pi
            self.inhoud_ok = True
        else:
            self.inhoud_ok = False

        # bereken reynolds getal
        if self.diameter_ok and self.kin_visc_ok and self.snelheid_ok:
            self.reynolds_getal = (self.snelheid * self.diameter) / self.kin_visc
            self.reynolds_getal_ok = True
            self.bepaal_ruwheid()
            self.bereken_frictiefactor()
            if self.reynolds_getal < 2320:
                self.stroming_type = 'Laminair'
            else:
                self.stroming_type = 'Turbulent'
        else:
            self.reynolds_getal_ok = False
            self.stroming_type = 'Niet Bekend'

    def bepaal_ruwheid(self):
        if self.reynolds_getal_ok and self.diameter_ok and self.wandruwheid_ok:
            if self.reynolds_getal * self.wandruwheid / self.diameter < 65:
                self.leiding_ruwheid = 'Gladde buis'
                self.leiding_gladde_buis = True
            elif 65 <= self.reynolds_getal * self.wandruwheid / self.diameter < 1300:
                self.leiding_ruwheid = 'Overgangsgebied'
                self.leiding_gladde_buis = False
            else:
                self.leiding_ruwheid = 'Ruwe buis'
                self.leiding_gladde_buis = False
        else:
            self.leiding_ruwheid = 'Niet Bekend'

    @staticmethod
    def colebrook_white(x, diameter, ruwheid, reynolds):
        return (1 / math.sqrt(x)) + 2 * math.log10((ruwheid / (3.7 * diameter)) + 2.51 / (reynolds * math.sqrt(x)))

    def bereken_frictiefactor(self):
        if self.reynolds_getal_ok and self.diameter_ok and self.wandruwheid_ok:
            if self.reynolds_getal < 2320 and self.leiding_gladde_buis:
                self.frictie_factor = 64/self.reynolds_getal
                self.frictie_factor_ok = True
                self.rekenmethode = 'Laminair, Glad'
            elif 2320 <= self.reynolds_getal < 4000 and self.leiding_gladde_buis:
                self.frictie_factor = 0.3164 * math.pow(self.reynolds_getal, -0.25)
                self.frictie_factor_ok = True
                self.rekenmethode = 'Blasius'
            else:
                self.frictie_factor = brentq(self.colebrook_white, 1e-10, 1e10, args=(
                    self.diameter, self.wandruwheid, self.reynolds_getal))
                self.frictie_factor_ok = True
                self.rekenmethode = 'Colebrook White'
            self.bereken_drukverschil()

    def bereken_drukverschil(self):
        if self.frictie_factor_ok and self.lengte_ok and self.diameter_ok and self.snelheid_ok and self.densiteit_ok:
            self.drukverschil = self.frictie_factor * self.lengte /\
                                self.diameter * self.densiteit / 2 * self.snelheid ** 2
            self.drukverschil_ok = True
        else:
            self.drukverschil_ok = False


class Invoerveld:
    def __init__(self):
        self.waarde_str = None
        self.waarde_float = None
        self.invoer_ok = False
        self.stijl_string = 'background-color: red;'

    def test_invoer(self):
        try:
            self.waarde_float = float(self.waarde_str)
        except ValueError:
            self.invoer_ok = False
            self.stijl_string = 'background-color: red;'
        else:
            self.invoer_ok = True
            self.stijl_string = 'background-color: white;'
            return self.waarde_float


class MainWindowExec:
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        mainwindow = QtWidgets.QMainWindow()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(mainwindow)

        # objecten
        self.reken = Rekenen()
        self.leiding_diameter = Invoerveld()
        self.leiding_lengte = Invoerveld()
        self.leiding_wandruwheid = Invoerveld()
        self.vloeistof_densiteit = Invoerveld()
        self.vloeistof_viscdyn = Invoerveld()
        self.vloeistof_visckin = Invoerveld()
        self.stroming_snelheid = Invoerveld()
        self.stroming_debiet = Invoerveld()

        self.bereken_start()

        mainwindow.show()
        sys.exit(app.exec_())

    def bereken_start(self):
        self.ui.Leiding_Lengte.editingFinished.connect(self.leiding_lengte_start)
        self.ui.Leiding_Diameter.editingFinished.connect(self.leiding_diameter_start)
        self.ui.Leiding_Wandruwheid.editingFinished.connect(self.leiding_wandruwheid_start)
        self.ui.Vloeistof_Densiteit.editingFinished.connect(self.vloeistof_densiteit_start)
        self.ui.Vloeistof_ViscDyn.editingFinished.connect(self.vloeistof_viscdyn_start)
        self.ui.Vloeistof_ViscKin.editingFinished.connect(self.vloeistof_visckin_start)
        self.ui.Stroming_Snelheid.editingFinished.connect(self.stroming_snelheid_start)
        self.ui.Stroming_Debiet.editingFinished.connect(self.stroming_debiet_start)
        self.ui.DynVisBekend.clicked.connect(self.visc_bekend)
        self.ui.KinViscBekend.clicked.connect(self.visc_bekend)
        self.ui.SnelheidBekend.clicked.connect(self.stromingtype_bekend)
        self.ui.DebietBekend.clicked.connect(self.stromingtype_bekend)

    def leiding_lengte_start(self):
        self.leiding_lengte.waarde_str = self.ui.Leiding_Lengte.text()
        self.reken.lengte = self.leiding_lengte.test_invoer()
        self.reken.lengte_ok = self.leiding_lengte.invoer_ok
        self.ui.Leiding_Lengte.setStyleSheet(self.leiding_lengte.stijl_string)
        self.reken.berekenen_start()
        self.uitvoer()

    def leiding_diameter_start(self):
        self.leiding_diameter.waarde_str = self.ui.Leiding_Diameter.text()
        self.reken.diameter = self.leiding_diameter.test_invoer()
        self.reken.diameter_ok = self.leiding_diameter.invoer_ok
        self.ui.Leiding_Diameter.setStyleSheet(self.leiding_diameter.stijl_string)
        self.reken.berekenen_start()
        self.uitvoer()

    def leiding_wandruwheid_start(self):
        self.leiding_wandruwheid.waarde_str = self.ui.Leiding_Wandruwheid.text()
        self.reken.wandruwheid = self.leiding_wandruwheid.test_invoer()
        self.reken.wandruwheid_ok = self.leiding_wandruwheid.invoer_ok
        self.ui.Leiding_Wandruwheid.setStyleSheet(self.leiding_wandruwheid.stijl_string)
        self.reken.berekenen_start()
        self.uitvoer()

    def vloeistof_densiteit_start(self):
        self.vloeistof_densiteit.waarde_str = self.ui.Vloeistof_Densiteit.text()
        self.reken.densiteit = self.vloeistof_densiteit.test_invoer()
        self.reken.densiteit_ok = self.vloeistof_densiteit.invoer_ok
        self.ui.Vloeistof_Densiteit.setStyleSheet(self.vloeistof_densiteit.stijl_string)
        self.reken.berekenen_start()
        self.uitvoer()

    def vloeistof_viscdyn_start(self):
        self.vloeistof_viscdyn.waarde_str = self.ui.Vloeistof_ViscDyn.text()
        self.reken.dyn_visc = self.vloeistof_viscdyn.test_invoer()
        self.reken.dyn_visc_ok = self.vloeistof_viscdyn.invoer_ok
        self.ui.Vloeistof_ViscDyn.setStyleSheet(self.vloeistof_viscdyn.stijl_string)
        self.reken.berekenen_start()
        self.uitvoer()

    def vloeistof_visckin_start(self):
        self.vloeistof_visckin.waarde_str = self.ui.Vloeistof_ViscKin.text()
        self.reken.kin_visc = self.vloeistof_visckin.test_invoer()
        self.reken.kin_visc_ok = self.vloeistof_visckin.invoer_ok
        self.ui.Vloeistof_ViscKin.setStyleSheet(self.vloeistof_visckin.stijl_string)
        self.reken.berekenen_start()
        self.uitvoer()

    def stroming_snelheid_start(self):
        self.stroming_snelheid.waarde_str = self.ui.Stroming_Snelheid.text()
        self.reken.snelheid = self.stroming_snelheid.test_invoer()
        self.reken.snelheid_ok = self.stroming_snelheid.invoer_ok
        self.ui.Stroming_Snelheid.setStyleSheet(self.stroming_snelheid.stijl_string)
        self.reken.berekenen_start()
        self.uitvoer()

    def stroming_debiet_start(self):
        self.stroming_debiet.waarde_str = self.ui.Stroming_Debiet.text()
        self.reken.debiet = self.stroming_debiet.test_invoer()
        self.reken.debiet_ok = self.stroming_debiet.invoer_ok
        self.ui.Stroming_Debiet.setStyleSheet(self.stroming_debiet.stijl_string)
        self.reken.berekenen_start()
        self.uitvoer()

    def visc_bekend(self):
        if self.ui.DynVisBekend.isChecked():
            self.ui.Vloeistof_ViscDyn.setEnabled(True)
            self.ui.Vloeistof_ViscKin.setEnabled(False)
            self.reken.dynvisc_actief = True
        else:
            self.ui.Vloeistof_ViscDyn.setEnabled(False)
            self.ui.Vloeistof_ViscKin.setEnabled(True)
            self.reken.dynvisc_actief = False

    def stromingtype_bekend(self):
        if self.ui.SnelheidBekend.isChecked():
            self.ui.Stroming_Snelheid.setEnabled(True)
            self.ui.Stroming_Debiet.setEnabled(False)
            self.reken.snelheid_actief = True
        else:
            self.ui.Stroming_Snelheid.setEnabled(False)
            self.ui.Stroming_Debiet.setEnabled(True)
            self.reken.snelheid_actief = False

    def uitvoer(self):
        # formatteren van invoervelden, na een invoer
        if self.reken.lengte_ok:
            self.ui.Leiding_Lengte.setText(f'{self.reken.lengte:.4e}')

        if self.reken.diameter_ok:
            self.ui.Leiding_Diameter.setText(f'{self.reken.diameter:.4e}')

        if self.reken.wandruwheid_ok:
            self.ui.Leiding_Wandruwheid.setText(f'{self.reken.wandruwheid:.4e}')

        if self.reken.densiteit_ok:
            self.ui.Vloeistof_Densiteit.setText(f'{self.reken.densiteit:.4e}')

        if self.reken.dyn_visc_ok:
            self.ui.Vloeistof_ViscDyn.setText(f'{self.reken.dyn_visc:.4e}')

        if self.reken.kin_visc_ok:
            self.ui.Vloeistof_ViscKin.setText(f'{self.reken.kin_visc:.4e}')

        if self.reken.snelheid_ok:
            self.ui.Stroming_Snelheid.setText(f'{self.reken.snelheid:.4e}')
        else:
            if not self.reken.snelheid_actief:
                self.ui.Stroming_Snelheid.setText('')

        if self.reken.debiet_ok:
            self.ui.Stroming_Debiet.setText(f'{self.reken.debiet:.4e}')
        else:
            if self.reken.snelheid_actief:
                self.ui.Stroming_Debiet.setText('')

        # Uitvoer velden
        if self.reken.inhoud_ok:
            self.ui.Uitvoer_Leiding_Diameter.setText(f'{self.reken.inhoud:.4e}')
        else:
            self.ui.Uitvoer_Leiding_Diameter.setText('Niet Bekend')

        if self.reken.reynolds_getal_ok:
            self.ui.Uitvoer_Reynolds.setText(f'{self.reken.reynolds_getal:.4e}')
        else:
            self.ui.Uitvoer_Reynolds.setText('Niet Bekend')

        if self.reken.drukverschil_ok:
            self.ui.Uitvoer_Drukverschil.setText(f'{self.reken.drukverschil:.4e}')
        else:
            self.ui.Uitvoer_Drukverschil.setText('Niet Bekend')

        if self.reken.frictie_factor_ok:
            self.ui.Uitvoer_FrictieFactor.setText(f'{self.reken.frictie_factor:.4e}')
        else:
            self.ui.Uitvoer_FrictieFactor.setText('Niet Bekend')

        self.ui.Uitvoer_TypeStroming.setText(self.reken.stroming_type)
        self.ui.Uitvoer_TypeLeiding.setText(self.reken.leiding_ruwheid)
        self.ui.Uitvoer_Methode.setText(self.reken.rekenmethode)



if __name__ == "__main__":
    MainWindowExec()
