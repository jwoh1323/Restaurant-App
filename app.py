from flask import Flask, render_template, url_for, flash, redirect, request,jsonify
from forms import *
import forms
import pandas as pd
import uuid
import log_in_check as check
import pymysql
from QueryEngine import QueryEngine
from flask_mail import Mail, Message
from random2 import randint
from datetime import datetime


qe = QueryEngine()
qe.setup_default()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a26ade032e7040309ba635818774a38b'
app.config['JAWSDB_URL'] = 'mysql://zp7gk8hwnxf8pr7r:zkwvjqtasu7wl5ir@ctgplw90pifdso61.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/vrjw534e3pgu7qdo'



mail= Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "uhdatabase2019@gmail.com"
app.config['MAIL_PASSWORD'] = "coscspring2019"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


#check transaction ID
global transaction_id





@app.route("/",methods=['GET', 'POST'])
@app.route("/home",methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route("/contact",methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

@app.route("/menu",methods=['GET', 'POST'])
def menu():
    global transaction_id
    transaction_id = randint(10, 99999999)
    return render_template('menu.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.user.data
        password = form.password.data
        if check.login_check(username, password) == True:
            return redirect(url_for('manager_view'))
        else:
            flash('Invalid Account, Check Your Username and Password', 'danger')
    return render_template('login.html',form=form)


@app.route("/manager_view", methods=['GET', 'POST'])
def manager_view():
    return render_template('manager_view.html')


@app.route("/survey", methods=['GET','POST'])
def survey():
    form = SurveyForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        sex = form.sex.data
        ethnicity = form.ethnicity.data
        age = form.age.data
        zipcode = form.zipcode.data
        return redirect(url_for('update_survey_data',transaction_id=transaction_id,first_name=first_name,sex=sex,ethnicity=ethnicity,age=age,zipcode=zipcode))
    return render_template('survey.html',form=form)


@app.route("/update_survey_data/<transaction_id>/<sex>/<ethnicity>/<age>/<zipcode>/<first_name>",methods=['GET','POST'])
def update_survey_data(transaction_id,sex,ethnicity,age,zipcode,first_name):
    qe.connect()
    query_string = f"INSERT INTO Survey VALUES({transaction_id},'{sex}','{ethnicity}',{age},{zipcode},'{first_name}');"
    qe.do_query(query_string)
    qe.commit()
    qe.disconnect()
    return redirect(url_for('home'))



@app.route("/cart", methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        response = request.get_json(force=True)  # parse as JSON
        keys = list(response.keys())
        order_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for i in range(len(keys)):
            food_id = keys[i]
            food_name = response[food_id][0]
            quantity = response[food_id][1]
            qe.connect()
            query_string = f"INSERT INTO Transaction VALUES({transaction_id},{food_id},'{food_name}',{quantity},'{order_time}');"
            qe.do_query(query_string)
            qe.commit()
            qe.disconnect()
    else:
        return redirect(url_for('survey'))

if __name__ == '__main__':
    app.run()





