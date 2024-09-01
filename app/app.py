import json
from flask import Flask, render_template, request, redirect

filename = "datos"

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

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/iniciar_sesion")
def iniciar_sesion():
    usuario = request.form.get("usuario")
    registrar = request.form.get("registrarse")
    for persona in base_datos:
        if persona.get("usuario") == usuario:
            if persona.get("contraseña") == registrar:
                return redirect()
    return render_template("iniciar_sesion.html")


with open(filename, "w", encoding="utf-8") as file:
    json.dump({"administrador" : administrador_base, "gestor de proyectos" : gp_base, "empleados" : empleados_base}, file, indent=5)

if __name__ == "__main__":
    app.run(debug=True, port=5000)