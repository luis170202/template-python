from flask import Flask, request, send_file
from flask_cors import CORS
import zipfile

import os
import random
import string



def generar_clave():
    caracteres = string.ascii_letters + string.digits
    clave = random.sample(caracteres, 10)
    return ''.join(clave)



app = Flask(__name__)
CORS(app)
port = int(os.environ.get("PORT", 5000))

@app.route('/')
def home():
    return "200 ok"


@app.route('/upload', methods=['POST'])
def handle_upload():
    zip_file = request.files['file']
    zip_data = zip_file.read()

    with open(f'carpetaPedidos/{generar_clave()}.zip', 'wb') as f:
        f.write(zip_data)

    #with zipfile.ZipFile('data.zip', 'r') as zip_ref:
        #zip_ref.extractall('extracted_files')



    return '200 OK'


carpeta_pedidos = 'carpetaPedidos'


usuario = 'luis'
contraseña = 'luis170303'

@app.route('/descargar_todo', methods=['GET'])
def descargar_todo():
    try:
        # Verificar las credenciales de autenticación
        if request.headers.get('token') == None:
            token = request.args.get('token')
        else:
            token = request.headers.get('token')
        print(token)
        if token != "luis170303":

            return 'Acceso no autorizado', 401

        # Ruta y nombre del archivo ZIP resultante
        ruta_zip_resultante = './todos_los_pedidos.zip'

        # Crear un archivo ZIP que contendrá todos los archivos ZIP de la carpeta "pedidos"
        with zipfile.ZipFile(ruta_zip_resultante, 'w') as zip_resultante:
            for archivo_zip in os.listdir(carpeta_pedidos):
                if archivo_zip.endswith('.zip'):
                    ruta_completa = os.path.join(carpeta_pedidos, archivo_zip)
                    zip_resultante.write(ruta_completa, os.path.basename(ruta_completa))
                    os.remove(os.path.join(carpeta_pedidos, archivo_zip))

        return send_file(ruta_zip_resultante, as_attachment=True)
    except Exception as e:
        return str(e), 500



if __name__ == '__main__':
    app.run(port=port)
