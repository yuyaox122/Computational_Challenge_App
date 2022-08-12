import numpy as np
import matplotlib.pyplot as plt

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
colours = ['#264653', '#2a9d8f', '#e9c46a', '#f4a261', '#e76f51']

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

def pressure_altitude(U):
    heights, pressures, lapse_rates, boiling_points, dew_points, temperatures = iterative_ISA(U)
    pressure_height = plt.plot(heights, pressures)
    plt.xlabel('Altitude / km')
    plt.ylabel('Pressure / mbar')
    plt.savefig("task3_pressure.jpg")
    plt.clf()

def lapse_rate_altitude(U):
    heights, pressures, lapse_rates, boiling_points, dew_points, temperatures = iterative_ISA(U)
    lapse_rate_height = plt.plot(heights, lapse_rates)
    plt.xlabel('Altitude / km')
    plt.ylabel('Lapse rate / ℃/km')
    plt.savefig("task3_lapse_rate.jpg")
    plt.clf()

def temperature_altitude(U):
    heights, pressures, lapse_rates, boiling_points, dew_points, temperatures = iterative_ISA(U)
    temperature_height = plt.plot(heights, temperatures)
    plt.xlabel('Altitude / km')
    plt.ylabel('Temperature / ℃')
    plt.savefig("task3_temperature.jpg")
    plt.clf()

def boiling_altitude(U):
    heights, pressures, lapse_rates, boiling_points, dew_points, temperatures = iterative_ISA(U)
    boiling_height = plt.plot(heights, boiling_points)
    plt.xlabel('Altitude / km')
    plt.ylabel('Boiling point / ℃')
    plt.savefig("task3_boiling.jpg")
    plt.clf()

def dew_altitude(U):
    heights, pressures, lapse_rates, boiling_points, dew_points, temperatures = iterative_ISA(U)
    dew_height = plt.plot(heights, dew_points)
    plt.xlabel('Altitude / km')
    plt.ylabel('Dew point / ℃')
    plt.savefig("task3_dew.jpg")
    plt.clf()

def plotter3():
    pressure_altitude(0)
    lapse_rate_altitude(0)
    temperature_altitude(0)
    boiling_altitude(0)
    dew_altitude(0)