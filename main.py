import os
import conf.Parameters as pm


if pm.on_server: 
    os.system('source ../myvenv/bin/activate')
os.system('pip3 install -r requirements.txt')

import DataUtils.DataProcess as DataProcess
import SimulationUtils.RunSimulation as RunSimulation
print('\n\n\n#######################################################  Simulation Start #######################################################')
RunSimulation.RunSimulation()
DataProcess.DataProcess()
