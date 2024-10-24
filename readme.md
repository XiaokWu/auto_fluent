命令行输入以部署，这会在项目文件夹里创建一个虚拟环境
```
git clone https://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@github.com/XiaokWu/auto_run.git
cd auto_run
git pull origin main
python3.6 -m venv myenv
source myenv/bin/activate
pip3 install -r requirements.txt
git update-index --assume-unchanged config.yaml
```
如不需要创建虚拟环境：
``
git clone https://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@github.com/XiaokWu/auto_run.git
cd auto_run
git pull origin main
git update-index --assume-unchanged config.yaml
```
在`config.yaml` 文件中修改仿真参数后运行`main.py`
```
python3 main.py
```