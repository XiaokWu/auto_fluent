def set_ini_case(inicase=None):
    tui_pras = f"/file/read-case/{inicase}\n"
    return tui_pras

def set_velocity(velocity=None):
    tui_pras = f"/define/boundary-conditions/set/velocity-inlet/inlet () vmag no {velocity} q\n"
    return tui_pras if velocity else None

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

def write_result(result_path=None, lst_surface, lst_data):
    surfaces = ''
    for surface in lst_surface:
        surfaces = f"{surfaces} {surface}"
    datas = ''
    for data in lst_data:
        datas = f"{datas} {data}"
    tui_paras = f'/file/export/ascii {result_path} {surfaces} () y {datas} q y'



def create_jou_line(dct_pram):
    dct_func = {
        'velocity':set_velocity,
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
    # yield "/exit OK"
            
def creat_jou(dct_pram):
    jou = "".join(create_jou_line(dct_pram))
    return jou

if __name__ == "__main__":
    dct_para = {
        'velocity':10,
        'iterate':100,
        'time_step':10,
        'convergence_criterion':1e-10,
        'result_file_path' : "set_result_file_path"
    }
    
    jou = creat_jou(dct_para)
    print(jou)
    

