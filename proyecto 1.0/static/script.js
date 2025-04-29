document.addEventListener("DOMContentLoaded", function () {
    // Botones y formularios
    const crearAFNBtn = document.getElementById('crearAFNBtn');
    const unirAFNBtn = document.getElementById('unirAFNBtn');
    const concatenarAFNBtn = document.getElementById('concatenarAFNBtn');
    const cerraduraPositivaBtn = document.getElementById('cerraduraPositivaBtn');
    const cerraduraKleeneBtn = document.getElementById('cerraduraKleeneBtn');
    const cerraduraOpcionalBtn = document.getElementById('cerraduraOpcionalBtn');
    const analizadorLexicoBtn = document.getElementById('analizadorLexicoBtn');

    const crearAFNForm = document.getElementById('crearAFNForm');
    const unirAFNForm = document.getElementById('unirAFNForm');
    const concatenarAFNForm = document.getElementById('concatenarAFNForm');
    const cerraduraPositivaForm = document.getElementById('cerraduraPositivaForm');
    const cerraduraKleeneForm = document.getElementById('cerraduraKleeneForm');
    const cerraduraOpcionalForm = document.getElementById('cerraduraOpcionalForm');
    const analizadorLexicoForm = document.getElementById('analizadorLexicoForm');
    const resultadoAFN = document.getElementById('resultadoAFN');
    const resultadoLexico = document.getElementById('resultadoLexico');

    function resetarVisibilidad() {
        const formularios = [
            crearAFNForm, unirAFNForm, concatenarAFNForm,
            cerraduraPositivaForm, cerraduraKleeneForm, cerraduraOpcionalForm,
            analizadorLexicoForm, resultadoAFN, resultadoLexico
        ];
        formularios.forEach(form => form.classList.add('d-none'));
    }

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
});
