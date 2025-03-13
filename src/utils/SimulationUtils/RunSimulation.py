import src.conf.liquids as liq
from src.utils.SimulationUtils.auto_fluent import AutoFluent
import numpy as np
import src.conf.Parameters as pm
import src.utils.SimulationUtils.InputEngine as InputEngine

def ConcateJOUargs(dct_variable_args):
    lst_key = list(dct_variable_args.keys())
    for key in lst_key:
        if len(dct_variable_args[key]) == 0:
            del dct_variable_args[key]
    dct_simularion_variables = {
    'initialize': 'hyb',
    'iterate': pm.iterate
    }
    dct_sim_args = {**dct_variable_args, **dct_simularion_variables}
    return dct_sim_args
    
    
def GenJou(fluent, lst_dct_simulation_variables_of_single_case):
    for dct in lst_dct_simulation_variables_of_single_case:
        case_name = InputEngine.getSimFileName(dct)
        dct_sim_args = ConcateJOUargs(InputEngine.analysis_dct_sim_to_jou_args(dct))
        dct_result_data = {
        'lst_surface' : pm.output_result_facesname,
        'lst_data' : pm.output_result_dataname
            }
        fluent.joural_gen_beta(case_name, dct_sim_args, dct_result_data)
    

def simualtionIsRun():
    if pm.dataprocessing_only or pm.extracting_mode:
        return False
    else:    
        return True
    
def RunSimulation():
    if simualtionIsRun():
        Fluent = AutoFluent(pm.simulation_name, pm.mesh_folder, pm.case_folder, pm.result_folder, pm.jou_folder, pm.ini_case_folder)
        Fluent.initial()
        
        if pm.on_server:
            fluent = AutoFluent.Server(Fluent)
        else:
            fluent = AutoFluent.Local(Fluent)
        
        
        
        dct_simulation_variables= pm.simulation_variables.copy()  
        non_null_input_info = pm.get_non_null_input_info(dct_simulation_variables)
        lst_key = pm.simulation_variables.keys()
        for key in lst_key:
            if len(pm.simulation_variables[key]) == 0:
                #删去不包含输入的模拟变量
                del dct_simulation_variables[key]
        
        lst_dct_simulation_variables = InputEngine.get_lst_dct_simulation_variables(dct_simulation_variables, non_null_input_info)
        lst_dct_simulation_variables_of_single_case = InputEngine.get_lst_dct_simulation_variables_of_single_case(lst_dct_simulation_variables)
        lst_dct_simulation_variables_of_single_case = InputEngine.distingush_sim_variable(lst_dct_simulation_variables_of_single_case)
        
        
        
        GenJou(fluent, lst_dct_simulation_variables_of_single_case)
        print(' ###########################################  Simulation  ###########################################\n\n')
        fluent.runSim_beta(pm.core_number, pm.os_name, pm.fluent_path)
