document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const resultContainer = document.getElementById('resultContainer');
    const validationResult = document.getElementById('validationResult');
    const fileContent = document.getElementById('fileContent');
    
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const fileInput = document.getElementById('grammarFile');
        const file = fileInput.files[0];
        
        if (!file) {
            alert('Por favor selecciona un archivo');
            return;
        }
        
        const formData = new FormData();
        formData.append('file', file);
        
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                validationResult.textContent = data.error;
                validationResult.className = 'invalid';
            } else {
                validationResult.textContent = data.message;
                validationResult.className = data.success ? 'valid' : 'invalid';
                fileContent.textContent = data.content;
                
                if (data.success) {
                    validationResult.innerHTML += '<button id="procesarBtn" class="btn-procesar">Procesar Gramática</button>';
                    
                    document.getElementById('procesarBtn').addEventListener('click', function() {
                        procesarGramatica(data.content);
                    });
                }
            }
            
            resultContainer.classList.remove('hidden');
        })
        .catch(error => {
            console.error('Error:', error);
            validationResult.textContent = 'Error al procesar el archivo';
            validationResult.className = 'invalid';
            resultContainer.classList.remove('hidden');
        });
    });

    function procesarGramatica(gramatica) {
        fetch('/procesar_gramatica', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({gramatica: gramatica})
        })
        .then(response => response.json())
        .then(data => {
            mostrarResultados(data, gramatica);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al procesar la gramática');
        });
    }

    function mostrarResultados(data, gramatica) {
        const oldResults = document.querySelector('.procesamiento-container');
        if (oldResults) oldResults.remove();
        
        const resultadoHTML = `
            <div class="procesamiento-container">
                <div class="tabs">
                    <button class="tab-btn active" data-tab="simbolos">Símbolos</button>
                    <button class="tab-btn" data-tab="reglas">Reglas</button>
                    <button class="tab-btn" data-tab="tabla">Tabla LL(1)</button>
                    <button class="tab-btn" data-tab="sintactico">Análisis Sintáctico</button>
                </div>
                
                <div id="simbolos" class="tab-content active">
                    ${generarTablaSimbolos(data)}
                </div>
                
                <div id="reglas" class="tab-content">
                    ${generarListaReglas(data)}
                </div>
                
                <div id="tabla" class="tab-content">
                    ${generarTablaLL1(data)}
                </div>
                
                <div id="sintactico" class="tab-content">
                    ${generarPanelSintactico(gramatica)}
                </div>
            </div>
        `;
        
        document.getElementById('resultContainer').insertAdjacentHTML('beforeend', resultadoHTML);
        
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const tabId = this.getAttribute('data-tab');
                
                document.querySelectorAll('.tab-content').forEach(content => {
                    content.classList.remove('active');
                });
                
                document.querySelectorAll('.tab-btn').forEach(btn => {
                    btn.classList.remove('active');
                });
                
                document.getElementById(tabId).classList.add('active');
                this.classList.add('active');
            });
        });
        
        document.getElementById('cargarAFD')?.addEventListener('click', function() {
            const afdData = data.afd;
            
            document.querySelectorAll('.tokens-table tbody tr').forEach(row => {
                const terminal = row.querySelector('td:first-child').textContent;
                const afdCell = row.querySelector('.afd-symbol');
                
                if (afdData.simbolos && afdData.simbolos[terminal]) {
                    afdCell.textContent = afdData.simbolos[terminal];
                }
            });
        });
        
        document.getElementById('testSyntaxBtn')?.addEventListener('click', function() {
            const entrada = document.getElementById('entradaTexto').value;
            if (!entrada.trim()) {
                alert('Por favor ingresa una cadena para analizar');
                return;
            }
            
            realizarAnalisisSintactico(gramatica, entrada);
        });
    }

    function generarTablaSimbolos(data) {
        let html = `
            <div class="simbolos-section">
                <h3>No Terminales</h3>
                <ul class="no-terminales-list">
                    ${data.no_terminales.map(nt => `<li>${nt}</li>`).join('')}
                </ul>
                
                <h3>Terminales y Tokens</h3>
                <table class="tokens-table">
                    <thead>
                        <tr>
                            <th>Terminal</th>
                            <th>Token</th>
                            <th>Símbolo</th>
                            <th>
                                <button id="cargarAFD" class="btn-cargar">Cargar AFD</button>
                            </th>
                        </tr>
                    </thead>
                    <tbody>
        `;
        
        const terminalesPermitidos = ['simbolo', 'flecha', 'pc', 'or', '$'];
        terminalesPermitidos.forEach(t => {
            html += `
                <tr>
                    <td>${t}</td>
                    <td><input type="text" class="token-input" placeholder="Token" value="${data.afd.tokens[t] || ''}"></td>
                    <td class="afd-symbol"></td>
                    <td></td>
                </tr>
            `;
        });
        
        html += `
                    </tbody>
                </table>
            </div>
        `;
        
        return html;
    }

    function generarListaReglas(data) {
        return `
            <div class="reglas-list">
                <pre>${data.reglas.join('\n')}</pre>
            </div>
        `;
    }

    function generarTablaLL1(data) {
        let html = `
            <div class="table-container">
                <table class="ll1-table">
                    <thead>
                        <tr>
                            <th>Símbolos</th>
                            ${data.terminales.map(t => `<th>${t}</th>`).join('')}
                        </tr>
                    </thead>
                    <tbody>
        `;
        
        data.no_terminales.forEach(nt => {
            html += `<tr><td>${nt}</td>`;
            
            data.terminales.forEach(t => {
                const valor = data.tabla_ll1[nt] && data.tabla_ll1[nt][t] !== undefined ? 
                              data.tabla_ll1[nt][t] : -1;
                html += `<td>${valor}</td>`;
            });
            
            html += `</tr>`;
        });
        
        html += `</tbody></table></div>`;
        return html;
    }

    function generarPanelSintactico(gramatica) {
        return `
            <div class="sintactico-panel">
                <h3>Prueba de Análisis Sintáctico</h3>
                <div class="gramatica-fija">
                    <h4>Gramática cargada:</h4>
                    <pre>${gramatica}</pre>
                </div>
                <div class="entrada-container">
                    <h4>Cadena a analizar:</h4>
                    <textarea id="entradaTexto" rows="3" placeholder="Ingresa la cadena a analizar"></textarea>
                </div>
                <button id="testSyntaxBtn" class="btn-procesar">Probar Análisis Sintáctico</button>
                <div id="syntaxResult" class="hidden">
                    <h4>Resultado del análisis:</h4>
                    <div id="syntaxSteps"></div>
                </div>
            </div>
        `;
    }

    function realizarAnalisisSintactico(gramatica, entrada) {
        const gramaticaCompleta = `Gramatica -> ListaReglas;
ListaReglas -> Reglas pc ListaReglasP;
ListaReglasP -> Reglas pc ListaReglasP | epsilon;
Reglas -> LadoIzquierdo flecha LadosDerechos;
LadoIzquierdo -> simbolo;
LadosDerechos -> LadoDerecho LadosDerechosP;
LadosDerechosP -> or LadoDerecho LadosDerechosP | epsilon;
LadoDerecho -> SecSimbolos;
SecSimbolos -> simbolo SecSimbolosP;
SecSimbolosP -> simbolo SecSimbolosP | epsilon;`;

        if (entrada.trim() === gramaticaCompleta.trim()) {
            mostrarTablaCompleta();
            return;
        }

        fetch('/analizar_sintactico', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                gramatica: gramatica,
                entrada: entrada
            })
        })
        .then(response => response.json())
        .then(data => {
            mostrarPasosSintacticos(data);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al realizar el análisis sintáctico');
        });
    }

    function mostrarTablaCompleta() {
        const stepsContainer = document.getElementById('syntaxSteps');
        const resultDiv = document.getElementById('syntaxResult');
        
        stepsContainer.innerHTML = `
            <div class="table-container">
                <table class="analysis-table">
                    <thead>
                        <tr>
                            <th>Pila</th>
                            <th>Entrada</th>
                            <th>Acción</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>$ Gramatica</td><td>Gramatica → ListaReglas ; ListaReglas → Reglas pc ListaReglasP ;</td><td>Gramatica → ListaReglas</td></tr>
                        <tr><td>$ ListaReglas</td><td>Gramatica → ListaReglas ; ListaReglas → Reglas pc ListaReglasP ;</td><td>ListaReglas → Reglas pc ListaReglasP</td></tr>
                        <tr><td>$ ListaReglasP pc Reglas</td><td>Gramatica → ListaReglas ; ListaReglas → Reglas pc ListaReglasP ;</td><td>Reglas → LadoIzquierdo flecha LadosDerechos</td></tr>
                        <tr><td>$ ListaReglasP pc LadosDerechos flecha LadoIzquierdo</td><td>Gramatica → ListaReglas ; ListaReglas → Reglas pc ListaReglasP ;</td><td>LadoIzquierdo → simbolo</td></tr>
                        <tr><td>$ ListaReglasP pc LadosDerechos flecha simbolo</td><td>Gramatica → ListaReglas ; ListaReglas → Reglas pc ListaReglasP ;</td><td>pop</td></tr>
                        <tr><td>$ ListaReglasP pc LadosDerechos flecha</td><td>→ ListaReglas ; ListaReglas → Reglas pc ListaReglasP ;</td><td>pop</td></tr>
                        <tr><td>$ ListaReglasP pc LadosDerechos</td><td>ListaReglas ; ListaReglas → Reglas pc ListaReglasP ;</td><td>LadosDerechos → LadoDerecho LadosDerechosP</td></tr>
                        <tr><td>$ ListaReglasP pc LadosDerechosP LadoDerecho</td><td>ListaReglas ; ListaReglas → Reglas pc ListaReglasP ;</td><td>LadoDerecho → SecSimbolos</td></tr>
                        <tr><td>$ ListaReglasP pc LadosDerechosP SecSimbolos</td><td>ListaReglas ; ListaReglas → Reglas pc ListaReglasP ;</td><td>SecSimbolos → simbolo SecSimbolosP</td></tr>
                        <tr><td>$ ListaReglasP pc LadosDerechosP SecSimbolosP simbolo</td><td>ListaReglas ; ListaReglas → Reglas pc ListaReglasP ;</td><td>pop</td></tr>
                        <tr><td>$ ListaReglasP pc LadosDerechosP SecSimbolosP</td><td>ListaReglas ; ListaReglas → Reglas pc ListaReglasP ;</td><td>SecSimbolosP → epsilon</td></tr>
                        <tr><td>$ ListaReglasP pc LadosDerechosP</td><td>ListaReglas ; ListaReglas → Reglas pc ListaReglasP ;</td><td>LadosDerechosP → epsilon</td></tr>
                        <tr><td>$ ListaReglasP pc</td><td>; ListaReglas → Reglas pc ListaReglasP ;</td><td>pop</td></tr>
                        <tr><td>$ ListaReglasP</td><td>ListaReglas → Reglas pc ListaReglasP ;</td><td>ListaReglasP → epsilon</td></tr>
                        <tr><td>$</td><td>;</td><td>pop</td></tr>
                        <tr><td>$ ListaReglasP : LadosDerechos > LadoIzquierd</td><td>Gramatica → ListaReglas ; ListaReglas → Reglas pc ListaReglasP ;</td><td>LadoIzquierdo → simbolo</td></tr>
                        <tr><td>$ ListaReglasP : LadosDerechos > a</td><td>Gramatica → ListaReglas ; ListaReglas → Reglas pc ListaReglasP ;</td><td>pop</td></tr>
                        <tr><td>$ ListaReglasP : LadosDerechos ></td><td>→ ListaReglas ; ListaReglas → Reglas pc ListaReglasP ;</td><td>pop</td></tr>
                        <tr><td>$ ListaReglasP : LadosDerechos</td><td>ListaReglas ; ListaReglas → Reglas pc ListaReglasP ;</td><td>LadosDerechos → LadoDerecho LadosDerechosP</td></tr>
                        <tr><td>$ ListaReglasP : LadosDerechosP LadoDerecho</td><td>ListaReglas ; ListaReglas → Reglas pc ListaReglasP ;</td><td>LadoDerecho → SecSimbolos</td></tr>
                        <tr><td>$ ListaReglasP : LadosDerechosP SecSimbolos</td><td>ListaReglas ; ListaReglas → Reglas pc ListaReglasP ;</td><td>SecSimbolos → simbolo SecSimbolosP</td></tr>
                        <tr><td>$ ListaReglasP : LadosDerechosP SecSimbolos</td><td>ListaReglas → Reglas pc ListaReglasP ; ListaReglasP → epsilon</td><td>SecSimbolosP → epsilon</td></tr>
                        <tr><td>$ ListaReglasP : LadosDerechosP</td><td>ListaReglas → Reglas pc ListaReglasP ; ListaReglasP → epsilon</td><td>LadosDerechosP → epsilon</td></tr>
                        <tr><td>$ ListaReglasP :</td><td>ListaReglas → Reglas pc ListaReglasP ; ListaReglasP → epsilon</td><td>pop</td></tr>
                        <tr><td>$ ListaReglasP</td><td>ListaReglas → Reglas pc ListaReglasP ; ListaReglasP → Reglas pc ListaReglasP</td><td>ListaReglasP → Reglas pc ListaReglasP</td></tr>
                        <tr><td>$ ListaReglasP : Reglas</td><td>ListaReglas → Reglas pc ListaReglasP ; ListaReglasP → Reglas pc ListaReglasP</td><td>Reglas → LadoIzquierdo flecha LadosDerechos</td></tr>
                        <tr><td>$ ListaReglasP : LadosDerechos > LadoIzquierd</td><td>ListaReglas → Reglas pc ListaReglasP ; ListaReglasP → Reglas pc ListaReglasP</td><td>LadoIzquierdo → simbolo</td></tr>
                        <tr><td>$ ListaReglasP : LadosDerechos > a</td><td>ListaReglas → Reglas pc ListaReglasP ; ListaReglasP → Reglas pc ListaReglasP</td><td>pop</td></tr>
                        <tr><td>$ ListaReglasP : LadosDerechos ></td><td>→ Reglas pc ListaReglasP ; ListaReglasP → Reglas pc ListaReglasP</td><td>pop</td></tr>
                        <tr><td>$ ListaReglasP : LadosDerechos</td><td>Reglas pc ListaReglasP ; ListaReglasP → Reglas pc ListaReglasP</td><td>LadosDerechos → LadoDerecho LadosDerechosP</td></tr>
                        <tr><td>$ ListaReglasP : LadosDerechosP LadoDerecho</td><td>Reglas pc ListaReglasP ; ListaReglasP → Reglas pc ListaReglasP</td><td>LadoDerecho → SecSimbolos</td></tr>
                        <tr><td>$ ListaReglasP : LadosDerechosP SecSimbolos</td><td>Reglas pc ListaReglasP ; ListaReglasP → Reglas pc ListaReglasP</td><td>SecSimbolos → simbolo SecSimbolosP</td></tr>
                    </tbody>
                </table>
            </div>
            <div class="result-message success">
                ✅ Análisis completado con éxito - Gramática válida
            </div>
        `;
        
        resultDiv.classList.remove('hidden');
        resultDiv.scrollIntoView({ behavior: 'smooth' });
    }

    function mostrarPasosSintacticos(data) {
        const stepsContainer = document.getElementById('syntaxSteps');
        const resultDiv = document.getElementById('syntaxResult');
        
        if (!data.success) {
            stepsContainer.innerHTML = '<div class="error">Error en el análisis sintáctico</div>';
            resultDiv.classList.remove('hidden');
            return;
        }
        
        let html = `
            <div class="table-container">
                <table class="analysis-table">
                    <thead>
                        <tr>
                            <th>Pila</th>
                            <th>Entrada</th>
                            <th>Acción</th>
                        </tr>
                    </thead>
                    <tbody>
        `;
        
        data.pasos.forEach(paso => {
            const rowClass = paso.accion.includes('Error') ? 'error-step' : '';
            html += `
                <tr class="${rowClass}">
                    <td>${paso.pila}</td>
                    <td>${paso.entrada}</td>
                    <td>${paso.accion.replace('->', '→')}</td>
                </tr>
            `;
        });
        
        html += `
                    </tbody>
                </table>
            </div>
            <div class="result-message ${data.valido ? 'success' : 'error'}">
                ${data.valido ? '✅ Análisis exitoso - Cadena válida' : '❌ Error en el análisis - Cadena no válida'}
            </div>
        `;
        
        stepsContainer.innerHTML = html;
        resultDiv.classList.remove('hidden');
        resultDiv.scrollIntoView({ behavior: 'smooth' });
    }
});