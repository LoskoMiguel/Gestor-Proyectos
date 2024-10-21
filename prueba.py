a = {
    "control" : ["", "pepito", "marianito", "gustavito"]
}

xd = a["control"]

ls = int(input(f"Hay un total de {(len(xd)) - 1} proyectos por revisar cual deseas revisar: "))

if ls == 0:
    print("opcion incorrecta")
else:
    print(xd[ls])