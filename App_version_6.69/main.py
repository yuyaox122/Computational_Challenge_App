from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.datatables import MDDataTable
from task1 import data_creator, plotter1
from task2 import plotter2
from task3 import plotter3, pressure_altitude, lapse_rate_altitude, temperature_altitude, boiling_altitude, dew_altitude, iterative_ISA
from task3 import get_planet, plot_pressure, plot_boiling, plot_lapse, plot_temperature
from kivymd.uix.menu import MDDropdownMenu

def new_colour(cindex):
	cindex += 1
	cindex %= len(colours)
	return colours[cindex], cindex

class MenuWindow(Screen):
	pass

class Task1(Screen):
	pass

class Task2(Screen):
	pass

class Task3(Screen):
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
		if(altitude == ''):
			altitude = 0
		U = self.ids.U_input.text
		if(U == ''):
			U = 0
		self.heights, self.pressures, self.lapse_rates, self.boiling_points, self.dew_points, self.temperatures = iterative_ISA(float(U))
		index = int(float(altitude) / 0.01)
		self.pressure = self.pressures[index]
		self.lapse_rate = self.lapse_rates[index]
		self.boiling_point = self.boiling_points[index]
		self.dew_point = self.dew_points[index]
		self.temperature = self.temperatures[index]
		self.ids.boiling_value.text = str(round(self.boiling_point, 2))  + '°C'
		self.ids.dew_value.text = str(round(self.dew_point, 2))  + '°C'
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
	def dropdown(self, planet):
		self.menu_list = [
			{
				"viewclass": "OneLineListItem",
				"text": "Pressure",
				"on_release": lambda x = "Pressure" : self.pressure(planet)
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
			caller = self.ids.selection_venus,
			items = self.menu_list,
			width_mult = 4
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
	pass

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
