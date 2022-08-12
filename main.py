from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from task1 import data_creator, plotter1
from task2 import plotter2
from task3 import plotter3, pressure_altitude, lapse_rate_altitude, temperature_altitude, boiling_altitude, dew_altitude

class MenuWindow(Screen):
	pass

class Task1(Screen):
	pass

class Task2(Screen):
	pass

class Task3(Screen):
	U_slider_boiling = ObjectProperty()
	def new_boiling(self):
		boiling_altitude(self.U_slider_boiling.value)
	pass

class WindowManager(ScreenManager):
	pass

class ComputingChallenge(MDApp):
	def build(self):
		df_values, isa_layers, bounds, df_layers = data_creator()
		plotter1(df_values['altitude'], df_values['temperature'])
		plotter2(df_values, df_values['altitude'], bounds, df_layers, isa_layers)
		plotter3()
		self.theme_cls.primary_hue = "200"
		self.theme_cls.primary_palette = "Blue"
		self.theme_cls.accent_palette = "Teal"
		return Builder.load_file('new_window.kv')

if __name__ == '__main__':
	ComputingChallenge().run()
