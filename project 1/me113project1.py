import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

emissivity = 0.3 # unitless
boltzman = 5.67 * pow(10, -8) # W/m^2/K^4
heat_transfer = 15 # W/m^2
q_cond = 5000 # W/m^2
t_surr = 40 + 273.15 # K

auto_ignition_temp = 250 + 273.15 # K
max_engine_surface_temp = 200 + 273.15 # K

def set_c0(t_surr_param, q_cond_param):
    c0_def = -(heat_transfer * t_surr) - (emissivity * boltzman * pow(t_surr_param, 4)) - q_cond_param
    return c0_def

# PART A
c4 = emissivity * boltzman
c3 = 0
c2 = 0
c1 = heat_transfer
# c0 = -(heat_transfer * t_surr) - (emissivity * boltzman * pow(t_surr, 4)) - q_cond
c0_a = set_c0(t_surr, q_cond)

poly = [c4, c3, c2, c1, c0_a]
t_s_mat = np.roots(poly)
t_s = t_s_mat[3]
t_s_real = np.real(t_s)

# print("\nTs_mat: ", t_s_mat)
dashes = "---------------------------------------------------------------------"
print(dashes)
print("PART A")
print("Given surrounding temperature: {0} K".format(t_surr))
print("Surface temperature: {0:.4f} K".format(t_s_real))
print(dashes, "\n")

# PART B

t_s_b_values = []
t_surr_b_values = []
for i in range (9):
    t_surr_b = i*5 + 273.15 + 10
    t_surr_b_values.append(t_surr_b)
    # c0_b = -(heat_transfer * t_surr) - (emissivity * boltzman * pow(t_surr_b, 4)) - q_cond
    c0_b = set_c0(t_surr_b, q_cond)
    poly2 = [c4, c3, c2, c1, c0_b]
    t_s_b = np.roots(poly2)
    t_s_b_real = np.real(t_s_b[3])
    t_s_b_values.append(t_s_b_real)

    print("{0}. Surrounding temperature: {1} K. Surface temperature {2:.4f} K".format(i, t_surr_b, t_s_b_real))

# print("\nt_s values: ", t_s_b_values)
# print("t_surr values: ", t_surr_b_values)
print(dashes, "\n")

plt.figure()
plt.xlabel("T surrounding (K)")
plt.ylabel("T surface (K)")
plt.title("Engine Surface Temperature vs Surrounding Temperature")
auto_ignite_list = [auto_ignition_temp] * len(t_s_b_values)
plt.plot(t_surr_b_values, t_s_b_values, label="Engine surface temperature")
plt.plot(t_surr_b_values, auto_ignite_list, 'r--', label="Automatic ignition temperature")
plt.legend()
plt.show()

# PART C
print(dashes)
print("PART C")

plt.figure()
plt.xlabel("T surrounding (K)")
plt.ylabel("T surface (K)")
plt.title("Engine Surface Temperature vs Surrounding Temperature")

q_cond_c = 2000 # W/m^2
heat_flux_list = []
for k in range (13):
    # heat_flux_list = []
    q_cond_c = 2000 + k * 500
    heat_flux_list.append(q_cond_c)
    print("Heat flux {0} w/m^2".format(q_cond_c))
    # c0_c = -(heat_transfer * t_surr) - (emissivity * boltzman * pow(t_surr, 4)) - q_cond_c
    c0_c = set_c0(t_surr, q_cond_c)

    poly3 = [c4, c3, c2, c1, c0_c]
    t_s_mat_c = np.roots(poly3)
    t_s_c = t_s_mat_c[3]
    t_s_real_c = np.real(t_s)

    t_s_c_values = []
    t_surr_c_values = []
    # test_heat_flux = [q_cond_c] * len(t_s_c_values)
    # print("---")
    for i in range (9):
        t_surr_c = i*5 + 273.15 + 10
        t_surr_c_values.append(t_surr_c)
        c0_pt_c = -(heat_transfer * t_surr_c) - (emissivity * boltzman * pow(t_surr_c,  4)) - q_cond_c
        poly3 = [c4, c3, c2, c1, c0_c]
        t_s_c = np.roots(poly3)
        t_s_c_real = np.real(t_s_c[3])
        t_s_c_values.append(t_s_c_real)
        
        print("{0}. Surrounding temperature: {1} K. Surface temperature {2:.4f} K". format(i, t_surr_c, t_s_c_real))

        # z_val = q_cond_c
        # x_val = t_s_real_c
        # y_val = t_surr_c

        # fig = plt.figure()
        # ax = Axes3D(fig)
        # ax.plot(x_val, y_val, z_val)
        
    print("---")

    # z_values = np.array(heat_flux_list)
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.plot_surface(t_surr_c_values, t_s_c_values, z_values)
    # Axes3D.plot(t_surr_c_values, t_s_c_values, heat_flux_list)

    auto_ignite_list = [auto_ignition_temp] * len(t_s_c_values)
    # plt.plot(t_surr_c_values, t_s_c_values, label="Engine surface temperature")
    plt.plot(t_surr_c_values, t_s_c_values, label="h = {0} W/m^2".format(q_cond_c))

    test_heat_flux_list = [q_cond_c] * len(t_s_c_values)

    # print("test")
    # print("t_s_c_values: ", len(t_s_c_values))
    # print("t_surr_c_values: ", len(t_surr_c_values))
    # # print("heat_flux_list: ", len(heat_flux_list))
    # print("test_heat_flux_list: ", len(test_heat_flux_list))

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot(t_s_c_values, t_surr_c_values, test_heat_flux_list)

# fig = plt.figure()
# ax = Axes3D(fig)
# ax.plot(t_s_c_values, t_surr_c_values, heat_flux_list)

# plt.plot(t_surr_c_values, auto_ignite_list, 'r--', label="Auto ignite temp")
plt.legend(loc='upper right')
plt.show()

# plt.figure()
# plt.xlabel("T surrounding (K)")
# plt.ylabel("T surface (K)")
# plt.title("Engine Surface Temperature vs Surrounding Temperature")
# auto_ignite_list = [auto_ignition_temp] * len(t_s_c_values)
# plt.plot(t_surr_c_values, t_s_c_values, label="Engine surface temperature")
# plt.plot(t_surr_c_values, auto_ignite_list, 'r--', label="Automatic ignition temperature")
# plt.legend()
# plt.show()

# Axes3D.plot(t_surr_c_values, t_s_c_values, heat_flux_list)

print(dashes, "\n")
