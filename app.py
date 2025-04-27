import os
from flask import Flask, render_template, jsonify, request
from crear_afn_basico import crear_afn_basico
from unir_afn import unir_afn_desde_archivos
from concatenar import concatenar_afn_desde_archivos, AFN, cargar_afn_desde_archivo
from cerradurapositiva import cerradura_positiva_afn, aplicar_cerradura_positiva
from cerradurakleenestar import cerradura_kleene_afn, aplicar_cerradura_kleene
from cerraduraopcional import cerradura_opcional_afn, aplicar_cerradura_opcional
from AnalizadorLexico import AnalizadorLexico

from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/crear_afn', methods=['POST'])
def crear_afn():
    simbolo = request.get_json().get('simbolo')
    if simbolo:
        # Crear el AFN con el símbolo
        afn = crear_afn_basico(simbolo)

        # Guardar el AFN en un archivo
        nombre_archivo = f"afn_{simbolo}"  # Puedes modificar el nombre según lo que prefieras
        afn.guardar_en_archivo(nombre_archivo)

        # Devolver la descripción del AFN
        return jsonify({'afn': afn.mostrar()})
    else:
        return jsonify({'error': 'Símbolo no proporcionado'}), 400

@app.route('/unir_afn', methods=['POST'])
def unir_afn():
    unir_afn_desde_archivos()
    return jsonify({'status': 'AFN unido exitosamente'})

@app.route('/concatenar_afn', methods=['POST'])
def concatenar_afn():
    concatenar_afn_desde_archivos()
    return jsonify({'status': 'AFN concatenado exitosamente'})

@app.route('/cerradura_positiva', methods=['POST'])
def cerradura_positiva():
    cerradura_positiva_afn()
    return jsonify({'status': 'Cerradura positiva aplicada exitosamente'})

@app.route('/cerradura_kleene', methods=['POST'])
def cerradura_kleene():
    data = request.get_json()
    nombre_afn = data.get('nombre')

    if not nombre_afn:
        return jsonify({"error": "No se ha proporcionado un AFN."}), 400

    try:
        # Cargar el AFN desde el archivo
        afn = cargar_afn_desde_archivo(nombre_afn, carpeta='autbasic')
        # Aplicar la cerradura de Kleene
        afn_cerradura = aplicar_cerradura_kleene(afn)

        # Guardar el nuevo AFN con la cerradura de Kleene
        nombre_resultado = f"{nombre_afn}_cerradura_kleene"
        afn_cerradura.guardar_en_archivo(nombre_resultado, carpeta='cerradurakleene')

        mensaje = f"AFN con cerradura de Kleene guardado en: cerradurakleene/{nombre_resultado}.txt"
        return jsonify({"mensaje": mensaje})

    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404

@app.route('/cerradura_opcional', methods=['POST'])
def cerradura_opcional():
    cerradura_opcional_afn()
    return jsonify({'status': 'Cerradura opcional aplicada exitosamente'})

@app.route('/analizador_lexico', methods=['POST'])
def analizador_lexico():
    data = request.get_json()
    cadena = data.get('cadena')
    archivo_afd = "afd.txt"  # Asegúrate de tener este archivo generado previamente

    if not cadena:
        return jsonify({'error': 'Cadena no proporcionada'}), 400

    try:
        analizador = AnalizadorLexico(cadena, archivo_afd)
        tokens = []

        while True:
            token = analizador.yylex()
            if token == 0:
                break
            tokens.append({
                'lexema': analizador.Lexema,
                'token': token
            })

        return jsonify({'tokens': tokens})

    except FileNotFoundError:
        return jsonify({'error': f"Archivo {archivo_afd} no encontrado"}), 404
    except Exception as e:
        return jsonify({'error': f"Ocurrió un error: {str(e)}"}), 500

UPLOAD_FOLDER = 'autbasic'
RESULT_FOLDER = 'concaafn'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/concatenar_afns', methods=['POST'])
def concatenar_afns():
    afn1 = request.files['afn1']
    afn2 = request.files['afn2']
    nombre = request.form['nombre']

    # Guardar los archivos subidos
    nombre1 = secure_filename(afn1.filename)
    nombre2 = secure_filename(afn2.filename)
    afn1.save(os.path.join(UPLOAD_FOLDER, nombre1))
    afn2.save(os.path.join(UPLOAD_FOLDER, nombre2))

    # Cargar AFNs
    afn1_obj = cargar_afn_desde_archivo(nombre1.replace('.txt', ''))
    afn2_obj = cargar_afn_desde_archivo(nombre2.replace('.txt', ''))

    # Renombrar estados de afn2
    offset = max(afn1_obj.estado_final, afn2_obj.estado_final) + 1
    trans2 = [(q1 + offset, s, q2 + offset) for (q1, s, q2) in afn2_obj.transiciones]
    trans_total = afn1_obj.transiciones + trans2 + [(afn1_obj.estado_final, 'ε', afn2_obj.estado_inicial + offset)]

    concatenado = AFN(f"{afn1_obj.simbolo}{afn2_obj.simbolo}", trans_total, afn1_obj.estado_inicial, afn2_obj.estado_final + offset)
    concatenado.guardar_en_archivo(nombre, carpeta=RESULT_FOLDER)

    return jsonify({'success': True})

@app.route('/cerradura_positiva_aplicar', methods=['POST'])
def cerradura_positiva_aplicar():
    nombre_afn = request.get_json().get('nombre')
    try:
        # Cargar el AFN desde el archivo
        afn = cargar_afn_desde_archivo(nombre_afn)

        # Aplicar la cerradura positiva
        afn_resultado = aplicar_cerradura_positiva(afn)
        
        # Guardar el resultado
        nombre_resultado = f"{nombre_afn}_cerradura_positiva"
        afn_resultado.guardar_en_archivo(nombre_resultado, carpeta='cerradurapositiva')
        
        return jsonify({"mensaje": f"Guardado como cerradurapositiva/{nombre_resultado}.txt"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def listar_afns():
    return [f.replace('.txt', '') for f in os.listdir('autbasic') if f.endswith('.txt')]

# Ruta para listar los AFNs disponibles
@app.route('/listar_afns', methods=['GET'])
def listar_afns_route():
    afns = listar_afns()
    return jsonify(afns)

# Ruta para obtener los archivos AFNs disponibles
@app.route('/obtener_afns', methods=['GET'])
def obtener_afns():
    carpeta_afns = 'autbasic'
    archivos_afns = [f.replace('.txt', '') for f in os.listdir(carpeta_afns) if f.endswith('.txt')]
    return jsonify({'afns': archivos_afns})

if __name__ == '__main__':
    app.run(debug=True)
