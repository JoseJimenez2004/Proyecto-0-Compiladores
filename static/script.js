document.addEventListener("DOMContentLoaded", function () {
    const crearAFNBtn = document.getElementById('crearAFNBtn');
    const unirAFNBtn = document.getElementById('unirAFNBtn');
    const concatenarAFNBtn = document.getElementById('concatenarAFNBtn');
    const cerraduraPositivaBtn = document.getElementById('cerraduraPositivaBtn');
    const cerraduraKleeneBtn = document.getElementById('cerraduraKleeneBtn');
    const cerraduraOpcionalBtn = document.getElementById('cerraduraOpcionalBtn');
    const guardarAFNBtn = document.getElementById('guardarAFNBtn');
    const crearAFNForm = document.getElementById('crearAFNForm');
    const resultadoAFN = document.getElementById('resultadoAFN');
    const afnDetails = document.getElementById('afnDetails');

    const analizadorLexicoBtn = document.getElementById('analizadorLexicoBtn');
    const analizadorLexicoForm = document.getElementById('analizadorLexicoForm');
    const analizarCadenaBtn = document.getElementById('analizarCadenaBtn');
    const cadenaAnalizar = document.getElementById('cadenaAnalizar');
    const resultadoLexico = document.getElementById('resultadoLexico');
    const lexicoResultado = document.getElementById('lexicoResultado');

    const unirAFNForm = document.getElementById('form-unir-afns');
    const concatenarAFNForm = document.getElementById('concatenarAFNForm');
    const formConcatenarAFNs = document.getElementById('form-concatenar-afns');

    // Mostrar formulario para crear AFN
    crearAFNBtn.addEventListener('click', function () {
        resetarVisibilidad();
        crearAFNForm.classList.remove('d-none');
    });

    unirAFNBtn.addEventListener('click', function () {
        resetarVisibilidad();
        unirAFNForm.classList.remove('d-none');
    });

    concatenarAFNBtn.addEventListener('click', function () {
        resetarVisibilidad();
        concatenarAFNForm.classList.remove('d-none');
    });

    cerraduraPositivaBtn.addEventListener('click', function () {
        resetarVisibilidad();
        alert("Función de cerradura positiva aún no implementada.");
    });

    cerraduraKleeneBtn.addEventListener('click', function () {
        resetarVisibilidad();
        alert("Función de cerradura Kleene (*) aún no implementada.");
    });

    cerraduraOpcionalBtn.addEventListener('click', function () {
        resetarVisibilidad();
        alert("Función de cerradura opcional (?) aún no implementada.");
    });

    guardarAFNBtn.addEventListener('click', function () {
        const simbolo = document.getElementById('simboloInput').value;

        fetch('/crear_afn', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ simbolo: simbolo })
        })
        .then(response => response.json())
        .then(data => {
            if (data.afn) {
                afnDetails.textContent = JSON.stringify(data.afn, null, 2);
                resultadoAFN.classList.remove('d-none');
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => console.error('Error:', error));
    });

    analizadorLexicoBtn.addEventListener('click', function () {
        resetarVisibilidad();
        analizadorLexicoForm.classList.remove('d-none');
    });

    analizarCadenaBtn.addEventListener('click', function () {
        const cadena = cadenaAnalizar.value;

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

    // Enviar formulario de unir AFNs
    unirAFNForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const afn1 = document.getElementById('afn1').files[0];
        const afn2 = document.getElementById('afn2').files[0];
        const nombre = document.getElementById('nombre').value;

        if (!afn1 || !afn2 || !nombre) {
            alert('Por favor, completa todos los campos.');
            return;
        }

        const formData = new FormData();
        formData.append('afn1', afn1);
        formData.append('afn2', afn2);
        formData.append('nombre', nombre);

        fetch('/unir_afns', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('AFNs unidos exitosamente!');
            } else {
                alert('Hubo un error al unir los AFNs.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error de conexión. Por favor, inténtalo de nuevo más tarde.');
        });
    });

    // Enviar formulario de concatenar AFNs
    formConcatenarAFNs.addEventListener('submit', function (event) {
        event.preventDefault();

        const afn1 = document.getElementById('afn1Concat').files[0];
        const afn2 = document.getElementById('afn2Concat').files[0];
        const nombre = document.getElementById('nombreConcat').value;

        if (!afn1 || !afn2 || !nombre) {
            alert('Completa todos los campos.');
            return;
        }

        const formData = new FormData();
        formData.append('afn1', afn1);
        formData.append('afn2', afn2);
        formData.append('nombre', nombre);

        fetch('/concatenar_afns', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('¡AFNs concatenados correctamente!');
            } else {
                alert('Hubo un error en la concatenación.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error de conexión al servidor.');
        });
    });

    // Ocultar todos los formularios
    function resetarVisibilidad() {
        crearAFNForm.classList.add('d-none');
        resultadoAFN.classList.add('d-none');
        analizadorLexicoForm.classList.add('d-none');
        resultadoLexico.classList.add('d-none');
        unirAFNForm.classList.add('d-none');
        concatenarAFNForm.classList.add('d-none');
    }
});
