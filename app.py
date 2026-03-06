from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def conexion():
    return sqlite3.connect("moto.db")


@app.route("/")
def index():
    return render_template("index.html")


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

        return redirect("/dashboard")

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

        return redirect("/dashboard")

    return render_template("gasolina.html")


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
    app.run()