from flask import Flask
from flask import render_template, redirect, url_for,request, Response, session, flash, g
from flask_mysqldb import MySQL, MySQLdb
from config import config
from functools import wraps


app = Flask(__name__,template_folder='templates')

db= MySQL(app)

'''
def login_required(role_id):
    def wrapper(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if 'loggedin' not in session or session['role_id'] != role_id:
                return redirect('/')
            return func(*args, **kwargs)
        return decorated_function
    return wrapper
'''
@app.before_request
def before_request():
    # La función get_logged_in_user() obtiene el usuario actual de la sesión
    g.user = get_logged_in_user()

def get_logged_in_user():
    user_id = session.get('user_id')
    if user_id:
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
        user = cur.fetchone()
        cur.close()
        return user
    return None

@app.route('/')
def index():
    return render_template('login.html')
'''
@app.route('/admin',  methods=["GET", "POST"])
@login_required(role_id=1)
def admin():
    session['user_data'] = session.get('user_data') or {}
    return redirect(url_for('inventario', role='admin'))

@app.route('/visor')
#@login_required(role_id=3)
def visor():
    session['user_data'] = session.get('user_data') or {}
    return redirect(url_for('home', role='visor'))

@app.route('/editor')
#@login_required(role_id=2)
def editor():
    session['user_data'] = session.get('user_data') or {}
    return redirect(url_for('inventario', role='editor'))'''

@app.route('/access-login', methods=["GET", "POST"])
def login():

    if request.method == "POST" and 'inputUsername' in request.form and 'inputPassword' in request.form:
        username = request.form['inputUsername']
        password = request.form['inputPassword']

        cur = db.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        account = cur.fetchone()

        if account:
            session['loggedin'] = True
            session['user_id'] = account['user_id']
            session['role_id'] = account['role_id']
            session['first_name'] = account['first_name']
            session['last_name'] = account['last_name']
            session['username'] = account['username']

            if session['role_id'] == 1:
                return redirect(url_for('show_prod'))
            
            elif session['role_id'] == 2:
                return redirect(url_for('show_prod'))
            
            elif session['role_id'] == 3:
                return redirect(url_for('home'))
        else:
            return render_template('login.html', mensaje="Usuario o contraseña incorrecta")
    return redirect('/')

#cerrar sesion
'''@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')'''
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html', first_name=session['first_name'])
    else:
        return redirect(url_for('login'))

@app.route('/registro')
def registro():
    if 'username' in session:
        return render_template('register.html', first_name=session['first_name'])
    else:
        return redirect(url_for('login'))

@app.route('/inventario')
def show_prod():
    if 'username' in session:
        sort_by = request.args.get('sort_by')
        if sort_by:
            if sort_by == 'nombre':
                order_by_clause = 'ORDER BY nombre'
            elif sort_by == 'descripcion':
                order_by_clause = 'ORDER BY descripcion'
            elif sort_by == 'ubicacion':
                order_by_clause = 'ORDER BY ubicacion'
            elif sort_by == 'cantidad':
                order_by_clause = 'ORDER BY cantidad'
            elif sort_by == 'categoria':
                order_by_clause = 'ORDER BY categoria'

            # Realiza la consulta a la base de datos para obtener los productos ordenados
            cur = db.connection.cursor()
            cur.execute(f'''SELECT p.*, c.cat_name AS categoria_nombre
                    FROM products p
                    LEFT JOIN categories c ON p.category = c.cat_id {order_by_clause}''')
            productos = cur.fetchall()
            cur.close()
            return render_template('inventario.html', first_name=session['first_name'],productos=productos)

        
        cur = db.connection.cursor()
        cur.execute('''SELECT p.*, c.cat_name AS categoria_nombre
        FROM products p
        LEFT JOIN categories c ON p.category = c.cat_id''')
        productos = cur.fetchall()
        cur.close()
        return render_template('inventario.html', first_name=session['first_name'],productos=productos)
    else:
        return redirect(url_for('login'))

