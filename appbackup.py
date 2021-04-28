from flask import Flask
from flask import request, render_template, redirect, url_for, session, g
from dataclasses import dataclass
from datetime import timedelta

app= Flask(__name__,static_url_path="/")
app.config['SECRET_KEY'] = "sdfklas5fa2k42j"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

from SportRec_v2 import Model
rf=Model()

@dataclass
class User:
    id: int
    user_id: int
    username: str
    password: str

users = [
	User(1, 11111116,"Admin", "123456"),
	User(2, 222,"Eason", "888888"),
	User(3, 333,"Tommy", "666666"),
]

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = [u for u in users if u.id == session['user_id']][0] #todo 替换成数据库
        g.user = user

#路由主页
@app.route("/")
def homepage():           
    return render_template("homepage.html")

#路由运动推荐，目前需要登录才能使用
@app.route("/workoutrec")
def workoutRec():       
    if not g.user:
        return redirect(url_for('login'))    
    return render_template("workoutrec.html")

@app.route("/sportrec_model",methods=['GET', 'POST'])
def sportrec_model():
    rf.load_data_from_path('./testdata.csv')
    rf.load_model_from_path('./model_run.m', './model_bike.m', './model_mountain.m')
    calories=request.form.get("calories") 
    
    data=rf.predict_data(11111116, calories)
    print(data)
    return render_template("workoutrec.html",result=calories)
    
#路由饮食推荐
@app.route("/dietrec")
def mealRec():          
    return render_template("dietrec.html")

#路由运动记录    
@app.route("/activitylog")
def activitylog():        
    return render_template("activitylog.html")

#路由用户登录后显示的页面
@app.route("/profile")
def profile():        
    return render_template("profile.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('profile'))

    if request.method == 'POST':
        # login
        session.pop('user_id', None)
        username = request.form.get("username", None)
        password = request.form.get("password", None)
        print(username)
        user = [u for u in users if u.username==username] #todo 替换成数据库
        if len(user) > 0:
            user = user[0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('workoutRec'))
        
    return render_template("sign.html")