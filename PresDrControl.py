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
        self.kinematic_viscosity_ok = False
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
        # convert velocity into flow rate vice versa triggered by the radio buttons
        if self.velocity_active:
            if self.diameter_ok and self.velocity_ok:
                self.flow_rate = math.pow(self.diameter / 2, 2) * math.pi * self.velocity
                self.flow_rate_ok = True
            else:
                self.flow_rate_ok = False
        else:
            if self.diameter_ok and self.flow_rate_ok:
                self.velocity = self.flow_rate / (math.pow(self.diameter / 2, 2) * math.pi)
                self.velocity_ok = True
            else:
                self.velocity_ok = False

        # convert kinematic into dynamic viscosity vice versa triggered by the radio buttons.
        if self.dynamic_viscosity_active:
            if self.density_ok and self.dynamic_viscosity_ok:
                self.kinematic_viscosity = self.dynamic_viscosity / self.density
                self.kinematic_viscosity_ok = True
            else:
                self.kinematic_viscosity_ok = False
        else:
            if self.density_ok and self.kinematic_viscosity_ok:
                self.dynamic_viscosity = self.kinematic_viscosity * self.density
                self.dynamic_viscosity_ok = True
            else:
                self.dynamic_viscosity_ok = False

        # Calculate line volume
        if self.length_ok and self.diameter_ok:
            self.volume = self.length * (self.diameter/2)**2*math.pi
            self.volume_ok = True
        else:
            self.volume_ok = False

        # Calculate Reynolds number
        if self.diameter_ok and self.kinematic_viscosity_ok and self.velocity_ok:
            self.reynolds_number = (self.velocity * self.diameter) / self.kinematic_viscosity
            self.reynolds_number_ok = True
            self.determine_relative_roughness()
            self.calculate_friction_factor()
            if self.reynolds_number < 2320:
                self.flow_regime = 'Laminar'
            else:
                self.flow_regime = 'Turbulent'
        else:
            self.reynolds_number_ok = False
            self.flow_regime = 'Unknown'

    def determine_relative_roughness(self):
        if self.reynolds_number and self.diameter_ok and self.roughness_ok:
            if self.reynolds_number * self.roughness / self.diameter < 65:
                self.type_of_conduit = 'Smooth conduit'
                self.line_smooth = True
            elif 65 <= self.reynolds_number * self.roughness / self.diameter < 1300:
                self.type_of_conduit = 'Intermediate conduit'
                self.line_smooth = False
            else:
                self.type_of_conduit = 'Rough conduit'
                self.line_smooth = False
        else:
            self.type_of_conduit = 'Unknown'

    @staticmethod
    def colebrook_white(x, diameter, roughness, reynolds):
        return (1 / math.sqrt(x)) + 2 * math.log10((roughness / (3.7 * diameter)) + 2.51 / (reynolds * math.sqrt(x)))

    def calculate_friction_factor(self):
        if self.reynolds_number_ok and self.diameter_ok and self.roughness_ok:
            if self.reynolds_number < 2320 and self.line_smooth:
                self.friction_factor = 64/self.reynolds_number
                self.frictie_factor_ok = True
                self.method = 'Laminar, Smooth'
            elif 2320 <= self.reynolds_number < 4000 and self.line_smooth:
                self.friction_factor = 0.3164 * math.pow(self.reynolds_number, -0.25)
                self.friction_factor_ok = True
                self.method = 'Blasius'
            else:
                self.friction_factor = brentq(self.colebrook_white, 1e-10, 1e10, args=(
                    self.diameter, self.roughness, self.reynolds_number))
                self.friction_factor_ok = True
                self.method = 'Colebrook White'
            self.calculate_pressure_drop()

    def calculate_pressure_drop(self):
        if self.friction_factor_ok and self.length_ok and self.diameter_ok and self.velocity_ok and self.density_ok:
            self.pressure_drop = self.friction_factor * self.length /\
                                self.diameter * self.density / 2 * self.velocity ** 2
            self.pressure_drop_ok = True
        else:
            self.pressure_drop_ok = False


class Check_input:
    def __init__(self):
        self.value_str = None
        self.value_float = None
        self.input_ok = False
        self.style_string = 'background-color: red;'

    def test_input(self):
        try:
            self.value_float = float(self.value_str)
        except ValueError:
            self.input_ok = False
            self.style_string = 'background-color: red;'
        else:
            self.input_ok = True
            self.style_string = 'background-color: white;'
            return self.value_float


class MainWindowExec:
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        mainwindow = QtWidgets.QMainWindow()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(mainwindow)

        # objecten
        self.calc = Calculate()
        self.line_length = Check_input()
        self.line_diameter = Check_input()
        self.line_roughness = Check_input()
        self.liquid_density = Check_input()
        self.liquid_viscdyn = Check_input()
        self.liquid_visckin = Check_input()
        self.flow_velocity = Check_input()
        self.flow_rate = Check_input()

        self.bereken_start()

        mainwindow.show()
        sys.exit(app.exec_())

    def bereken_start(self):
        self.ui.Line_Length.editingFinished.connect(self.line_length_start)
        self.ui.Line_Diameter.editingFinished.connect(self.line_diameter_start)
        self.ui.Line_WallRoughness.editingFinished.connect(self.leiding_wandruwheid_start)  # nog doen
        self.ui.Liquid_Density.editingFinished.connect(self.vloeistof_densiteit_start)  # nog doen
        self.ui.Liquid_ViscDyn.editingFinished.connect(self.vloeistof_viscdyn_start)  # nog doen
        self.ui.Liquid_ViscKin.editingFinished.connect(self.vloeistof_visckin_start)  # nog doen
        self.ui.Flow_Velocity.editingFinished.connect(self.stroming_snelheid_start)  # nog doen
        self.ui.Flow_Rate.editingFinished.connect(self.stroming_debiet_start)  # nog doen
        self.ui.DynVisKnown.clicked.connect(self.visc_bekend)  # nog doen
        self.ui.KinViscKnown.clicked.connect(self.visc_bekend)  # nog doen
        self.ui.VelocityKnown.clicked.connect(self.stromingtype_bekend)  # nog doen
        self.ui.FlowRateKnown.clicked.connect(self.stromingtype_bekend)  # nog doen

    def line_length_start(self):
        self.line_length.value_str = self.ui.Line_Length.text()
        self.calc.length = self.line_length.test_input()
        self.calc.length_ok = self.line_length.input_ok
        self.ui.Line_Length.setStyleSheet(self.line_length.style_string)
        self.calc.calculate_start()
        self.output()

    def line_diameter_start(self):
        self.line_diameter.value_str = self.ui.Line_Diameter.text()
        self.calc.diameter = self.line_diameter.test_input()
        self.calc.diameter_ok = self.line_diameter.input_ok
        self.ui.Line_Diameter.setStyleSheet(self.line_diameter.style_string)
        self.calc.calculate_start()
        self.output()

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

    def output(self):
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
