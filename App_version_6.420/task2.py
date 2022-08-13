import numpy as np
import matplotlib.pyplot as plt

def pressure(row, df_layers, isa_layers):
    constant_mgr = 0.034171
    alt, temp, lapse, layer = row['altitude'], row['temperature'], row['lapse rate'], row['layer']

    lapse /= -1000
    alt *= 1000

    firsts = df_layers.first()

    h0, t0 = firsts['altitude'][layer] * 1000, firsts['temperature'][layer]

    if layer == 'troposphere':
        p0 = 101325

    else:
        previous_layer = isa_layers[isa_layers.index(layer) - 1]

        for attribute in ['altitude', 'temperature']:
            row[attribute] = firsts[attribute][layer]
        row['lapse rate'] = firsts['lapse rate'][previous_layer]
        row['layer'] = previous_layer
        p0 = pressure(row, df_layers, isa_layers)

    if lapse == 0:
        return p0 * np.e ** (-constant_mgr * (alt - h0) / t0)
    else:
        return p0 * (1 - lapse * (alt - h0) / t0) ** (constant_mgr / lapse)

def plotter2(df_values, altitudes, bounds, df_layers, isa_layers):
    pressures = np.array([])
    for i in range(len(df_values)):
        pressures = np.append(pressures, pressure(df_values.iloc[i], df_layers, isa_layers))
    df_values['pressure'] = pressures

    for i in bounds:
        plt.plot(altitudes[np.logical_and(i[0] <= altitudes, altitudes < i[1])], pressures[np.logical_and(i[0] <= altitudes, altitudes < i[1])])
    plt.xlabel('Altitude / km')
    plt.ylabel('Pressure / Pa')
    plt.savefig("task2.jpg")
    plt.clf()
