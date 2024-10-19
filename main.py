import os
import Parameters as pm

# if pm.on_server:
#     os.system('source ./myenv/bin/activate')

import DataProcess 
import RunSimulation

# os.system('pip install -r requirements.txt')
RunSimulation.RunSimulation()
DataProcess.DataProcess()