import paramiko
import time
import re

def new_ssh_client():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    return ssh

def get_remote_cpu_usage(ssh, hostIP, username, password):
    try:
        # 连接到目标主机
        ssh.connect(hostname=hostIP, username=username, password=password)
        
        # 执行命令获取CPU占用率
        stdin, stdout, stderr = ssh.exec_command("top -bn1 | grep 'Cpu(s)'")
        cpu_usage = stdout.read().decode('utf-8')
        
        # 使用正则表达式提取CPU占用率
        cpu_usage = re.search(r'\d+\.\d+ id', cpu_usage).group()
        return round(100 - float(cpu_usage.split()[0]), 2)
        
    except Exception as e:
        print(f"发生错误: {e}")
        return None
    finally:
        ssh.close()

def ssh_interactive_command(ssh, host, username, password, command):
    try:
        # 连接到目标主机
        ssh.connect(hostname=host, username=username, password=password)
        
        # 创建交互式Shell会话
        channel = ssh.invoke_shell()
        time.sleep(1)  # 等待会话初始化
        
        # 读取初始输出（欢迎信息等）
        output = ''
        while channel.recv_ready():
            output += channel.recv(1024).decode('utf-8')
        print(output, end='')
        
        # 发送命令并执行（注意末尾添加换行符）
        channel.send(command + '\n')
        
        # 循环读取输出直到检测到提示符
        while True:
            if channel.recv_ready():
                data = channel.recv(1024).decode('utf-8', errors='ignore')
                print(data, end='')  # 实时输出到本地终端
                # 检查是否出现提示符（示例为常见的 '$ ' 或 '# '）
                if data.strip().endswith(('$', '$ ')):
                    break
                    
            else:
                time.sleep(0.1)
                
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        ssh.close()
        print("远程连接已关闭")
        
    
# if __name__ == '__main__':
#     # 使用示例
#     host = '10.20.106.70'
#     username = 'wuxk'
#     password = 'wu1234'
#     command = 'cd work_dir \n python3 main.py'  # 要执行的命令

#     # 创建SSH客户端实例
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#     print(get_remote_cpu_usage(ssh, host, username, password))