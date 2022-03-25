from matplotlib import pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
from scipy.stats import linregress

def func(x, a, b):
    return a*x + b

lamb, A = np.loadtxt('Bi4Ti3O12.txt', delimiter=',', unpack=True,  skiprows=1)


x = 1240 / lamb
y = (2.303 * x * A)**2

y_smooth = savgol_filter(y, 51, 3)

dy = np.diff(y_smooth, 1)
dx = np.diff(x, 1)
dydx_smooth = savgol_filter(dy / dx, 101, 3)
maxindex = np.argmax(dydx_smooth)


x_linear = x[maxindex - 10: maxindex + 10]
y_linear = y_smooth[maxindex - 10: maxindex + 10]
a, b, r_value, p_value, stderr = linregress(x_linear, y_linear)
E_bandgap = round(-b/a, 2)


visualization_x = np.linspace(E_bandgap, x[maxindex-60], 2)

plt.scatter(E_bandgap, 0, marker='x', color='k', label="Bandgap = " + str(E_bandgap) + "eV")
plt.plot(x, y_smooth)
plt.plot(visualization_x, func(visualization_x, a, b), color='red')


plt.xlabel("Energia")
plt.ylabel("$(alpha h nu)^2$")
plt.title("Tauc plot")
plt.legend()
plt.grid()
plt.show()