@app.route('/modifications')
def show_modifications():
    if 'username' in session:
        sort_by = request.args.get('sort_by')
        if sort_by:
            if sort_by == 'first_name':
                order_by = 'ORDER BY first_name'
            elif sort_by == 'producto':
                order_by = 'ORDER BY producto_nombre'
            elif sort_by == 'id':
                order_by = 'ORDER BY id'
            elif sort_by == 'id_prod':
                order_by = 'ORDER BY id_producto'
            elif sort_by == 'fecha':
                order_by = 'ORDER BY time_date DESC'
        else:
            order_by = 'ORDER BY time_date DESC'
        
        cur = db.connection.cursor()
        cur.execute(f'''SELECT m.*, p.name_prod as producto_nombre, p.prod_id as id_producto
                    FROM modifications m JOIN products p 
                    ON p.prod_id = m.id_prod {order_by}''')
        modificaciones = cur.fetchall()
        cur.close()
        return render_template('modifications.html', first_name=session['first_name'],modificaciones=modificaciones)
    else:
        return redirect(url_for('login'))

#MOSTRAR PROVEEDORES
@app.route('/supplier')
def show_supplier():
    if 'username' in session:
        '''sort_by = request.args.get('sort_by')
        if sort_by:
            if sort_by == 'first_name':
                order_by = 'ORDER BY first_name'
            elif sort_by == 'producto':
                order_by = 'ORDER BY producto_nombre'
            elif sort_by == 'id':
                order_by = 'ORDER BY id'
            elif sort_by == 'nro_serie':
                order_by = 'ORDER BY nro_serie'
            elif sort_by == 'fecha':
                order_by = 'ORDER BY fecha_hora DESC'
        else:
            order_by = 'ORDER BY fecha_hora DESC'''
        
        cur = db.connection.cursor()
        cur.execute(f'''SELECT * 
                    FROM supplier''')
        proveedores = cur.fetchall()
        cur.close()
        return render_template('supplier.html', first_name=session['first_name'],proveedores=proveedores)
    else:
        return redirect(url_for('login'))

#Generar contraseña
def generate_password():
    import string
    import random

    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(8))  # Genera una contraseña de 8 caracteres
    return password

#Mostrar usuarios
@app.route('/users', methods=["GET", "POST"])
def show_users():

    if 'username' in session:
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM users')
        usuarios = cur.fetchall()
        cur.close()
        return render_template('users.html', first_name=session['first_name'],usuarios=usuarios)
    else:
        return redirect(url_for('login'))


#Registro usuarios
@app.route('/add_user', methods=["POST"])
#@login_required(role_id=1) 
def add_user():
    if request.method == "POST":
        if request.method == 'POST':
            if 'id_rol' not in request.form:
                flash('El campo "Rol" es obligatorio.', 'danger')
                return render_template('register.html')
            
            role_id = request.form['id_rol']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            run = request.form['run']

            # Verificar si se han dejado campos en blanco
            if not first_name or not last_name or not run:
                flash('Por favor, completa todos los campos.', 'danger')
                return render_template('register.html')
            try:
                rut = format_rut(run)
            except ValueError as e:
                flash(str(e))
                return redirect(url_for('registro'))
        
            password = generate_password()

            #Creacion del nombre de usuario con 3 primeras letras del nombre y apellido completo
            username = f"{first_name[:3].lower()}.{last_name.lower()}"
            
            cur = db.connection.cursor()
            cur.execute('INSERT INTO users(role_id, username, password, first_name, last_name, run) VALUES(%s,%s,%s,%s,%s,%s)',
                        (role_id,username,password,first_name, last_name, rut))
            db.connection.commit()
            cur.close()

            flash('Usuario creado!', 'success')
            return render_template('register.html')
        return render_template('register.html')

