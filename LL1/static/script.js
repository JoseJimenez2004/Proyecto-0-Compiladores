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
            mostrarResultados(data);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al procesar la gramática');
        });
    }

    function mostrarResultados(data) {
        // Limpiar resultados anteriores
        const oldResults = document.querySelector('.procesamiento-container');
        if (oldResults) oldResults.remove();
        
        const resultadoHTML = `
            <div class="procesamiento-container">
                <div class="tabs">
                    <button class="tab-btn active" data-tab="simbolos">Símbolos</button>
                    <button class="tab-btn" data-tab="reglas">Reglas</button>
                    <button class="tab-btn" data-tab="tabla">Tabla LL(1)</button>
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
            </div>
        `;
        
        document.getElementById('resultContainer').insertAdjacentHTML('beforeend', resultadoHTML);
        
        // Manejar clics en pestañas
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const tabId = this.getAttribute('data-tab');
                
                // Ocultar todos los contenidos
                document.querySelectorAll('.tab-content').forEach(content => {
                    content.classList.remove('active');
                });
                
                // Desactivar todos los botones
                document.querySelectorAll('.tab-btn').forEach(btn => {
                    btn.classList.remove('active');
                });
                
                // Mostrar contenido seleccionado
                document.getElementById(tabId).classList.add('active');
                this.classList.add('active');
            });
        });
        
        // Configurar el botón de cargar AFD
        configurarBotonAFD(data);
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
        
        // Solo mostrar los terminales específicos
        const terminalesPermitidos = ['simbolo', 'flecha', 'pc', 'or', '$'];
        terminalesPermitidos.forEach(t => {
            html += `
                <tr>
                    <td>${t}</td>
                    <td><input type="text" class="token-input" placeholder="Token"></td>
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

    function configurarBotonAFD(data) {
        document.getElementById('cargarAFD').addEventListener('click', function() {
            const afdData = data.afd;
            
            // Actualizar cada fila de la tabla
            document.querySelectorAll('.tokens-table tbody tr').forEach(row => {
                const terminal = row.querySelector('td:first-child').textContent;
                const tokenInput = row.querySelector('.token-input');
                const afdCell = row.querySelector('.afd-symbol');
                
                if (afdData.simbolos[terminal]) {
                    // Asignar el símbolo correspondiente
                    afdCell.textContent = afdData.simbolos[terminal];
                    
                    // Asignar el token si existe en los datos del AFD
                    if (afdData.tokens[terminal]) {
                        tokenInput.value = afdData.tokens[terminal];
                    }
                }
            });
        });
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
});