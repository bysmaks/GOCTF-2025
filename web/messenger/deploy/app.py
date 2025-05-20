from flask import Flask, request, redirect, url_for, render_template, make_response, flash, jsonify, render_template_string
from dotenv import load_dotenv
import time
import random
import jwt
import re
import uuid
import logging
import datetime
import mysql.connector
from os import getenv
from markupsafe import Markup
from werkzeug.security import generate_password_hash, check_password_hash

logger = logging.getLogger(__name__)

print('Waiting for MySQL service...')
time.sleep(3)

load_dotenv()

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
JWT_SECRET = app.config['SECRET_KEY']


app.config['SECRET_KEY'] = getenv('SECRET_KEY')
flag = getenv('flag')

logger.info(app.config['SECRET_KEY'], flag)


def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=getenv('MYSQL_HOST'),
            user=getenv('MYSQL_USER'),
            password=getenv('MYSQL_PASSWORD'),
            database=getenv('MYSQL_DATABASE')
        )
    except mysql.connector.Error as e:
        print(f"The error '{e}' occurred")
    return connection

print('MySQL password', getenv('MYSQL_PASSWORD'))
print('Mysql connector:', create_connection())
print(getenv('MYSQL_USER'), getenv('MYSQL_PASSWORD'))

def sanitize_input(input_string):
    forbidden_patterns = [  
        r'eval',
        r'exec',
        r'import',
        r'os',
        r'sys',
        r'subprocess',
        r'\.',            
        r'\_',                        
        r'\[', r'\]',     
        r'mro',           
        r'base',
        r'config',          
    ]

    for pattern in forbidden_patterns:
        input_string = re.sub(pattern, '', input_string, flags=re.IGNORECASE)

    print('Sanitized input: ', input_string)
    return input_string



def jwt_decode(cookie):
    try:
        data = jwt.decode(cookie, app.config['SECRET_KEY'], algorithms=['HS256'])
        return data
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def jwt_encode(data):
    return jwt.encode(data, app.config['SECRET_KEY'], algorithm='HS256')


@app.route('/', methods=['GET'])
def index():
    print(dir(request.application.__globals__.values()))
    cookie = request.cookies.get('token')
    print('user cookie: '+str(cookie))
    if cookie is None or jwt_decode(cookie) is None:
        return redirect(url_for('login'))
    user = jwt_decode(cookie)['user_id']
    if type(user) == list:
        user = user[0]
    print(user)
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username FROM users WHERE user_id = %s', (user,))
    response = cursor.fetchone()
    print(response)

    if response is None:
        return redirect(url_for('login'))
    elif response[1] == 'admin':
        return flag

    return render_template('messenger.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    cookie = request.cookies.get('token')
    if cookie is not None and jwt_decode(cookie) is not None:
        return redirect('/')

    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        conn.close()

        if user is None or not check_password_hash(user[3], password):
            flash('Неверное имя пользователя или пароль')
            return redirect(url_for('login'))

        token = jwt_encode({'user_id': user[1], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)})
        response = make_response(redirect(url_for('index')))
        response.set_cookie('token', token)
        return response


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    cookie = request.cookies.get('token')
    if cookie is not None and jwt_decode(cookie) is not None:
        return redirect('/')
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Пароли не совпадают')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, user_id, password) VALUES (%s, %s, %s)', (username, str(uuid.uuid4()), hashed_password))
            conn.commit()
            cursor.execute('SELECT user_id FROM users WHERE username = %s', (username,))
            user_id = cursor.fetchone()
            print(user_id[0])
        except mysql.connector.IntegrityError:
            flash('Имя пользователя уже существует')
            return redirect(url_for('signup'))
        finally:
            conn.close()

        token = jwt_encode({'user_id': user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)})
        response = make_response(redirect(url_for('index')))
        response.set_cookie('token', token)
        return response

@app.route('/logout', methods=['GET'])
def logout():
    cookie = request.cookies.get('token')

    if cookie is None or jwt_decode(cookie) is None:
        return redirect('/login')

    response = make_response(redirect('/login'))
    response.set_cookie('token', '', expires=0)
    return response


@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        message = sanitize_input(data.get('message'))
        response = Markup(render_template_string(message)).unescape()
        print(response)
        time.sleep(random.randint(1, 4))
        return jsonify({'status': 'success', 'message': response})
    except Exception as e:
        raise e
        print(e)
        time.sleep(random.randint(1, 4))
        return jsonify({'status': 'error', 'message': 'Ошибка'})


@app.route('/user_search', methods=['GET'])
def user_search():
    q = request.args.get('q', '')
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM users WHERE username LIKE %s', (f"{q}%",))
    response = cursor.fetchall()
    return jsonify({'users': [x[0] for x in response]})




if __name__ == '__main__':
    app.run(port=8080)


