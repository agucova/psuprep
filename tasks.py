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
    # Borra la carpeta de compilación del cache, llamado 120 segundos después por Huey.
    comp = run(["rm", "-rf", "cache/" + identificador])
    return bool(comp.returncode)


@tareas.task()
def compilar(identificador, secciones, pedido):
    pedido = encontrar_ejes(secciones, pedido)
    lpedido = ""
    for subseccion in pedido:
        if subseccion[1]: # Si comienza un eje
            lpedido = lpedido + "secciones/" + subseccion[1] + ".md " # Agrega ese eje
        lpedido = lpedido + "secciones/" + subseccion[0] + ".md " # Agrega la subseccion
    run(
        "cp -r resumen/* cache/" + identificador + "/", shell=True
    )  # OPTIMIZAR WILDCARD
    args = "--standalone --from=markdown+yaml_metadata_block --template=tema.tex --pdf-engine=xelatex -o main.pdf variables.yml "
    comp = run("pandoc " + args + lpedido, cwd=(os.getcwd() + "/cache/" + identificador), shell=True)
    limpiar.schedule(args=(identificador,), delay=120)  # Borrar resumen en 120 segundos.
    return bool(comp.returncode)