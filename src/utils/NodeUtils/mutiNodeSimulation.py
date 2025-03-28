import src.utils.netUtils.ssh_connect as ssh_connect
import src.utils.netUtils.ssh_connect as sftp_connect
import src.utils.NodeUtils.mutiConsle as mutiConsle
import src.conf.Parameters as Parameters
import time
import os
import json
import sys
    

    
def get_dct_nodes():
    with open(r'NodesSet/nodes.json') as f:
        dct_nodes = json.load(f)
    return dct_nodes

def search_avaliable_node(dct_nodes, minium_usage,  lst_avoid_node) -> list:
    """
    搜索可用节点
    Args:
        dct_nodes (dict): 节点信息字典
        minium_usage (int): 最小CPU使用率
    Returns:
        list: available nodes
    """
    avaiable_nodes = []
    for key, value in dct_nodes.items():
        ssh = ssh_connect.new_ssh_client()
        CPU_usage = ssh_connect.get_remote_cpu_usage(ssh, value['hostIP'], value['username'], value['password'])
        if CPU_usage is not None and CPU_usage <= minium_usage and key not in lst_avoid_node:
            value['hostname'] = key
            avaiable_nodes.append(value)
            print(f'nodeName: {key}')
            print(f'CPU_usage: {CPU_usage}')
    
    return avaiable_nodes

def asign_task_to_node(lst_avaiable_nodes, given_node_mode, lst_pirority_node, exp_num_nodes, module_path, node_script_dir, command = 'python3'):
    if not given_node_mode:
        if len(lst_avaiable_nodes) < exp_num_nodes:
            print(f'Not enough nodes, only {len(lst_avaiable_nodes)} nodes available')
            continue_flag = input('Do you want to continue? (y/n): ')
            if continue_flag == 'n':
                sys.exit()
            else:
                print('Proceeding with maxium available nodes')
        lst_avaiable_pirority_nodes = [node for node in lst_avaiable_nodes if node['hostname'] in lst_pirority_node]
        lst_avaiable_nodes_without_pirority = [node for node in lst_avaiable_nodes if node not in lst_avaiable_pirority_nodes]
        lst_avaiable_nodes = lst_avaiable_pirority_nodes + lst_avaiable_nodes_without_pirority[:exp_num_nodes-len(lst_avaiable_pirority_nodes)]
    if not os.path.exists(node_script_dir):
        os.mkdir(node_script_dir)
    for node in lst_avaiable_nodes:
        script_path = os.path.join(node_script_dir, f'{node["hostname"]}.py')
        mutiConsle.new_script_from_module(module_path, node,script_path, command)
        mutiConsle.new_console_from_script(script_path)
        time.sleep(5)#给每个节点分配时间进行初始化
    print('All nodes are ready')
        

def simulation():
    dct_nodes = get_dct_nodes()
    exp_num_nodes = Parameters.exp_num_nodes
    minium_usage = 100-Parameters.minium_avaliable_CPU_usage
    if Parameters.run_on_given_node:
        lst_avaiable_nodes = []
        for nodename in Parameters.given_node_name:
            if nodename in dct_nodes:
                dct_nodes[nodename]['hostname'] = nodename
                lst_avaiable_nodes.append(dct_nodes[nodename])
            else:
                print(f'Node {nodename} does not exist')
                sys.exit()
    else:
        lst_avaiable_nodes = search_avaliable_node(dct_nodes,minium_usage, Parameters.avoid_node)
    command = f"{Parameters.fluent_path} 3ddp -g -t{Parameters.core_number} -i"
    asign_task_to_node(lst_avaiable_nodes, Parameters.run_on_given_node, Parameters.pirority_node, exp_num_nodes, r'src/utils/NodeUtils/node_script', 'src', command)
    