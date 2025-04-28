document.addEventListener("DOMContentLoaded", function () {
    // Botones y formularios
    const crearAFNBtn = document.getElementById('crearAFNBtn');
    const unirAFNBtn = document.getElementById('unirAFNBtn');
    const concatenarAFNBtn = document.getElementById('concatenarAFNBtn');
    const cerraduraPositivaBtn = document.getElementById('cerraduraPositivaBtn');
    const cerraduraKleeneBtn = document.getElementById('cerraduraKleeneBtn');
    const cerraduraOpcionalBtn = document.getElementById('cerraduraOpcionalBtn');
    const analizadorLexicoBtn = document.getElementById('analizadorLexicoBtn');
    const guardarAFNBtn = document.getElementById('guardarAFNBtn');
    const analizarCadenaBtn = document.getElementById('analizarCadenaBtn');
    
    const crearAFNForm = document.getElementById('crearAFNForm');
    const unirAFNForm = document.getElementById('unirAFNForm');
    const concatenarAFNForm = document.getElementById('concatenarAFNForm');
    const cerraduraPositivaForm = document.getElementById('cerraduraPositivaForm');
    const cerraduraKleeneForm = document.getElementById('cerraduraKleeneForm');
    const cerraduraOpcionalForm = document.getElementById('cerraduraOpcionalForm');
    const analizadorLexicoForm = document.getElementById('analizadorLexicoForm');

    const resultadoAFN = document.getElementById('resultadoAFN');
    const resultadoLexico = document.getElementById('resultadoLexico');

    const afnSelect = document.getElementById('afn-select');
    const resultadoDivKleene = document.getElementById('resultadoCerraduraKleene');
    const lexicoResultado = document.getElementById('lexicoResultado');
    const afnDetails = document.getElementById('afnDetails');

    // Función para ocultar todos los formularios
    function resetarVisibilidad() {
        const formularios = [
            crearAFNForm, unirAFNForm, concatenarAFNForm,
            cerraduraPositivaForm, cerraduraKleeneForm, cerraduraOpcionalForm,
            analizadorLexicoForm, resultadoAFN, resultadoLexico
        ];
        formularios.forEach(form => form.classList.add('d-none'));
    }

    // Cargar opciones de AFNs
    function cargarAFNsDisponibles() {
        fetch('/obtener_afns')
            .then(response => response.json())
            .then(data => {
                const select = document.getElementById('afn-select-opcional');
                select.innerHTML = '<option value="">Seleccionar un AFN</option>';
                data.afns.forEach(afn => {
                    const option = document.createElement('option');
                    option.value = afn;
                    option.textContent = afn;
                    select.appendChild(option);
                });
            })
            .catch(error => console.error('Error al cargar AFNs:', error));
    }

    // Cargar lista de AFNs para cerradura Kleene
    function cargarAFNsParaCerradura() {
        fetch("/listar_afns")
            .then(response => response.json())
            .then(data => {
                data.forEach(nombre => {
                    afnSelect.append(new Option(nombre, nombre));
                });
            })
            .catch(error => console.error('Error al cargar lista de AFNs:', error));
    }

    // Botones de menú
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
        cerraduraPositivaForm.classList.remove('d-none');
    });

    cerraduraKleeneBtn.addEventListener('click', function () {
        resetarVisibilidad();
        cerraduraKleeneForm.classList.remove('d-none');
    });

    cerraduraOpcionalBtn.addEventListener('click', function () {
        resetarVisibilidad();
        cerraduraOpcionalForm.classList.remove('d-none');
    });

    analizadorLexicoBtn.addEventListener('click', function () {
        resetarVisibilidad();
        analizadorLexicoForm.classList.remove('d-none');
    });

    // Guardar nuevo AFN
    guardarAFNBtn.addEventListener('click', function () {
        const simbolo = document.getElementById('simboloInput').value;
        if (!simbolo) {
            alert('Introduce un símbolo.');
            return;
        }

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

    // Analizar cadena
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

    // Unir AFNs
    document.getElementById('form-unir-afns').addEventListener('submit', function (event) {
        event.preventDefault();
        const afn1 = document.getElementById('afn1').files[0];
        const afn2 = document.getElementById('afn2').files[0];
        const nombre = document.getElementById('nombre').value;

        if (!afn1 || !afn2 || !nombre) {
            alert('Completa todos los campos.');
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
                alert('¡AFNs unidos exitosamente!');
            } else {
                alert('Error al unir AFNs.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error de conexión.');
        });
    });

    // Concatenar AFNs
    document.getElementById('form-concatenar-afns').addEventListener('submit', function (event) {
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
                alert('¡AFNs concatenados exitosamente!');
            } else {
                alert('Error al concatenar AFNs.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error de conexión.');
        });
    });

    // Aplicar cerradura de Kleene
    document.getElementById('aplicarCerraduraKleeneBtn').addEventListener('click', function () {
        const nombre = afnSelect.value;
        if (!nombre) {
            alert("Selecciona un AFN.");
            return;
        }

        fetch('/cerradura_kleene', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre: nombre })
        })
        .then(response => response.json())
        .then(data => {
            resultadoDivKleene.textContent = data.mensaje || 'Operación realizada.';
        })
        .catch(error => {
            console.error('Error:', error);
            resultadoDivKleene.textContent = "Error en la operación.";
        });
    });

    // Aplicar cerradura opcional
    document.getElementById('form-cerradura-opcional').addEventListener('submit', function (event) {
        event.preventDefault();
        const afnSeleccionado = document.getElementById('afn-select-opcional').value;
        if (!afnSeleccionado) {
            alert('Selecciona un AFN.');
            return;
        }

        fetch(`/cerradura_opcional/${afnSeleccionado}`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('resultadoCerraduraOpcional').innerHTML = `<p>${data.mensaje}</p>`;
        })
        .catch(error => {
            console.error('Error al aplicar cerradura opcional:', error);
        });
    });

    // Finalmente, cargar AFNs disponibles
    cargarAFNsDisponibles();
    cargarAFNsParaCerradura();
});
