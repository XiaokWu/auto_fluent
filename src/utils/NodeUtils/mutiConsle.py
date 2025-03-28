import subprocess
import re
import threading
    
def script_content_from_module(module_name, host, command):
    module_file = module_name + '.py'
    with open(module_file, 'r', encoding='utf-8') as file:
        module_content = file.read()
    
    # 替换文本内容
    hostIP = host['hostIP']
    working_directory = host['working_directory'].split('\\')[-1]
    host_username = host['username']
    host_password = host['password']
    script_content = re.sub(r'username_position', host_username, module_content)
    script_content = re.sub(r'password_position', host_password, script_content)
    script_content = re.sub(r'host_ip', hostIP, script_content)
    script_content = re.sub(r'work_dir_position', working_directory, script_content)
    script_content = re.sub(r'command_position', command, script_content)
    return script_content

def generate_new_console_script(script_path, script_content):
    with open(script_path, 'w', encoding='utf-8') as file:
        file.write(script_content)

def new_script_from_module(module_name, host, script_path, command):
    script_content = script_content_from_module(module_name, host, command)
    generate_new_console_script(script_path, script_content)
    
def new_console_from_script(script_path): 
    command = f'start cmd /k python "{script_path}"'
    subprocess.Popen(command, shell=True)
    
def console_run(module_name, host):
    new_script_from_module(module_name, host)
    script_name = host['hostname']
    new_console_from_script(script_name + '.py')
    
def multi_thread_console_run(module_name, lst_dct_host):
    threads = []
    
    for host in lst_dct_host:
        args_host = [module_name, host]
        thread = threading.Thread(
            target=console_run,
            args=(args_host)
        )
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

def mutiConsole_run(script_name, lst_dct_host):
    for host in lst_dct_host:
        console_run(script_name, host)


