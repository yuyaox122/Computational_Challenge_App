G = 6.674 * 10**(-11)

# PLANET = (SHC, RMM, RADIUS, MASS, T0, P0)
VENUS = (0.846, 0.04401, 6051800, 4.867*(10**24), 467, 93000, 'Venus')
EARTH = (1.0035, 0.02896, 6371000, 5.972*(10**24), 15, 1013.25, 'Earth')
MARS = (0.846, 0.04401, 3389500, 6.42*(10**23), -60, 6, 'Mars')
JUPITER = (12.17, 2.328, 69911000, 1.898*(10**27), -108, 1000, 'Jupiter')
SATURN = (14.3, 2.016, 58232000, 5.683*(10**26), -139, 1000, 'Saturn')
URANUS = (11.93, 2.314, 25362000, 8.681*(10**25), -197, 1000, 'Uranus')
NEPTUNE = (11.277, 2.413, 24622000, 1.024*(10**26), -201, 1000, 'Neptune')

planets = [VENUS, EARTH, MARS, JUPITER, SATURN, URANUS, NEPTUNE]


def gravity(r, h, M):
    return G * M / (r + h)**2

def lapse_rate(shc, r, h, M):
    return gravity(r, h, M) / shc

def pressure_diff(Mr, Tc, P, r, h, M):
    Tk = Tc + 273
    return -(Mr * gravity(r, h, M)) * P * dh / (R * Tk)
  
  
def planetary_ISA(shc, Mr, r, M, T0, P0):
    heights = pressures = lapse_rates = boiling_points = temperatures = satpresses = np.array([])
    h = 0
    h_max = 10000
    dh = 10
    Tc = T0
    P = P0
    while h <= h_max:
        # Calculations
            L = lapse_rate(shc, r, h, M)
            Tboil = boiling_point(P)
            satpres = saturation_pressure(Tc)

            dP = pressure_diff(Mr, Tc, P, r, h, M)
        # Appending
            heights = np.append(heights, h / 1000)
            pressures = np.append(pressures, P)
            lapse_rates = np.append(lapse_rates, L)
            boiling_points = np.append(boiling_points, Tboil - 273)
            temperatures = np.append(temperatures, Tc)
            satpresses = np.append(satpresses, satpres)
        # Incrementing
            h += dh
            Tc -= L * dh / 1000
            P += dP
    
    return heights, pressures, lapse_rates, boiling_points, temperatures, satpresses
  

'''To plot a graph, use the following code:
for planet in planets:
    heights, pressures, lapse_rates, boiling_points, temperatures, ratios = planetary_ISA(*planet[:-1])
    lapse_rate_height = plt.plot(heights, Y_AXIS, label=planet[-1])
plt.xlabel('Altitude / km')
plt.ylabel('Y_AXIS / UNIT')
plt.legend()
'''
