import json
from flask import Flask, render_template, request, redirect, url_for

filename = "datos.json"

def cargar_datos():
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            administrador_base = data.get("administrador", [])
            gp_base = data.get("gestor de proyectos", [])
            empleados_base = data.get("empleados", [])
            proyectos_base = data.get("proyectos", {})
    except Exception as e:
        administrador_base = []
        gp_base = []
        empleados_base = []
        proyectos_base = {}

    return administrador_base, gp_base, empleados_base, proyectos_base

def guardar_datos(administrador_base, gp_base, empleados_base):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump({"administrador": administrador_base, "gestor de proyectos": gp_base, "empleados": empleados_base}, file, indent=5)


administrador_base, gp_base, empleados_base, proyectos_base = cargar_datos()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/iniciar_sesion", methods=["GET", "POST"])
def iniciar_sesion():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        contraseña = request.form.get("contraseña")
        cedula = request.form.get("cedula")
        for persona in administrador_base:
            if persona.get("usuario") == usuario and persona.get("contraseña") == contraseña and persona.get("cedula") == cedula:
                return redirect(url_for("administrador", cedula=cedula))

        for persona in gp_base:
            if persona.get("usuario") == usuario and persona.get("contraseña") == contraseña and persona.get("cedula") == cedula:
                return "hola gp"
        for persona in empleados_base:
            if persona.get("usuario") == usuario and persona.get("contraseña") == contraseña and persona.get("cedula") == cedula:
                return "hola emple"

    return render_template("iniciar_sesion.html")

@app.route("/registrarse", methods=["GET", "POST"])
def registrarse():
    if request.method == "POST":
        cedula = request.form.get("cedula_r")
        nombre = request.form.get("nombre")
        usuario = request.form.get("usuario_r")
        contraseña = request.form.get("contraseña_r")
        valor = request.form.get("valor")

        agregar = {
            "cedula": cedula,
            "nombre": nombre,
            "usuario": usuario,
            "contraseña": contraseña,
        }

        if valor == "empleado":
            empleados_base.append(agregar)
        elif valor == "gestor":
            gp_base.append(agregar)

        guardar_datos(administrador_base, gp_base, empleados_base)

        return redirect("/iniciar_sesion")

    return render_template("registrarse.html")

@app.route("/administrador")
def administrador():
    cedula = request.args.get("cedula")
    return render_template("administrador", cedula=cedula)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
