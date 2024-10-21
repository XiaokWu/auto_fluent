import os
import Parameters as pm
if pm.on_server: 
    os.system('source ../myvenv/bin/activate')
os.system('pip3 install -r requirements.txt')
os.system('python3 Run.py')
