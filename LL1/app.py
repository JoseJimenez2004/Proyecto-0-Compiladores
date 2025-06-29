from flask import Flask, render_template, request, jsonify
import os
import re
from collections import OrderedDict

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def validar_gramatica(contenido):
    contenido = contenido.replace('ε', 'epsilon')
    lineas = [linea.strip() for linea in contenido.split('\n') if linea.strip()]
    errores = []
    
    for i, linea in enumerate(lineas, 1):
        if not (linea.endswith(';') or 'epsilon' in linea):
            errores.append(f"Línea {i}: Falta punto y coma al final: {linea}")
            continue
            
        if '->' not in linea:
            errores.append(f"Línea {i}: Formato incorrecto, falta '->': {linea}")
            continue
            
        partes = linea.split('->')
        lado_izq = partes[0].strip()
        lado_der = partes[1].replace(';', '').strip()
        
        if not lado_izq or ' ' in lado_izq:
            errores.append(f"Línea {i}: Lado izquierdo inválido: {lado_izq}")
            
        for opcion in lado_der.split('|'):
            opcion = opcion.strip()
            if not opcion and 'epsilon' not in linea:
                errores.append(f"Línea {i}: Opción vacía no marcada como epsilon: {linea}")
                
    if errores:
        return False, "Errores encontrados:\n" + "\n".join(errores)
    return True, "Gramática válida"

def analizar_gramatica(contenido):
    try:
        contenido = contenido.replace('ε', 'epsilon')
        lineas = [linea.strip() for linea in contenido.split('\n') if linea.strip()]
        
        no_terminales = OrderedDict()
        terminales = OrderedDict({'$': None})
        producciones = OrderedDict()
        reglas_numeradas = []
        
        for linea in lineas:
            if '->' in linea:
                lado_izq = linea.split('->')[0].strip()
                lado_der = linea.split('->')[1].split(';')[0].strip()
                
                if lado_izq not in no_terminales:
                    no_terminales[lado_izq] = None
                
                if lado_izq not in producciones:
                    producciones[lado_izq] = []
                    
                for produccion in lado_der.split('|'):
                    produccion = produccion.strip()
                    producciones[lado_izq].append(produccion)
                    reglas_numeradas.append(f"{lado_izq} -> {produccion}")
                    
                    for token in produccion.split():
                        if token != 'epsilon' and not token.isupper() and token not in terminales:
                            terminales[token] = None
        
        terminales = OrderedDict({'$': None, **{t: None for t in sorted(terminales.keys()) if t != '$'}})
        
        # Mapeo de terminales a símbolos
        simbolos_afd = {
            'simbolo': 'a',
            'flecha': '>',
            'pc': ';',
            'or': '|',
            '$': '$'
        }
        
        # Datos del AFD
        afd_data = {
            'simbolos': simbolos_afd,
            'tokens': {
                'simbolo': 10,
                'flecha': 30,
                'pc': 20,
                'or': 40,
                '$': 0
            }
        }
        
        # Generar tabla LL(1) como en la versión original
        tabla_ll1 = OrderedDict()
        for nt in no_terminales:
            tabla_ll1[nt] = OrderedDict()
            for t in terminales:
                tabla_ll1[nt][t] = -1
        
        # Asignaciones de ejemplo (como en tu versión original)
        asignaciones = {
            'Gramatica -> ListaReglas': {'simbolo': 1},
            'ListaReglas -> Reglas pc ListaReglasP': {'simbolo': 2},
            'ListaReglasP -> Reglas pc ListaReglasP': {'simbolo': 3},
            'ListaReglasP -> epsilon': {'$': 4},
            'Reglas -> LadoIzquierdo flecha LadosDerechos': {'simbolo': 5},
            'LadoIzquierdo -> simbolo': {'simbolo': 6},
            'LadosDerechos -> LadoDerecho LadosDerechosP': {'simbolo': 7},
            'LadosDerechosP -> or LadoDerecho LadosDerechosP': {'or': 8},
            'LadosDerechosP -> epsilon': {'pc': 9, '$': 9},
            'LadoDerecho -> SecSimbolos': {'simbolo': 10},
            'SecSimbolos -> simbolo SecSimbolosP': {'simbolo': 11},
            'SecSimbolosP -> simbolo SecSimbolosP': {'simbolo': 12},
            'SecSimbolosP -> epsilon': {'or': 13, 'pc': 13, '$': 13}
        }
        
        # Aplicar asignaciones (como en tu versión original)
        for regla, valores in asignaciones.items():
            nt = regla.split('->')[0].strip()
            for t, num in valores.items():
                if nt in tabla_ll1 and t in tabla_ll1[nt]:
                    tabla_ll1[nt][t] = num
        
        return {
            'no_terminales': list(no_terminales.keys()),
            'terminales': list(terminales.keys()),
            'tabla_ll1': {k: dict(v) for k, v in tabla_ll1.items()},
            'reglas': [f"{i+1}. {regla}" for i, regla in enumerate(reglas_numeradas)],
            'afd': afd_data
        }
    except Exception as e:
        print(f"Error al analizar gramática: {str(e)}")
        raise

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

@app.route('/procesar_gramatica', methods=['POST'])
def procesar_gramatica():
    data = request.json
    gramatica = data.get('gramatica', '')
    
    resultado = analizar_gramatica(gramatica)
    
    return jsonify({
        'success': True,
        'no_terminales': resultado['no_terminales'],
        'terminales': resultado['terminales'],
        'tabla_ll1': resultado['tabla_ll1'],
        'reglas': resultado['reglas'],
        'afd': resultado['afd']
    })

if __name__ == '__main__':
    app.run(debug=True)