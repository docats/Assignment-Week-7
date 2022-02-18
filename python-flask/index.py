import pymysql #匯入資料庫模組
from distutils.log import debug
from os import name
from flask import Flask # 載入Flask 
from flask import request # 載入Request物件(要取得POST參數值)
from flask import redirect # 載入redirect函式
from flask import render_template # 使用樣板引擎
from flask import session # 使用session
from flask import jsonify # 使用jsonify

#嘗試連接到資料庫
mydb = pymysql.connect(
    host="localhost",
    user="root",
    password="root123",
    database="mydatabase",
    charset='utf8'
)

print("資料庫訊息:",mydb)
# mydb.close() #關閉資料庫

# 建立 Application物件，可以設定靜態檔案的路徑處理
# 所有在 static 資料夾底下的檔案，都對應到網址路徑 /static/ 檔案名稱
app=Flask(
    __name__,
    static_folder="static", # 靜態檔案的資料夾名稱
    static_url_path="/static" #靜態檔案對應的網址路徑
    ) 

#不讓中文呈現亂碼
app.config["JSON_AS_ASCII"] = False


# 使用 Session密鑰
app.secret_key = "any string but secret" 


# 建立路徑 / 對應的處理函式
@app.route('/')
def index(): #用來回應路徑 / 的處理函式
    
    return render_template('index.html') # 回傳網站首頁內容

#建立路徑 /signin對應的處理函式
@app.route("/signin",methods=['POST'])
def signin():
    username = request.form['uname']
    password = request.form['psw']
    if username=="" or password=="":
        return redirect('/empty/?message=帳號或密碼不能為空')
    with mydb.cursor() as cursor:
        got=cursor.execute("SELECT * FROM member WHERE username=%s",(username,))
        result=cursor.fetchone() #我只需要讀取一筆紀錄
        # print("result:",result[3])
        mydb.commit() #確定要更新資料庫
        if got == 0:
            return redirect("error/?message=帳號或密碼錯誤")
        elif got == 1:
            if password == result[3]: #result[3]是資料庫裡的password
                session['username']=[username,result[1]] #result[1]是資料庫裡的name
                return redirect("/member")
            else:
                return redirect("error/?message=帳號或密碼錯誤")
        else:
            return redirect("error/?message=全部都錯")
# mydb.close() #關閉資料庫 

#建立路徑 /signup對應的處理函式，獲取註冊請求及處理
@app.route("/signup",methods=['POST'])
def signup():
    name = request.form['nickname'] #取得表格輸入的姓名
    username = request.form['new_ac'] #取得表格輸入的新帳號
    password = request.form['new_psw'] #取得表格輸入的新密碼
    with mydb.cursor() as cursor: #使用cursor方法新增cursor物件來執行mydb是連線物件
        got=cursor.execute("SELECT username FROM member where username=%s",(username,))
        mydb.commit() #確定要更新資料庫
    # result = mycursor.fetchall()
    if got!=0:
       return redirect("/error/?message=帳號已經被註冊")    
    else:
        with mydb.cursor() as cursor:
            result = cursor.execute("INSERT INTO member (name,username,password) VALUES (%s,%s,%s)",
                (name,username,password))
            mydb.commit() #確定要更新資料庫
            print("新增",result,"筆，恭喜記錄成功")
            return redirect("/")
# mydb.close() #關閉資料庫 

# 建立路徑 /member對應的處理函式
@app.route("/member/",methods=['GET'])
def member():
    if session.get("username"):
        # username=request.args.get("username","大豆貓")
        # username=session["username"] #session把資料放到username，取得名字
        return  render_template('member.html',username=session['username'][1]+"恭喜您，成功登入系統")
    else:
        return redirect("/signout")

#後端建立查詢會員資料的 API
@app.route("/api/members",methods=["GET"])
def api():
    username=request.args.get("username")
    with mydb.cursor() as cursor:
        got = cursor.execute("SELECT * FROM member WHERE username=%s",(username,))
        result=cursor.fetchone() #我只需要讀取一筆紀錄
        mydb.commit()
    if got!=0:
        # id=result["id"]
        # name=result["name"]
        # user_name=result["username"]
        id=result[0]
        name=result[1]
        user_name=result[2]
        allData={"id":id,"name":name,"username":user_name}
        print("allData:",type(allData))
        return jsonify(allData)
    else:
        return jsonify({"data":None})

# 建立路徑 /error對應的處理函式
@app.route("/error/",methods=['GET'])
def error():
    message=request.args.get("message")
    return render_template('error.html',message=message)

# 建立路徑 /empty對應的處理函式
@app.route("/empty/",methods=['GET'])
def empty():
    message=request.args.get("message")
    return render_template('empty.html',message=message)

#建立路徑 /signout對應的處理函式
@app.route("/signout",methods=['GET'])
def signout():
     session.pop("username"," ") #登出使用pop()方法把session紀錄刪除
     return redirect("/")
  

# (啟動網站伺服器)host,port,debug等參數，要在這邊設定
app.run(port=3000,debug='true') 

