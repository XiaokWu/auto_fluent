import os
os.system('source ./venv/bin/activate')

# import DataProcess 
import RunSimulation

os.system('pip install -r requirements.txt')
RunSimulation.RunSimulation()
# DataProcess.DataProcess()
    