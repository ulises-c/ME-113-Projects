import CoolProp.CoolProp as CP
import matplotlib.pyplot as plt

# Global Vars
fluid = "Water"

# after boiler
P1_ideal = 2000 # kPa
T1_ideal = 300 # °C

# after boiler, but before turbine
P1_actual = 0.95 * P1_ideal # kPa
T1_actual = 0.95 * T1_ideal # °C

# after turbine
P2 = 15 # kPa
T2 = "unknown" # °C
q2_factor = 0.9 # 90% quality factor
W_out_pump = 4 # kJ/kg

# after condenser
P3 = 15 # kPa
T3 = 45 # °C


# Heat released to environment from boiler to turbine inlet
def problem_1():
    print("\n----- Problem 1 -----\n")
    
    h1_ideal = CP.PropsSI('H', 'T', T1_ideal+273.15, 'P', P1_ideal*1000, fluid) # J/kg
    h1_ideal = h1_ideal/1000 # kJ/kg
    h1_actual = CP.PropsSI('H', 'T', T1_actual+273.15, 'P', P1_actual*1000, fluid) # J/kg
    h1_actual = h1_actual/1000 # kJ/kg
    q1_dot = abs(h1_actual-h1_ideal) # kJ/kg

    print('Enthalpy h1_ideal: {0:.2f} kJ/kg'.format(h1_ideal))
    print('Enthalpy h1_actual: {0:.2f} kJ/kg'.format(h1_actual))
    print('Heat released to environment q1_dot: {0:.2f} kJ/kg'.format(q1_dot))
    # return q1_dot

# Heat released from condenser    
def problem_2():
    print("\n----- Problem 2 -----\n")

    T2 = CP.PropsSI('T', 'P', P2*1000, 'Q', q2_factor, fluid) # K
    h2 = CP.PropsSI('H', 'P', P2*1000, 'Q', q2_factor, fluid) # J/kg
    h2 = h2/1000 # kJ/kg
    h3 = CP.PropsSI('H', 'T', T3+273.15, 'P', P3*1000, fluid) # J/kg
    h3 = h3/1000 # kJ/kg
    q3_dot = abs(h3-h2) # kJ/kg

    print('Temperature T2: {0:.2f} Celsius'.format(T2-273.15))
    print('Enthalpy h2: {0:.2f} kJ/kg'.format(h2))
    print('Enthalpy h3: {0:.2f} kJ/kg'.format(h3))
    print('Heat released from condenser q3_dot: {0:.2f} kJ/kg'.format(q3_dot))
    # return q3_dot

# Efficiency of steam power plant
def problem_3(T_increment, P_increment):
    print("\n----- Problem 3 -----\n")
    print(T1_ideal+T_increment)
    print(P1_ideal+P_increment)

    h1_ideal = CP.PropsSI('H', 'T', (T1_ideal+T_increment)+273.15, 'P', (P1_ideal+P_increment)*1000, fluid) # J/kg
    h1_ideal = h1_ideal/1000 # kJ/kg
    h1_actual = CP.PropsSI('H', 'T', T1_actual+273.15, 'P', P1_actual*1000, fluid) # J/kg
    h1_actual = h1_actual/1000 # kJ/kg

    h2 = CP.PropsSI('H', 'P', P2*1000, 'Q', q2_factor, fluid) # J/kg
    h2 = h2/1000 # kJ/kg
    h3 = CP.PropsSI('H', 'T', T3+273.15, 'P', P3*1000, fluid) # J/kg
    h3 = h3/1000 # kJ/kg

    h4 = h3 + W_out_pump
    Q_boiler = h1_actual - h4
    W_net = h1_actual - h2 - W_out_pump
    plant_eff = W_net / Q_boiler
    plant_eff = plant_eff * 100

    print('Enthalpy h4: {:.2f} kJ/kg'.format(h4))
    print('Net work: {0:.2f} kJ/kg'.format(W_net))
    print('Heat in: {0:.2f} kJ/kg'.format(Q_boiler))
    print('Efficiency of the power plant is: {0:.2f}%'.format(plant_eff))
    return plant_eff

# Plot turbine work as a function of steam exit temperature from the boiler
# Pressure, P1_ideal, changes from 2 MPa to 2.5MPa, step of 0.1 MPa
def problem_4(T_increment, T1_ideal):
    print("\n----- Problem 4 -----")
    print("Constant temperature at {} °C\n".format(T1_ideal + T_increment))

    P1_ideal_values = []
    P1_actual_values = []
    W_turb_values_const_T = []
    h2 = CP.PropsSI('H', 'P', P2*1000, 'Q', q2_factor, fluid) # J/kg
    h2 = h2/1000 # kJ/kg
    T1_ideal = T1_ideal + T_increment
    T1_actual = 0.95 * T1_ideal
    for k in range(0,6):
        P1_ideal_current = P1_ideal + (k * 100)
        P1_ideal_values.append(P1_ideal_current)
        P1_actual_current = 0.95 * P1_ideal_current
        P1_actual_values.append(P1_actual_current)

        h1_actual_current = CP.PropsSI('H', 'T', T1_actual+273.15, 'P', P1_actual_current*1000, fluid) # J/kg
        h1_actual_current = h1_actual_current/1000 # kJ/kg
        W_turb_current = h1_actual_current - h2
        W_turb_values_const_T.append(W_turb_current)
        print("Work out from turbine: {:.2f} kJ/kg, when pressure is {} kPa".format(W_turb_current, P1_ideal_current))

    # print("List of actual pressures (kPa):", P1_actual_values)
    # print("List of ideal pressures (kPa):", P1_ideal_values)
    # print("List of W_turb (kJ/kg):", W_turb_values_const_T)
    plt.plot(P1_ideal_values, W_turb_values_const_T, 'bo-', label="Turbine work with constant temperature {}°C".format(T1_ideal))
    plt.ylabel("Turbine work [kJ/kg]")
    plt.xlabel("Pressure [kPa]")
    plt.title("Turbine Work vs Pressure")
    plt.legend()
    plt.show()
    return W_turb_values_const_T, P1_ideal_values

