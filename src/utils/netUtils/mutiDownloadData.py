import sftp_connect as sftp_connect
import threading
import time
import os

def download_data(hostname, port, username, password, remote_directory, local_directory):
    sftp, transport = sftp_connect.sftp_connect(hostname, port, username, password)
    try:
        sftp_connect.download_directory(sftp, remote_directory, local_directory)
    finally:
        sftp.close()
        transport.close()
        
def get_last_log_line(log_file_path):
    with open(log_file_path, 'r') as file:
        lines = file.readlines()
        if lines:
            return lines[-1].strip()
        return None


def monitor_and_transfer_files(host,remove_remote_directory_after_download=True):
    hostname = host['hostname']
    port = host['port']
    username = host['username']
    password = host['password']
    working_directory = host['working_directory']
    simulation_name = host['simulation_name']
    remote_directory = host['remote_directory']
    local_directory = host['local_directory']
    sftp, transport = sftp_connect.sftp_connect(hostname, port, username, password)
    ssh = sftp_connect.ssh_connect(hostname, port, username, password)
    keep_monitoring = True
    try:
        while keep_monitoring:
            #获取日志文件
            log_file = os.path.join(local_directory, 'simulation.log')
            sftp.get(os.path.join(working_directory, 'simulation.log'), log_file)
            last_line = get_last_log_line(log_file)
            if last_line:
                if 'Simulation ended.' in last_line:
                    keep_monitoring = False
            local_file_list = sftp_connect.list_local_files(local_directory)
            if 'simulation.log' in local_file_list:
                local_file_list.remove('simulation.log')
            # 获取并对比目标文件夹内文件名列表
            remote_file_list = sftp_connect.list_remote_files(sftp, remote_directory)
            unDownloaded_files = list(set(remote_file_list) - set(local_file_list))
            # 下载远程文件
            if unDownloaded_files:
                time.sleep(60)
                for file_name in unDownloaded_files:
                    remote_file_path = os.path.join(remote_directory, file_name)
                    local_file_path = f'{local_directory}/{file_name}'
                    sftp_connect.download_file(sftp, remote_file_path, local_file_path)
            else:    
                time.sleep(10)
            
        # 删除远程文件
        if remove_remote_directory_after_download:
            _, error = sftp_connect.execute_command(ssh, f'rm -r {remote_directory}')
            if error:
                print(f"Command error: \n{error}")
    finally:
        sftp.close()
        transport.close()

def MutiThread_download(hosts):
    threads = []
    
    for host in hosts:
        thread = threading.Thread(
            target=download_data,
            args=(
                host['hostname'],
                host['port'],
                host['username'],
                host['password'],
                host['remote_directory'],
                host['local_directory']
            )
        )
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

def MutiThread_monitor(hosts):
    threads = []
    
    for host in hosts:
        thread = threading.Thread(
            target=monitor_and_transfer_files,
            args=(host,)
        )
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()