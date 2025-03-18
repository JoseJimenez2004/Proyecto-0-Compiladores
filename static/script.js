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

    // Mostrar formulario para crear AFN
    crearAFNBtn.addEventListener('click', function () {
        resetarVisibilidad();
        crearAFNForm.classList.remove('d-none');
    });

    // Botón para unir AFN's
    unirAFNBtn.addEventListener('click', function () {
        resetarVisibilidad();
        alert("Función de unir AFN's aún no implementada.");
    });

    // Botón para concatenar AFN's
    concatenarAFNBtn.addEventListener('click', function () {
        resetarVisibilidad();
        alert("Función de concatenar AFN's aún no implementada.");
    });

    // Botón para cerradura positiva
    cerraduraPositivaBtn.addEventListener('click', function () {
        resetarVisibilidad();
        alert("Función de cerradura positiva aún no implementada.");
    });

    // Botón para cerradura Kleene (*)
    cerraduraKleeneBtn.addEventListener('click', function () {
        resetarVisibilidad();
        alert("Función de cerradura Kleene (*) aún no implementada.");
    });

    // Botón para cerradura opcional (?)
    cerraduraOpcionalBtn.addEventListener('click', function () {
        resetarVisibilidad();
        alert("Función de cerradura opcional (?) aún no implementada.");
    });

    // Enviar el AFN para ser creado
    guardarAFNBtn.addEventListener('click', function () {
        const simbolo = document.getElementById('simboloInput').value;
        
        fetch('/crear_afn', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
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

    // Función para resetear visibilidad de formularios
    function resetarVisibilidad() {
        crearAFNForm.classList.add('d-none');
        resultadoAFN.classList.add('d-none');
    }
});
