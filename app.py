from flask import Flask, flash, jsonify, redirect, render_template, request, session
import json
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Desactivar cache
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/')
def hello_world():
    return render_template("resumen.html")

@app.route('/resumen', methods=["GET", "POST"])
def resumen():
    with open("secciones.json") as seccionesf:
        secciones = json.load(seccionesf)
    if request.method == "POST":
        print(request.form)
        pedido = request.form.getlist("secciones[]")
        for seccion in pedido:
            seccion = seccion.strip()
            if not seccion.isalpha():
                return 400
            
        return "Not implemented."
    else:
        return render_template("resumen.html", secciones=secciones)