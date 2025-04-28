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

        fetch('/analizador_lexico', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cadena: cadena })
        })
        .then(response => response.json())
        .then(data => {
            resultadoLexico.classList.remove('d-none');
            if (data.tokens) {
                lexicoResultado.textContent = data.tokens.map(tok =>
                    `Token: ${tok.token} | Lexema: '${tok.lexema}'`
                ).join("\n");
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
