from tasksc import tareas
from subprocess import run
import os

def encontrar_ejes(secciones, identificadores):
    # Asume que los identificadores ya vienen en grupos por seccion
    resultado = []
    ejes = []
    for identificador in identificadores:
        for eje,subsecciones in secciones.items():
            for subseccion in subsecciones:
                if subseccion["id"] == identificador:
                    if eje not in ejes:
                        ejes.append(eje)
                        resultado.append((identificador, eje))
                    else:
                        resultado.append((identificador, None))
    return resultado

@tareas.task()
def limpiar(identificador):
    comp = run(["rm", "-rf", "cache/" + identificador])
    return bool(comp.returncode)


@tareas.task()
def compilar(identificador, secciones, pedido):
    print("BPedido:", pedido)
    pedido = encontrar_ejes(secciones, pedido)
    print("APedido:", pedido)
    lpedido = r"\def\entrada{"
    for subseccion in pedido:
        if subseccion[1]: # Si comienza un eje
            lpedido = lpedido + "{" + subseccion[1] + "}," # Agrega ese eje
        lpedido = lpedido + "{" + subseccion[0] + "}," # Agrega la subseccion
    lpedido = lpedido[:-1] + r"} \input{main}"
    print("LPedido:", lpedido)
    run(
        "cp -r resumen/* cache/" + identificador + "/", shell=True
    )  # OPTIMIZAR WILDCARD
    comp = run(["pdflatex", lpedido], cwd=(os.getcwd() + "/cache/" + identificador))
    limpiar.schedule(args=(identificador,), delay=120)  # Borrar resumen en 120 segundos.
    return bool(comp.returncode)