#Agregar producto
@app.route('/add_product')
#@login_required(role_id=2) 
def add_product():
    if request.method == 'POST':
            if 'addCategory' not in request.form:
                flash('Seleccione opcion en el campo "Categoria".', 'danger')
                return redirect(url_for('show_prod'))

            name = request.form['addName']
            desc = request.form['addDesc']
            price = request.form['addprice']
            supplier = request.form['addSupplier']
            stock = request.form['addStock']
            category = request.form['addCategory']
            img = request.form['addImg']

            # Verificar si se han dejado campos en blanco
            if not name or not desc or not precio or not supplier or not stock:
                flash('Por favor, completa todos los campos.', 'danger')
                return redirect(url_for('show_prod'))

            
            cur = db.connection.cursor()
            cur.execute('INSERT INTO products(name_prod, desc_prod, price, supplier, category, stock, img) VALUES(%s,%s,%s,%s,%s,%s,%s)',
                        (name,desc,price,supplier,stock, category, img))
            db.connection.commit()
            cur.close()

            flash('Producto agregado!')
            return redirect(url_for('show_prod'))
        
    return redirect(url_for('show_prod'))

#Editar producto
@app.route('/edit_product')
#@login_required(role_id=2) 
def edit_product(id):

            name = request.form['editName']
            desc = request.form['editDesc']
            price = request.form['editPrice']
            supplier = request.form['editSupplier']
            category = request.form['editCategory']
            stock = request.form['editStock']
            img = request.form['editImg']
  
            
            #Obtiene usuario actual
            user_id = session['id']
            first_name = session['first_name']
            last_name = session['last_name']

            #Actualizar productos
            cur = db.connection.cursor()
            cur.execute('UPDATE products SET name_prod = %s, desc_prod = %s, price = %s, supplier = %s, category = %s,stock = %s, img = %s WHERE id = %s',
                    (name, desc, price, supplier, category, stock, img, id))
            db.connection.commit()
            cur.close()

            #Insertar datos en la tabla modificaciones
            cur = db.connection.cursor()
            cur.execute('INSERT INTO modifications (id_prod, id_user, first_name, last_name) VALUES(%s,%s,%s,%s)', 
                        (id, user_id, first_name,last_name))
            db.connection.commit()
            cur.close()

            flash('Producto Modificado!')
            return redirect(url_for('show_prod'))

#Formato del rut
def format_rut(run):
    rut_str = str(run)

    # Valida que el RUT tenga entre 8 y 9 caracteres numéricos
    if not rut_str.isdigit() or not (8 <= len(rut_str) <= 9):
        raise ValueError("El RUT debe ser numérico y tener entre 8 y 9 dígitos")

    # Formatear RUT
    formatted_rut = f"{rut_str[:-7]}.{rut_str[-7:-4]}.{rut_str[-4:-1]}-{rut_str[-1]}"
    return formatted_rut

# EDITAR USUARIOS POR PARTE DEL ADMIN
@app.route('/edit_user/<int:user_id>', methods=["POST"])
#@login_required(role_id=1)  
def edit_user(user_id):
    if request.method == "POST":
        id_rol = request.form['editIdRol']
        username = request.form['editUsername']
        first_name = request.form['editName']
        last_name = request.form['editLastName']
        run = request.form['editRut']

        try:
            rut = format_rut(run)
        except ValueError as e:
            flash(str(e))
            return redirect(url_for('show_users'))

        #Generar nueva contraseña
        generate_password_flag = request.form.get('generatePassword')
        if generate_password_flag:
            password = generate_password()
            cur = db.connection.cursor()
            cur.execute('UPDATE users SET role_id = %s, username = %s, first_name = %s, last_name = %s, run = %s, password = %s WHERE user_id = %s',
                    (id_rol, username, first_name, last_name, run, password, user_id))
        else:
            cur = db.connection.cursor()
            cur.execute('UPDATE users SET role_id = %s, username = %s, first_name = %s, last_name = %s, run = %s WHERE user_id = %s',
                (id_rol, username, first_name, last_name, rut, user_id))
            
        db.connection.commit()
        cur.close()

        flash(f'Usuario {first_name} Modificado!')
        return redirect(url_for('show_users'))

# ELIMINAR USUARIOS POR PARTE DEL ADMIN
@app.route('/delete_user/<int:user_id>', methods=["POST"])
#@login_required(role_id=1)  
def delete_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/users')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()
