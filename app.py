from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from flask import session, redirect, request, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from flask import send_file
from functools import wraps
from flask import url_for
from datetime import timedelta






app = Flask(__name__)
app.secret_key = "super_secret_key"
app.permanent_session_lifetime = timedelta(seconds=15)

def conexion():
    return sqlite3.connect("moto.db")

conn = conexion()
cursor = conn.cursor()




def login_required(f):


    @wraps(f)
    def decorated_function(*args, **kwargs):

        if 'usuario' not in session:
            return redirect('/login')
        
        return f(*args, **kwargs)
    
    return decorated_function


##@app.route("/")
#def home():
#    return "index.html"

@app.route('/')
@login_required
def index():
    if "usuario" not in session:
       return redirect("/login")
    return render_template("index.html")


@app.route('/logout')
def logout():

    session.pop("usuario", None)

    return redirect('/login')




@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        conn = conexion()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO usuarios (username,password) VALUES (?,?)",
            (username,password)
        )

        conn.commit()

        return redirect('/login')

    return render_template("register.html")

@app.route('/login', methods=['GET','POST'])
def login():

    error = None

    if request.method == 'POST':

        username = request.form["username"].strip()
        password = request.form["password"].strip()

        conn = conexion()
        cursor = conn.cursor()

        # fetch user record by username only
        cursor.execute(
            "SELECT * FROM usuarios WHERE username=?",
            (username,)
        )
        
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session.permanent = True              # usa la vida útil definida arriba
            session["usuario"] = username
            return redirect(url_for('index'))
        else:
            return render_template("login.html", error="Usuario o contraseña incorrectos")
        
    return render_template("login.html", error=error)

@app.route("/debug_users")

def debug_users():

    conn = conexion()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios")
    users = cursor.fetchall()

    conn.close()

    return str(users)

# -------------------------
# MANTENIMIENTO
# -------------------------

@app.route("/mantenimiento", methods=["GET","POST"])
def mantenimiento():

    if request.method == "POST":

        fecha = request.form["fecha"]
        km = request.form["km"]
        servicio = request.form["servicio"]
        costo = request.form["costo"]

        conn = conexion()
        cur = conn.cursor()

        cur.execute(
        "INSERT INTO mantenimiento (fecha,km,servicio,costo) VALUES (?,?,?,?)",
        (fecha,km,servicio,costo)
        )

        conn.commit()
        conn.close()

        return redirect("/index")

    return render_template("mantenimiento.html")


# -------------------------
# GASOLINA
# -------------------------

@app.route("/gasolina", methods=["GET","POST"])
def gasolina():

    if request.method == "POST":

        fecha = request.form["fecha"]
        km = request.form["km"]
        litros = request.form["litros"]
        precio = request.form["precio"]

        conn = conexion()
        cur = conn.cursor()

        cur.execute(
        "INSERT INTO gasolina (fecha,km,litros,precio) VALUES (?,?,?,?)",
        (fecha,km,litros,precio)
        )

        conn.commit()
        conn.close()

        return redirect("/index")

    return render_template("gasolina.html")

@app.route('/exportar_gasolina')
def exportar_gasolina():

    conn = conexion()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM gasolina")

    data = cursor.fetchall()

    df = pd.DataFrame(data)

    archivo = "gasolina.xlsx"

    df.to_excel(archivo, index=False)

    return send_file(archivo, as_attachment=True)


# -------------------------
# DASHBOARD
# -------------------------

@app.route("/dashboard")
def dashboard():

    conn = conexion()
    cur = conn.cursor()

    cur.execute("SELECT * FROM mantenimiento")
    mantenimiento = cur.fetchall()

    cur.execute("SELECT * FROM gasolina")
    gasolina = cur.fetchall()

    conn.close()

    total_gasto = sum([m[4] for m in mantenimiento])

    return render_template(
        "dashboard.html",
        mantenimiento=mantenimiento,
        gasolina=gasolina,
        total_gasto=total_gasto
    )




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)