# ==========================================
# FILEBOX SERVER v1.0
# Servidor casero para Termux
# ==========================================

from flask import (
    Flask,
    request,
    jsonify,
    send_file,
    send_from_directory
)

import os
import json
import time
import shutil
from datetime import datetime


# -------------------------------
# CONFIGURACIÓN
# -------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(
    BASE_DIR,
    "config.json"
)


if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
else:
    config = {
        "port": 8080,
        "storage": "storage",
        "name": "FILEBOX SERVER"
    }


STORAGE = os.path.join(
    BASE_DIR,
    config["storage"]
)


WEB = os.path.join(
    BASE_DIR,
    "web"
)


LOG_DIR = os.path.join(
    BASE_DIR,
    "logs"
)


LOG_FILE = os.path.join(
    LOG_DIR,
    "server.log"
)


# Crear carpetas necesarias

os.makedirs(STORAGE, exist_ok=True)
os.makedirs(WEB, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)



# -------------------------------
# APP
# -------------------------------

app = Flask(__name__)



# -------------------------------
# LOGS
# -------------------------------

def write_log(text):

    fecha = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    linea = f"[{fecha}] {text}\n"

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as f:
        f.write(linea)



# -------------------------------
# PÁGINA PRINCIPAL
# -------------------------------

@app.route("/")
def home():

    return send_from_directory(
        WEB,
        "index.html"
    )



@app.route("/<path:file>")
def web_files(file):

    return send_from_directory(
        WEB,
        file
    )



# -------------------------------
# LISTAR ARCHIVOS
# -------------------------------

@app.route("/api/files")
def list_files():

    resultado = []

    for root, dirs, files in os.walk(STORAGE):

        for file in files:

            path = os.path.join(
                root,
                file
            )

            size = os.path.getsize(path)

            fecha = os.path.getmtime(path)


            resultado.append({

                "name": file,

                "path":
                os.path.relpath(
                    path,
                    STORAGE
                ),

                "size": size,

                "date":
                datetime.fromtimestamp(
                    fecha
                ).strftime(
                    "%d/%m/%Y %H:%M"
                )

            })


    return jsonify(resultado)



# -------------------------------
# SUBIR ARCHIVO
# -------------------------------

@app.route(
    "/api/upload",
    methods=["POST"]
)
def upload():


    if "file" not in request.files:

        return jsonify({
            "error":"No hay archivo"
        }),400



    file = request.files["file"]


    folder = request.form.get(
        "folder",
        ""
    )


    destino = os.path.join(
        STORAGE,
        folder
    )


    os.makedirs(
        destino,
        exist_ok=True
    )


    ruta = os.path.join(
        destino,
        file.filename
    )


    file.save(ruta)



    write_log(
        f"Archivo subido: {file.filename}"
    )


    return jsonify({

        "status":"ok",

        "file":
        file.filename

    })



# -------------------------------
# DESCARGAR
# -------------------------------

@app.route(
    "/api/download/<path:name>"
)
def download(name):

    return send_file(
        os.path.join(
            STORAGE,
            name
        ),
        as_attachment=True
    )



# -------------------------------
# ELIMINAR
# -------------------------------

@app.route(
    "/api/delete",
    methods=["POST"]
)
def delete():


    data = request.json


    archivo = os.path.join(
        STORAGE,
        data["path"]
    )


    if os.path.exists(archivo):

        os.remove(archivo)


        write_log(
            f"Archivo eliminado: {data['path']}"
        )


        return jsonify({
            "status":"deleted"
        })


    return jsonify({
        "error":"No existe"
    }),404




# -------------------------------
# RENOMBRAR
# -------------------------------

@app.route(
    "/api/rename",
    methods=["POST"]
)
def rename():


    data=request.json


    viejo=os.path.join(
        STORAGE,
        data["old"]
    )


    nuevo=os.path.join(
        STORAGE,
        data["new"]
    )


    os.rename(
        viejo,
        nuevo
    )


    write_log(
        f"Renombrado: {data['old']} -> {data['new']}"
    )


    return jsonify({
        "status":"ok"
    })



# -------------------------------
# CREAR CARPETA
# -------------------------------

@app.route(
    "/api/folder",
    methods=["POST"]
)
def folder():


    data=request.json


    nueva=os.path.join(
        STORAGE,
        data["name"]
    )


    os.makedirs(
        nueva,
        exist_ok=True
    )


    write_log(
        f"Carpeta creada: {data['name']}"
    )


    return jsonify({
        "status":"ok"
    })



# -------------------------------
# INFORMACIÓN DEL SERVIDOR
# -------------------------------

@app.route("/api/system")
def system():


    total, usado, libre = shutil.disk_usage(
        BASE_DIR
    )


    return jsonify({

        "name":
        config["name"],


        "total":
        total,


        "used":
        usado,


        "free":
        libre,


        "uptime":
        time.time()

    })



# -------------------------------
# ARRANQUE
# -------------------------------

if __name__ == "__main__":


    print("""
=================================
        FILEBOX SERVER
=================================

Servidor iniciado

Puerto:
{}

Carpeta:
{}

=================================
""".format(
        config["port"],
        STORAGE
    ))


    write_log(
        "Servidor iniciado"
    )


    app.run(
        host="0.0.0.0",
        port=config["port"],
        debug=False
    )
