"""
Ulises Chavarria
September 29, 2020
ME 113 - Project 1
Professor Syed Zaidi
"""

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

emissivity = 0.3 # unitless
boltzmann = 5.67 * pow(10, -8) # W/m^2/K^4
heat_transfer = 15 # W/m^2
q_cond = 5000 # W/m^2
t_surr = 40 + 273.15 # K

auto_ignition_temp = 250 + 273.15 # K
max_engine_surface_temp = 200 + 273.15 # K

c4 = emissivity * boltzmann
c3 = 0
c2 = 0
c1 = heat_transfer

x_label = "T surrounding [K]"
y_label = "T surface [K]"
z_label = "Heat flux [W/m^2]"
graph_title = "Engine Surface Temperature vs Surrounding Temperature"
dashes = "---------------------------------------------------------------------"

def set_c0(t_surr_param, q_cond_param):
    c0_def = -(heat_transfer * t_surr) - (emissivity * boltzmann * pow(t_surr_param, 4)) - q_cond_param
    return c0_def

# PART A
c0_a = set_c0(t_surr, q_cond)
poly = [c4, c3, c2, c1, c0_a]
t_s_mat = np.roots(poly)
t_s = t_s_mat[3]
t_s_real = np.real(t_s)

print(dashes)
print("PART A")
print("Given surrounding temperature: {0} K".format(t_surr))
print("Surface temperature: {0:.4f} K".format(t_s_real))
print("Autoignition temperature: {} K".format(auto_ignition_temp))
if(t_s_real > auto_ignition_temp):
    print("Oil on the engine is at risk of igniting due to engine surface temperature.")
else:
    print("Oil on the engine is not at risk of igniting due to engine surface temperature.")
print(dashes, "\n")

# PART B
print(dashes)
print("PART B")
t_s_b_values = []
t_surr_b_values = []
for i in range (9):
    t_surr_b = i*5 + 273.15 + 10
    t_surr_b_values.append(t_surr_b)
    c0_b = set_c0(t_surr_b, q_cond)
    poly2 = [c4, c3, c2, c1, c0_b]
    t_s_b = np.roots(poly2)
    t_s_b_real = np.real(t_s_b[3])
    t_s_b_values.append(t_s_b_real)

    print("{0}. Surrounding temperature: {1} K. Surface temperature {2:.4f} K".format(i, t_surr_b, t_s_b_real))

plt.figure()
plt.xlabel(x_label)
plt.ylabel(y_label)
plt.title(graph_title)
auto_ignite_list = [auto_ignition_temp] * len(t_s_b_values)
plt.plot(t_surr_b_values, t_s_b_values, label="Engine surface temperature")
plt.plot(t_surr_b_values, auto_ignite_list, 'r--', label="Automatic ignition temperature")
plt.legend()
plt.show()
print(dashes, "\n")

# PART C
print(dashes)
print("PART C")

heat_flux_2d = []
t_surr_2d = []
t_s_2d = []
q_cond_c = 2000 # W/m^2
plt.figure()

for k in range (13):
    heat_flux_list = []
    t_s_c_values = []
    t_surr_c_values = []
    q_cond_c = 2000 + k * 500
    heat_flux_list.append(q_cond_c)

    print("Heat flux {0} w/m^2".format(q_cond_c))
    for i in range (9):
        t_surr_c = i*5 + 273.15 + 10
        t_surr_c_values.append(t_surr_c)
        c0_c = set_c0(t_surr_c, q_cond_c)
        poly3 = [c4, c3, c2, c1, c0_c]
        t_s_c = np.roots(poly3)
        t_s_c_real = np.real(t_s_c[3])
        t_s_c_values.append(t_s_c_real)
        print("{0}. Surrounding temperature: {1} K. Surface temperature {2:.4f} K".format(i, t_surr_c, t_s_c_real))

    test_heat_flux_list = [q_cond_c] * len(t_surr_c_values)
    t_s_2d.append(t_s_c_values)
    t_surr_2d.append(t_surr_c_values)
    heat_flux_2d.append(test_heat_flux_list)
    auto_ignite_list = [auto_ignition_temp] * len(t_s_c_values)
    plt.plot(t_surr_c_values, t_s_c_values, label="h = {0} W/m^2".format(q_cond_c))
    print("---")

plt.xlabel(x_label)
plt.ylabel(y_label)
plt.title(graph_title)
plt.plot(t_surr_c_values, auto_ignite_list, 'r--', label="Auto ignite temp")
plt.legend(loc='upper right')
plt.show()

auto_ignite_list_2d = [auto_ignite_list] * len(t_s_2d)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel(x_label)
ax.set_ylabel(y_label)
ax.set_zlabel(z_label)
ax.plot_surface(t_s_2d, t_surr_2d, np.array(heat_flux_2d), cmap="Oranges_r") 
ax.plot_wireframe(auto_ignite_list_2d, t_surr_2d, np.array(heat_flux_2d))
plt.title(graph_title)
plt.show()

print(dashes, "\n")
