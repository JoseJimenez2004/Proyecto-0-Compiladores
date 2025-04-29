document.addEventListener("DOMContentLoaded", function () {
    const analizarCadenaBtn = document.getElementById('analizarCadenaBtn');
    const resultadoLexico = document.getElementById('resultadoLexico');
    const lexicoResultado = document.getElementById('lexicoResultado');

    analizarCadenaBtn.addEventListener('click', function () {
        const cadena = document.getElementById('cadenaAnalizar').value;
        if (!cadena) {
            alert('Introduce una cadena.');
            return;
        }

        // Realizamos una llamada POST para enviar la cadena
        fetch('/analizador_lexico', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cadena: cadena })
        })
        .then(response => response.json())
        .then(data => {
            resultadoLexico.classList.remove('d-none');
            if (data.tokens) {
                // Mostrar la cadena original y los tokens con la etiqueta "Cadena Analizada"
                lexicoResultado.innerHTML = `<strong>Cadena Analizada:</strong> ${cadena}<br><br>`;
                lexicoResultado.innerHTML += data.tokens.map(tok =>
                    `Token: ${tok.token} | Cadena Analizada: '${tok.lexema}'`
                ).join("<br>"); // Usamos <br> en lugar de \n para HTML
            } else {
                lexicoResultado.textContent = "No se pudieron identificar tokens.";
            }
        })
        .catch(error => {
            console.error('Error en el análisis léxico:', error);
            lexicoResultado.textContent = "Error en el análisis léxico.";
        });
    });
});
