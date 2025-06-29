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
                <h2>Gramática Procesada</h2>
                <div class="tabs">
                    <button class="tab-btn active" data-tab="tabla">Tabla LL(1)</button>
                    <button class="tab-btn" data-tab="reglas">Reglas</button>
                    <button class="tab-btn" data-tab="simbolos">Símbolos</button>
                </div>
                
                <div id="tabla" class="tab-content active">
                    ${generarTablaLL1(data)}
                </div>
                
                <div id="reglas" class="tab-content">
                    ${generarListaReglas(data)}
                </div>
                
                <div id="simbolos" class="tab-content">
                    ${generarListaSimbolos(data)}
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
    }

    function generarTablaLL1(data) {
        let html = `
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
        
        html += `</tbody></table>`;
        return html;
    }

    function generarListaReglas(data) {
        return `
            <div class="reglas-list">
                <pre>${data.reglas.join('\n')}</pre>
            </div>
        `;
    }

    function generarListaSimbolos(data) {
        return `
            <div class="simbolos-container">
                <h3>No Terminales</h3>
                <ul>
                    ${data.simbolos.no_terminales.map(nt => `<li>${nt}</li>`).join('')}
                </ul>
                
                <h3>Terminales</h3>
                <ul>
                    ${data.simbolos.terminales.map(t => `<li>${t}</li>`).join('')}
                </ul>
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
        html += `<tr><td><strong>${nt}</strong></td>`;
        
        data.terminales.forEach(t => {
            const valor = data.tabla_ll1[nt] && data.tabla_ll1[nt][t] !== undefined ? 
                          data.tabla_ll1[nt][t] : '-1';
            const clase = valor !== '-1' ? 'celda-llena' : 'celda-vacia';
            html += `<td class="${clase}">${valor}</td>`;
        });
        
        html += `</tr>`;
    });
    
    html += `</tbody></table></div>`;
    return html;
}

});