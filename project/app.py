#encoding:utf-8
import flask
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from models import User
import pymysql

app = Flask(__name__)



def root_MHC(root):
    db = pymysql.connect(user='root', password='root', host='127.0.0.1', database='demo', port=3306)
    cursor = db.cursor()
    sql = """select peptide from second_version where MHC = '{}'
        """.format(root)
    cursor.execute(sql)
    ret = cursor.fetchall()
    i = 0
    array1 = []
    array2 = []
    array3 = []
    array4 = []
    array5 = []
    # 元组转化为列表
    while i < len(ret):
        array1.append(ret[i][0])
        sql = """select CDR3 from second_version where peptide = '{}'""".format(array1[i])
        cursor.execute(sql)
        ret1 = cursor.fetchall()
        ret1 = list(ret1[0])
        array2.append(ret1)
        i = i + 1
    i = 0
    j = 0
    while i < len(array2):
        array3.append([])
        while j < len(array2[i]):
            sql = """select disease from second_version where CDR3 = '{}'""".format(array2[i][j])
            cursor.execute(sql)
            ret2 = cursor.fetchall()
            ret2 = list(ret2[0])
            array3[i].append(ret2)
            j = j + 1
        i = i + 1
        j = 0
    cursor.close()
    db.close()
    return array1,array2,array3


@app.route('/',methods=['GET','POST'])
def index():
    array1 = ['GILGFVFTL', 'EAAGIGILTV', 'EAAGIGILTV', 'EAAGIGILTV']
    array2 = []
    array3 = []
    array4 = []
    array5 = []
    root = 'HLA-A*02'
    array1, array2, array3 = root_MHC(root)


    if flask.request.method == "POST":
        if flask.request.values.get("tag1") != None:
            root = flask.request.values.get("tag1")
            array1, array2,array3 = root_MHC(root)






    return render_template('index.html',root=root,array1=array1,array2=array2,array3=array3)


@app.route('/browse')
def browse():
    return render_template('browse.html')



@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/download')
def download():
    return render_template('download.html')



@app.route('/overview')
def overview():
    return render_template('overview.html')



@app.route('/submit')
def submit():
    return render_template('submit.html')


@app.route('/about')
def about():
    return render_template('about.html')


#登录页面
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')

        user = User.query.filter(User.telephone == telephone, User.password == password).first()
        if user:
            session['user_id'] = user.id
            #如果想再31天内都不需要登录
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'手机号或密码错误，请确认后再登录'

#注册页面
@app.route('/register/',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #手机号码验证，如果被注册了就不能再注册了
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u"该手机号码已被注册,请更换手机号"
        else:
            #password1 是否与password2相等
            if password1 != password2:
                return u'两次密码不一致，请核对后再填写'
            else:
                user = User(telephone=telephone, username=username, password=password1)
                db.session.add(user)
                db.session.commit()
                #如果注册成功，页面跳转到登录界面
                return redirect(url_for('login'))



@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))



@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {}



if __name__ == '__main__':
    app.run(host='127.0.0.1',port='5000',debug=True)
