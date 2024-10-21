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
    except Exception as e:
        administrador_base = []
        gp_base = []
        empleados_base = []

    return administrador_base, gp_base, empleados_base

def guardar_datos(administrador_base, gp_base, empleados_base):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump({
            "administrador": administrador_base,
            "gestor de proyectos": gp_base,
            "empleados": empleados_base,
        }, file, indent=5)

administrador_base, gp_base, empleados_base = cargar_datos()

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
                return redirect(url_for("administrador", cedula_A=cedula))

        for persona in gp_base:
            if persona.get("usuario") == usuario and persona.get("contraseña") == contraseña and persona.get("cedula") == cedula:
                return redirect(url_for("gestor", cedula_GP=cedula))
    
        for persona in empleados_base:
            if persona.get("usuario") == usuario and persona.get("contraseña") == contraseña and persona.get("cedula") == cedula:
                return redirect(url_for("empleado", cedula_E=cedula))


    return render_template("iniciar_sesion.html")

@app.route("/registrarse", methods=["GET", "POST"])
def registrarse():
    if request.method == "POST":
        cedula = request.form.get("cedula_r")
        usuario = request.form.get("usuario_r")
        contraseña = request.form.get("contraseña_r")
        valor = request.form.get("valor")

        agregar = {
            "cedula": cedula,
            "usuario": usuario,
            "contraseña": contraseña,
            "reviciones_pendientes" : ["Ninguna"]
        }

        agregar_empleado = {
            "cedula": cedula,
            "usuario": usuario,
            "contraseña": contraseña,
            "trabajos_pendientes": "sin trabajos pendientes"
        }

        if valor == "empleado":
            empleados_base.append(agregar_empleado)
        elif valor == "gestor":
            gp_base.append(agregar)

        guardar_datos(administrador_base, gp_base, empleados_base)

        return redirect("/iniciar_sesion")

    return render_template("registrarse.html")


@app.route("/administrador")
def administrador():
    for persona in administrador_base:
         nombre = persona.get("usuario")

    return render_template("administrador.html", nombre_a=nombre)

@app.route("/empleado")
def empleado():
    cedula_E = request.args.get("cedula_E")
    
    for persona in empleados_base:
        if persona.get("cedula") == cedula_E:
            nombre = persona.get("usuario")

    return render_template("empleado.html", nombre_e=nombre)

nombre_gp = None
cedula_GP = None
@app.route("/gestor")
def gestor():
    global cedula_GP
    cedula_GP = request.args.get("cedula_GP")
    for persona in gp_base:
        if persona.get("cedula") == cedula_GP:
            global nombre_gp
            nombre_gp = persona.get("usuario")

    return render_template("gestor.html", nombre_gp=nombre_gp)

@app.route("/administrador_acercade")
def acercade_administrador():
    for persona in administrador_base:
         nombre = persona.get("usuario")
    return render_template("acerca_administrador.html", nombre_a=nombre)

@app.route("/administrador_revisar", methods=["GET", "POST"])
def administrador_revisar():
    empleado = request.form.get("cedula_revisar_administrador")
    informacion = "" 
    
    if request.method == "POST":
        for persona in empleados_base:
            if persona.get("cedula") == empleado:
                informacion = persona.get("trabajos_pendientes")
                break
        
        if not informacion:
            informacion = "No se encontró información para esta cédula."
    
    return render_template("revisar_administrador.html", informacion=informacion)

@app.route("/administrador_cambiar", methods=["GET", "POST"])
def administrador_cambiar():
    if request.method == "POST":
        cedula = request.form.get("cedula_cambiar_administrador")
        nueva_contraseña = request.form.get("nueva_contraseña_administrador")
        empleado_tipo = request.form.get("empleados_cambiar_contraseña")
        actualizo = None

        if empleado_tipo == "empleado_cambiar":
            for persona in empleados_base:
                if persona.get("cedula") == cedula:
                    persona["contraseña"] = nueva_contraseña
                    actualizo = "Contraseña actualizada exitosamente."
                    break

            if actualizo is None:
                actualizo = "No se encontró esta cédula."
            
        elif empleado_tipo == "gestor_cambiar":
            for persona in gp_base:
                if persona.get("cedula") == cedula:
                    persona["contraseña"] = nueva_contraseña
                    actualizo = "Contraseña actualizada exitosamente."
                    break

            if actualizo is None:
                actualizo = "No se encontró esta cédula."
    
        return render_template("cambiar_administrador.html", actualizo=actualizo)

    return render_template("cambiar_administrador.html", actualizo="")

@app.route("/gestor_acercade")
def acercade_gestor():
    return render_template("acercade_gestor.html", nombre_gp=nombre_gp)

@app.route("/gestor_asignar", methods=["GET", "POST"])
def gestor_asignar():
    informativo = None

    if request.method == "POST":
        cedula = request.form.get("asignar_cedula")
        proyecto = request.form.get("asignar_proyecto")

        for persona in empleados_base:
            if persona.get("cedula") == cedula:
                persona["trabajos_pendientes"] = proyecto
                informativo = "Trabajo asignado correctamente"
                break
        
        if informativo is None:
            informativo = "Persona no encontrada"

    return render_template("asignar_gestor.html", informativo=informativo)

@app.route("/gestor_revisar_progresos", methods=["GET", "POST"])
def gestor_revisar():
    empleado = request.form.get("cedula_revisar_progreso_gestor")
    informacion = "" 
    
    if request.method == "POST":
        for persona in empleados_base:
            if persona.get("cedula") == empleado:
                informacion = persona.get("trabajos_pendientes")
                break
        
        if not informacion:
            informacion = "No se encontró información para esta cédula."
    
    return render_template("gestor_revisar_progresos.html", informacion=informacion) 

@app.route("/gestor_cambiar", methods=["GET", "POST"])
def gestor_cambiar():
    if request.method == "POST":
        cedula = request.form.get("cedula_cambiar_gestor")
        nueva_contraseña = request.form.get("nueva_contraseña_gestor")
        actualizo = None

        for persona in empleados_base:
            if persona.get("cedula") == cedula:
                persona["contraseña"] = nueva_contraseña
                actualizo = "Contraseña actualizada exitosamente."
                break

        if actualizo is None:
            actualizo = "No se encontró esta cédula."

        return render_template("gestor_cambiar.html", actualizo=actualizo)

    return render_template("gestor_cambiar.html", actualizo="")

@app.route("/gestor_revisar_trabajos", methods=["GET", "POST"])
def gestor_revisar_trabajos():
    informacion = "No se encontró información"
    if request.method == "GET":
        for persona in gp_base:
            if persona.get("cedula") == cedula_GP:
                acceder_trabajos = persona.get("reviciones_pendientes")
                informacion = f"Hola {acceder_trabajos}"
                break

    return render_template("gestor_revisar_trabajos.html", informacion_revisar=informacion)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
