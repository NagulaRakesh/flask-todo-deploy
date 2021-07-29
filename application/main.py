import psycopg2
import random

from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash

from werkzeug.security import check_password_hash, generate_password_hash

from flask import g

from . import db

bp = Blueprint("edit", __name__, url_prefix="/")

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = db.get_db()
        cursor = conn.cursor()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            
            try:
                cursor.execute('INSERT INTO user_details (username, password) VALUES (%s, %s)',(username,                     generate_password_hash(password)))
                conn.commit()
            except:
                error = f"User {username} is already registered."
    
            else:
                return redirect(url_for('edit.login'))
   
        flash(error)

    return render_template('main/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = db.get_db()
        cursor = conn.cursor()
        error = None

        user = cursor.execute('SELECT * FROM user_details WHERE username = (%s)',(username,))
        user = cursor.fetchone()
        conn.commit()
        if user is None:
            error = "Username doesn't exists"
        elif check_password_hash(user[2], password) is not True:
            error = 'Incorrect password.'

        if error is None:
            return redirect(url_for('edit.home', username = username))

        flash(error)
    return render_template('main/login.html')  

@bp.route('/<username>/home', methods = ('GET','POST'))
def home(username):
    
    quotes = [ "Better three hours too soon than a minute too late", "Better never than Late", "You may as well borrow a person's money as his time.", "Punctuality is the first step towards success."]
    quote = random.choice(quotes)
    conn = db.get_db()
    cursor = conn.cursor()   
     
    if request.method == 'GET':    
        todos = cursor.execute(f"select * from todo_list where username = %s order by user_id", (username,))
        todos = cursor.fetchall() 
        conn.commit()
        return render_template('main/todo/home.html', todos = todos, username = username, quote = quote)
        
    elif request.method == 'POST':
        user_id = request.args.get("user_id")
        cursor.execute("update todo_list set progress = %s where username = %s and user_id = %s;", ('Done', username, user_id))
        conn.commit()
        return redirect(url_for('edit.home', username = username))
   
@bp.route('/<username>/add_task', methods =('GET','POST'))
def add_task(username):
    if request.method == 'POST':
        task = request.form['task']
        due_date = request.form['due_date']
        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute(f"SELECT MAX(user_id) from todo_list where username = %s", (username,))
        user_id = cursor.fetchone()[0]
        conn.commit()
        if user_id is None:
            user_id = 1
        else:
            user_id = user_id +1    
        cursor.execute('INSERT INTO todo_list (username, task, due_date, progress, user_id) values (%s, %s, %s, %s, %s)',(username, task, due_date, 'In progress', user_id))
        conn.commit()
        return redirect(url_for('edit.home', username = username))

    return render_template('main/todo/add_task.html')     

@bp.route('/login')
def logout():
    return render_template('main/login.html') 
    
if __name__=="__main__":
    app.run(debug=True)    
