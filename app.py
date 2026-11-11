
from flask import (
    Flask, render_template, request,
    redirect, url_for, session, flash
)
from werkzeug.security import check_password_hash
from functools import wraps
from decimal import Decimal, InvalidOperation

from connection import obtener_conexion
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY


# --------------------------------
# PROTECCIÓN DE RUTAS ADMINISTRATIVAS
# --------------------------------

def administrador_requerido(funcion):
    @wraps(funcion)
    def decorador(*args, **kwargs):
        if not session.get("administrador"):
            return redirect(url_for("login"))

        return funcion(*args, **kwargs)

    return decorador


# --------------------------------
# PÁGINA PRINCIPAL
# --------------------------------

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


# --------------------------------
# LOGIN
# --------------------------------

@app.route("/admin", methods=["GET", "POST"])
def login():

    if session.get("administrador"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        usuario = request.form.get("usuario", "").strip()
        contraseña = request.form.get("contraseña", "")

        hash_guardado = config.ADMIN_PASSWORD_HASH

        if (
            usuario == config.ADMIN_USER
            and hash_guardado
            and check_password_hash(hash_guardado, contraseña)
        ):
            session.clear()
            session["administrador"] = True

            return redirect(url_for("dashboard"))

        flash("Usuario o contraseña incorrectos.", "error")

    return render_template("admin/login.html")


# --------------------------------
# CERRAR SESIÓN
# --------------------------------

@app.route("/admin/logout", methods=["POST"])
@administrador_requerido
def logout():

    session.clear()

    return redirect(url_for("login"))


# --------------------------------
# DASHBOARD
# --------------------------------

@app.route("/admin/dashboard")
@administrador_requerido
def dashboard():

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM servicios
            WHERE activo = TRUE
        """)
        total_servicios = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM clientes
        """)
        total_clientes = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM solicitudes
        """)
        total_solicitudes = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT id_solicitud, fecha_solicitud,
                   estado, precio_total
            FROM solicitudes
            ORDER BY fecha_solicitud DESC
            LIMIT 5
        """)
        solicitudes = cursor.fetchall()

    finally:
        cursor.close()
        conexion.close()

    return render_template(
        "admin/dashboard.html",
        total_servicios=total_servicios,
        total_clientes=total_clientes,
        total_solicitudes=total_solicitudes,
        solicitudes=solicitudes
    )


# --------------------------------
# LISTAR SERVICIOS
# --------------------------------

@app.route("/admin/servicios")
@administrador_requerido
def servicios_admin():

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT *
            FROM servicios
            ORDER BY categoria, nombre
        """)

        servicios = cursor.fetchall()

    finally:
        cursor.close()
        conexion.close()

    return render_template(
        "admin/servicios.html",
        servicios=servicios
    )


# --------------------------------
# AGREGAR SERVICIO
# --------------------------------

@app.route("/admin/servicios/agregar", methods=["POST"])
@administrador_requerido
def agregar_servicio():

    nombre = request.form.get("nombre", "").strip()
    categoria = request.form.get("categoria", "").strip()
    descripcion = request.form.get("descripcion", "").strip()

    try:
        precio = Decimal(request.form.get("precio", "0"))

        if not precio.is_finite() or precio < 0:
            raise InvalidOperation

    except InvalidOperation:
        flash("Ingresá un precio válido.", "error")
        return redirect(url_for("servicios_admin"))

    if not nombre or categoria not in ("Piscineria", "Jardineria"):
        flash("Completá correctamente los datos del servicio.", "error")
        return redirect(url_for("servicios_admin"))

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            INSERT INTO servicios
            (nombre, categoria, descripcion, precio_base, activo)
            VALUES (%s, %s, %s, %s, TRUE)
        """, (nombre, categoria, descripcion, precio))

        conexion.commit()
        flash("Servicio agregado correctamente.", "success")

    except Exception:
        conexion.rollback()
        flash("No se pudo agregar el servicio.", "error")
        raise

    finally:
        cursor.close()
        conexion.close()

    return redirect(url_for("servicios_admin"))


# --------------------------------
# MODIFICAR SERVICIO
# --------------------------------

@app.route("/admin/servicios/editar/<int:id_servicio>", methods=["POST"])
@administrador_requerido
def editar_servicio(id_servicio):

    nombre = request.form.get("nombre", "").strip()
    categoria = request.form.get("categoria", "").strip()
    descripcion = request.form.get("descripcion", "").strip()

    try:
        precio = Decimal(request.form.get("precio", "0"))

        if not precio.is_finite() or precio < 0:
            raise InvalidOperation

    except InvalidOperation:
        flash("Ingresá un precio válido.", "error")
        return redirect(url_for("servicios_admin"))

    if not nombre or categoria not in ("Piscineria", "Jardineria"):
        flash("Los datos del servicio no son válidos.", "error")
        return redirect(url_for("servicios_admin"))

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            UPDATE servicios
            SET nombre = %s,
                categoria = %s,
                descripcion = %s,
                precio_base = %s
            WHERE id_servicio = %s
        """, (
            nombre, categoria, descripcion,
            precio, id_servicio
        ))

        conexion.commit()

        if cursor.rowcount:
            flash("Servicio modificado correctamente.", "success")
        else:
            flash("No se encontró el servicio.", "error")

    finally:
        cursor.close()
        conexion.close()

    return redirect(url_for("servicios_admin"))


# --------------------------------
# ACTIVAR / DESACTIVAR SERVICIO
# --------------------------------

@app.route("/admin/servicios/estado/<int:id_servicio>", methods=["POST"])
@administrador_requerido
def cambiar_estado_servicio(id_servicio):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            UPDATE servicios
            SET activo = NOT activo
            WHERE id_servicio = %s
        """, (id_servicio,))

        conexion.commit()

        if cursor.rowcount:
            flash("Estado del servicio actualizado.", "success")
        else:
            flash("No se encontró el servicio.", "error")

    finally:
        cursor.close()
        conexion.close()

    return redirect(url_for("servicios_admin"))


if __name__ == "__main__":
    app.run(debug=True)
