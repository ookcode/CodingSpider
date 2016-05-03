--------------------------------------------------------------------------------<br>
5月3日申明：coding已经开启的刷码币的检测，本脚本仅供学习，使用本脚本造成的任何损失，本人概不负责！
--------------------------------------------------------------------------------
#Coding小蜘蛛
##主要功能
* 自动登录coding
* 自动创建项目
* 自动创建分支
* 自动推送代码，0.01码币
* 自动创建任务，0.01码币
* 自动创建合并请求，0.01码币
* 自动使用webIDE（默认关闭）（弃用）
* 自动修改生日，0.1码币（默认关闭）（一次有效）
* 自动关注作者（默认关闭）

##使用说明
1、请将本目录下的.coding.config文件复制到用户*主目录*<br>
2、在配置文件中填入账号密码，保证json格式正确即可<br>
3、在命令行中执行coding_spider.py -h查看帮助<br>

##演示平台
http://codingspider.coding.io/spider?username=xx@xx.com&password=yourpassword<br>
访问此URL并带上您的账号密码可以快速完成码币任务<br>
郑重承诺：本程序不会保存任何账号密码，请放心使用，密码可用sha1加密后再填入<br>

##本地演示平台搭建(linux)
1、安装virtualenv<br>
使用easy_install安装pip<br>
$ sudo easy_install pip<br>
使用pip安装virutalenv<br>
$ sudo pip install virtualenv<br>

2、启动py<br>
for linux
cd至仓库目录<br>
$ virtualenv venv<br>
$ source venv/bin/activate<br>
$ pip install -r requirements.txt<br>
$ gunicorn hello:app<br>

访问 http://localhost:8000 查看效果。

##本地演示平台搭建(windows)
1、安装easy_install<br>
```
cd至python目录
>>> from urllib import urlopen
>>> data = urlopen('http://peak.telecommunity.com/dist/ez_setup.py')
>>> open('ez_setup.py','wb').write(data.read())
>>> exit
通过以上命令下载ez_setup.py
```
2、将C:\Python27\scripts添加至环境变量<br>

3、安装virutalenv<br>
$ easy_install virtualenv<br>

4、启动项目<br>
$ virtualenv venv<br>
$ venv/bin/activate.bat<br>
$ pip install -r requirements.txt<br>
$ python hello.py<br>


