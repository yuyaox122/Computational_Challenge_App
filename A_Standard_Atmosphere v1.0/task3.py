import numpy as np
import matplotlib.pyplot as plt

def saturation_pressure(Tc):
    return 6.1121 * np.e ** ((18.678 - Tc / 234.5) * (Tc / (Tc + 257.14)))

def pressure_diff(U, Tc, P):
    Tk = Tc + 273
    return -(Md * g) / (R * Tk) * (P - U * (1 - Mv / Md) * saturation_pressure(Tc)) * dh

def ratio_water_air(U, Tc, P):
    return (Rsd * U * saturation_pressure(Tc)) / (Rsw * (P - U * saturation_pressure(Tc)))

def lapse_rate(U, Tc, P):
    Tk = Tc + 273
    r = ratio_water_air(U, Tc, P)
    return g * (1 + (r * dHv) / (Rsd * Tk)) / (cpd + (dHv**2 * r) / (Rsw * Tk**2))

def boiling_point(P):
    return 1 / (1 / Tstar - R / dH * np.log(P / Pstar))

def dew_point(U, Tc):
    frac = (a * Tc) / (b + Tc)
    return b * (np.log(U) + frac) / (a - np.log(U) - frac)


def iterative_ISA(U):
    heights = pressures = lapse_rates = boiling_points = dew_points = temperatures = np.array([])
    h = 0
    Tc = T0
    P = P0
    while h <= h_max:
        # Calculations
        L = lapse_rate(U, Tc, P)
        Tboil = boiling_point(P)
        Tdew = dew_point(U, Tc)

        dP = pressure_diff(U, Tc, P)
        # Appending
        heights = np.append(heights, h / 1000)
        pressures = np.append(pressures, P)
        lapse_rates = np.append(lapse_rates, L * 1000)
        boiling_points = np.append(boiling_points, Tboil - 273)
        dew_points = np.append(dew_points, Tdew)
        temperatures = np.append(temperatures, Tc)
        # Incrementing
        h += dh
        Tc -= L * dh
        P += dP
    return heights, pressures, lapse_rates, boiling_points, dew_points, temperatures

def pressure_altitude(U, current_colour):
    heights, pressures, lapse_rates, boiling_points, dew_points, temperatures = iterative_ISA(U)
    pressure_height = plt.plot(heights, pressures, color = current_colour)
    plt.xlabel('Altitude / km')
    plt.ylabel('Pressure / mbar')
    plt.savefig("task3_pressure.jpg")
    plt.clf()

def lapse_rate_altitude(U, current_colour):
    heights, pressures, lapse_rates, boiling_points, dew_points, temperatures = iterative_ISA(U)
    lapse_rate_height = plt.plot(heights, lapse_rates, color = current_colour)
    plt.xlabel('Altitude / km')
    plt.ylabel('Lapse rate / ℃/km')
    plt.savefig("task3_lapse_rate.jpg")
    plt.clf()

def temperature_altitude(U, current_colour):
    heights, pressures, lapse_rates, boiling_points, dew_points, temperatures = iterative_ISA(U)
    temperature_height = plt.plot(heights, temperatures, color = current_colour)
    plt.xlabel('Altitude / km')
    plt.ylabel('Temperature / ℃')
    plt.savefig("task3_temperature.jpg")
    plt.clf()

def boiling_altitude(U, current_colour):
    heights, pressures, lapse_rates, boiling_points, dew_points, temperatures = iterative_ISA(U)
    boiling_height = plt.plot(heights, boiling_points, color = current_colour)
    plt.xlabel('Altitude / km')
    plt.ylabel('Boiling point / ℃')
    plt.savefig("task3_boiling.jpg")
    plt.clf()

def dew_altitude(U, current_colour):
    heights, pressures, lapse_rates, boiling_points, dew_points, temperatures = iterative_ISA(U)
    dew_height = plt.plot(heights, dew_points, color = current_colour)
    plt.xlabel('Altitude / km')
    plt.ylabel('Dew point / ℃')
    plt.savefig("task3_dew.jpg")
    plt.clf()

def plotter3(current_colour):
    pressure_altitude(0, current_colour)
    lapse_rate_altitude(0, current_colour)
    temperature_altitude(0, current_colour)
    boiling_altitude(0, current_colour)
    dew_altitude(0, current_colour)

T0 = 15
Tstar = 373
P0 = Pstar = 1013.25
dh = 10
Md = 0.02896
Mv = 0.01802
R = 8.314
g = 9.81
dHv = 2501000
cpd = 1003.5
Rsd = 287
Rsw = 461.5
a = 17.625
b = 243.04
dH = 40800
h_max = 11000

