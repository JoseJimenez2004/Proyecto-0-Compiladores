from flask import Flask, render_template, request, jsonify
import os
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Crear directorio de uploads si no existe
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def validar_gramatica(contenido):
    # Normalizar el contenido
    contenido = contenido.replace('ε', '')  # Tratamos epsilon como cadena vacía
    
    lineas = [linea.strip() for linea in contenido.split('\n') if linea.strip()]
    errores = []
    
    for i, linea in enumerate(lineas, 1):
        if not linea.endswith(';'):
            errores.append(f"Línea {i}: Falta punto y coma al final: {linea}")
            continue
            
        partes = linea[:-1].split('->')  # Removemos el ; antes de dividir
        if len(partes) != 2:
            errores.append(f"Línea {i}: Formato incorrecto, debe ser 'A -> B;': {linea}")
            continue
            
        lado_izq = partes[0].strip()
        lado_der = partes[1].strip()
        
        # Validar lado izquierdo
        if not lado_izq or ' ' in lado_izq:
            errores.append(f"Línea {i}: Lado izquierdo inválido: {lado_izq}")
            
        # Validar lado derecho
        for opcion in lado_der.split('|'):
            opcion = opcion.strip()
            if not opcion and 'ε' not in linea:  # Permitimos epsilon explícito
                errores.append(f"Línea {i}: Opción vacía no marcada como epsilon: {linea}")
                
    if errores:
        return False, "Errores encontrados:\n" + "\n".join(errores)
    return True, "Gramática válida"
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No se seleccionó archivo'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nombre de archivo vacío'}), 400
        
    if file and file.filename.endswith('.txt'):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        with open(filename, 'r') as f:
            contenido = f.read()
            
        valido, mensaje = validar_gramatica(contenido)
        
        return jsonify({
            'success': valido,
            'message': mensaje,
            'filename': file.filename,
            'content': contenido
        })
    else:
        return jsonify({'error': 'Formato de archivo no soportado'}), 400

if __name__ == '__main__':
    app.run(debug=True)