from flask import Flask, render_template, request, send_from_directory,redirect
from subprocess import run
from tasksc import tareas
from tasks import compilar
import json
import random
import os

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

rng = random.SystemRandom()

# Desactivar cache
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Limpiar cache de pedidos y regenerar
run(["rm", "-rf", "./cache/"], cwd=os.getcwd())  # DANGEROUS
os.makedirs("cache/", exist_ok=True)

with open("secciones.json") as seccionesf:
    secciones = json.load(seccionesf)
# Generador de Resumenes, necesita mucha optimización
def generar(secciones, pedido):
    # TODO: Prevenir colisiones
    identificador = str(rng.randint(0, 999999))
    os.makedirs("cache/" + identificador)
    resumen = compilar(identificador, secciones, pedido)
    print(resumen)
    return (identificador, resumen)


@app.route("/")
def hello_world():
    # TODO: Hacer homepage
    return redirect("/resumen")


@app.route("/resumen", methods=["GET", "POST"])
def resumen():
    if request.method == "POST":
        pedido = request.form.getlist("secciones[]")
        if pedido is None:
            return "400"
        for subseccion in pedido:
            subseccion = subseccion.strip()
            if not subseccion.isalpha():
                return "400"
        identificador, resumen = generar(secciones, pedido)
        if not identificador or not resumen:
            return render_template("error.html")
        link = "/descargar?id=" + identificador
        return render_template("generando.html", link=link)
    return render_template("resumen.html", secciones=secciones)


@app.route("/descargar", methods=["GET"])
def descargar():
    identificador = request.args.get("id").strip()  # SANITIZAR
    if identificador is None:
        return "401"
    elif not os.path.exists("cache/" + identificador):
        return "404"
    # Se debe reemplazar esta condición por una comprobación directa a Huey.
    elif not os.path.exists("cache/" + identificador + "/main.pdf"):
        return render_template("sigue-generando.html")
    return send_from_directory(
        os.getcwd() + "/cache/" + identificador, "main.pdf", as_attachment=True
    )
