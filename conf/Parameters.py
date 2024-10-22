import yaml

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

simulation_name = config['simulation_name']
on_server = config['on_server']
on_venv = config['on_venv']
core_number = config['core_number']
os_name = config['os_name']
fluent_path = config['fluent_path']

folders = config['folders']
mesh_folder = folders['mesh_folder']
ini_case_folder = folders['ini_case_folder']
jou_folder = folders['jou_folder']
result_folder = folders['result_folder']
output_folder = folders['output_folder']
case_folder = folders['case_folder']

simulation_variables = config['simulation_variables']
Re = simulation_variables['Re']
massflow = simulation_variables['massflow']
case = simulation_variables['case']
heatflux = simulation_variables['heatflux']
tem = simulation_variables['tem']
fluids = simulation_variables['fluid']

simulation_parameters = config['simluation_parameters']
iterate = simulation_parameters['iterate']
velocity_bc_facesname = simulation_parameters['velocity_bc_facesname']
heatflux_bc_facesname = simulation_parameters['heatflux_bc_facesname']

geometry = config['geometry']
inlet_area = float(geometry['inlet_area'])
characteristic_length = geometry['characteristic_length']
inlet_position = geometry['inlet_position']
outlet_position = geometry['outlet_position']

output_result_facesname = config['output_result_facesname']
output_result_dataname = config['output_result_dataname']
output_features = config['output_features']

def get_dct_simu_parameters():
    dct_para = {
        'fluid_name' : fluids,
        'iterate' : iterate
    }
    
    return dct_para

def get_inputs_info():
    dct_inputs = {
        'velocity':['Re', 'massflow'],
        'heat':['heatflux','tem'],
        'fluid':['fluid'],
        'case':['case']
    }
    return dct_inputs

def get_non_null_input_info(simulation_variables):
    dct_inputs = get_inputs_info()
    for key, value in simulation_variables.items():
        if len(value) == 0:
            print(f'value of {key} is null')
            for key_input, value_input in dct_inputs.items():
                if key in value_input:
                    value_input.remove(key)
    return dct_inputs
            

def parameters_check():
    input_info = get_inputs_info()
    for key, value in input_info.items():
        non_null_num = 0
        for variable in value:
            if len(simulation_variables[variable]) != 0:
                non_null_num +=1
                break
        if non_null_num == 0:
            raise ValueError(f"No input in {key}")

parameters_check()