import yaml

# 定义文件路径
yaml_file_path = 'config.yaml'

try:
    # 尝试读取 YAML 文件
    with open(yaml_file_path, 'r') as file:
        config = yaml.safe_load(file)
    
    # 检查是否成功加载
    if config is None:
        raise ValueError("YAML file is empty or could not be parsed")

    # 从 config 中提取数据
    simulation_name = config['simulation_name']
    on_server = config['on_server']

    folders = config['folders']
    mesh_folder = folders['mesh_folder']
    ini_case_folder = folders['ini_case_folder']
    jou_folder = folders['jou_folder']
    result_folder = folders['result_folder']
    output_folder = folders['output_folder']
    case_folder = folders['case_folder']

    simulation_parameters = config['simluation_parameters']
    inlet_area = simulation_parameters['inlet_area']
    D = simulation_parameters['D']
    Re = simulation_parameters['Re']
    massflow = simulation_parameters['massflow']
    heatsink = simulation_parameters['heatsink']
    inlet_position = simulation_parameters['inlet_position']
    outlet_position = simulation_parameters['outlet_position']

except FileNotFoundError:
    print(f"Error: The file '{yaml_file_path}' does not exist.")
except yaml.YAMLError as exc:
    print(f"Error parsing YAML file: {exc}")
except ValueError as ve:
    print(f"ValueError: {ve}")
except KeyError as ke:
    print(f"Missing key in YAML file: {ke}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
