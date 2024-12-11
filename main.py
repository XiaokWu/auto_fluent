import os
import sys
import subprocess
import src.conf.Parameters as pm

if pm.on_server and pm.on_venv:
    # 检查是否在虚拟环境中运行
    if 'VIRTUAL_ENV' not in os.environ:
        os.system('chmod +x src/conf/run_with_venv.sh')
        subprocess.run(['./src/conf/run_with_venv.sh'])
        sys.exit()  # 退出当前脚本，避免递归调用


# 主要逻辑
import src.utils.DataUtils.DataProcess as DataProcess
import src.utils.SimulationUtils.RunSimulation as RunSimulation
subprocess.run(['pip3', 'install', '-r', 'requirements.txt'])

print('\n\n\n#######################################################  Prograss Start #######################################################')
RunSimulation.RunSimulation()
if pm.dataprocessing_only:
    os.chdir(pm.simulation_name)
# DataProcess.DataProcess()
