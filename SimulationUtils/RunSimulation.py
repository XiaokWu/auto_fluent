import conf.liquids as liq
from SimulationUtils.auto_fluent import AutoFluent
import numpy as np
import conf.Parameters as pm

def Extract_BC(fluid):
    # 将边界条件转化为速度以及热量输入
    dct_Re = {
        'name' : 'Re',
        'val' : pm.Re,
        'velocity': np.array(pm.Re)*fluid['viscosity']/(fluid['density']*pm.characteristic_length)
    }
    
    dct_massflow = {
        'name' : 'massflow',
        'val' : pm.massflow,
        'velocity': np.array(pm.massflow)/(fluid['density']*pm.inlet_area)
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
     
    lst_dct_fluids = []   
    for fluid_name in pm.fluids:
        _, fluid = liq.Extract_fluid(fluid_name)
        lst_dct_fluids.append(fluid)
    lst_dct_fluids = [liq.Extract_fluid(fluid_name) for fluid_name in pm.fluids]
    
    print(lst_dct_fluids)
    lst_flow_varibles, lst_heat_varibles = Extract_BC(fluid)
    lst_velocity_args = [lst_flow_varibles,pm.velocity_bc_facesname]
    lst_heatflux_args = [lst_heat_varibles, pm.heatflux_bc_facesname]
    print(lst_velocity_args)
    
    dct_simularion_variables = {
        'case': pm.case,
        'velocity': lst_velocity_args,
        'heatflux': lst_heatflux_args,
        'fluid': lst_dct_fluids
    }
    
    for key, val in dct_simularion_variables:
        print()
    
    # dct_Simulation = {
    #     'initialize': 'hyb',
    #     'iterate': pm.iterate,
    # }
    
    # dct_simu_para = pm.get_dct_simu_parameters()
    # dct_result_data = {
    #     'lst_surface' : pm.output_result_facesname,
    #     'lst_data' : pm.output_result_dataname
    # }
    
    
    # fluent.joural_gen_case(pm.case, lst_flow_varibles, dct_simu_para, dct_result_data)
    # fluent.runSim_case(lst_flow_varibles, pm.case, pm.core_number, pm.os_name, pm.fluent_path)


