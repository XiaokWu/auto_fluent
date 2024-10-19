import os
import Parameters as pm

# if pm.on_server:
#     os.system('source ./myenv/bin/activate')

import DataProcess 
import RunSimulation

os.system('pip3 install -r requirements.txt')
print('\n\n\n#######################################################  Simulation Start #######################################################')
RunSimulation.RunSimulation()
DataProcess.DataProcess()