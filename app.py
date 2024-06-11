from flask import Flask
from flask import render_template, redirect, request, Response, session
from flask_mysqldb import MySQL, MySQLdb
from functools import wraps
from flask import url_for
from functools import wraps


app = Flask(__name__,template_folder='templates')

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='123456'
app.config['MYSQL_DB']='MAESTRANZAS'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql= MySQL(app)


def login_required(role_id):
    def wrapper(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if 'loggedin' not in session or session['role_id'] != role_id:
                return redirect('/')
            return func(*args, **kwargs)
        return decorated_function
    return wrapper

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/admin',  methods=["GET", "POST"])
@login_required(role_id=1)
def admin():
    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id, username, first_name, last_name, run, password, role_id FROM users")
    usuarios = cur.fetchall()
    cur.close()
    user_data = session['user_data']
    return render_template('admin.html', user_data=user_data, usuarios=usuarios)


@app.route('/visor')
@login_required(role_id=3)
def visor():
    session['user_data'] = session.get('user_data') or {}
    return redirect(url_for('inventario', role='visor'))

@app.route('/editor')
@login_required(role_id=2)
def editor():
    session['user_data'] = session.get('user_data') or {}
    return redirect(url_for('inventario', role='editor'))

@app.route('/inventario/<role>')
def inventario(role):
    user_data = session.get('user_data')
    return render_template('inventario.html', role=role, user_data=user_data)


@app.route('/access-login', methods=["GET", "POST"])
def login():

    if request.method == "POST" and 'inputUsername' in request.form and 'inputPassword' in request.form:
        username = request.form['inputUsername']
        password = request.form['inputPassword']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        account = cur.fetchone()

        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            session['first_name'] = account['first_name']
            session['last_name'] = account['last_name']
            session['run'] = account['run']
            session['role_id'] = account['role_id']
            session['user_data'] = account

            if session['role_id'] == 1:
                return redirect('/admin')
            
            elif session['role_id'] == 2:
                return redirect('/editor')
            
            elif session['role_id'] == 3:
                return redirect('/visor')
        else:
            return render_template('login.html', mensaje="Usuario o contraseña incorrecta")

    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

def generate_username(first_name, last_name):
    return f"{first_name.lower()}.{last_name.lower()}"

def generate_password():
    import string
    import random

    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(8))  # Genera una contraseña de 8 caracteres
    return password

@app.route('/add_user', methods=["POST"])
@login_required(role_id=1) 
def add_user():
    if request.method == "POST":
        username = generate_username(request.form['first_name'], request.form['last_name'])
        password = generate_password()
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        run = request.form['run']
        role_id = request.form['role_id']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, first_name, last_name, run, password, role_id) VALUES (%s, %s, %s, %s, %s, %s)",
                    (username, first_name, last_name, run, password, role_id))
        mysql.connection.commit()
        cur.close()

        return redirect('/admin')  


@app.route('/add_product')
@login_required(role_id=2) 
def add_product():
    return render_template('addProduct.html')


# EDITAR Y ELIMINAR USUARIOS POR PARTE DEL ADMIn
@app.route('/edit_user/<int:user_id>', methods=["POST"])
@login_required(role_id=1)  
def edit_user(user_id):
    if request.method == "POST":
        username = request.form['editUsername']
        first_name = request.form['editFirstName']
        last_name = request.form['editLastName']
        run = request.form['editRun']
        id_role = request.form['editIdRole']


        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET username = %s, first_name = %s, last_name = %s, run = %s, role_id = %s WHERE user_id = %s",
                    (username, first_name, last_name, run, id_role, user_id))
       

        mysql.connection.commit()
        cur.close()

        return redirect('/admin') 


@app.route('/delete_user/<int:user_id>', methods=["POST"])
@login_required(role_id=1)  
def delete_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/admin')

if __name__ == '__main__':
    app.secret_key = "whatever"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)