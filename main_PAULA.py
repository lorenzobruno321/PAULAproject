# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 10:15:37 2023

@author: bruno
"""
import pyomo.environ as pyo
#import math
import globalPARAMETERS_PAULA as pau


mod = pyo.ConcreteModel()                           #AbstractModel()

##### Model Sets #####
mod.t = pyo.Set(initialize=pau.l_t)
mod.i_pv = pyo.Set(initialize=pau.l_i_pv)
mod.i_wind = pyo.Set(initialize=pau.l_i_wind)
mod.i_wind_off = pyo.Set(initialize=pau.l_i_wind_off)

##### Model Parameters #####

# System
mod.demand = pyo.Param(mod.t, initialize=pau.dict_demand(pau.get_import('Demand')))  # hourly demand [kW]  
mod.L_prj = pyo.Param(initialize=pau.L_prj) # project lifetime [years]

# Nuclear
mod.CAPEX_nuclear = pyo.Param(initialize=pau.CAPEX_nuclear)  # €/kW installed
mod.OPEX_nuclear = pyo.Param(initialize=pau.OPEX_nuclear)  # €/kWh produced
mod.cost_fuel_nuclear = pyo.Param(initialize=pau.cost_fuel_nuclear)  # €/kWh produced
mod.max_P_nuclear = pyo.Param(initialize=pau.max_P_nuclear)  # maximum installed power [kW]
mod.P_nuclear_existent = pyo.Param(initialize=pau.P_nuclear_existent)  # installed power already in the system [kW]
mod.L_nuclear = pyo.Param(initialize=pau.L_nuclear)  # nuclear power plant lifetime [years]

# Gas
mod.CAPEX_gas = pyo.Param(initialize=pau.CAPEX_gas)  # €/kW installed
mod.OPEX_gas = pyo.Param(initialize=pau.OPEX_gas)  # €/kWh produced
mod.cost_fuel_gas = pyo.Param(initialize=pau.cost_fuel_gas)  # €/kWh produced
mod.max_P_gas = pyo.Param(initialize=pau.max_P_gas)  # maximum installed power [kW]
mod.P_gas_existent = pyo.Param(initialize=pau.P_gas_existent)  # installed power already in the system [kW]
mod.L_gas = pyo.Param(initialize=pau.L_gas)  # gas power plant lifetime [years]

# PV
mod.forecast_pv = pyo.Param(mod.t, mod.i_pv, initialize=pau.Forecast_i(pau.get_import('PV')))  # hourly PV generation [MW]
mod.CAPEX_pv = pyo.Param(initialize=pau.CAPEX_pv)  # €/kW installed
mod.OPEX_pv = pyo.Param(initialize=pau.OPEX_pv)  # €/kWh produced
mod.max_P_pv = pyo.Param(initialize=pau.max_P_pv)  # maximum installed power [kW]
mod.L_pv = pyo.Param(initialize=pau.L_pv)  # PV power plant lifetime [years]

# Wind
mod.forecast_wind = pyo.Param(mod.t, mod.i_wind, initialize=pau.Forecast_i(pau.get_import('Wind')))  # hourly PV generation [MW]
mod.CAPEX_wind = pyo.Param(initialize=pau.CAPEX_wind)  # €/kW installed
mod.OPEX_wind = pyo.Param(initialize=pau.OPEX_wind)  # €/kWh produced
mod.max_P_wind = pyo.Param(initialize=pau.max_P_wind)  # maximum installed power [kW]
mod.L_wind = pyo.Param(initialize=pau.L_wind)  # wind power plant lifetime [years]

# Offshore Wind
mod.forecast_wind_off = pyo.Param(mod.t, mod.i_wind_off, initialize=pau.Forecast_i(pau.get_import('Offshore Wind')))  # hourly PV generation [MW]
mod.CAPEX_wind_off = pyo.Param(initialize=pau.CAPEX_wind_off)  # €/kW installed
mod.OPEX_wind_off = pyo.Param(initialize=pau.OPEX_wind_off)  # €/kWh produced
mod.max_P_wind_off = pyo.Param(initialize=pau.max_P_wind_off)  # maximum installed power [kW]
mod.L_wind_off = pyo.Param(initialize=pau.L_wind_off)  # wind power plant lifetime [years]

# Storage
mod.CAPEX_storage = pyo.Param(initialize=pau.CAPEX_storage)  # €/kWh of capacity
mod.OPEX_storage = pyo.Param(initialize=pau.OPEX_storage)  # €/kWh installed/year
mod.max_batteries = pyo.Param(initialize=pau.max_batteries)  # maximum number of batteries
mod.L_storage = pyo.Param(initialize=pau.L_storage)  # Storage plant lifetime [years]
mod.maxPow_bat = pyo.Param(initialize=pau.maxPow_bat)  # maximum power [kW] of 1 battery
mod.cap_bat = pyo.Param(initialize=pau.cap_bat)  # storage capacity [kWh] of 1 battery
mod.SOC_max = pyo.Param(initialize=pau.SOC_max)  # maximum state of charge [pu]
mod.SOC_min = pyo.Param(initialize=pau.SOC_min)  # minimum state of charge [pu]
mod.charging_eff = pyo.Param(initialize=pau.charging_eff)  # charging efficiency [pu]
mod.discharging_eff = pyo.Param(initialize=pau.discharging_eff)  # discharging efficiency [pu]
mod.ncycles = pyo.Param(initialize=pau.ncycles)  # number of charge and discharge cycles


##### Model Variables #####

# System

# Nuclear
mod.P_nuclear = pyo.Var(within=pyo.NonNegativeReals)  # nuclear power installed [kW]
mod.x_nuclear = pyo.Var(mod.t, within=pyo.NonNegativeReals)  # instantaneous nuclear power generation [kW]

# Gas
mod.P_gas = pyo.Var(within=pyo.NonNegativeReals)  # gas power installed [kW]
mod.x_gas = pyo.Var(mod.t, within=pyo.NonNegativeReals)  # instantaneous gas power generation [kW]

# PV
mod.P_pv = pyo.Var(mod.i_pv, within=pyo.NonNegativeReals)  # PV power installed [kWp]
mod.x_pv = pyo.Var(mod.t, mod.i_pv, within=pyo.NonNegativeReals)  # instantaneous PV power generation [kW]

# Wind (onshore)
mod.P_wind = pyo.Var(mod.i_wind, within=pyo.NonNegativeReals)  # wind power installed [kW]
mod.x_wind = pyo.Var(mod.t, mod.i_wind, within=pyo.NonNegativeReals)  # instantaneous wind power generation [kW]

# Offshore Wind
mod.P_wind_off = pyo.Var(mod.i_wind_off, within=pyo.NonNegativeReals)  # Offshore wind power installed [kW]
mod.x_wind_off = pyo.Var(mod.t, mod.i_wind_off, within=pyo.NonNegativeReals)  # instantaneous offshore wind power generation [kW]

# Storage
mod.max_st = pyo.Var(within=pyo.NonNegativeReals)  # installed stored capacity [kWh]
mod.E_st = pyo.Var(mod.t, within=pyo.NonNegativeReals)  # instantaneous energy stored (SOC) [kWh]
mod.charge = pyo.Var(mod.t, within=pyo.NonNegativeReals)  # instantaneous charging power [kW]
mod.discharge = pyo.Var(mod.t, within=pyo.NonNegativeReals)  # instantaneous discharging power [kW]
mod.batteries = pyo.Var(within=pyo.NonNegativeIntegers)  # number of batteries installed


##### Model Constraints #####
mod.constraints = pyo.ConstraintList()

for k in range(0, pau.h_year):
    
    # Nuclear
    # installed nuclear power can be limited
    mod.constraints.add(mod.P_nuclear <= mod.max_P_nuclear)      
    # nuclear generation remains constant through the year
    mod.constraints.add(mod.x_nuclear[k] == mod.P_nuclear + mod.P_nuclear_existent)
    
    # Gas
    # installed gas power can be limited
    mod.constraints.add(mod.P_gas <= mod.max_P_gas)
    # instantaneous gas power is <= than installed
    mod.constraints.add(mod.x_gas[k] <= mod.P_gas + mod.P_gas_existent)
    
    # PV
    # installed pv power can be limited
    #mod.constraints.add(mod.P_pv[k] <= mod.max_P_pv)
    # instantaneous pv power is <= than available = installed * forecast
    mod.constraints.add(mod.x_pv[mod.t, mod.i_pv] <= mod.P_pv[mod.i_pv] * mod.forecast_pv[mod.t, mod.i_pv])


'''
# PV
def Constraint_max_P_pv(m, i_pv):  # installed pv power can be limited
    return m.P_pv[i_pv] <= m.max_P_pv
model.Constr_pv1 = pyo.Constraint(model.i_pv, rule=Constraint_max_P_pv)

# instantaneous pv power is <= than available = installed * forecast
def Constraint_max_x_pv(m, t, i_pv):
    return m.x_pv[t, i_pv] <= m.P_pv[i_pv] * m.forecast_pv[t, i_pv]
model.Constr_pv2 = pyo.Constraint(
    model.t, model.i_pv, rule=Constraint_max_x_pv)

# Wind
def Constraint_max_P_wind(m, i_wind):  # installed wind power can be limited
    return m.P_wind[i_wind] <= m.max_P_wind
model.Constr_wind1 = pyo.Constraint(model.i_wind, rule=Constraint_max_P_wind)
def Constraint_max_x_wind(m, t, i_wind):  # instantaneous wind power is <= than available = installed * forecast
    return m.x_wind[t, i_wind] <= m.P_wind[i_wind] * m.forecast_wind[t, i_wind]
model.Constr_wind2 = pyo.Constraint(model.t, model.i_wind, rule=Constraint_max_x_wind)

# Offshore Wind
def Constraint_max_P_wind_off(m, i_wind_off):  # installed offshore wind power can be limited
    return m.P_wind_off[i_wind_off] <= m.max_P_wind_off
model.Constr_wind1_off = pyo.Constraint(model.i_wind_off, rule=Constraint_max_P_wind_off)
def Constraint_max_x_wind_off(m, t, i_wind_off):  # instantaneous offshore wind power is <= than available = installed * forecast
    return m.x_wind_off[t, i_wind_off] <= m.P_wind_off[i_wind_off] * m.forecast_wind_off[t, i_wind_off]
model.Constr_wind2_off = pyo.Constraint(model.t, model.i_wind_off, rule=Constraint_max_x_wind_off)

# Energy Storage (battery)
def Constraint_max_nbateries(m):  # installed nº of batteries can be limited
    return m.batteries <= m.max_batteries
model.Constr_max_bateries = pyo.Constraint(rule=Constraint_max_nbateries)
def Constraint_max_st(m):  # total capacity of storage
    return m.batteries * m.cap_bat == m.max_st
model.Constr_max_st = pyo.Constraint(rule=Constraint_max_st)
def Constraint_min_st_cap(m, t):  # minimum energy stored
    return m.SOC_min * m.max_st <= m.E_st[t]
model.Constr_min_st_cap = pyo.Constraint(model.t, rule=Constraint_min_st_cap)
def Constraint_max_st_cap(m, t):  # maximum energy stored
    return m.E_st[t] <= m.max_st * m.SOC_max
model.Constr_max_st_cap = pyo.Constraint(model.t, rule=Constraint_max_st_cap)
def Constraint_max_P_charge(m, t):  # maximum charging power
    return m.charge[t] <= m.batteries * m.maxPow_bat
model.Constr_max_P_charge = pyo.Constraint(model.t, rule=Constraint_max_P_charge)
def Constraint_max_P_disch(m, t):  # maximum discharging power
    return m.discharge[t] <= m.batteries * m.maxPow_bat
model.Constr_max_P_discharge = pyo.Constraint(model.t, rule=Constraint_max_P_disch)
def Constraint_energy_stored(m, t):  # energy stored calculation
    if t == 0:
        return m.E_st[0] == m.E_st[l_t[-1]] + m.charge[0] * m.charging_eff - m.discharge[0] / m.discharging_eff
    else:
        return m.E_st[t] == m.E_st[t - 1] + m.charge[t] * m.charging_eff - m.discharge[t] / m.discharging_eff
model.Constr_energySt = pyo.Constraint(model.t, rule=Constraint_energy_stored)

# Balance generation=demand
def Constraint_balance_system(m, t):
    return m.demand[t] + m.charge[t] == m.x_nuclear[t] + m.x_gas[t] + m.discharge[t] + sum(m.x_pv[t, i_pv] for i_pv in l_i_pv) + sum(m.x_wind[t, i_wind] for i_wind in l_i_wind) + sum(m.x_wind_off[t, i_wind_off] for i_wind_off in l_i_wind_off)
model.Constr_balance = pyo.Constraint(model.t, rule=Constraint_balance_system)
def Constraint_min_renewables(m):
    return sum(m.x_nuclear[t] + m.x_gas[t] for t in l_t) <= (1-m.min_ren) * sum(m.demand[t] for t in l_t)  #sum(sum(m.x_pv[t, i_pv] for i_pv in l_i_pv) + sum(m.x_wind[t, i_wind] for i_wind in l_i_wind) + sum(m.x_wind_off[t, i_wind_off] for i_wind_off in l_i_wind_off) for t in l_t) >= m.min_ren * sum(m.demand[t] for t in l_t)
model.Constr_min_renewables = pyo.Constraint(rule=Constraint_min_renewables)

'''