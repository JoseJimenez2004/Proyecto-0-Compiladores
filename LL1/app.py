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
        
        simbolos_afd = {
            'simbolo': 'a',
            'flecha': '>',
            'pc': ';',
            'or': '|',
            '$': '$'
        }
        
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
        
        tabla_ll1 = OrderedDict()
        for nt in no_terminales:
            tabla_ll1[nt] = OrderedDict()
            for t in terminales:
                tabla_ll1[nt][t] = -1
        
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
            'afd': afd_data,
            'producciones': producciones
        }
    except Exception as e:
        print(f"Error al analizar gramática: {str(e)}")
        raise

class AnalizadorSintacticoLL1:
    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.tabla = gramatica['tabla_ll1']
        self.producciones = self._convertir_producciones(gramatica['producciones'])
        self.terminales = gramatica['terminales']
        self.no_terminales = gramatica['no_terminales']
        self.pasos = []
    
    def _convertir_producciones(self, producciones):
        producciones_convertidas = {}
        for nt, prods in producciones.items():
            producciones_convertidas[nt] = []
            for prod in prods:
                partes = prod.split()
                producciones_convertidas[nt].append(partes)
        return producciones_convertidas
    
    def _obtener_produccion(self, no_terminal, terminal):
        num_produccion = self.tabla.get(no_terminal, {}).get(terminal, -1)
        if num_produccion == -1:
            return None
        
        for nt, prods in self.producciones.items():
            for i, prod in enumerate(prods, 1):
                regla_completa = f"{nt} -> {' '.join(prod)}"
                regla_en_gramatica = self.gramatica['reglas'][num_produccion-1].split('. ')[1]
                if regla_completa == regla_en_gramatica:
                    return prod
        return None
    
    def analizar(self, entrada):
        self.pasos = []
        pila = ['$', 'Gramatica']
        entrada_tokens = entrada.split() + ['$']
        entrada_ptr = 0
        
        while len(pila) > 0:
            tope = pila[-1]
            actual = entrada_tokens[entrada_ptr] if entrada_ptr < len(entrada_tokens) else '$'
            
            registro = {
                'pila': ' '.join(pila),
                'entrada': ' '.join(entrada_tokens[entrada_ptr:]),
                'accion': ''
            }
            
            if tope == actual:
                registro['accion'] = "pop"
                pila.pop()
                entrada_ptr += 1
            elif tope in self.terminales:
                registro['accion'] = f"Error: terminal inesperado {tope}"
                self.pasos.append(registro)
                return False
            else:
                produccion = self._obtener_produccion(tope, actual)
                if produccion is None:
                    registro['accion'] = f"Error: no hay producción para {tope} con {actual}"
                    self.pasos.append(registro)
                    return False
                
                pila.pop()
                if produccion[0] != 'epsilon':
                    pila.extend(reversed(produccion))
                
                registro['accion'] = f"{tope} → {' '.join(produccion)}"
            
            self.pasos.append(registro)
        
        return True

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
        'afd': resultado['afd'],
        'producciones': resultado['producciones']
    })

@app.route('/analizar_sintactico', methods=['POST'])
def analizar_sintactico():
    data = request.json
    gramatica_texto = data.get('gramatica', '')
    entrada = data.get('entrada', '')
    
    resultado_gramatica = analizar_gramatica(gramatica_texto)
    analizador = AnalizadorSintacticoLL1(resultado_gramatica)
    exito = analizador.analizar(entrada)
    
    return jsonify({
        'success': exito,
        'pasos': analizador.pasos,
        'valido': exito
    })

if __name__ == '__main__':
    app.run(debug=True)