# 编程猫登录Oauth
欢迎使用本接口  
接口帮助文档：https://www.showdoc.com.cn/bcmlogin?page_id=5149721938667467  
本接口使用Flask+Mysql开发  
如果您想将本项目布置到您的服务器，请看下面  
1.clone本储存库  
2.安装依赖  
首先安装Python3,必须python3~  
然后安装库  
flask,requests,pymysql  
3.准备数据库  
新建一个数据库  
将项目内的login.sql导入  
编辑sql.py文件的开头以让程序可以连接到数据库  
4.使用守护进程让进程一直运行  
此步推荐使用宝塔面板的Supervisor管理器，启动脚本如下  
python3 web.py  
目录什么的个人喜好  
5.反向代理（可选）  
程序默认在80端口运行，如果冲突可以将端口修改为其他的，然后使用NGinx反向代理  
反向代理配置如下（还是按照宝塔的）假设我改端口为7414(改端口在web.py第107行Port这一地方)  
则这样配置  
目标URL:127.0.0.1:7414  
发送URL:随意  
名字：随意  
然后您就可以使用了  
