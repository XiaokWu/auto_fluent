import subprocess
import os
os.system('chmod +x conf/prepare.sh')
subprocess.run(['./src/conf/prepare.sh'])