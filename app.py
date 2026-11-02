from flask import Flask, render_template
from connection import obtener_conexion

app = Flask(__name__)

@app.route("/")
def inicio():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT id_servicio, nombre, categoria,
                   descripcion, precio_base
            FROM servicios
            WHERE activo = TRUE
            ORDER BY categoria, nombre
        """)
        servicios = cursor.fetchall()
    finally:
        cursor.close()
        conexion.close()

    return render_template("index.html", servicios=servicios)

if __name__ == "__main__":
    app.run(debug=True)