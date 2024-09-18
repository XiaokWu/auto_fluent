import yaml
import fluent_tui
import Parameters

dct_para = {
    'velocity':10,
    'iterate':100,
    'time_step':10,
    'convergence_criterion':1e-10,
    'result_file_path' : "set_result_file_path"
}

jou = fluent_tui.creat_jou(dct_para)
print(jou)
