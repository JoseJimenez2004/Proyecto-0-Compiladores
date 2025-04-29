document.addEventListener("DOMContentLoaded", function () {
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

    function cargarAFNsParaCerradura() {
        fetch("/listar_afns")
            .then(response => response.json())
            .then(data => {
                const afnSelect = document.getElementById('afn-select');
                data.forEach(nombre => {
                    afnSelect.append(new Option(nombre, nombre));
                });
            })
            .catch(error => console.error('Error al cargar lista de AFNs:', error));
    }

    cargarAFNsDisponibles();
    cargarAFNsParaCerradura();
});
