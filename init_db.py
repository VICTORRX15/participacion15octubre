import sqlite3
import hashlib

def create_database():
    # Conexión a la base de datos
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    # Crear la tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Insertar un usuario de ejemplo (usuario: admin, contraseña: password)
    # La contraseña se almacena en formato hash
    username = "admin"
    password = hashlib.sha256("password".encode()).hexdigest()
    try:
        cursor.execute('INSERT INTO Usuarios (username, password) VALUES (?, ?)', (username, password))
    except sqlite3.IntegrityError:
        print("El usuario ya existe en la base de datos")

    # Guardar cambios y cerrar la conexión
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
    print("Base de datos creada y usuario inicial agregado.")
