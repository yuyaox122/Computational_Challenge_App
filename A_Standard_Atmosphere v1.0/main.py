from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.datatables import MDDataTable
from task1 import plotter1
from task2 import plotter2
from task3 import plotter3, pressure_altitude, lapse_rate_altitude, temperature_altitude, boiling_altitude, \
    dew_altitude, iterative_ISA
from task3 import get_planet, plot_pressure, plot_boiling, plot_lapse, plot_temperature
from kivymd.uix.menu import MDDropdownMenu
import numpy as np
import pandas as pd


def temperature(altitude_range):
    temperature_range = np.zeros(shape=(len(altitude_range, )))
    temperature_range[0] = 288
    for altitude in altitude_range[1:]:
        # current_index = altitude_range.index(altitude)
        current_index = np.where(altitude_range == altitude)[0][0]

        dt = 0
        if 0 <= altitude <= 11:
            dt = -6.5
        elif 11 <= altitude <= 20 or 47 <= altitude <= 51:
            dt = 0
        elif 20 <= altitude <= 32:
            dt = 1
        elif 32 <= altitude <= 47:
            dt = 2.8
        elif 51 <= altitude <= 71:
            dt = -2.8
        elif altitude >= 71:
            dt = -2

        temperature_range[current_index] = temperature_range[current_index - 1] + dt * (
                    altitude_range[current_index] - altitude_range[current_index - 1])

    return (temperature_range)


def data_creator():
    altitudes = np.around(np.linspace(0, 99, num=200), 5)
    altitudes = np.sort(np.append(altitudes, [11, 20, 32, 47, 51, 71]))
    temperatures = np.around(temperature(altitudes), 5)

    lapse_rates = np.array([-6.5 for altitude in altitudes if 0 <= altitude < 11] +
                           [0 for altitude in altitudes if 11 <= altitude < 20] +
                           [1 for altitude in altitudes if 20 <= altitude < 32] +
                           [2.8 for altitude in altitudes if 32 <= altitude < 47] +
                           [0 for altitude in altitudes if 47 <= altitude < 51] +
                           [-2.8 for altitude in altitudes if 51 <= altitude < 71] +
                           [-2 for altitude in altitudes if altitude >= 71])

    layers = np.array(['troposphere' for altitude in altitudes if 0 <= altitude < 11] +
                      ['tropopause' for altitude in altitudes if 11 <= altitude < 20] +
                      ['stratosphere1' for altitude in altitudes if 20 <= altitude < 32] +
                      ['stratosphere2' for altitude in altitudes if 32 <= altitude < 47] +
                      ['stratopause' for altitude in altitudes if 47 <= altitude < 51] +
                      ['mesosphere1' for altitude in altitudes if 51 <= altitude < 71] +
                      ['mesosphere2' for altitude in altitudes if altitude >= 71])

    df_values = pd.DataFrame(
        {'altitude': altitudes, 'temperature': temperatures, 'lapse rate': lapse_rates, 'layer': layers})
    df_layers = df_values.groupby(['layer'])
    isa_layers = ['troposphere', 'tropopause', 'stratosphere1', 'stratosphere2', 'stratopause', 'mesosphere1',
                  'mesosphere2']
    bounds = [(0, 11), (11, 20), (20, 32), (32, 47), (47, 51), (51, 71)]
    return df_values, isa_layers, bounds, df_layers


def new_colour(cindex):
    cindex += 1
    cindex %= len(colours)
    return colours[cindex], cindex


class MenuWindow(Screen):
    pass


class Task1(Screen):
    df_values, isa_layers, bounds, df_layers = data_creator()


class Task2(Screen):
    df_values, isa_layers, bounds, df_layers = data_creator()


class Task3(Screen):
    df_values, isa_layers, bounds, df_layers = data_creator()
    cindex = 0

    def new_lapse(self, u_lapse):
        current_colour, self.cindex = new_colour(self.cindex)
        lapse_rate_altitude(u_lapse, current_colour)
        self.ids.graph_lapse.reload()

    def new_pressure(self, u_pressure):
        current_colour, self.cindex = new_colour(self.cindex)
        pressure_altitude(u_pressure, current_colour)
        self.ids.graph_pressure.reload()

    def new_temperature(self, u_temperature):
        current_colour, self.cindex = new_colour(self.cindex)
        temperature_altitude(u_temperature, current_colour)
        self.ids.graph_temperature.reload()

    def new_boiling(self, u_boiling):
        current_colour, self.cindex = new_colour(self.cindex)
        boiling_altitude(u_boiling, current_colour)
        self.ids.graph_boiling.reload()

    def new_dew(self, u_dew):
        current_colour, self.cindex = new_colour(self.cindex)
        dew_altitude(u_dew, current_colour)
        self.ids.graph_dew.reload()

    pass


