from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Crear tabla si no existe
def crear_tabla():
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        telefono TEXT,
        correo TEXT
    )
    """)

    conn.commit()
    conn.close()

# Obtener clientes
def obtener_clientes():
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()

    conn.close()
    return clientes


def agregar_cliente(nombre, telefono, correo):
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO clientes (nombre, telefono, correo) VALUES (?, ?, ?)",
        (nombre, telefono, correo)
    )

    conn.commit()
    conn.close()

# Ruta principal
@app.route("/")
def inicio():
    clientes = obtener_clientes()
    return render_template("index.html", clientes=clientes)

# ruta para agregar
@app.route("/agregar", methods=["POST"])
def agregar():
    nombre = request.form["nombre"]
    telefono = request.form["telefono"]
    correo = request.form["correo"]

    agregar_cliente(nombre, telefono, correo)

    return redirect("/")

def eliminar_cliente(id):
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM clientes WHERE id = ?", (id,))

    conn.commit()
    conn.close()

@app.route("/eliminar/<int:id>")
def eliminar(id):
    eliminar_cliente(id)
    return redirect("/")


def obtener_cliente(id):
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clientes WHERE id = ?", (id,))
    cliente = cursor.fetchone()

    conn.close()
    return cliente

@app.route("/editar/<int:id>")
def editar(id):
    cliente = obtener_cliente(id)
    return render_template("editar.html", cliente=cliente)


def actualizar_cliente(id, nombre, telefono, correo):
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE clientes
        SET nombre = ?, telefono = ?, correo = ?
        WHERE id = ?
    """, (nombre, telefono, correo, id))

    conn.commit()
    conn.close()

@app.route("/actualizar/<int:id>", methods=["POST"])
def actualizar(id):
    nombre = request.form["nombre"]
    telefono = request.form["telefono"]
    correo = request.form["correo"]

    actualizar_cliente(id, nombre, telefono, correo)

    return redirect("/")


# Ejecutar app
if __name__ == "__main__":
    crear_tabla()
    app.run(host="0.0.0.0", port=5000)