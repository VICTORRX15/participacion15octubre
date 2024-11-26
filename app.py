from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'clave secreta'  # Clave secreta para manejar sesiones

DATABASE = 'usuarios.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Ruta para la página de inicio de sesión
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Convertir la contraseña en hash para la verificación
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Verificar las credenciales en la base de datos
        db = get_db()
        cursor = db.execute('SELECT * FROM Usuarios WHERE username = ? AND password = ?', (username, password_hash))
        user = cursor.fetchone()
        db.close()

        if user:
            # Almacenar el usuario en la sesión
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('welcome'))
        else:
            flash('Nombre de usuario o contraseña incorrectos')

    return render_template('login.html')

# Ruta para la página de bienvenida
@app.route('/welcome')
def welcome():
    if 'username' in session:
        username = session['username']
        return render_template('welcome.html', username=username)
    else:
        return redirect(url_for('login'))

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.clear()  # Limpiar la sesión
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
