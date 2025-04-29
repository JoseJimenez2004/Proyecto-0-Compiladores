import os
from flask import Flask, render_template, jsonify, request
from werkzeug.utils import secure_filename
from crear_afn_basico import crear_afn_basico
from unir_afn import unir_afn_desde_archivos
from concatenar import concatenar_afn_desde_archivos, AFN, cargar_afn_desde_archivo
from cerradurapositiva import cerradura_positiva_afn, aplicar_cerradura_positiva
from cerradurakleenestar import cerradura_kleene_afn, aplicar_cerradura_kleene
from cerraduraopcional import cerradura_opcional_afn, aplicar_cerradura_opcional
from AnalizadorLexico import AnalizadorLexico

app = Flask(__name__)

UPLOAD_FOLDER = 'autbasic'
RESULT_FOLDER = 'concaafn'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

# --- AFNs básicos y operaciones ---

@app.route('/crear_afn', methods=['POST'])
def crear_afn():
    simbolo = request.get_json().get('simbolo')
    if not simbolo:
        return jsonify({'error': 'Símbolo no proporcionado'}), 400

    afn = crear_afn_basico(simbolo)
    nombre_archivo = f"afn_{simbolo}"
    afn.guardar_en_archivo(nombre_archivo)

    return jsonify({
        'afn': {
            'simbolo': afn.simbolo,
            'estado_inicial': afn.estado_inicial,
            'estado_final': afn.estado_final,
            'transiciones': afn.transiciones
        }
    })

@app.route('/unir_afns', methods=['POST'])
def unir_afns():
    try:
        afn1 = request.files['afn1']
        afn2 = request.files['afn2']
        nombre_resultado = request.form['resultado']

        if not afn1 or not afn2 or not nombre_resultado:
            return jsonify({'error': 'Faltan parámetros'}), 400

        nombre1 = secure_filename(afn1.filename)
        nombre2 = secure_filename(afn2.filename)
        afn1.save(os.path.join(UPLOAD_FOLDER, nombre1))
        afn2.save(os.path.join(UPLOAD_FOLDER, nombre2))
        archivo_guardado = unir_afn_desde_archivos(nombre1.replace('.txt', ''), nombre2.replace('.txt', ''), nombre_resultado)
        return jsonify({'mensaje': f'AFNs unidos exitosamente, archivo guardado como {archivo_guardado}.txt'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/concatenar_afns', methods=['POST'])
def concatenar_afns():
    try:
        afn1 = request.files['afn1']
        afn2 = request.files['afn2']
        nombre = request.form['nombre']

        nombre1 = secure_filename(afn1.filename)
        nombre2 = secure_filename(afn2.filename)
        afn1.save(os.path.join(UPLOAD_FOLDER, nombre1))
        afn2.save(os.path.join(UPLOAD_FOLDER, nombre2))

        afn1_obj = cargar_afn_desde_archivo(nombre1.replace('.txt', ''))
        afn2_obj = cargar_afn_desde_archivo(nombre2.replace('.txt', ''))

        offset = max(afn1_obj.estado_final, afn2_obj.estado_final) + 1
        trans2 = [(q1 + offset, s, q2 + offset) for (q1, s, q2) in afn2_obj.transiciones]
        trans_total = afn1_obj.transiciones + trans2 + [(afn1_obj.estado_final, 'ε', afn2_obj.estado_inicial + offset)]

        concatenado = AFN(f"{afn1_obj.simbolo}{afn2_obj.simbolo}", trans_total, afn1_obj.estado_inicial, afn2_obj.estado_final + offset)
        concatenado.guardar_en_archivo(nombre, carpeta=RESULT_FOLDER)

        return jsonify({'success': True})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cerradura_positiva_aplicar', methods=['POST'])
def cerradura_positiva_aplicar():
    try:
        nombre_afn = request.get_json().get('nombre')
        if not nombre_afn:
            return jsonify({'error': 'Nombre de AFN no proporcionado'}), 400

        afn = cargar_afn_desde_archivo(nombre_afn)
        afn_resultado = aplicar_cerradura_positiva(afn)
        
        nombre_resultado = f"{nombre_afn}_cerradura_positiva"
        afn_resultado.guardar_en_archivo(nombre_resultado, carpeta='cerradurapositiva')

        return jsonify({"mensaje": f"Guardado como cerradurapositiva/{nombre_resultado}.txt"})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cerradura_kleene', methods=['POST'])
def cerradura_kleene():
    try:
        nombre_afn = request.get_json().get('nombre')
        if not nombre_afn:
            return jsonify({"error": "No se ha proporcionado un AFN."}), 400

        afn = cargar_afn_desde_archivo(nombre_afn, carpeta='autbasic')
        afn_cerradura = aplicar_cerradura_kleene(afn)

        nombre_resultado = f"{nombre_afn}_cerradura_kleene"
        afn_cerradura.guardar_en_archivo(nombre_resultado, carpeta='cerradurakleene')

        return jsonify({"mensaje": f"Guardado como cerradurakleene/{nombre_resultado}.txt"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/cerradura_opcional', methods=['POST'])
def cerradura_opcional():
    try:
        cerradura_opcional_afn()
        return jsonify({'status': 'Cerradura opcional aplicada exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- Análisis Léxico ---
@app.route('/analizador_lexico', methods=['POST'])
def analizador_lexico():
    # Recibimos la cadena del frontend
    data = request.get_json()
    cadena = data.get('cadena', '')

    if not cadena:
        return jsonify({"error": "Cadena vacía proporcionada"}), 400

    # Llamamos a tu analizador léxico
    archivo_afd = "AFN_File/mi_afd_guardado.afd"  # Ajusta la ruta a tu AFD
    analizador = AnalizadorLexico(cadena, archivo_afd)

    tokens = []
    while True:
        token = analizador.yylex()
        if token == 0:
            break
        tokens.append({"token": token, "lexema": analizador.Lexema})

    if tokens:
        return jsonify({"tokens": tokens})
    else:
        return jsonify({"error": "No se pudieron identificar tokens."}), 400

# --- Utilidades ---

@app.route('/listar_afns', methods=['GET'])
def listar_afns():
    afns = [f.replace('.txt', '') for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.txt')]
    return jsonify(afns)

@app.route('/obtener_afns', methods=['GET'])
def obtener_afns():
    archivos_afns = [f.replace('.txt', '') for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.txt')]
    return jsonify({'afns': archivos_afns})

if __name__ == '__main__':
    app.run(debug=True)
