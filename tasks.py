from tasksc import tareas
from subprocess import run
import os


@tareas.task()
def limpiarResumen(id):
    comp = run(["rm", "-rf", "cache/" + id])
    return True if comp.returncode else False


@tareas.task()
def compilarResumen(id, secciones, pedido):
    lpedido = "\def\entrada{"
    for seccion in pedido:
        lpedido = lpedido + "{" + seccion + "},"
    lpedido = lpedido[:-1] + "} \input{main}"
    print(lpedido)
    run("cp -r resumen/* cache/" + id + "/", shell=True)  # OPTIMIZAR WILDCARD
    comp = run(["pdflatex", lpedido], cwd=os.getcwd() + "/cache/" + id)
    limpiarResumen.schedule(args=(id,), delay=120)  # Borrar resumen en 120 segundos.
    return bool(comp.returncode)
