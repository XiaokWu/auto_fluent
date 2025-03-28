# This file contains the class Node which is used to create a node object
# The node object is used to interact with the remote server
import os
import time
import sys
import utils.netUtils.ssh_connect as ssh_connect
import utils.netUtils.sftp_connect as sftp_connect
import logging

class Node:
    
    def __init__(self, hostIP, username, password, work_dir):
        self.username = username
        self.password = password
        self.hostIP = hostIP
        self.work_dir = work_dir
        self.ssh = ssh_connect.new_ssh_client()
        self.sftp, self.transport = sftp_connect.sftp_connect(hostIP, 22, username, password)
            
    def necessary_file_transport(self, dct_necessary_files):
        # 获取本地文件相关信息
        lst_local_file = []
        lst_local_work_dir = ['case','iniCase','journal','result']
        lst_ini_case = dct_necessary_files['ini_case']
        for ini_case in lst_ini_case:
            try:
                ini_case_path = os.path.join('iniCase', ini_case+'.cas.h5')
                lst_local_file.append(ini_case_path)
            except FileNotFoundError:
                print(f"File not found: {ini_case}")
        
        # 创建远程目录
        remote_file_dir = self.work_dir.split('/')[-1]
        remote_file_dir = '/'+remote_file_dir
        self.create_remote_directory(remote_file_dir)
        for dir in lst_local_work_dir:
            dir_path = os.path.join(remote_file_dir, dir)
            self.create_remote_directory(dir_path)
        # 上传文件
        for file in lst_local_file:
            abs_remote_file_path = os.path.join(self.work_dir, file).replace('\\', '/')
            sftp_connect.upload_file(self.sftp, file, abs_remote_file_path)
        print("File transport completed")

    def create_remote_directory(self, remote_directory):
        dirs = remote_directory.split('/')
        path = ''
        for dir in dirs:
            if dir:
                path = os.path.join(path, dir).replace('\\', '/')
                try:
                    self.sftp.stat(path)
                except FileNotFoundError:
                    try:
                        self.sftp.mkdir(path)  # 如果不存在，则创建目录
                        print(f"Created remote directory: {path}")
                    except OSError as e:
                        print(f"Failed to create directory {path}: {e}, check the permission")
                        sys.exit()
        
    def ssh_interactive_command_single(self, channel, base_command):
        """用于交互式执行命令单个执行命令

        Args:
            channel (_type_): 传入的ssh通道
            base_command (_type_): 基准命令,用于启动相关程序
        """
        channel.send(base_command + '\n')# 发送命令
        self.ssh_display(channel)# 实时输出
    
        
            
    def ssh_display(self,channel):
        while True:
            if channel.recv_ready():
                data = channel.recv(1024).decode('utf-8', errors='ignore')
                print(data, end='')  # 实时输出到本地终端
                # 检查是否出现提示符（示例为常见的 '$ ' 或 '# '）
                if data.strip().endswith(('$', '$ ')):
                    break
                    
            else: 
                time.sleep(0.1)
    def ssh_interactive_command(self, base_command):   
        """用于交互式执行命令批量执行命令

        Args:
            base_command (_type_): 基准命令,用于启动相关程序
        """
        try:
            # 连接到目标主机
            self.ssh.connect(hostname=self.hostIP, username=self.username, password=self.password)
            
            # 创建交互式Shell会话
            channel = self.ssh.invoke_shell()
            time.sleep(1)  # 等待会话初始化
            
            # 读取初始输出（欢迎信息等）
            output = ''
            while channel.recv_ready():
                output += channel.recv(1024).decode('utf-8')
            print(output, end='')
            
            #转入工作目录
            work_dir_command = self.work_dir.split('/')[-1]
            self.ssh_interactive_command_single(channel, f"cd {work_dir_command}\n")
            
            have_task = True
            while have_task:
                have_task = self.ssh_shell_interact_fluent(channel, base_command)
                    
        except Exception as e:
            print(f"发生错误: {e}")
        finally:
            channel.send('rm -r journal\n')
            self.ssh.close()
            print("远程连接已关闭")
            
    def ssh_shell_interact_fluent(self, channel, fluent_command):
        """shell交互指令,用于启动fluent,该接口需要保证工作目录为work_dir

        Args:
            fluent_command (_type_): fluent相关指令,包含fluent的位置和启动参数
            channel (_type_): 传入的ssh通道

        Returns:
            _type_: 返回是否有未仿真的journal文件
        """
        #获取未仿真的journal文件
        lst_unsimulated_journal = self.get_unsimed_journal('journal')
        if len(lst_unsimulated_journal) !=0:
            #上传journal文件
            target_journal = self.journal_transport('journal')
            target_journal_path = os.path.join(self.work_dir, 'journal', target_journal).replace('\\', '/')
            print(f"Start to simulate journal file: {target_journal}")
            sim_name = target_journal.replace('.jou','')
            # 拼接命令
            command = f"{fluent_command} {target_journal_path}"
            logging.basicConfig(filename='simulation.log', filemode='a', level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s - %(message)s')
            
            # 发送命令并执行
            logging.info(f'Running simulation {sim_name}...')
            self.ssh_interactive_command_single(channel, command)
            logging.info(f'{sim_name} have been calculated.')
            have_unsimed_journal = True
            return have_unsimed_journal
        else:
            last_log_line = self.get_last_log_line('simulation.log')
            if last_log_line != 'Simulation ended.':
                logging.info('Simulation ended.')
            have_unsimed_journal = False
            return have_unsimed_journal
    
    def get_unsimed_journal(self, journal_dir):
        lst_journal_file = os.listdir(journal_dir)
        return lst_journal_file
    
    def get_last_log_line(log_file_path):
        with open(log_file_path, 'r') as file:
            lines = file.readlines()
            if lines:
                return lines[-1].strip()
            return None

    def journal_transport(self, journal_dir):
        """用于上传以及管理本地的journal文件

        Args:
            journal_dir (_type_): 本地journal文件夹路径

        Returns:
            _type_: 返回上传的journal文件名
        """
        lst_journal_file = self.get_unsimed_journal(journal_dir)
        target_journal = lst_journal_file[0]
        local_journal_file = os.path.join(journal_dir, target_journal)
        remote_journal_dir = os.path.join(self.work_dir, 'journal')
        remote_journal_file = os.path.join(remote_journal_dir, target_journal).replace('\\', '/')
        try:
            sftp_connect.upload_file(self.sftp, local_journal_file, remote_journal_file)
            self.delete_local_file(local_journal_file)
            return target_journal
        except FileNotFoundError:
            print(f"File not found: {journal_dir}")
            
    @staticmethod       
    def delete_local_file(file_path):
        """
        删除本地指定文件
        Args:
            file_path (str): 要删除的文件路径
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted local file: {file_path}")
            else:
                print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Failed to delete file {file_path}: {e}")
        
    
        
            
            
    def get_sftp_root_directory(self):
        """
        获取 SFTP 的根目录
        """
        try:
            root_directory = self.sftp.getcwd()  # 获取当前工作目录
            print(f"SFTP root directory: {root_directory}")
            return root_directory
        except Exception as e:
            print(f"Failed to get SFTP root directory: {e}")
            return None
    
    def node_process():
        pass  