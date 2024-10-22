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

def  extract_velocitys(lst_velocity_args):
    pass

def extract_case(lst_case):
    return lst_case

def extract_heatflux(lst_heatflux_args):
    return lst_heatflux_args['val']

def extract_fluids(lst_dct_fluids):
    pass 

def traverse_simulation_varibles(dct_simulation_varibles, dct_run=None, lst_run_varibles=None):
    dct_simulation_varibles_copy = dct_simulation_varibles.copy()
    #递归调用每一级的变量
    if dct_run is None:
        dct_run = {}
    if lst_run_varibles is None:
        lst_run_varibles = []
    dct_run = dct_run
    lst_key = list(dct_simulation_varibles_copy.keys())
    key = lst_key[0]

    if len(lst_key) == 1 :
        for varible in dct_simulation_varibles_copy[key]:
            dct_run[key] = varible
            lst_run_varibles.append(dct_run.copy())
            del dct_run[key]
        return lst_run_varibles
    else:
        dct_simulation_varibles_sub = dct_simulation_varibles_copy.copy()
        del dct_simulation_varibles_sub[key]
        for varible in dct_simulation_varibles_copy[key]:
            dct_run[key] = varible
            lst_run_varibles = traverse_simulation_varibles(dct_simulation_varibles_sub, dct_run=dct_run, lst_run_varibles=lst_run_varibles)
    return lst_run_varibles
        
def seperate_input(dct_simulation_variables, lst_seperate_variables):
    #将多种同类型的输入分开，比如雷诺数以及流量输入都属于速度输入
    lst_dct_inputs = []
    for variable in lst_seperate_variables:
        dct_simulation_variables_copy = dct_simulation_variables.copy()
        del dct_simulation_variables_copy[variable]
        lst_dct_inputs.append(dct_simulation_variables_copy.copy())
    return lst_dct_inputs
    
def get_lst_dct_simulation_variables(dct_simulation_variables, dct_input_info):
    #将分开后的所有输入整合成列表，每个元素只包含一个同类输入
    lst_dct_simulation_variables = [dct_simulation_variables]
    lst_dct = lst_dct_simulation_variables.copy()
    for input_class , input in dct_input_info.items():
        if len(input) >1:  
            # print('lst_dct:',lst_dct)
            # print('dc:',dct_simulation_variables)
            lst_dct = []
            for item in lst_dct_simulation_variables:
                # print(f'item: {item}\n')
                for dct in seperate_input(item,input):  
                    lst_dct.append(dct)
                # print('lst_dct',lst_dct)
            lst_dct_simulation_variables = lst_dct.copy()
                
    return lst_dct_simulation_variables

def get_lst_dct_simulation_variables_of_single_case(lst_dct_simulation_variables):
    lst_dct_simulation_variables_of_single_case = []
    for dct_simulation_variables in lst_dct_simulation_variables:
        lst_dct_simulation_variables_of_single_case += traverse_simulation_varibles(dct_simulation_variables)
    return lst_dct_simulation_variables_of_single_case
        

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
    
    
    dct_simulation_variables= pm.simulation_variables.copy()  
    non_null_input_info = pm.get_non_null_input_info(dct_simulation_variables)
    lst_key = pm.simulation_variables.keys()
    for key in lst_key:
        if len(pm.simulation_variables[key]) == 0:
            #删去不包含输入的模拟变量
            del dct_simulation_variables[key]
    
    lst_dct_simulation_variables = get_lst_dct_simulation_variables(dct_simulation_variables, non_null_input_info)
    
    # print(lst_dct_fluids)
    lst_flow_varibles, lst_heat_varibles = Extract_BC(fluid)
    lst_velocity_args = [lst_flow_varibles,pm.velocity_bc_facesname]
    lst_heatflux_args = [lst_heat_varibles, pm.heatflux_bc_facesname]
    # print(lst_velocity_args)
    # print(lst_heatflux_args)
    
    # print(pm.simulation_variables)
    for dct in get_lst_dct_simulation_variables_of_single_case(lst_dct_simulation_variables):
        print(dct)
    
    dct_simularion_variables = {
        'case': pm.case,
        'heatflux': lst_heatflux_args,
        'fluid': lst_dct_fluids,
        'velocity': lst_velocity_args
    }

    
    
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
