import json

def get_tui_database(json_path):
    with open(json_path) as file:
        tui_database = json.load(file)
    return tui_database

def format_tui_pras(template, placeholders):
    """
    通用接口函数，接受占位符列表和参数列表，返回格式化的字符串
    """
    return template.format(**placeholders)

def get_tui_pras(pras_name, placeholders, tui_database):
    tui_pras_template = tui_database[pras_name]
    return format_tui_pras(tui_pras_template, placeholders)


def set_ini_case(inicase=None):
    tui_pras = f"/file/read-case/{inicase}\n"
    return tui_pras

def set_fluid(fluid):
    pass

def set_pressure(lst_press_args):
    pass

def set_velocity(lst_velocity_args=None):
    velocity = lst_velocity_args[0]
    lst_faces = lst_velocity_args[1]
    faces = ''
    if not velocity:    
        return None
    for face in lst_faces:
        faces = f"{faces} {face}"
    tui_pras = f"/define/boundary-conditions/set/velocity-inlet/{faces} () vmag no {velocity} q\n"
    return tui_pras

def set_heatflux(lst_heatflux_args = None):
    heatfux = lst_heatflux_args[0]
    lst_faces = lst_heatflux_args[1]
    faces = ''
    if not heatfux:
        return None
    for face in lst_faces:
        faces = f"{faces} {face}"
    tui_pras = f"/define/boundary-conditions/set/wall/{faces} () heat-flux () no {heatfux} q q q\n"
    return tui_pras

def set_fluid(fluid=None):
    tui_paras = f"/define/boundary-conditions/set/fluid fluid* () material yes {fluid} q"
    return tui_paras
    
def set_iterate(iterate=None):
    tui_pras = f"/solve/iterate {iterate}\n"
    return tui_pras if iterate else None

def set_time_step(time_step=None):
    tui_pras = f"/solve/set/time-step {time_step}\n"
    return tui_pras if time_step else None

def set_convergence_criterion(convergence_criterion=None):
    tui_pras = f"/solve/set/convergence-criterion {convergence_criterion}\n"
    return tui_pras if convergence_criterion else None

def set_initialize(initialization=None):
    tui_paras = f"/solve/initialize/hyb-initialization\n"
    return tui_paras

def set_fluid(fluid=None):
    tui_paras = f"/define/boundary-conditions/set/fluid fluid* () material yes {fluid} q"
    return tui_paras

def write_case(case_file_path = None):
    tui_pras = f"/file/write-case-data {case_file_path}.cas\n"
    return tui_pras

def write_result(lst_result_args):
    result_path = lst_result_args[0]
    lst_surface = lst_result_args[1]
    lst_data = lst_result_args[2]
    datas = ''
    tui_paras = ''
    for data in lst_data:
        datas = f"{datas} {data}"
    for surface in lst_surface:
        result_path_surface = result_path.replace('.csv',f'_{surface}.csv')
        tui_surface = f"/file/export/ascii {result_path_surface} {surface} () y {datas} q n"
        if surface == lst_surface[0]:
            tui_paras = tui_surface
        else:
            tui_paras = f"{tui_paras}\n{tui_surface}"
    return tui_paras



def create_jou_line(dct_pram):
    dct_func = {
        'velocity':set_velocity,
        'heatflux':set_heatflux,
        'pressure':set_pressure,
        'fluid': set_fluid,
        'iterate':set_iterate,
        'time_step':set_time_step,
        'convergence_criterion':set_convergence_criterion,
        'write_case' : write_case,
        'ini_case' : set_ini_case,
        'initialize' : set_initialize,
        'write_result' : write_result
    }
    for key, value in dct_pram.items():
        if value:
            yield dct_func[key](value)
    yield "\n/exit OK"
            
def creat_jou(dct_pram):
    jou = "".join(create_jou_line(dct_pram))
    return jou
    
    
