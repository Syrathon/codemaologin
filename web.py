from flask import request, Flask, jsonify,render_template
import hashlib
import sql
import random
import codemao
import requests
import re
#导入库

#html = render_template("page.html")#加载html页，
#app=Flask(__name__,static_folder="static",template_folder='templates')
f=open('./static/index.html', 'rb')#读取html页面文件
html = f.read()#加载html页，
f.close()
app=Flask(__name__)  


@app.route('/newloginrequest',methods=['POST'])    #新登录请求的函数部分 
def newloginre():   

    try:#获得参数
        data =  request.form
        inputad = str(data['AD']) 
        inputsalt = str(data['salt'])
        inputkey = str(data['key'])
        inputcallback = str(data['callback'])
        inputreturn = str(data['return'])
    except KeyError:
        return {"code":"Error","message":"缺失参数！"}
    
    userlist = sql.queries('SELECT * FROM user;')#从MySQL中读取所有用户信息

    if inputad in str(userlist): #如果AD在已知列表
        for i in range(len(userlist)):
            if userlist[i][0] == inputad:
                trueak = userlist[i][1]#获得正确的对应AK
                break
    else:#如果不在
        return {"code":"Error","message":"无效的AD！"}

    daimd5 = inputad+trueak+inputsalt+inputcallback+inputreturn#拼接即将md5的字符串
    truesign = hashlib.md5(daimd5.encode('utf-8')).hexdigest()#MD5

    if truesign == inputkey: #判断用户签名是否正确
        loginid = random.randint(100000000,999999999)#计算随机请求ID
        sql.write(f'INSERT INTO loginre VALUES ({loginid},"peting","{inputcallback}","{inputreturn}");')#将数据存入数据库
        return {#返回
            "code":"OK",
            "AD":inputad,
            "loginurl":'https://api.syrathon.com/codemaologin/login/' + str(loginid),
            "callbackurl":inputcallback,
            "loginid":str(loginid)


        }
    else:
        return {"code":"Error","message":"签名错误！"}

@app.route('/codemaologin/login/<loginid>',methods=['GET'])#用户前端登录接口
def login(loginid):
    loginlog = sql.queries(f'SELECT * FROM loginre WHERE type="peting" AND loginid = {loginid}')#查询id是否已经在数据库
    if loginid in str(loginlog):
        return html
    else:
        return "没有这个登录请求"

@app.route('/codemaologin/post/<loginid>',methods=['POST'])#用户登录接口
def postlogin(loginid):
    loginlog = sql.queries(f'SELECT * FROM loginre WHERE type="peting" AND loginid = {loginid}')#查找登录请求
    if loginid in str(loginlog):#如果是已知登录请求
        data =  request.get_json()#获得参数
        try:
            phone = str(data['phone'])#还是获得参数
            password = str(data['password'])
        except KeyError:
            return {"code":"ERROR","message":"缺失参数"}
        data = sql.queries(f'SELECT * FROM loginre WHERE loginid={loginid} AND type="peting"')#查询到第一个接口输入的回调链接和返回链接
        callback = data[0][2]
        returnurl = data[0][3]
        back = codemao.codemao(phone, password)#尝试登录
        if 'ERROR' in str(back):
            return({"code":"ERROR","message":"用户名或密码错误"})
        else:
            try:
                back.update(loginid=loginid)#回调数据中加入登录ID
                HTTPPOST = requests.post(callback,data=back)#尝试回调
            except OSError:#如果链接超时
                print(callback)#调试用可以注释掉
                return {"code":"ERROR","message":"未能通知回调地址"}
            else:
                if 'OK' == HTTPPOST.text:#如果回调服务器返回正确
                    return({"code":"OK","message":"登录成功，准备跳转","return":returnurl,"loginid":loginid})
                else:
                    print(callback)#调试用可以注释
                    return {"code":"ERROR","message":"未能通知回调地址"}
                    
    else:
            return {"code":"ERROR","message":"无效的登录请求"}
    
@app.route('/test',methods=['POST'])#调试回调用可以直接删除
def test():
    data =  request.form
    print(data)
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True,port=80)              #启动这个应用服务器，并开启debug,才能定位问题
