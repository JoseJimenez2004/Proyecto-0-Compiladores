document.addEventListener("DOMContentLoaded", function () {
    const guardarAFNBtn = document.getElementById('guardarAFNBtn');
    const afnDetails = document.getElementById('afnDetails');
    const resultadoAFN = document.getElementById('resultadoAFN');

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
});
