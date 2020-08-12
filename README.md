# 编程猫登录Oauth
### 介绍
>本接口使用Python语言，Flask+Mysql开发
**通过简单的几步给网站加入编程猫账户登录功能**

欢迎使用本接口🎉🎉🎉

### 注意    
合并分支一般不直接合并到`master`,可以新建一个分支或合并到`lovely`分支  
未经允许对`master`分支的 Pull Requests 会被 Close
 
### 使用接口

我们已将该接口部署到我们的服务器上面，接入方法请看 [接口文档](https://www.showdoc.com.cn/bcmlogin?page_id=5149721938667467)

### 部署
如果您想将本项目布置到您的服务器，请看下面  
**clone 本仓库**
**安装依赖 **
1. 安装 Python3,必须 Python3~  
2. 安装库  
`flask``requests``pymysql `

**准备数据库**
1. 新建一个数据库  
2. 将项目内的 `login.sql` 导入  
3. 编辑 `sql.py` 文件的开头以让程序可以连接到数据库  

**守护进程**
此步推荐 Supervisor，参考 [Supervisor 官网](http://supervisord.org/)安装，也可使用宝塔 Supervisor 管理器，启动脚本如下  `python3 web.py `
目录改为自己的
**反向代理（可选）** 
程序默认在`80`端口运行，如果冲突可以将端口修改为其他的，然后使用nginx反向代理  
反向代理配置如下：
**nginx配置文件：**
找到 `nginx.conf` 并打开
`vim nginx.conf`
假设我改API端口为7414(改端口在web.py第107行Port这一地方)  

```
server {
    listen       80;
    server_name  oauth.example.com;# 改为你要使用的域名（不用加http://或https://）
    location / { # 访问80端口后的所有路径都转发到 proxy_pass 配置的ip中
        root   /usr/share/nginx/html;
        index  index.html index.htm;
   		proxy_pass http://127.0.0.1:7414; # 反向代理地址及端口（必须加上http://）
    }
}
```

  
**如果服务器上安装了宝塔面板**

则这样配置  
目标URL:127.0.0.1:7414  
发送域名：$host
名字：随意 
如下图所示：
![](/img/bt.png)
然后您就可以使用了  
