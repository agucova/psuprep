from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    send_from_directory,
    safe_join,
)
from subprocess import run
from tasksc import tareas
from tasks import compilarResumen
import json
import random
import os

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


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


# Generador de Resumenes, necesita mucha optimización
def generarResumen(secciones, pedido):
    id = str(random.randint(0, 999999))
    os.makedirs("cache/" + id)
    resumen = compilarResumen(id, secciones, pedido)
    print(resumen)
    return (id, resumen)


@app.route("/")
def hello_world():
    return "Hi there."


@app.route("/resumen", methods=["GET", "POST"])
def resumen():
    with open("secciones.json") as seccionesf:
        secciones = json.load(seccionesf)
    if request.method == "POST":
        pedido = request.form.getlist("secciones[]")
        if pedido is None:
            return "400"
        for subseccion in pedido:
            subseccion = subseccion.strip()
            if not subseccion.isalpha():
                return "400"
        id, resumen = generarResumen(secciones, pedido)
        if not id:
            return "Error compilando."
        link = "/descargar?id=" + id
        return render_template("generando.html", link=link)
    else:
        return render_template("resumen.html", secciones=secciones)


@app.route("/descargar", methods=["GET"])
def descargar():
    id = request.args.get("id").strip()  # SANITIZAR
    if id is None:
        return "401"
    elif not os.path.exists("cache/" + id):
        return "404"
    # Se debe reemplazar esta condición por una comprobación directa a Huey.
    elif not os.path.exists("cache/" + id + "/main.pdf"):
        return render_template("sigue-generando.html")
    return send_from_directory(
        os.getcwd() + "/cache/" + id, "main.pdf", as_attachment=True
    )
