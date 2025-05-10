# 米家PC插件
米家PC插件，通过[巴法云](https://bemfa.com)，把你的电脑接入米家

本脚本基于巴法云MQTT服务器，通过米家“连接其他平台”功能实现接入米家及小爱语音控制

电脑伪装为灯，使用巴法云中的灯类亮度控制来控制电脑音量

# 开发计划
1.~~音量控制~~（已完成）

2.播放/暂停控制

3.屏幕亮度控制

（欢迎各位移步[issues](https://github.com/guayun/mijia-pc-plugin/issues)踊跃发言）

# 打包
```bash
pip install -r requirements.txt
pyinstaller --onefile --windowed --add-data "icon.ico;." --icon=icon.ico --name="MijiaPlugin" main.py
```

# 我是小白，不会打包？
请根据教程一步一步来吧

1.移步到右侧[releases](https://github.com/guayun/mijia-pc-plugin/releases)栏目，下载已打包程序并解压

2.用文本编辑器打开config.txt

![](https://cdn.nlark.com/yuque/0/2025/png/26331268/1746850289861-71cece87-75bf-49b8-acf9-529911f03088.png)

3.打开[巴法云](https://bemfa.com)并注册登录

![](https://cdn.nlark.com/yuque/0/2025/png/26331268/1746850517522-cbdfaca0-1cd3-41a7-9833-f89aa926f8bc.png)

把图中位置的私钥复制粘贴到config.txt中BEMFA_CLIENT_ID的等于号后面

4.全部设置完成后如下图所示

![](https://cdn.nlark.com/yuque/0/2025/png/26331268/1746851061417-6984ba2d-e3c0-4ad3-9a07-1bfa469fb3cf.png)



OK，至此客户端部分配置完毕，请继续在巴法云服务端配置教程

1.继续打开巴法云，点击MQTT设备云![](https://cdn.nlark.com/yuque/0/2025/png/26331268/1746850585578-4b2c0848-6b7f-473c-a464-a52af98a1ad0.png)

2.右侧输入框中输入：PC002![](https://cdn.nlark.com/yuque/0/2025/png/26331268/1746850816215-a797c82f-56d4-45fe-aae4-8628be9815cd.png)

3.给你创建的设备修改一个名字

![](https://cdn.nlark.com/yuque/0/2025/png/26331268/1746851006185-80edb984-b30d-4e36-b7be-e7edffe8cedd.png)

4.全部设置完成后如下图所示

![](https://cdn.nlark.com/yuque/0/2025/png/26331268/1746850868508-586286d2-6429-4f79-9ffa-84701194e003.png)

至此巴法云部分配置完成，继续进行米家的配置

1.打开米家APP->我的->连接其他平台->搜索“巴法”->把你刚刚创建的设备同步进来

![](https://cdn.nlark.com/yuque/0/2025/jpeg/26331268/1746851127659-139acb4b-8dec-444e-ab83-5f20a6053083.jpeg)

好了，现在所有配置都已完成，你可以双击电脑中的MijiaPlugin.exe

运行成功屏幕右下角会弹出提示

![](https://cdn.nlark.com/yuque/0/2025/png/26331268/1746851237536-00e89f3b-883d-4509-93f0-56240d44a1fc.png)

你可以对小爱说：小爱同学，将[你设置的设备名称]的亮度调整为20%
