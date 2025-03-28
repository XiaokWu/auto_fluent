import paramiko
import os
import time
from tqdm import tqdm
import subprocess

def sftp_connect(hostname, port, username, password):
    transport = paramiko.Transport((hostname, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    return sftp, transport

def list_local_files(local_directory):
    file_list = []
    for root, dirs, files in os.walk(local_directory):
        if not files:
            for dir in dirs:
                file_list.append(os.path.relpath(os.path.join(root, dir), local_directory))
        for file in files:
            file_list.append(os.path.relpath(os.path.join(root, file), local_directory))
    return file_list

def list_remote_files(sftp, remote_directory):
    try:
        return sftp.listdir(remote_directory)
    except IOError:
        return []

def download_file(sftp, remote_path, local_path):
    # 确保本地目录存在
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    file_size = sftp.stat(remote_path).st_size
    start_time = time.time()
    
    with tqdm(total=file_size, unit='B', unit_scale=True, desc=os.path.basename(local_path)) as progress_bar:
        def print_progress(transferred, total):
            elapsed_time = time.time() - start_time
            speed = transferred / elapsed_time if elapsed_time > 0 else 0
            progress_message = f"AverageSpeed: {speed/(1024*1024):.2f} MB/s"
            progress_bar.set_postfix_str(progress_message)
            progress_bar.update(transferred - progress_bar.n)
        
        sftp.get(remote_path, local_path, callback=print_progress)


def download_directory(sftp, remote_directory, local_directory):
    # 获取远程目录中的所有文件
    file_list = list_remote_files(sftp, remote_directory)
    # 获取本地目录中的所有文件
    local_file_list = list_local_files(local_directory)
    # 下载远程
    for file_name in file_list:
        remote_file_path = os.path.join(remote_directory, file_name)
        local_file_path = f'{local_directory}/{file_name}'
        if file_name in local_file_list:
            continue
        else:
            print(f"Downloading {remote_file_path} to {local_file_path}")
            print(f"Start time: {get_current_time()}")
            download_file(sftp, remote_file_path, local_file_path)

def upload_file(sftp, local_path, remote_path):
    remote_path = remote_path.replace('\\', '/')
    try:
        sftp.stat(remote_path)
        if sftp.stat(remote_path).st_size :
            print(f"File {remote_path} already exists")
            return
    except FileNotFoundError:
        pass
    file_size = os.path.getsize(local_path)
    start_time = time.time()
    with tqdm(total=file_size, unit='B', unit_scale=True, desc=os.path.basename(local_path)) as progress_bar:
        def print_progress(transferred, total):
            elapsed_time = time.time() - start_time
            speed = transferred / elapsed_time if elapsed_time > 0 else 0
            progress_message = f"AverageSpeed: {speed/(1024*1024):.2f} MB/s"
            progress_bar.set_postfix_str(progress_message)
            progress_bar.update(transferred - progress_bar.n)
            
        sftp.put(local_path, remote_path, callback=print_progress)
    print(f"Uploaded {local_path} to {remote_path}")

def upload_directory(sftp, local_directory, remote_directory):
    # 获取本地目录中的所有文件
    file_list = list_local_files(local_directory)
    # 获取远程目录中的所有文件
    remote_file_list = list_remote_files(sftp, remote_directory)
    
    for file_name in file_list:
        local_file_path = os.path.join(local_directory, file_name)
        remote_file_path = os.path.join(remote_directory, file_name).replace('\\', '/')
        
        # 创建远程目录
        remote_dir = os.path.dirname(remote_file_path)
        try:
            sftp.stat(remote_dir)
        except FileNotFoundError:
            mkdir_p(sftp, remote_dir)
        
        if file_name in remote_file_list:
            continue
        else:
            print(f"Uploading {local_file_path} to {remote_file_path}")
            upload_file(sftp, local_file_path, remote_file_path)
    
def mkdir_p(sftp, remote_directory):
    dirs = remote_directory.split('/')
    path = ''
    for dir in dirs:
        path = os.path.join(path, dir)
        path = path.replace('\\', '/')
        try:
            sftp.stat(path)
        except FileNotFoundError:
            sftp.mkdir(path)
            
def execute_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode().strip()
    error = stderr.read().decode().strip()
    return output, error

def get_current_time():
    current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    return current_time