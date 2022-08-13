import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def temperature(altitude_range):
    temperature_range = np.zeros(shape=(len(altitude_range,)))
    temperature_range[0] = 288
    for altitude in altitude_range[1:]:
        # current_index = altitude_range.index(altitude)
        current_index = np.where(altitude_range==altitude)[0][0]

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

        temperature_range[current_index] = temperature_range[current_index - 1] + dt * (altitude_range[current_index] - altitude_range[current_index - 1])

    return(temperature_range)

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

    df_values = pd.DataFrame({'altitude': altitudes, 'temperature': temperatures, 'lapse rate': lapse_rates, 'layer': layers})
    df_layers = df_values.groupby(['layer'])
    isa_layers = ['troposphere', 'tropopause', 'stratosphere1', 'stratosphere2', 'stratopause', 'mesosphere1', 'mesosphere2']
    bounds = [(0, 11), (11, 20), (20, 32), (32, 47), (47, 51), (51, 71)]
    return df_values, isa_layers, bounds, df_layers

def plotter1(altitudes, temperatures):
    plt.plot(altitudes, temperatures)
    plt.xlabel('Altitude / m')
    plt.ylabel('Temperature / K')
    plt.savefig("task1.jpg")
    plt.clf()
