## charging_dashboard

### 充电图表

```bash
#运行
py main.py
```

```bash
#start
python main.py
```

## 以下是效果

[充电图表](chart.png)

## 如何使用？？

第一步：在vivo手机上打开电源信息的活动，然后进入"电源记录"界面，找到"开始"然后点击按钮即可
第二步：打开MT管理器（例子）在存储目录下找到名为 "fuel_log" 选择后缀是CSV的文件，移动到电脑上的一个目录中
第三步：运行`py -m pip install matplotlib pandas numpy`命令安装依赖
第四步：把PY脚本中的`'ItemData_2026.07.02_11.32.39.csv`换成你自己移动过来的文件名即可
第五步：使用上方的目录运行，脚本会自动创建一个名为png图片的图表

## DEV

QQ:3520687734