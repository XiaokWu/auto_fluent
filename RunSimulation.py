import liquids as liq
from auto_fluent import AutoFluent
import numpy as np
import yaml
import Parameters as pm

fluid = liq.Extract_fluid(pm.fluid_name)

def Extract_BC():
    dct_Re = {
        'name' : 'Re',
        'val' : pm.Re,
        'velocity': np.array(pm.Re)*fluid.viscosity/(fluid.density*pm.characteristic_length)
    }
    
    dct_massflow = {
        'name' : 'massflow',
        'val' : pm.massflow,
        'velocity': np.array(pm.massflow)/(fluid.density*pm.inlet_area)
    }
    
    dct_heatflux = {
        'name' : 'heatflux',
        'val' : pm.heatflux
    }
    
    lst_flow_varibles = [dct_Re, dct_massflow]
    lst_heat_bc = [dct_heatflux]
    
    return lst_flow_varibles, lst_heat_bc



def RunSimulation():
    Fluent = AutoFluent(pm.simulation_name, pm.mesh_folder, pm.case_folder, pm.result_folder, pm.jou_folder, pm.ini_case_folder)
    Fluent.initial()
    
    if pm.on_server:
        fluent = AutoFluent.Server(Fluent)
    else:
        fluent = AutoFluent.Local(Fluent)
        
    
    lst_flow_varibles, lst_heat_bc = Extract_BC()
     
  
    
    
    fluent.joural_gen_case(pm.heatsink, lst_flow_varibles)
    fluent.runSim_case(lst_flow_varibles, pm.heatsink, pm.core_number, pm.os_name, pm.fluent_path)


