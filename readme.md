命令行输入以部署，这会在项目文件夹里创建一个虚拟环境
```
git clone https://github.com/XiaokWu/auto_run.git
cd auto_run
python3.6 -m venv myenv
source myenv/bin/activate
pip3 install -r requirements.txt
git update-index --assume-unchanged config.yaml
```
如果不需要创建虚拟环境：
```
git clone https://github.com/XiaokWu/auto_run.git
cd auto_run
git update-index --assume-unchanged config.yaml
```