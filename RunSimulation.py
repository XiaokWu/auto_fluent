import liquids as liq
from auto_fluent import AutoFluent
import numpy as np
import yaml

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

simulation_name = config['simulation_name']
on_server = config['on_server']
core_number = config['core_number']
os_name = config['os_name']

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

geometry = config['geometry']
inlet_area = float(geometry['inlet_area'])
characteristic_length = geometry['characteristic_length']
inlet_position = geometry['inlet_position']
outlet_position = geometry['outlet_position']

output_features = config['output_features']
fluid = liq.Extract_fluid(fluid_name)

def Extract_BC():
    dct_Re = {
        'name' : 'Re',
        'val' : Re,
        'velocity': np.array(Re)*fluid.viscosity/(fluid.density*characteristic_length)
    }
    
    dct_massflow = {
        'name' : 'massflow',
        'val' : massflow,
        'velocity': np.array(massflow)/(fluid.density*inlet_area)
    }
    
    dct_heatflux = {
        'name' : 'heatflux',
        'val' : heatflux
    }
    
    lst_flow_varibles = [dct_Re, dct_massflow]
    lst_heat_bc = [dct_heatflux]
    
    return lst_flow_varibles, lst_heat_bc



def RunSimulation():
    Fluent = AutoFluent(simulation_name, mesh_folder, case_folder, result_folder, jou_folder, ini_case_folder)
    Fluent.initial()
    
    if on_server:
        fluent = AutoFluent.Server(Fluent)
    else:
        fluent = AutoFluent.Local(Fluent)
        
    
    lst_flow_varibles, lst_heat_bc = Extract_BC()
     
  
    
    
    fluent.joural_gen_case(heatsink, lst_flow_varibles)
    fluent.runSim_case(lst_flow_varibles, heatsink, core_number)


