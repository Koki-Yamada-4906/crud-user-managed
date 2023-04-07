import mysql.connector as mydb
from flask import Flask, request, render_template
from connect_db import conn_db

app = Flask(__name__)

@app.route("/get_users", methods=["GET"])
def get_users():
    sql = 'SELECT * FROM users'
    result = {}
    try:
        conn = conn_db()  # ここでDBに接続
        cursor = conn.cursor(dictionary=True)  # カーソルを取得
        cursor.execute(sql)  # selectを投げる
        rows = cursor.fetchall()  # selectの結果を全件タプルに格納
        print(rows)
        result['users'] = rows
        result['message'] = 'OK'
    except Exception as e:
        result['message'] = 'NG'
        result['error'] = str(e)
    return result

@app.route("/delete/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    result = {}
    sql = "DELETE FROM users WHERE id = %s"
    try:
        conn = conn_db()  # ここでDBに接続
        cursor = conn.cursor(dictionary=True)  # カーソルを取得
        cursor.execute(sql, (user_id,))  # selectを投げる
        conn.commit()        
        result['message'] = 'OK'
    except Exception as e:
        result['message'] = 'NG'
        result['error'] = str(e)
    return result

@app.route("/add", methods=["POST"])
def add_user():
    sql = "INSERT INTO users (name, email, phone) VALUES (%s, %s, %s)"
    result = {}
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    try:
        conn = conn_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (name, email, phone))  # selectを投げる
        conn.commit()
        result['message'] = 'OK'
    except Exception as e:
        result['message'] = 'NG'
        result['error'] = str(e)
    return result

@app.route("/update/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    sql = "UPDATE users SET name=%s, email=%s, phone=%s WHERE id=%s"
    result = {}
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    try:
        conn = conn_db()  # ここでDBに接続
        cursor = conn.cursor(dictionary=True)  # カーソルを取得
        cursor.execute(sql, (name, email, phone, user_id))  # selectを投げる
        conn.commit()        
        result['message'] = 'OK'
    except Exception as e:
        result['message'] = 'NG'
        result['error'] = str(e)
    return result

@app.route('/users/<user_id>', methods=["GET"])
def get_user(user_id):
    '''
    ユーザ情報の取得
    '''
    sql = 'SELECT * FROM users where id = %s'
    result = {}
    try:
        conn = conn_db()  # ここでDBに接続
        cursor = conn.cursor(dictionary=True)  # カーソルを取得
        cursor.execute(sql, (user_id,))  # selectを投げる
        row = cursor.fetchone()  # selectの結果を一件取得
        result['user'] = row
        result['message'] = 'OK'
    except Exception as e:
        result['message'] = 'NG'
        result['error'] = str(e)
    return render_template('update_user.html', result=result)
            




@app.route('/')
def index():
    users = get_users()['users']
    return render_template('index.html', users=users)

@app.route("/add_user")
def add():
    return render_template("add_user.html")


    
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
