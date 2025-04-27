import os
from flask import Flask, render_template, jsonify, request
from crear_afn_basico import crear_afn_basico
from unir_afn import unir_afn_desde_archivos
from concatenar import concatenar_afn_desde_archivos, AFN, cargar_afn_desde_archivo
from cerradurapositiva import cerradura_positiva_afn, aplicar_cerradura_positiva
from cerradurakleenestar import cerradura_kleene_afn
from cerraduraopcional import cerradura_opcional_afn
from AnalizadorLexico import AnalizadorLexico
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/crear_afn', methods=['POST'])
def crear_afn():
    simbolo = request.json.get('simbolo')
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
    cerradura_kleene_afn()
    return jsonify({'status': 'Cerradura Kleene aplicada exitosamente'})

@app.route('/cerradura_opcional', methods=['POST'])
def cerradura_opcional():
    cerradura_opcional_afn()
    return jsonify({'status': 'Cerradura opcional aplicada exitosamente'})

@app.route('/analizador_lexico', methods=['POST'])
def analizador_lexico():
    data = request.json
    cadena = data.get('cadena')
    archivo_afd = "afd.txt"  # Asegúrate de tener este archivo generado previamente

    if not cadena:
        return jsonify({'error': 'Cadena no proporcionada'}), 400

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
    nombre_afn = request.json.get('nombre')
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

if __name__ == '__main__':
    app.run(debug=True)
