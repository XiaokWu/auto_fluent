import src.conf.liquids as liq
import src.conf.Parameters as pm

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
            lst_dct = []
            for item in lst_dct_simulation_variables:
                for dct in seperate_input(item,input):  
                    lst_dct.append(dct)
            lst_dct_simulation_variables = lst_dct.copy()
                
    return lst_dct_simulation_variables

def get_lst_dct_simulation_variables_of_single_case(lst_dct_simulation_variables):
    #返还单个算例输入的仿真变量的列表
    lst_dct_simulation_variables_of_single_case = []
    for dct_simulation_variables in lst_dct_simulation_variables:
        lst_dct_simulation_variables_of_single_case += traverse_simulation_varibles(dct_simulation_variables)
    return lst_dct_simulation_variables_of_single_case

def distingush_sim_variable (dct_sim_variable):
    # 对传入的变量进行分类以及排序
    for dct in dct_sim_variable:
        dct_new = {}
        for _, value_input in pm.get_inputs_info().items():
            for key, value in dct.items():
                if key in value_input:
                    dct_new[key] = value
                    break
        dct.clear()
        dct.update(dct_new)
    return dct_sim_variable

def getSimFileName (dct_simulation_variable_single_case):
    #根据输入的变量生成相关文件的名称
    file_name = ""
    for key, value in dct_simulation_variable_single_case.items():
        file_name += f"{key}={value},"
    file_name = file_name[:-1]
    return file_name

def analysis_dct_sim_to_jou_args(dct_simulation_variable_single_case):
    dct_simulation_variable_args =  {}
    fluid = liq.Extract_fluid(dct_simulation_variable_single_case['fluid'])[1]
    lst_fluid_args = []
    dct_simulation_variable_args.update({'case' : dct_simulation_variable_single_case['case']})
    if "pressure "in dct_simulation_variable_single_case.keys():
        pressure = dct_simulation_variable_single_case['pressure']
        lst_pressure_args = [pressure, pm.pressure_bc_name]
    else:
        lst_pressure_args = []
    dct_simulation_variable_args.update({'pressure' : lst_pressure_args})
    
    velocity = pm.variablesToVelocity(dct_simulation_variable_single_case, fluid)
    lst_velocity_args = [velocity, pm.velocity_bc_facesname]
    dct_simulation_variable_args.update({'velocity' : lst_velocity_args})
    
    if pm.energy_on:
        energy_type, energy_value = list(dct_simulation_variable_single_case.items())[2]
        lst_energy_args = [energy_value, pm.heat_bc_facesname]
        key_energy_args = energy_type
        dct_simulation_variable_args.update({key_energy_args : lst_energy_args})
        

    dct_simulation_variable_args.update({'fluid' : lst_fluid_args})
    print(dct_simulation_variable_args)
    return dct_simulation_variable_args