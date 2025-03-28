import sys
from utils.NodeUtils.Node import Node
import conf.Parameters as pm


host = 'host_ip' # 服务器IP
username = 'username_position' # 用户名
password = 'password_position' # 密码
work_dir = r'work_dir_position' # 工作目录
command = 'command_position'  # 要执行的命令

dct_necessary_files = {'ini_case':pm.case}

node = Node(host, username, password, work_dir)

# 获取 SFTP 根目录
# sftp_root = node.get_sftp_root_directory()
# print(f"SFTP 根目录为: {sftp_root}")

node.necessary_file_transport(dct_necessary_files)
node.ssh_interactive_command(command)
sys.exit()