# Plot turbine work as steam exit temperature changes
# T1_ideal Changes from 300 °C to 350 °C , step of 50 °C 
def problem_5(P_increment, P1_ideal):
    print("\n----- Problem 5 -----")
    print("Constant perssure at {} kPa\n".format(P1_ideal + P_increment))

    T1_ideal_values = []
    T1_actual_values = []
    W_turb_values_const_P = []
    h2 = CP.PropsSI('H', 'P', P2*1000, 'Q', q2_factor, fluid) # J/kg
    h2 = h2/1000 # kJ/kg
    P1_ideal = P1_ideal + P_increment # kPa
    P1_actual = 0.95 * P1_ideal
    for k in range(0,6):
        T1_ideal_current = T1_ideal + (k * 10)
        T1_ideal_values.append(T1_ideal_current)
        T1_actual_current = 0.95 * T1_ideal_current
        T1_actual_values.append(T1_actual_current)
        
        h1_actual_current = CP.PropsSI('H', 'T', T1_actual_current+273.15, 'P', P1_actual*1000, fluid) # J/kg
        h1_actual_current = h1_actual_current/1000 # kJ/kg
        W_turb_current = h1_actual_current - h2
        W_turb_values_const_P.append(W_turb_current)
        print("Work out from turbine: {:.2f} kJ/kg, when temperature is {}°C".format(W_turb_current, T1_ideal_current))

    # print("List of actual pressures (kPa):", T1_actual_values)
    # print("List of ideal pressures (kPa):", T1_ideal_values)
    # print("List of W_turb (kJ/kg):", W_turb_values_const_P)

    plt.plot(T1_ideal_values, W_turb_values_const_P, 'bo-', label="Turbine work with constant pressure {} kPa".format(P1_ideal), color="red")
    plt.ylabel("Turbine work [kJ/kg]")
    plt.xlabel("Temperature [°C]")
    plt.title("Turbine Work vs Temperature")
    plt.legend()
    plt.show()
    return W_turb_values_const_P, T1_ideal_values

# Plot turbine work for problem_4() and problem_5()
def problem_6(y1, x1, y2, x2, string1, string2, units1, units2, int1, int2):
    print("\n----- Problem 6 -----\n")

    plt.plot(x2, y2, 'bo-', color="green", label="Turbine work with constant {} at {} {}".format(string1, int2, units2))
    plt.plot(x1, y1, 'bo-', color="orange", label="Turbine work with constant {} at {} {}".format(string1, int1, units2))
    plt.ylabel("Turbine Work [kJ/kg]")
    plt.xlabel("{} [{}]".format(string2.title(), units1))
    plt.title("Turbine Work vs {}".format(string2.title()))
    plt.legend()
    plt.show()

# Plot plant efficiency for problem_5() and problem_6()
def problem_7():
    print("\n----- Problem 7 -----\n")
    P = [2000, 2100, 2200, 2300, 2400, 2500]
    W_T300 = [631.16, 628.15, 625.11, 622.04, 618.94, 615.81]
    W_T350 = [739.67, 737.47, 735.26, 733.03, 730.79, 728.54]
    eff_300 = []
    eff_350 = []
    for i in W_T300:
        efficiency = ((i-4))/2380 * 100
        eff_300.append(efficiency)
    for i in W_T350:
        efficiency = ((i-4))/2380 * 100
        eff_350.append(efficiency)

    plt.plot(P, eff_300, 'bo-', color="purple", label="At 300°C")
    plt.plot(P, eff_350, 'bo-', color="gray", label="At 350°C")
    plt.ylabel("Efficiency [%]")
    plt.xlabel("Pressure [kPa]")
    plt.title("Efficiency")
    plt.legend()
    plt.show()

# Anaylze the entire problem
def problem_8():
    print("\n----- Problem 8 -----\n")
    # Work increases as the temperature rises and the pressure lowers.
    # Efficiency increases as work increases.

T_increment = 50 #°C
P_increment = 500 #kPa

q1_dot = problem_1()
q3_dot = problem_2()
plant_eff = problem_3(0,0)

W_turb_values_const_T_300, P1_ideal_values = problem_4(0, T1_ideal)
W_turb_values_const_T_350, P1_ideal_values = problem_4(T_increment, T1_ideal)

W_turb_values_const_P_2000, T1_ideal_values = problem_5(0, P1_ideal)
W_turb_values_const_P_2500, T1_ideal_values = problem_5(P_increment, P1_ideal)

turbine_work_const_T = problem_6(W_turb_values_const_T_300, P1_ideal_values, W_turb_values_const_T_350, P1_ideal_values, "temperature", "pressure", "kPa", "°C", 350, 300)
turbine_work_const_P = problem_6(W_turb_values_const_P_2000, T1_ideal_values, W_turb_values_const_P_2500, T1_ideal_values, "pressure", "temperature", "°C", "kPa", 2500, 2000)

problem_7()

# eff_const_P_no_inc = problem_3(0,0)
# eff_const_P = problem_3(0,P_increment)

# eff_const_T_no_inc = problem_3(0,0)
# eff_const_T = problem_3(T_increment, 0)

# print("")
# print(eff_const_P_no_inc)
# print(eff_const_P)
# print(eff_const_T_no_inc)
# print(eff_const_T)