from flask import Flask, render_template, url_for, flash, redirect, request
from forms import *
import forms
import pandas as pd
import uuid
import log_in_check
import pymysql
from QueryEngine import QueryEngine
from flask_mail import Mail, Message


qe = QueryEngine()
qe.setup_default()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a26ade032e7040309ba635818774a38b'


mail= Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "uhdatabase2019@gmail.com"
app.config['MAIL_PASSWORD'] = "coscspring2019"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)




@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/menu")
def menu():
    return render_template('menu.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.user.data
        password = form.password.data
        if log_in_check.login_check(username, password) == True:
            return redirect(url_for('manager_view'))
        else:
            flash('Invalid Account, Check Your Username and Password', 'danger')
    return render_template('login.html',form=form)


@app.route("/manager_view", methods=['GET', 'POST'])
def manager_view():
    return render_template('manager_view.html')


if __name__ == '__main__':
    app.run(debug=True)