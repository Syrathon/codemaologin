from flask import request, Flask, jsonify,render_template
import hashlib
import sql
import random
import codemao
import requests
import re


html = render_template("page.html")
app=Flask(__name__,static_folder="static",template_folder='templates') 

@app.route('/newloginrequest',methods=['POST'])     
def newloginre():   

    try:
        data =  request.form
        inputad = str(data['AD']) 
        inputsalt = str(data['salt'])
        inputkey = str(data['key'])
        inputcallback = str(data['callback'])
        inputreturn = str(data['return'])
    except KeyError:
        return {"code":"Error","message":"缺失参数！"}
    
    userlist = sql.queries('SELECT * FROM user;')

    if inputad in str(userlist):
        for i in range(len(userlist)):
            if userlist[i][0] == inputad:
                trueak = userlist[i][1]
                break
    else:
        return {"code":"Error","message":"无效的AD！"}

    daimd5 = inputad+trueak+inputsalt+inputcallback+inputreturn
    truesign = hashlib.md5(daimd5.encode('utf-8')).hexdigest()

    if truesign == inputkey:
        loginid = random.randint(100000000,999999999)
        sql.write(f'INSERT INTO loginre VALUES ({loginid},"peting","{inputcallback}","{inputreturn}");')
        return {
            "code":"OK",
            "AD":inputad,
            "loginurl":'https://api.syrathon.com/codemaologin/login/' + str(loginid),
            "callbackurl":inputcallback,
            "loginid":str(loginid)


        }
    else:
        return {"code":"Error","message":"签名错误！"}

@app.route('/codemaologin/login/<loginid>',methods=['GET'])
def login(loginid):
    loginlog = sql.queries(f'SELECT * FROM loginre WHERE type="peting" AND loginid = {loginid}')
    if loginid in str(loginlog):
        return html
    else:
        return "没有这个登录请求"

@app.route('/codemaologin/post/<loginid>',methods=['POST'])
def postlogin(loginid):
    loginlog = sql.queries(f'SELECT * FROM loginre WHERE type="peting" AND loginid = {loginid}')
    if loginid in str(loginlog):
        data =  request.get_json()
        try:
            phone = str(data['phone'])
            password = str(data['password'])
        except KeyError:
            return {"code":"ERROR","message":"缺失参数"}
        data = sql.queries(f'SELECT * FROM loginre WHERE loginid={loginid} AND type="peting"')
        callback = data[0][2]
        returnurl = data[0][3]
        back = codemao.codemao(phone, password)
        if 'ERROR' in str(back):
            return({"code":"ERROR","message":"用户名或密码错误"})
        else:
            try:
                back.update(loginid=loginid)
                HTTPPOST = requests.post(callback,data=back)
            except OSError:
                print(callback)
                return {"code":"ERROR","message":"未能通知回调地址"}
            else:
                if 'OK' == HTTPPOST.text:
                    return({"code":"OK","message":"登录成功，准备跳转","return":returnurl})
                else:
                    print(callback)
                    return {"code":"ERROR","message":"未能通知回调地址"}
                    
    else:
            return {"code":"ERROR","message":"无效的登录请求"}
    
@app.route('/test',methods=['POST'])
def test():
    data =  request.form
    print(data)
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True,port=80)              #启动这个应用服务器，并开启debug,才能定位问题
