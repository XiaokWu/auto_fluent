#!/bin/bash

#创建虚拟环境以及安装依赖库
python3.6 -m venv myenv
source myenv/bin/activate
pip3 install -r requirements.txt
