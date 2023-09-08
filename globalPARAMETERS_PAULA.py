# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 10:17:58 2023

@author: bruno
"""

# Integration of renewable energy sustems to the grid
# Asignment 1

# Nuclear: constant generation, 1 source
# Gas: generation as desired, 1 source
# PV: generation as forecast, multiple sources
# Wind: generation as forecast, multiple sources
# Offshore Wind: generation as forecast, single source

# Comments: to have multiple sources, modify section 5
#           it can be added replacement costs to the objective function
#           max_P in pv and wind is the same for all locations (if not, change program)

import pandas
#from main import min_renewables

''' 1) Import/introduce data '''

import_demand = pandas.read_excel('Data.xlsx', sheet_name='Demand', header=0, index_col=None)  # demand = import_demand.iloc[:,1]
import_pv = pandas.read_excel('Data.xlsx', sheet_name='PV', header=0, index_col=None)  # pv_i = import_pv.iloc[:,i] // i=1...
import_wind = pandas.read_excel('Data.xlsx', sheet_name='Wind', header=0, index_col=None)  # wind_i = import_wind.iloc[:,i] // i=1...
import_wind_off = pandas.read_excel('Data.xlsx', sheet_name="Wind-Offshore", header=0, index_col=None) # wind_off_i = import_wind_off.iloc[:,i] // i=1...

# min_renewables = 0  # minimum percentage of renewables [pu]
L_prj = 50  # project lifetime [years]
h_year = 8760

# Nuclear
CAPEX_nuclear = 7989  # €/kW installed
OPEX_nuclear = 146/8760  # €/kWh produced
cost_fuel_nuclear = 0.0036  # €/kWh produced
max_P_nuclear = 1000**10  # maximum installed power [kW] --> inf = 1000**10 // no nuclear = 0
P_nuclear_existent = 0  # installed power already in the system [kW]
L_nuclear = 60  # nuclear power plant lifetime [years]

# Gas
CAPEX_gas = 2228  # €/kW installed
OPEX_gas = 63/8760  # €/kWh produced
cost_fuel_gas = 0.071  # €/kWh produced
max_P_gas = 1000**10  # maximum installed power [kW] --> inf = 1000**10 // no gas = 0
P_gas_existent = 0  # installed power already in the system [kW]
L_gas = 30  # gas power plant lifetime [years]

# PV
CAPEX_pv = 990  # €/kW installed
OPEX_pv = 16.42/8760  # €/kWh produced
max_P_pv = 1000**10  # maximum installed power [kW] --> inf = 1000**10 // no PV = 0
L_pv = 25  # PV power plant lifetime [years]

# Wind
CAPEX_wind = 1462  # €/kW installed
OPEX_wind = 34/8760  # €/kWh produced
max_P_wind = 1000**10  # maximum installed power [kW] --> inf = 1000**10 // no wind = 0
L_wind = 25  # wind power plant lifetime [years]

# Offshore Wind 
CAPEX_wind_off = 3756  # €/kW installed     https://guidetoanoffshorewindfarm.com/wind-farm-costs
OPEX_wind_off = 110/8760  # €/kWh produced       https://guidetoanoffshorewindfarm.com/wind-farm-costs
max_P_wind_off = 1000**10  # maximum installed power [kW] --> inf = 1000**10 // no wind = 0
L_wind_off = 27  # wind power plant lifetime [years]    https://guidetoanoffshorewindfarm.com/wind-farm-costs

# Storage: battery
CAPEX_storage = 395  # €/kWh of capacity
OPEX_storage = 0.025*395/8760  # €/kWh installed/year
max_batteries = 1000**10  # maximum number of batteries --> inf = 1000**10 // no storage = 0
L_storage = 15  # Storage plant lifetime [years]
maxPow_bat = 60000  # maximum power [kW] of 1 battery
cap_bat = 240000  # storage capacity [kWh] of 1 battery
SOC_max = 1  # maximum state of charge [pu]
SOC_min = 0.2  # minimum state of charge [pu]
charging_eff = 0.95  # charging efficiency [pu]
discharging_eff = 0.95  # discharging efficiency [pu]
ncycles = 3650  # number of charge and discharge cycles

''' 2) Pre-processing'''

l_t = list(range(365*24))  # number of periods (365 days)
l_i_pv = list(range(1, import_pv.shape[1]))
l_i_wind = list(range(1, import_wind.shape[1]))
l_i_wind_off = list(range(1, import_wind_off.shape[1]))


def dict_demand(importa):
    dict_Forecast = {t: importa.iloc[t, 1] for t in l_t}
    return dict_Forecast
def Forecast_i(importa):
    n_locations = importa.shape[1]
    dict_Forecast = {(t, i): importa.iloc[t, i] for t in l_t for i in list(range(1, n_locations))}
    return dict_Forecast


def get_import(x):
    if x == 'Demand':
        return import_demand
    elif x == 'PV':
        return import_pv
    elif x == 'Wind':
        return import_wind
    elif x == 'Offshore Wind':
        return import_wind_off
    else:
        return
def get_l(x):
    if x == 'time':
        return l_t
    elif x == 'PV':
        return l_i_pv
    elif x == 'Wind':
        return l_i_wind
    elif x == 'Offshore Wind':
        return l_i_wind_off
    else:
        return
#def get_min_renewables():
#    return min_renewables
def get_L_prj():
    return L_prj
def get_CAPEX(tech):
    if tech == 'Nuclear':
        return CAPEX_nuclear
    elif tech == 'Gas':
        return CAPEX_gas
    elif tech == 'PV':
        return CAPEX_pv
    elif tech == 'Wind':
        return CAPEX_wind
    elif tech == 'Offshore Wind':
        return CAPEX_wind_off
    elif tech == 'Storage':
        return CAPEX_storage
    else:
        return
def get_OPEX(tech):
    if tech == 'Nuclear':
        return OPEX_nuclear
    elif tech == 'Gas':
        return OPEX_gas
    elif tech == 'PV':
        return OPEX_pv
    elif tech == 'Wind':
        return OPEX_wind
    elif tech == 'Offshore Wind':
        return OPEX_wind_off
    elif tech == 'Storage':
        return OPEX_storage
    else:
        return
def get_cost_fuel(tech):
    if tech == 'Nuclear':
        return cost_fuel_nuclear
    elif tech == 'Gas':
        return cost_fuel_gas
    else:
        return
def get_max_P(tech):
    if tech == 'Nuclear':
        return max_P_nuclear
    elif tech == 'Gas':
        return max_P_gas
    elif tech == 'PV':
        return max_P_pv
    elif tech == 'Wind':
        return max_P_wind
    elif tech == 'Offshore Wind':
        return max_P_wind_off
    else:
        return
def get_P_existent(tech):
    if tech == 'Nuclear':
        return P_nuclear_existent
    elif tech == 'Gas':
        return P_gas_existent
    else:
        return
def get_L(tech):
    if tech == 'Nuclear':
        return L_nuclear
    elif tech == 'Gas':
        return L_gas
    elif tech == 'PV':
        return L_pv
    elif tech == 'Wind':
        return L_wind
    elif tech == 'Offshore Wind':
        return L_wind_off
    elif tech == 'Storage':
        return L_storage
    else:
        return

def get_max_batteries():
    return max_batteries
def get_storage_properties(prop):
    if prop == 'maxPow_bat':
        return maxPow_bat
    elif prop == 'cap_bat':
        return cap_bat
    elif prop == 'SOC_max':
        return SOC_max
    elif prop == 'SOC_min':
        return SOC_min
    elif prop == 'charging_eff':
        return charging_eff
    elif prop == 'discharging_eff':
        return discharging_eff
    elif prop == 'ncycles':
        return ncycles
    else:
        return
