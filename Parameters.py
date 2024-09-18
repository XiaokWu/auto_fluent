import yaml

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

simulation_name = config['simulation_name']
on_server = config['on_server']
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

simulation_parameters = config['simluation_parameters']
Re = simulation_parameters['Re']
massflow = simulation_parameters['massflow']
heatsink = simulation_parameters['heatsink']
heatflux = simulation_parameters['heatflux']
fluid_name = simulation_parameters['fluid']
iterate = simulation_parameters['iterate']

geometry = config['geometry']
inlet_area = float(geometry['inlet_area'])
characteristic_length = geometry['characteristic_length']
inlet_position = geometry['inlet_position']
outlet_position = geometry['outlet_position']

output_features = config['output_features']

def get_dct_simu_parameters():
    dct_para = {
        'Re' : Re,
        'massflow' : massflow,
        'heatsink' : heatsink,
        'heatflux' : heatflux,
    }