class Calculator(Screen):
    heights, pressures, lapse_rates, boiling_points, dew_points, temperatures = iterative_ISA(0)
    pressure = None
    lapse_rate = None
    boiling_point = None
    dew_point = None
    temperature = None

    def refresh_values(self):
        altitude = self.ids.altitude_input.text
        if (altitude == ''):
            altitude = 0
        U = self.ids.U_input.text
        if (U == ''):
            U = 0
        self.heights, self.pressures, self.lapse_rates, self.boiling_points, self.dew_points, self.temperatures = iterative_ISA(
            float(U))
        index = int(float(altitude) / 0.01)
        self.pressure = self.pressures[index]
        self.lapse_rate = self.lapse_rates[index]
        self.boiling_point = self.boiling_points[index]
        self.dew_point = self.dew_points[index]
        self.temperature = self.temperatures[index]
        self.ids.boiling_value.text = str(round(self.boiling_point, 2)) + '°C'
        self.ids.dew_value.text = str(round(self.dew_point, 2)) + '°C'
        self.ids.temperature_value.text = str(round(self.temperature, 2)) + '°C'
        self.ids.lapse_value.text = str(round(self.lapse_rate, 2)) + '°C/km'
        self.ids.pressure_value.text = str(round(self.pressure, 2)) + 'mbar'

    pass


class Planets(Screen):
    current_graph = 'venus_pressure.jpg'

    def refresh_graphs(self):
        self.ids.graph_venus.source = self.current_graph
        self.ids.graph_earth.source = self.current_graph
        self.ids.graph_mars.source = self.current_graph
        self.ids.graph_jupiter.source = self.current_graph
        self.ids.graph_saturn.source = self.current_graph
        self.ids.graph_uranus.source = self.current_graph
        self.ids.graph_neptune.source = self.current_graph
        self.ids.graph_custom.source = self.current_graph

    def dropdown(self, planet):
        self.menu_list = [
            {
                "viewclass": "OneLineListItem",
                "text": "Pressure",
                "on_release": lambda x="Pressure": self.pressure(planet)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Lapse Rate",
                "on_release": lambda x="Lapse Rate": self.lapse(planet)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Boiling Point",
                "on_release": lambda x="Boiling Point": self.boiling(planet)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Temperature",
                "on_release": lambda x="Temperature": self.temperature(planet)
            }
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.selection_venus,
            items=self.menu_list,
            width_mult=4
        )
        self.menu.open()

    def custom_dropdown(self):
        vals = (float(self.ids.shc_input.text),
				float(self.ids.rmm_input.text),
				float(self.ids.radius_input.text),
				float(self.ids.mass_input.text),
				float(self.ids.t0_input.text),
				float(self.ids.p0_input.text),
				'Stum')
        self.menu_list = [
            {
                "viewclass": "OneLineListItem",
                "text": "Pressure",
                "on_release": lambda x="Pressure": self.custom_pressure(vals)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Lapse Rate",
                "on_release": lambda x="Lapse Rate": self.custom_lapse(vals)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Boiling Point",
                "on_release": lambda x="Boiling Point": self.custom_boiling(vals)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Temperature",
                "on_release": lambda x="Temperature": self.custom_temperature(vals)
            }
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.selection_venus,
            items=self.menu_list,
            width_mult=4
        )
        self.menu.open()

    def temperature(self, planet):
        p = get_planet(planet)
        self.current_graph = plot_temperature(p, planet)
        self.refresh_graphs()

    def pressure(self, planet):
        p = get_planet(planet)
        self.current_graph = plot_pressure(p, planet)
        self.refresh_graphs()

    def lapse(self, planet):
        p = get_planet(planet)
        self.current_graph = plot_lapse(p, planet)
        self.refresh_graphs()

    def boiling(self, planet):
        p = get_planet(planet)
        self.current_graph = plot_boiling(p, planet)
        self.refresh_graphs()

    def custom_temperature(self, vals):
        self.current_graph = plot_temperature(vals, 'Stum')
        self.refresh_graphs()

    def custom_pressure(self, vals):
        self.current_graph = plot_pressure(vals, 'Stum')
        self.refresh_graphs()

    def custom_lapse(self, vals):
        self.current_graph = plot_lapse(vals, 'Stum')
        self.refresh_graphs()

    def custom_boiling(self, vals):
        self.current_graph = plot_boiling(vals, 'Stum')
        self.refresh_graphs()


class WindowManager(ScreenManager):
    pass


class ComputingChallenge(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Amber"
        self.theme_cls.theme_style = "Light"
        return Builder.load_file('new_window.kv')


colours = ['#264653', '#2a9d8f', '#e9c46a', '#f4a261', '#e76f51']
current_colour = colours[0]
df_values, isa_layers, bounds, df_layers = data_creator()
plotter1(df_values['altitude'], df_values['temperature'])
plotter2(df_values, df_values['altitude'], bounds, df_layers, isa_layers)
plotter3(current_colour)

if __name__ == '__main__':
    ComputingChallenge().run()