G = 6.674 * 10 ** (-11)

# PLANET = (SHC, RMM, RADIUS, MASS, T0, P0)
VENUS = (0.846, 0.04401, 6051800, 4.867 * (10 ** 24), 467, 93000, 'Venus')
EARTH = (1.0035, 0.02896, 6371000, 5.972 * (10 ** 24), 15, 1013.25, 'Earth')
MARS = (0.846, 0.04401, 3389500, 6.42 * (10 ** 23), -60, 6, 'Mars')
JUPITER = (12.17, 2.328, 69911000, 1.898 * (10 ** 27), -108, 1000, 'Jupiter')
SATURN = (14.3, 2.016, 58232000, 5.683 * (10 ** 26), -139, 1000, 'Saturn')
URANUS = (11.93, 2.314, 25362000, 8.681 * (10 ** 25), -197, 1000, 'Uranus')
NEPTUNE = (11.277, 2.413, 24622000, 1.024 * (10 ** 26), -201, 1000, 'Neptune')

planets = [VENUS, EARTH, MARS, JUPITER, SATURN, URANUS, NEPTUNE]


def gravity(r, h, M):
    return G * M / (r + h) ** 2


def planet_lapse_rate(shc, r, h, M):
    return gravity(r, h, M) / shc


def planet_pressure_diff(Mr, Tc, P, r, h, M):
    Tk = Tc + 273
    return -(Mr * gravity(r, h, M)) * P * dh / (R * Tk)


def planetary_ISA(shc, Mr, r, M, T0, P0):
    heights = pressures = lapse_rates = boiling_points = temperatures = np.array([])
    h = 0
    h_max = 10000
    dh = 10
    Tc = T0
    P = P0
    while h <= h_max:
        # Calculations
        L = planet_lapse_rate(shc, r, h, M)
        Tboil = boiling_point(P)

        dP = planet_pressure_diff(Mr, Tc, P, r, h, M)
        # Appending
        heights = np.append(heights, h / 1000)
        pressures = np.append(pressures, P)
        lapse_rates = np.append(lapse_rates, L)
        boiling_points = np.append(boiling_points, Tboil - 273)
        temperatures = np.append(temperatures, Tc)
        # Incrementing
        h += dh
        Tc -= L * dh / 1000
        P += dP

    return heights, pressures, lapse_rates, boiling_points, temperatures


'''To plot a graph, use the following code:
for planet in planets:
    heights, pressures, lapse_rates, boiling_points, temperatures, ratios = planetary_ISA(*planet[:-1])
    lapse_rate_height = plt.plot(heights, Y_AXIS, label=planet[-1])
plt.xlabel('Altitude / km')
plt.ylabel('Y_AXIS / UNIT')
plt.legend()
'''
def get_planet(planet):
    for p in planets:
        if(p[-1] == planet):
            return p

def plot_pressure(p, planet):
    heights, pressures, lapse_rates, boiling_points, temperatures = planetary_ISA(*p[:-1])
    plt.plot(heights, pressures)
    plt.xlabel('Altitude /km')
    plt.ylabel('Pressure /mbar')
    plt.savefig(planet.lower() + "_pressure.jpg")
    plt.clf()
    return planet.lower() + "_pressure.jpg"

def plot_lapse(p, planet):
    heights, pressures, lapse_rates, boiling_points, temperatures = planetary_ISA(*p[:-1])
    plt.plot(heights, lapse_rates)
    plt.xlabel('Altitude /km')
    plt.ylabel('Lapse Rate /℃/km')
    plt.savefig(planet.lower() + "_lapse.jpg")
    plt.clf()
    return planet.lower() + "_lapse.jpg"

def plot_boiling(p, planet):
    heights, pressures, lapse_rates, boiling_points, temperatures = planetary_ISA(*p[:-1])
    plt.plot(heights, boiling_points)
    plt.xlabel('Altitude /km')
    plt.ylabel('Boiling Point /℃')
    plt.savefig(planet.lower() + "_boiling.jpg")
    plt.clf()
    return planet.lower() + "_boiling.jpg"

def plot_temperature(p, planet):
    heights, pressures, lapse_rates, boiling_points, temperatures = planetary_ISA(*p[:-1])
    plt.plot(heights, temperatures)
    plt.xlabel('Altitude /km')
    plt.ylabel('Temperature /℃')
    plt.savefig(planet.lower() + "_temperature.jpg")
    plt.clf()
    return planet.lower() + "_temperature.jpg"