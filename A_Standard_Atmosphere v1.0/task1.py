import matplotlib.pyplot as plt

def plotter1(altitudes, temperatures):
    plt.plot(altitudes, temperatures)
    plt.xlabel('Altitude / m')
    plt.ylabel('Temperature / K')
    plt.savefig("task1.jpg")
    plt.clf()