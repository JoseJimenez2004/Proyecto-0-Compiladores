import os
from flask import Flask, render_template, jsonify, request
from crear_afn_basico import crear_afn_basico
from unir_afn import unir_afn_desde_archivos
from concatenar import concatenar_afn_desde_archivos
from cerradurapositiva import cerradura_positiva_afn
from cerradurakleenestar import cerradura_kleene_afn
from cerraduraopcional import cerradura_opcional_afn

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

if __name__ == '__main__':
    app.run(debug=True)
