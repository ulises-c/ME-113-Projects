"""
Ulises Chavarria
September 29, 2020
ME 113 - Project 1
Professor Syed Zaidi
"""
# Modified into functions as of May 25, 2021

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

""" ----- CONSTANTS ----- """
EMISSIVITY = 0.3 # unitless
BOLTZMANN = 5.67 * pow(10, -8) # W/m^2/K^4
HEAT_TRANSFER_COEFF = 15 # W/m^2
Q_COND = 5000 # W/m^2
T_SURR = 40 + 273.15 # K

AUTO_IGNITION_TEMP = 250 + 273.15 # K
MAX_ENGINE_SURFACE_TEMP = 200 + 273.15 # K

C4 = EMISSIVITY * BOLTZMANN
C3 = 0
C2 = 0
C1 = HEAT_TRANSFER_COEFF

X_LABEL = "T surrounding [K]"
Y_LABEL = "T surface [K]"
Z_LABEL = "Heat flux [W/m^2]"
GRAPH_TITLE = "Engine Surface Temperature vs Surrounding Temperature"
DASHES = "---------------------------------------------------------------------"

"""
Project Notes
    (Q conduction dot) = (Q convection dot) + (Q radiation dot)
    After some algebra and use of thermodynamic formulas...

    0 = (HEAT_TRANSFER_COEFF) * (Ts - Tsurr) + (EMISSIVITY) * (BOLTZMANN) * (Ts^4 - Tsurr^4) - (Q conduction dot)
    0 = (C4 * Ts^4) + (C3 * Ts^3) + (C2 * Ts^2) + (C1 * Ts) + (C0)
    0 = (C4 * Ts^4) + (0) + (0) + (C1 * Ts) + (C0)
    0 = (C4 * Ts^4) + (C1 * Ts) + (C0)

    Where
        C4 = EMISSIVITY * BOLTZMANN
        C1 = HEAT_TRANSFER_COEFF
        C0 = -(HEAT_TRANSFER_COEFF) * (Tsurr) - (EMISSIVITY) * (BOLTZMANN) * (Tsurr)^4 - (Q conduction dot)
"""

def set_c0(t_surr_current, q_cond_current):
    """ c0 is the only variable changing in the polynomial equation """
    c0 = -(HEAT_TRANSFER_COEFF * T_SURR) - (EMISSIVITY * BOLTZMANN * pow(t_surr_current, 4)) - q_cond_current
    return c0

def thermodynamics(c0_current):
    poly = [C4, C3, C2, C1, c0_current]
    t_s_mat = np.roots(poly)
    t_s = t_s_mat[3]
    t_s_real = np.real(t_s)
    return t_s_real

def partA():
    c0_a = set_c0(T_SURR, Q_COND)
    t_s_real_a = thermodynamics(c0_a)
    print(DASHES)
    print("PART A")
    print("Given surrounding temperature: {0} K".format(T_SURR))
    print("Surface temperature: {0:.4f} K".format(t_s_real_a))
    print("Autoignition temperature: {} K".format(AUTO_IGNITION_TEMP))
    if(t_s_real_a > AUTO_IGNITION_TEMP):
        print("Oil on the engine is at risk of igniting due to engine surface temperature.")
    else:
        print("Oil on the engine is not at risk of igniting due to engine surface temperature.")
    print(DASHES, "\n")

def partB(q_cond_current=Q_COND):
    t_s_b_values = []
    t_surr_b_values = []
    for i in range(9):
        t_surr_b = (i * 5) + 273.15 + 10 # incrementing by 10K every loop, changed compared to original
        t_surr_b_values.append(t_surr_b)
        c0_b = set_c0(t_surr_b, q_cond_current)
        t_s_real_b = thermodynamics(c0_b)
        t_s_b_values.append(t_s_real_b)
        print("{0}. Surrounding temperature: {1} K. Surface temperature {2:.4f} K".format(i, t_surr_b, t_s_real_b))
    
    return t_s_b_values, t_surr_b_values

def partB_graph(t_s_b_vals, t_surr_b_vals):
    """ Graphing portion """
    plt.figure()
    plt.xlabel(X_LABEL)
    plt.ylabel(Y_LABEL)
    plt.title(GRAPH_TITLE)
    auto_ignite_list = [AUTO_IGNITION_TEMP] * len(t_s_b_vals)
    plt.plot(t_surr_b_vals, t_s_b_vals, label="Engine surface temperature")
    plt.plot(t_surr_b_vals, auto_ignite_list, 'r--', label="Automatic ignition temperature")
    plt.legend()
    plt.show()
    print(DASHES, "\n")

def partC():
    print(DASHES)
    print("PART C")
    heat_flux_2d = []
    t_s_2d = []
    t_surr_2d = []
    # ^^^ The lists above eventually become 2d lists
    q_cond_c_start = 2000 # W/m^2 , changed compared to original

    for k in range (13):
        heat_flux_list = []
        q_cond_c = q_cond_c_start + k * 500 # Incrementing conductivity by 500 each loop
        heat_flux_list.append(q_cond_c)
        print("Heat flux {0} w/m^2".format(q_cond_c))
        t_s_c_values, t_surr_c_values = partB(q_cond_c)
        t_s_2d.append(t_s_c_values)
        t_surr_2d.append(t_surr_c_values)
        heat_flux_2d.append(heat_flux_list)
        auto_ignite_list = [AUTO_IGNITION_TEMP] * len(t_s_c_values)
        print("---")
    auto_ignite_list_2d = [auto_ignite_list] * len(t_s_2d)
    return t_s_2d, t_surr_2d, auto_ignite_list_2d, heat_flux_2d

def partC_graph(t_s_2d, t_surr_2d, auto_ignite_list_2d, heat_flux):
    # 2D Graph
    plt.figure()
    plt.xlabel(X_LABEL)
    plt.ylabel(Y_LABEL)
    plt.title(GRAPH_TITLE)
    for i in range(len(auto_ignite_list_2d)):
        plt.plot(t_surr_2d[i], t_s_2d[i], label="h = {0} W/m^2".format(heat_flux[i]))
    plt.plot(t_surr_2d[i], auto_ignite_list_2d[i], 'r--', label="Auto ignite temp")
    plt.legend(loc='upper right')
    plt.show()

    # 3D Graph
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel(X_LABEL)
    ax.set_ylabel(Y_LABEL)
    ax.set_zlabel(Z_LABEL)
    ax.plot_surface(t_s_2d, t_surr_2d, np.array(heat_flux), cmap="Oranges_r") 
    ax.plot_wireframe(auto_ignite_list_2d, t_surr_2d, np.array(heat_flux))
    plt.title(GRAPH_TITLE)
    plt.show()
    print(DASHES, "\n")

""" MAIN """
partA()

t_s_b, t_surr_b = partB()
partB_graph(t_s_b, t_surr_b)

t_s_c, t_surr_c, ignite, heat = partC()
partC_graph(t_s_c, t_surr_c, ignite, heat)